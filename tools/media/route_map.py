#!/usr/bin/env python3
"""Draw a satellite route map (pins, road route, inset) for a portfolio case study.

    python tools/media/route_map.py <inventory.csv> <out_dir> --drive 7 8 9 --base 28 29 [--waypoints 6 13]

Inputs:
  * inventory.csv: one row per photo, columns file, ext, mb, w, h, date, lat, lon, alt, model.
    Photo number N = the Nth row with a non-empty `w` (video rows are not counted).
  * --drive / --base: photo numbers of the road points and of the base camp. Every other GPS place becomes a
    numbered pin, in order of first visit. --waypoints names places that are neither (they are not drawn).

Photos within --cluster-km of each other (chained) form one place. Nothing location-specific lives in this file.

The route is the union of the shortest paths over the OpenStreetMap road network (Overpass API, answers cached in
<out_dir>/osm/) from the base camp to every pin; a place off the network gets a straight stub, a disconnected part
a straight bridge. The inset follows the main roads through the road points.

Writes to <out_dir>:
  route-map.jpg   the map (long edge 2400 px)
  pins.txt        pin number, date of first visit, photo numbers at that place (no coordinates)
  tiles/, osm/, ne/   caches

Locator inset: a small flat map of the country with a marker at the centroid of the pins (computed at run time),
drawn from the Natural Earth 1:50m admin-0 countries GeoJSON (public domain, cached in <out_dir>/ne/). Skip it with --no-locator.

Basemap: Sentinel-2 cloudless 2016 by EOX (CC BY 4.0), fetched tile by tile, politely, and cached.
Roads: (c) OpenStreetMap contributors (ODbL). Country outlines: Natural Earth (public domain).
Requires Pillow (pip install pillow). Standard library for HTTP, JSON and XML.
"""
from __future__ import annotations

import argparse
import csv
import heapq
import itertools
import json
import math
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont
except ImportError:  # pragma: no cover
    sys.exit("Pillow is not installed. Run:  pip install pillow")

TILE_URL = "https://tiles.maps.eox.at/wmts/1.0.0/s2cloudless_3857/default/g/{z}/{y}/{x}.jpg"
USER_AGENT = "portfolio-route-map/1.0 (static map for a personal portfolio; sequential requests, tiles cached)"
OVERPASS = ["https://overpass-api.de/api/interpreter", "https://overpass.kumi.systems/api/interpreter"]
ATTRIBUTION = ("Imagery: Sentinel-2 cloudless 2016 by EOX IT Services GmbH (contains modified Copernicus Sentinel data 2016). "
               "Roads: © OpenStreetMap contributors")
LOCATOR_CREDIT = ". Locator map: Natural Earth"
NE_URLS = ["https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_50m_admin_0_countries.geojson",
           "https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_110m_admin_0_countries.geojson"]
CAPITAL_LL = (3.06, 36.75)  # the capital of the country, a generic public point (orientation dot of the locator)
SEA, LAND_OTHER, LAND_HOME, BORDER = (0x9D, 0xAF, 0xC2), (0xC9, 0xCB, 0xCE), (0xF4, 0xF1, 0xEA), (0x7C, 0x88, 0x96)

INK = (0x1B, 0x24, 0x30)
ACCENT = (0x1F, 0x3A, 0x5F)
WHITE = (255, 255, 255)
FONTS = [r"C:\Windows\Fonts\segoeuib.ttf", r"C:\Windows\Fonts\arialbd.ttf", "DejaVuSans-Bold.ttf"]

SS = 2  # supersampling for overlays
PIN = 64  # pin diameter, px of the final image (readable when the 2400 px image is shown at ~600 px)
RING = 5
LINE_W, LINE_CASE = 8, 13  # main route: white line on dark casing
INSET_W, INSET_CASE = 3.5, 6.5
MARGIN = 36  # distance of furniture from the image edge
EARTH_KM = 40075.017


# ---------- small geometry helpers ----------

def merc(lon: float, lat: float) -> tuple[float, float]:
    """Lon/lat to unit Web Mercator square (0..1, y down)."""
    s = math.sin(math.radians(lat))
    return (lon + 180.0) / 360.0, 0.5 - math.log((1 + s) / (1 - s)) / (4 * math.pi)


class Local:
    """Flat local km grid around a reference point (good enough for a few hundred km)."""

    def __init__(self, lon0: float, lat0: float):
        self.lon0, self.lat0 = lon0, lat0
        self.kx = math.cos(math.radians(lat0)) * 111.32
        self.ky = 110.57

    def xy(self, lon: float, lat: float) -> tuple[float, float]:
        return (lon - self.lon0) * self.kx, (lat - self.lat0) * self.ky

    def ll(self, x: float, y: float) -> tuple[float, float]:
        return x / self.kx + self.lon0, y / self.ky + self.lat0


def dist(a, b) -> float:
    return math.hypot(a[0] - b[0], a[1] - b[1])


def cumlen(poly) -> list[float]:
    c = [0.0]
    for a, b in zip(poly, poly[1:]):
        c.append(c[-1] + dist(a, b))
    return c


def nearest_on_poly(poly, cum, p):
    """(distance, along-track position, nearest point) of point p to a polyline."""
    best = (float("inf"), 0.0, poly[0])
    for i in range(len(poly) - 1):
        a, b = poly[i], poly[i + 1]
        dx, dy = b[0] - a[0], b[1] - a[1]
        L2 = dx * dx + dy * dy
        t = 0.0 if L2 == 0 else max(0.0, min(1.0, ((p[0] - a[0]) * dx + (p[1] - a[1]) * dy) / L2))
        q = (a[0] + t * dx, a[1] + t * dy)
        d = dist(p, q)
        if d < best[0]:
            best = (d, cum[i] + t * math.sqrt(L2), q)
    return best


def sub_poly(poly, cum, lo, hi):
    """Part of a polyline between two along-track positions."""

    def at(s):
        for i in range(len(poly) - 1):
            if cum[i + 1] >= s:
                seg = cum[i + 1] - cum[i]
                t = 0.0 if seg == 0 else (s - cum[i]) / seg
                return (poly[i][0] + t * (poly[i + 1][0] - poly[i][0]), poly[i][1] + t * (poly[i + 1][1] - poly[i][1]))
        return poly[-1]

    mid = [p for p, c in zip(poly, cum) if lo < c < hi]
    return [at(lo)] + mid + [at(hi)]


def resample(poly, step):
    out = [poly[0]]
    cum = cumlen(poly)
    s = step
    while s < cum[-1]:
        out.append(sub_poly(poly, cum, s, s)[0])
        s += step
    out.append(poly[-1])
    return out


def chaikin(pts, iters=3):
    for _ in range(iters):
        if len(pts) < 3:
            break
        new = [pts[0]]
        for a, b in zip(pts, pts[1:]):
            new.append((0.75 * a[0] + 0.25 * b[0], 0.75 * a[1] + 0.25 * b[1]))
            new.append((0.25 * a[0] + 0.75 * b[0], 0.25 * a[1] + 0.75 * b[1]))
        new.append(pts[-1])
        pts = new
    return pts


def bow(a, b, amount=0.04):
    """A gently curved line a->b (quadratic, bulging to one side by `amount` of its length)."""
    mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
    dx, dy = b[0] - a[0], b[1] - a[1]
    sign = 1 if (round(a[0] * 7 + a[1] * 13 + b[0] * 5 + b[1] * 3) % 2 == 0) else -1
    c = (mx - dy * amount * sign, my + dx * amount * sign)
    n = max(8, int(dist(a, b) / 0.3))
    return [((1 - t) ** 2 * a[0] + 2 * (1 - t) * t * c[0] + t * t * b[0], (1 - t) ** 2 * a[1] + 2 * (1 - t) * t * c[1] + t * t * b[1])
            for t in (i / n for i in range(n + 1))]


# ---------- input ----------

def read_photos(path: Path):
    photos = []
    with path.open(encoding="utf-8", newline="") as f:
        for r in csv.DictReader(f):
            if not r["w"]:
                continue
            n = len(photos) + 1
            when = datetime.strptime(r["date"], "%Y:%m:%d %H:%M:%S") if r["date"] else None
            gps = (float(r["lon"]), float(r["lat"])) if r["lat"] else None
            photos.append({"n": n, "when": when, "gps": gps})
    return photos


def make_places(photos, loc: Local, cluster_km, drive, base, waypoints):
    gp = [p for p in photos if p["gps"]]
    par = {p["n"]: p["n"] for p in gp}

    def find(x):
        while par[x] != x:
            par[x] = par[par[x]]
            x = par[x]
        return x

    xy = {p["n"]: loc.xy(*p["gps"]) for p in gp}
    for a, b in itertools.combinations(gp, 2):
        if dist(xy[a["n"]], xy[b["n"]]) <= cluster_km:
            par[find(a["n"])] = find(b["n"])
    groups: dict[int, list] = {}
    for p in gp:
        groups.setdefault(find(p["n"]), []).append(p)
    places = []
    for g in groups.values():
        nums = sorted(p["n"] for p in g)
        lon = sum(p["gps"][0] for p in g) / len(g)
        lat = sum(p["gps"][1] for p in g) / len(g)
        first = min(p["when"] for p in g if p["when"])
        if set(nums) & set(base):
            kind = "base"
        elif set(nums) & set(drive):
            kind = "drive"
        elif set(nums) <= set(waypoints):
            kind = "waypoint"
        else:
            kind = "pin"
            if set(nums) & set(waypoints):
                print(f"note: waypoint photo(s) {sorted(set(nums) & set(waypoints))} share a place with other photos; the place is a pin")
        places.append({"kind": kind, "photos": nums, "lon": lon, "lat": lat, "first": first})
    places.sort(key=lambda p: p["first"])
    k = 0
    for p in places:
        if p["kind"] == "pin":
            k += 1
            p["pin"] = k
    return places


# ---------- tiles and panels ----------

def fetch_tile(z, x, y, cache: Path) -> Image.Image:
    f = cache / str(z) / f"{y}_{x}.jpg"
    if not f.exists():
        f.parent.mkdir(parents=True, exist_ok=True)
        last = None
        for attempt in range(3):
            try:
                req = urllib.request.Request(TILE_URL.format(z=z, x=x, y=y), headers={"User-Agent": USER_AGENT})
                with urllib.request.urlopen(req, timeout=30) as r:
                    f.write_bytes(r.read())
                break
            except (urllib.error.URLError, OSError) as e:
                last = e
                time.sleep(1.5 * (attempt + 1))
        else:
            sys.exit(f"Tile server not reachable ({last}); stopping, no other imagery provider is used.")
        time.sleep(0.12)  # be polite: sequential, small pause
    return Image.open(f).convert("RGB")


class Panel:
    """A map window (unit-mercator box) rendered to a W x H pixel image."""

    def __init__(self, box, width, min_native=True):
        self.u0, self.v0, self.u1, self.v1 = box
        self.W = width
        self.H = round(width * (self.v1 - self.v0) / (self.u1 - self.u0))
        z = 0
        while 256 * 2 ** z * (self.u1 - self.u0) < width and z < 17:
            z += 1
        self.z = z  # smallest zoom whose native pixels cover the output width

    def proj(self, lon, lat):
        u, v = merc(lon, lat)
        return (u - self.u0) / (self.u1 - self.u0) * self.W, (v - self.v0) / (self.v1 - self.v0) * self.H

    def km_per_px(self):
        lat_c = math.degrees(2 * math.atan(math.exp(math.pi * (1 - 2 * (self.v0 + self.v1) / 2))) - math.pi / 2)
        return (self.u1 - self.u0) * EARTH_KM * math.cos(math.radians(lat_c)) / self.W

    def basemap(self, cache: Path) -> Image.Image:
        n = 2 ** self.z
        x0, x1 = int(self.u0 * n), int(self.u1 * n)
        y0, y1 = int(self.v0 * n), int(self.v1 * n)
        mosaic = Image.new("RGB", ((x1 - x0 + 1) * 256, (y1 - y0 + 1) * 256))
        total = (x1 - x0 + 1) * (y1 - y0 + 1)
        print(f"  zoom {self.z}: {total} tiles (cached ones are not fetched again)")
        for ty in range(y0, y1 + 1):
            for tx in range(x0, x1 + 1):
                mosaic.paste(fetch_tile(self.z, tx, ty, cache), ((tx - x0) * 256, (ty - y0) * 256))
        box = ((self.u0 * n - x0) * 256, (self.v0 * n - y0) * 256, (self.u1 * n - x0) * 256, (self.v1 * n - y0) * 256)
        img = mosaic.resize((self.W, self.H), Image.LANCZOS, box=box)
        return img


def box_around(points_uv, aspect_min, aspect_max, pad_frac, aspect_fixed=None):
    """Unit-mercator box around points with a margin, widened to a wanted aspect (w/h)."""
    us, vs = [p[0] for p in points_uv], [p[1] for p in points_uv]
    w, h = max(us) - min(us), max(vs) - min(vs)
    cu, cv = (max(us) + min(us)) / 2, (max(vs) + min(vs)) / 2
    w, h = w * (1 + 2 * pad_frac), h * (1 + 2 * pad_frac)
    if aspect_fixed:
        aspect_min = aspect_max = aspect_fixed
    if w / h > aspect_max:
        h = w / aspect_max
    elif w / h < aspect_min:
        w = h * aspect_min
    return cu - w / 2, cv - h / 2, cu + w / 2, cv + h / 2


# ---------- drawing ----------

_fonts: dict[int, ImageFont.FreeTypeFont] = {}


def font(px: float) -> ImageFont.FreeTypeFont:
    size = max(6, round(px))
    if size not in _fonts:
        for f in FONTS:
            try:
                _fonts[size] = ImageFont.truetype(f, size)
                break
            except OSError:
                continue
        else:
            _fonts[size] = ImageFont.load_default()
    return _fonts[size]


def draw_routes(d, lines_px, white_w, case_w):
    """Dark casing for every line first, then the white cores, so junctions merge cleanly."""
    for width, color in ((case_w, INK), (white_w, WHITE)):
        w = width * SS
        r = w / 2
        for pts in lines_px:
            p = [(x * SS, y * SS) for x, y in pts]
            d.line(p, fill=color, width=round(w), joint="curve")
            for x, y in (p[0], p[-1]) + tuple(p[1:-1:2]):
                d.ellipse([x - r, y - r, x + r, y + r], fill=color)


def shadow_layer(size, shapes, blur, offset, alpha=110):
    sh = Image.new("RGBA", size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(sh)
    for cx, cy, r in shapes:
        sd.ellipse([cx - r, cy + offset - r, cx + r, cy + offset + r], fill=(0, 0, 0, alpha))
    return sh.filter(ImageFilter.GaussianBlur(blur))


def draw_pin(d, x, y, label):
    x, y, r = x * SS, y * SS, PIN * SS / 2
    d.ellipse([x - r, y - r, x + r, y + r], fill=WHITE)
    r2 = r - RING * SS
    d.ellipse([x - r2, y - r2, x + r2, y + r2], fill=ACCENT)
    d.text((x, y), label, font=font(PIN * 0.60 * SS), fill=WHITE, anchor="mm")


def draw_base(d, x, y):
    x, y, r = x * SS, y * SS, PIN * SS / 2
    d.rounded_rectangle([x - r, y - r, x + r, y + r], radius=5 * SS, fill=WHITE)
    b = 4 * SS
    d.rounded_rectangle([x - r + b, y - r + b, x + r - b, y + r - b], radius=3 * SS, fill=ACCENT)
    b = 17 * SS
    d.rectangle([x - r + b, y - r + b, x + r - b, y + r - b], fill=WHITE)


def text_outlined(d, xy, txt, size, anchor="lm"):
    d.text((xy[0] * SS, xy[1] * SS), txt, font=font(size * SS), fill=WHITE, anchor=anchor, stroke_width=3 * SS, stroke_fill=INK)


def nice_km(max_km):
    for v in (500, 200, 100, 50, 20, 10, 5, 2, 1, 0.5):
        if v <= max_km:
            return v
    return 0.5


def scale_bar_size(panel, frac):
    km = nice_km(panel.W * frac * panel.km_per_px())
    return km, km / panel.km_per_px()


def draw_scale_bar(d, x, y, km, length):
    """Bar with its left end at x, vertical centre y; label above."""
    h, c = 8, 3
    d.rectangle([(x - c) * SS, (y - h / 2 - c) * SS, (x + length + c) * SS, (y + h / 2 + c) * SS], fill=INK)
    d.rectangle([x * SS, (y - h / 2) * SS, (x + length) * SS, (y + h / 2) * SS], fill=WHITE)
    for tx in (x, x + length):
        d.rectangle([(tx - 1.5 - c) * SS, (y - 12 - c) * SS, (tx + 1.5 + c) * SS, (y + 12 + c) * SS], fill=INK)
        d.rectangle([(tx - 1.5) * SS, (y - 12) * SS, (tx + 1.5) * SS, (y + 12) * SS], fill=WHITE)
    label = f"{km:g} km"
    text_outlined(d, (x + length / 2, y - 24), label, 22, anchor="mm")


def draw_north(d, cx, top):
    """Small north arrow; `top` is the y of the N label centre."""
    ay = top + 18
    poly = [(cx, ay), (cx + 11, ay + 40), (cx, ay + 32), (cx - 11, ay + 40)]
    p = [(x * SS, y * SS) for x, y in poly]
    d.polygon(p, fill=INK)
    d.line(p + [p[0]], fill=INK, width=6 * SS, joint="curve")
    d.polygon(p, fill=WHITE)
    d.line([p[0], p[2]], fill=INK, width=2 * SS)
    text_outlined(d, (cx, top), "N", 24, anchor="mm")


# ---------- locator (Natural Earth) ----------

def fetch_countries(cache: Path):
    """Natural Earth admin-0 countries (GeoJSON, 1:50m, else 1:110m); downloaded once and cached."""
    for url in NE_URLS:
        f = cache / url.rsplit("/", 1)[1]
        if not f.exists():
            try:
                req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
                with urllib.request.urlopen(req, timeout=120) as r:
                    body = r.read()
                cache.mkdir(parents=True, exist_ok=True)
                f.write_bytes(body)
            except (urllib.error.URLError, OSError) as ex:
                print(f"  {url} failed: {ex}")
                continue
        return json.loads(f.read_text(encoding="utf-8"))["features"]
    sys.exit("Natural Earth countries not reachable; use --no-locator to skip the locator.")


def rings_of(geom):
    """Outer rings (lists of lon/lat) of a Polygon or MultiPolygon."""
    polys = [geom["coordinates"]] if geom["type"] == "Polygon" else geom["coordinates"] if geom["type"] == "MultiPolygon" else []
    return [poly[0] for poly in polys]


def draw_locator(features, iso, lon, lat, label, city, width, margin_deg=1.5):
    """Flat locator map of one country (equirectangular, cropped to its bounding box plus a margin), framed like the inset."""
    home = [f for f in features if iso in (f["properties"].get(k) for k in ("ADM0_A3", "ISO_A3", "ADM0_A3_US"))]
    if not home:
        sys.exit(f"Country {iso} not found in the Natural Earth data.")
    pts = [pt for r in rings_of(home[0]["geometry"]) for pt in r]
    lon0, lon1 = min(p[0] for p in pts) - margin_deg, max(p[0] for p in pts) + margin_deg
    lat0, lat1 = min(p[1] for p in pts) - margin_deg, max(p[1] for p in pts) + margin_deg
    kx = math.cos(math.radians((lat0 + lat1) / 2))
    bw = 4
    W = width - 2 * bw
    H = round(W * (lat1 - lat0) / ((lon1 - lon0) * kx))
    sc = W * SS / (lon1 - lon0)

    def px(lo, la):
        return (lo - lon0) * sc, (lat1 - la) * sc / kx

    img = Image.new("RGB", (W * SS, H * SS), SEA)
    d = ImageDraw.Draw(img)
    for f in features:
        is_home = f is home[0]
        for ring in rings_of(f["geometry"]):
            xs, ys = [p[0] for p in ring], [p[1] for p in ring]
            if max(xs) < lon0 or min(xs) > lon1 or max(ys) < lat0 or min(ys) > lat1:
                continue
            xy = [px(*p[:2]) for p in ring]
            d.polygon(xy, fill=LAND_HOME if is_home else LAND_OTHER)
            d.line(xy + [xy[0]], fill=INK if is_home else BORDER, width=round((2.2 if is_home else 1.4) * SS), joint="curve")
    # orientation dot (capital) and the marker
    cx, cy = px(*CAPITAL_LL)
    r = 6 * SS
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=INK, outline=WHITE, width=2 * SS)
    d.text((cx + 16 * SS, cy + 6 * SS), city, font=font(34 * SS), fill=INK, anchor="lm", stroke_width=4 * SS, stroke_fill=WHITE)
    mx, my = px(lon, lat)
    for rr, col in ((32, ACCENT), (28, WHITE), (20, ACCENT), (15, WHITE), (10.5, ACCENT)):
        d.ellipse([mx - rr * SS, my - rr * SS, mx + rr * SS, my + rr * SS], fill=col)
    d.text((mx - 42 * SS, my), label, font=font(42 * SS), fill=ACCENT, anchor="rm", stroke_width=5 * SS, stroke_fill=WHITE)
    img = img.resize((W, H), Image.LANCZOS)
    framed = Image.new("RGB", (W + 2 * bw, H + 2 * bw), WHITE)
    framed.paste(img, (bw, bw))
    print(f"  locator {framed.width}x{framed.height}")
    return framed


# ---------- road network (OpenStreetMap through Overpass) ----------

def fetch_osm(cache_file: Path, bbox_ll, highway_filter: str):
    """Ways with geometry inside bbox (south, west, north, east); the JSON answer is cached."""
    if cache_file.exists():
        return json.loads(cache_file.read_text(encoding="utf-8"))
    s, w, n, e = bbox_ll
    query = f"[out:json][timeout:180];way[highway{highway_filter}]({s:.5f},{w:.5f},{n:.5f},{e:.5f});out geom;"
    data = urllib.parse.urlencode({"data": query}).encode()
    last = None
    for url in OVERPASS:  # main server, then the mirror once
        try:
            req = urllib.request.Request(url, data=data, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(req, timeout=240) as r:
                body = r.read()
            result = json.loads(body)
            cache_file.parent.mkdir(parents=True, exist_ok=True)
            cache_file.write_bytes(body)
            return result
        except (urllib.error.URLError, OSError, ValueError) as ex:
            last = ex
            print(f"  Overpass {url} failed: {ex}")
    sys.exit(f"Overpass not reachable ({last}); stopping.")


class Graph:
    """Road graph on the local km grid. Edges are straight pieces between consecutive way vertices."""

    def __init__(self):
        self.pos: list[tuple[float, float]] = []
        self.adj: list[dict[int, float]] = []
        self.virtual: set[tuple[int, int]] = set()  # stubs and bridges (not on a road)
        self._key: dict[tuple[float, float], int] = {}

    def add_node(self, p):
        self.pos.append(p)
        self.adj.append({})
        return len(self.pos) - 1

    def length(self, a, b):
        return dist(self.pos[a], self.pos[b])

    def add_edge(self, a, b, virtual=False, factor=1.0):
        """Edge cost = length x factor (a factor above 1 makes a straight link less attractive than a road)."""
        if a == b:
            return
        d = dist(self.pos[a], self.pos[b]) * factor
        self.adj[a][b] = self.adj[b][a] = d
        if virtual:
            self.virtual.add((min(a, b), max(a, b)))

    def is_virtual(self, a, b):
        return (min(a, b), max(a, b)) in self.virtual

    @classmethod
    def from_osm(cls, osm, loc: Local):
        g = cls()
        for el in osm.get("elements", []):
            geom = el.get("geometry")
            if el.get("type") != "way" or not geom:
                continue
            prev = None
            for pt in geom:
                k = (round(pt["lon"], 7), round(pt["lat"], 7))
                if k not in g._key:
                    g._key[k] = g.add_node(loc.xy(*k))
                n = g._key[k]
                if prev is not None:
                    g.add_edge(prev, n)
                prev = n
        return g

    def add_terminal(self, p):
        """New node at p, tied to the nearest road point by a stub. The road edge is split at that point."""
        best = None
        for a, nbrs in enumerate(self.adj):
            for b in nbrs:
                if b < a or self.is_virtual(a, b):
                    continue
                pa, pb = self.pos[a], self.pos[b]
                dx, dy = pb[0] - pa[0], pb[1] - pa[1]
                L2 = dx * dx + dy * dy
                t = 0.0 if L2 == 0 else max(0.0, min(1.0, ((p[0] - pa[0]) * dx + (p[1] - pa[1]) * dy) / L2))
                q = (pa[0] + t * dx, pa[1] + t * dy)
                d = dist(p, q)
                if best is None or d < best[0]:
                    best = (d, a, b, t, q)
        t_node = self.add_node(p)
        if best is None:
            return t_node, float("inf")
        d, a, b, t, q = best
        if t <= 1e-9:
            snap = a
        elif t >= 1 - 1e-9:
            snap = b
        else:
            snap = self.add_node(q)
            del self.adj[a][b], self.adj[b][a]
            self.add_edge(a, snap)
            self.add_edge(snap, b)
        self.add_edge(t_node, snap, virtual=True)
        return t_node, d

    def add_shortcuts(self, root, max_km=30.0, ratio=4.0, factor=2.0, cell=2.0, max_links=6):
        """Straight links (cost x factor) between road points that are close as the crow flies but far apart by road
        from root: stands for the unmapped tracks a driver would really take instead of a huge road detour.
        Greedy: the link with the largest saving first, then the distances are recomputed."""
        added = 0
        for _ in range(max_links):
            dd, _p = self.dijkstra(root)
            cells: dict[tuple[int, int], int] = {}
            for n in dd:
                if all(self.is_virtual(n, m) for m in self.adj[n]):
                    continue
                cells.setdefault((int(self.pos[n][0] // cell), int(self.pos[n][1] // cell)), n)
            nodes = list(cells.values())
            best = None
            for i, u in enumerate(nodes):
                for v in nodes[i + 1:]:
                    s = dist(self.pos[u], self.pos[v])
                    gap = abs(dd[u] - dd[v])
                    if s <= max_km and gap > ratio * s and (best is None or gap - factor * s > best[0]):
                        best = (gap - factor * s, u, v)
            if best is None:
                break
            self.add_edge(best[1], best[2], virtual=True, factor=factor)
            added += 1
        return added

    def dijkstra(self, src, dst=None):
        dd = {src: 0.0}
        prev: dict[int, int] = {}
        heap = [(0.0, src)]
        while heap:
            d, u = heapq.heappop(heap)
            if d > dd.get(u, float("inf")):
                continue
            if u == dst:
                break
            for v, w in self.adj[u].items():
                nd = d + w
                if nd < dd.get(v, float("inf")):
                    dd[v] = nd
                    prev[v] = u
                    heapq.heappush(heap, (nd, v))
        return dd, prev

    def connect(self, root, terms):
        """Bridge unreachable terminals to the network reachable from root with straight segments. Returns [(terminal, km)]."""
        bridged = []
        while True:
            dd, _ = self.dijkstra(root)
            lost = [t for t in terms if t not in dd]
            if not lost:
                return bridged
            reach = list(dd)
            best = min(((dist(self.pos[t], self.pos[r]), t, r) for t in lost for r in reach), key=lambda x: x[0])
            self.add_edge(best[1], best[2], virtual=True)
            bridged.append((best[1], best[0]))

    def path(self, src, dst):
        dd, prev = self.dijkstra(src, dst)
        if dst not in dd:
            return None
        out = [dst]
        while out[-1] != src:
            out.append(prev[out[-1]])
        return out[::-1]


def chains(g: Graph, edges):
    """Merge a set of edges into polylines (xy); returns (lines, road_km, off_road_km)."""
    nb: dict[int, set[int]] = {}
    for a, b in edges:
        nb.setdefault(a, set()).add(b)
        nb.setdefault(b, set()).add(a)
    road = sum(g.length(a, b) for a, b in edges if not g.is_virtual(a, b))
    off = sum(g.length(a, b) for a, b in edges if g.is_virtual(a, b))
    seen: set[tuple[int, int]] = set()
    lines = []

    def walk(start, nxt):
        line = [start]
        prev, cur = start, nxt
        seen.add((min(prev, cur), max(prev, cur)))
        line.append(cur)
        while len(nb[cur]) == 2:
            n2 = next(x for x in nb[cur] if x != prev)
            key = (min(cur, n2), max(cur, n2))
            if key in seen:
                break
            seen.add(key)
            prev, cur = cur, n2
            line.append(cur)
        return line

    for n in [n for n in nb if len(nb[n]) != 2] + list(nb):
        for m in nb[n]:
            if (min(n, m), max(n, m)) not in seen:
                lines.append(walk(n, m))
    return [[g.pos[i] for i in l] for l in lines], road, off

# ---------- layout ----------

def spread(pts, min_d, iters=60):
    """Push markers apart until none is closer than min_d. Returns displaced copies."""
    pts = [list(p) for p in pts]
    for _ in range(iters):
        moved = False
        for i, j in itertools.combinations(range(len(pts)), 2):
            dx, dy = pts[j][0] - pts[i][0], pts[j][1] - pts[i][1]
            dd = math.hypot(dx, dy)
            if dd < min_d:
                if dd < 1e-6:
                    dx, dy, dd = 1.0, 0.0, 1.0
                push = (min_d - dd) / 2 + 0.5
                ux, uy = dx / dd, dy / dd
                pts[i][0] -= ux * push
                pts[i][1] -= uy * push
                pts[j][0] += ux * push
                pts[j][1] += uy * push
                moved = True
        if not moved:
            break
    return [tuple(p) for p in pts]


def assign_corners(items, W, H, obstacles, route_pts):
    """Give each furniture item its own corner with the least overlap on pins and route.
    items: {name: (w, h, preferred_corner, bottom_only)}; corners: tl tr bl br."""
    corners = ["tl", "tr", "bl", "br", "tm", "bm", "ml", "mr"]  # four corners, then the middle of each edge

    def rect(corner, w, h):
        x = MARGIN if corner[1] == "l" else W - MARGIN - w if corner[1] == "r" else (W - w) / 2
        y = MARGIN if corner[0] == "t" else H - MARGIN - h if corner[0] == "b" else (H - h) / 2
        return x, y, x + w, y + h

    def cost(name, corner):
        w, h, pref, bottom = items[name]
        if bottom and corner[0] != "b":
            return 1e9
        x0, y0, x1, y1 = rect(corner, w, h)
        c = 0.0 if corner == pref else 1.0
        if "m" in corner:
            c += 0.5  # corners first
        for ox, oy, r in obstacles:
            if x0 - r < ox < x1 + r and y0 - r < oy < y1 + r:
                c += 1000
        c += sum(1 for px, py in route_pts if x0 < px < x1 and y0 < py < y1) * 2
        return c

    best = None
    for perm in itertools.permutations(corners, len(items)):
        total = sum(cost(n, c) for n, c in zip(items, perm))
        rects = [rect(c, items[n][0], items[n][1]) for n, c in zip(items, perm)]
        for a, b in itertools.combinations(rects, 2):  # furniture must not overlap furniture
            if a[0] < b[2] + 12 and b[0] < a[2] + 12 and a[1] < b[3] + 12 and b[1] < a[3] + 12:
                total += 1e6
        if best is None or total < best[0]:
            best = (total, perm)
    return {n: rect(c, items[n][0], items[n][1]) for n, c in zip(items, best[1])}, best[0]


# ---------- main ----------

def route_edges(g: Graph, root, targets):
    """Union of the shortest paths from root to every target, as a set of (a, b) edges."""
    edges = set()
    per = {}
    for t in targets:
        p = g.path(root, t)
        e = {(min(a, b), max(a, b)) for a, b in zip(p, p[1:])}
        edges |= e
        per[t] = (sum(g.length(a, b) for a, b in e if not g.is_virtual(a, b)), sum(g.length(a, b) for a, b in e if g.is_virtual(a, b)))
    return edges, per


def main() -> int:
    ap = argparse.ArgumentParser(description="Satellite route map with pins, road route and inset.")
    ap.add_argument("inventory", type=Path)
    ap.add_argument("out_dir", type=Path)
    ap.add_argument("--drive", type=int, nargs="+", required=True, help="photo numbers of the road points (inset route)")
    ap.add_argument("--base", type=int, nargs="+", required=True, help="photo numbers at the base camp")
    ap.add_argument("--waypoints", type=int, nargs="*", default=[], help="photo numbers of waypoint-only places (no pin, not drawn)")
    ap.add_argument("--cluster-km", type=float, default=1.5, help="photos closer than this belong to one place")
    ap.add_argument("--width", type=int, default=2400, help="width of the main panel in px (default 2400)")
    ap.add_argument("--inset-width", type=int, default=800)
    ap.add_argument("--sat", type=float, default=0.45, help="colour saturation factor for the imagery (1 = untouched)")
    ap.add_argument("--dim", type=float, default=0.9, help="brightness factor for the imagery (1 = untouched)")
    ap.add_argument("--no-locator", action="store_true", help="skip the country locator inset")
    ap.add_argument("--locator-label", default="Alrar", help="label of the marker in the locator")
    ap.add_argument("--locator-city", default="Alger", help="label of the orientation dot (the capital) in the locator")
    ap.add_argument("--locator-country", default="DZA", help="ISO alpha-3 code of the country drawn in the locator")
    ap.add_argument("--locator-width", type=int, default=560)
    ap.add_argument("--name", default="route-map", help="output file name (without .jpg)")
    args = ap.parse_args()

    if not args.inventory.is_file():
        sys.exit(f"File not found: {args.inventory}")
    out = args.out_dir
    out.mkdir(parents=True, exist_ok=True)
    cache = out / "tiles"

    photos = read_photos(args.inventory)
    gps = [p for p in photos if p["gps"]]
    loc = Local(sum(p["gps"][0] for p in gps) / len(gps), sum(p["gps"][1] for p in gps) / len(gps))
    places = make_places(photos, loc, args.cluster_km, args.drive, args.base, args.waypoints)
    pins = [p for p in places if p["kind"] == "pin"]
    drive = [p for p in places if p["kind"] == "drive"]
    wpts = [p for p in places if p["kind"] == "waypoint"]
    base_l = [p for p in places if p["kind"] == "base"]
    if len(base_l) != 1 or not pins or not drive:
        sys.exit(f"Expected one base, some pins and road points; got base={len(base_l)} pins={len(pins)} drive={len(drive)}")
    base = base_l[0]
    print(f"{len(places)} places: {len(pins)} pins, {len(wpts)} waypoints (not drawn), {len(drive)} road points, 1 base")

    # pins.txt (no coordinates)
    lines = ["pin  first visit  photos"]
    for p in pins:
        lines.append(f"{p['pin']:>3}  {p['first']:%Y-%m-%d}   {', '.join(map(str, p['photos']))}")
    lines += ["", "base camp: photos " + ", ".join(map(str, base["photos"])), "waypoints (no pin, not drawn): " + "; ".join(
        f"{', '.join(map(str, w['photos']))} ({w['first']:%Y-%m-%d})" for w in wpts),
        "road points (inset): " + "; ".join(f"{', '.join(map(str, w['photos']))} ({w['first']:%Y-%m-%d})" for w in drive)]
    (out / "pins.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")

    # ---- road route for the field: query area = pins + base with a wide margin
    field_uv = [merc(p["lon"], p["lat"]) for p in pins + [base]]
    qbox = box_around(field_uv, 1.0, 4 / 3, 0.30)
    (w_, n_), (e_, s_) = _uv_to_ll(qbox[0], qbox[1]), _uv_to_ll(qbox[2], qbox[3])
    print("OSM roads for the field")
    g = Graph.from_osm(fetch_osm(out / "osm" / "field.json", (s_, w_, n_, e_), ""), loc)
    print(f"  graph: {len(g.pos)} nodes")
    base_node, base_off = g.add_terminal(loc.xy(base["lon"], base["lat"]))
    pin_nodes = []
    pin_off = []
    for p in pins:
        t, d = g.add_terminal(loc.xy(p["lon"], p["lat"]))
        pin_nodes.append(t)
        pin_off.append(d)
    bridged = g.connect(base_node, pin_nodes)
    print(f"  {g.add_shortcuts(base_node)} straight shortcut links added (stand-in for unmapped tracks)")
    bridged_nodes = {t for t, _ in bridged}
    edges, per = route_edges(g, base_node, pin_nodes)
    field_lines, road_km, off_km = chains(g, edges)
    print(f"route: {road_km:.1f} km on OSM ways, {off_km:.1f} km straight stubs/bridges ({100 * road_km / (road_km + off_km):.0f}% on roads)")
    print(f"  base: {base_off * 1000:.0f} m from the nearest way")
    for p, t, d in zip(pins, pin_nodes, pin_off):
        on, off = per[t]
        flag = "  BRIDGED (network disconnected)" if t in bridged_nodes else ""
        print(f"  pin {p['pin']:>2}: {d * 1000:5.0f} m to nearest way{'  (> 300 m, straight stub)' if d > 0.3 else ''}; path {on:.1f} km road + {off:.2f} km off-road{flag}")

    # ---- panels: frame the whole network with a 6 % margin, aspect between 1:1 and 4:3
    frame_pts = [merc(*loc.ll(*pt)) for l in field_lines for pt in l] + field_uv
    main_box = box_around(frame_pts, 1.0, 4 / 3, 0.06)
    main = Panel(main_box, args.width)
    road = sorted(drive, key=lambda p: p["first"]) + [base]
    inset_box = box_around([merc(p["lon"], p["lat"]) for p in road], 1.6, 1.6, 0.14, aspect_fixed=1.6)
    inset = Panel(inset_box, args.inset_width)
    print(f"main {main.W}x{main.H}, inset {inset.W}x{inset.H}")

    # ---- road route for the drive in (big roads only), through the road points in order
    (w_, n_), (e_, s_) = _uv_to_ll(inset_box[0], inset_box[1]), _uv_to_ll(inset_box[2], inset_box[3])
    print("OSM main roads for the drive in")
    gi = Graph.from_osm(fetch_osm(out / "osm" / "drive.json", (s_, w_, n_, e_), '~"trunk|primary|secondary"'), loc)
    print(f"  graph: {len(gi.pos)} nodes")
    rnodes = []
    for p in road:
        t, d = gi.add_terminal(loc.xy(p["lon"], p["lat"]))
        rnodes.append(t)
        print(f"  road point {p['photos'][0]}: {d * 1000:.0f} m from the nearest main road")
    br = gi.connect(rnodes[0], rnodes[1:])
    d_edges = set()
    for a, b in zip(rnodes, rnodes[1:]):
        pth = gi.path(a, b)
        d_edges |= {(min(x, y), max(x, y)) for x, y in zip(pth, pth[1:])}
    drive_lines, d_road, d_off = chains(gi, d_edges)
    print(f"drive in: {d_road:.0f} km on OSM ways, {d_off:.1f} km stubs/bridges, {len(br)} bridges")

    print("fetching imagery")
    main_img = tone(main.basemap(cache), args.sat, args.dim)
    inset_img = tone(inset.basemap(cache), args.sat, args.dim)

    # inset: drive-in route, main-panel rectangle, base marker, scale bar
    road_px = [[inset.proj(*loc.ll(*pt)) for pt in l] for l in drive_lines]
    ov = Image.new("RGBA", (inset.W * SS, inset.H * SS), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    mx0, my0 = inset.proj(*_uv_to_ll(main.u0, main.v0))
    mx1, my1 = inset.proj(*_uv_to_ll(main.u1, main.v1))
    for w, col in ((6, INK), (3, WHITE)):
        d.rectangle([mx0 * SS, my0 * SS, mx1 * SS, my1 * SS], outline=col, width=round(w * SS))
    draw_routes(d, road_px, INSET_W, INSET_CASE)
    bx, by = inset.proj(base["lon"], base["lat"])
    r = 7 * SS
    d.rectangle([bx * SS - r - 2 * SS, by * SS - r - 2 * SS, bx * SS + r + 2 * SS, by * SS + r + 2 * SS], fill=INK)
    d.rectangle([bx * SS - r, by * SS - r, bx * SS + r, by * SS + r], fill=WHITE)
    km, length = scale_bar_size(inset, 0.30)
    draw_scale_bar(d, 28, inset.H - 28, km, length)
    ov = ov.resize((inset.W, inset.H), Image.LANCZOS)
    inset_final = Image.alpha_composite(inset_img.convert("RGBA"), ov).convert("RGB")
    bw = 4
    framed = Image.new("RGB", (inset.W + 2 * bw, inset.H + 2 * bw), WHITE)
    framed.paste(inset_final, (bw, bw))

    # locator inset: marker at the centroid of the pins
    loc_img, credit = None, ATTRIBUTION
    if not args.no_locator:
        print("locator map")
        loc_img = draw_locator(fetch_countries(out / "ne"), args.locator_country, sum(p["lon"] for p in pins) / len(pins),
                               sum(p["lat"] for p in pins) / len(pins), args.locator_label, args.locator_city, args.locator_width)
        credit = ATTRIBUTION + LOCATOR_CREDIT

    # furniture sizes (main panel)
    km_m, len_m = scale_bar_size(main, 0.16)
    att_font = font(15 * SS)
    att_w = ImageDraw.Draw(Image.new("L", (1, 1))).textlength(credit, font=att_font) / SS + 16
    items = {"inset": (framed.width, framed.height, "tl", False),
             "attribution": (att_w, 26, "br", True),
             "scale": (len_m + 16, 60, "bl", False),
             "north": (44, 84, "tr", False)}
    if loc_img:
        items["locator"] = (loc_img.width, loc_img.height, "br", False)

    pin_xy = [main.proj(p["lon"], p["lat"]) for p in pins]
    base_xy = main.proj(base["lon"], base["lat"])
    shown = spread(pin_xy + [base_xy], PIN + 8)
    pin_show, base_show = shown[:-1], shown[-1]

    lines_px = [[main.proj(*loc.ll(*pt)) for pt in l] for l in field_lines]
    obstacles = [(x, y, PIN / 2 + 10) for x, y in pin_show + [base_show]]
    route_pts = [pt for l in lines_px for a, b in zip(l, l[1:]) for pt in (a, b, ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2))]
    slots, penalty = assign_corners(items, main.W, main.H, obstacles, route_pts)
    if penalty >= 1000:
        print(f"  WARNING: a corner item overlaps a pin (penalty {penalty:.0f})")
    ov = Image.new("RGBA", (main.W * SS, main.H * SS), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    draw_routes(d, lines_px, LINE_W, LINE_CASE)
    for (sx, sy), (tx, ty) in zip(pin_show, pin_xy):  # leaders for displaced markers
        if dist((sx, sy), (tx, ty)) > 3:
            draw_routes(d, [[(sx, sy), (tx, ty)]], 3, 7)
            rr = 7
            d.ellipse([(tx - rr) * SS, (ty - rr) * SS, (tx + rr) * SS, (ty + rr) * SS], fill=WHITE, outline=INK, width=SS)
    if dist(base_show, base_xy) > 3:
        draw_routes(d, [[base_show, base_xy]], 3, 7)
    sh = shadow_layer(ov.size, [(x * SS, y * SS, PIN * SS / 2) for x, y in pin_show + [base_show]], 7 * SS, 5 * SS)
    ov = Image.alpha_composite(ov, sh)
    d = ImageDraw.Draw(ov)
    draw_base(d, *base_show)
    for (x, y), p in zip(pin_show, pins):
        draw_pin(d, x, y, str(p["pin"]))
    x0, y0, x1, y1 = slots["scale"]
    draw_scale_bar(d, x0 + 8, y1 - 14, km_m, len_m)
    x0, y0, x1, y1 = slots["north"]
    draw_north(d, (x0 + x1) / 2, y0 + 14)
    x0, y0, x1, y1 = slots["attribution"]
    d.rounded_rectangle([x0 * SS, y0 * SS, x1 * SS, y1 * SS], radius=4 * SS, fill=(*INK, 150))
    d.text(((x0 + 8) * SS, (y0 + y1) / 2 * SS), credit, font=att_font, fill=WHITE, anchor="lm")
    ov = ov.resize((main.W, main.H), Image.LANCZOS)
    final = Image.alpha_composite(main_img.convert("RGBA"), ov).convert("RGB")
    x0, y0, _, _ = slots["inset"]
    final.paste(framed, (round(x0), round(y0)))
    if loc_img:
        x0, y0, _, _ = slots["locator"]
        final.paste(loc_img, (round(x0), round(y0)))
    clean = Image.new("RGB", final.size)
    clean.paste(final)  # nothing but pixels, no metadata
    dest = out / f"{args.name}.jpg"
    clean.save(dest, "JPEG", quality=88, optimize=True)
    print(f"wrote {dest.name}  {clean.width}x{clean.height}  {dest.stat().st_size / 1024:.0f} KB  ({len(pins)} pins)")
    return 0


def tone(img: Image.Image, sat: float, dim: float) -> Image.Image:
    """Restrained look: less saturation, slightly darker, so the white route and navy pins stand out."""
    return ImageEnhance.Brightness(ImageEnhance.Color(img).enhance(sat)).enhance(dim)


def _uv_to_ll(u, v):
    lon = u * 360 - 180
    lat = math.degrees(2 * math.atan(math.exp(math.pi * (1 - 2 * v))) - math.pi / 2)
    return lon, lat


if __name__ == "__main__":
    sys.exit(main())
