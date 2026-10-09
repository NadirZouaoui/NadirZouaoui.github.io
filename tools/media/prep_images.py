#!/usr/bin/env python3
"""Prepare photos for the portfolio site.

    python tools/media/prep_images.py <input_dir> <slug> [--section projects|simulators]

For every image in <input_dir>:
  * rotate it upright according to its EXIF orientation,
  * strip ALL metadata (EXIF incl. GPS, XMP, IPTC, comments, ICC profile; colours are converted to sRGB first),
  * cap the long edge at 2400 px (never upscales),
  * save as JPEG quality 85 with a kebab-case file name,
  * write it to src/assets/<section>/<slug>/.
Then it prints a YAML snippet to paste into the entry frontmatter (alt and caption left empty).

The repository is PUBLIC: never commit originals, only the output of this script.

Requires Pillow (pip install pillow). HEIC/HEIF (iPhone) also needs pillow-heif (pip install pillow-heif).
"""
from __future__ import annotations

import argparse
import io
import re
import sys
from pathlib import Path

try:
    from PIL import Image, ImageCms, ImageOps
except ImportError:  # pragma: no cover
    sys.exit("Pillow is not installed. Run:  pip install pillow   (and optionally: pip install pillow-heif)")

HEIF_OK = False
try:  # optional
    import pillow_heif  # type: ignore

    pillow_heif.register_heif_opener()
    HEIF_OK = True
except Exception:
    pass

MAX_EDGE = 2400
QUALITY = 85
EXTS = {".jpg", ".jpeg", ".png", ".webp", ".tif", ".tiff", ".bmp", ".heic", ".heif"}
SECTIONS = ("projects", "simulators")
REPO_ROOT = Path(__file__).resolve().parents[2]

GPS_IFD = 0x8825  # EXIF tag holding the GPS block


def kebab(name: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    return s or "image"


def has_gps(img: Image.Image) -> bool:
    try:
        return bool(img.getexif().get_ifd(GPS_IFD))
    except Exception:
        return False


def to_srgb(img: Image.Image) -> Image.Image:
    """Convert an embedded ICC profile to sRGB so dropping the profile does not shift colours."""
    icc = img.info.get("icc_profile")
    if not icc:
        return img
    try:
        src = ImageCms.ImageCmsProfile(io.BytesIO(icc))
        dst = ImageCms.createProfile("sRGB")
        return ImageCms.profileToProfile(img, src, dst, outputMode="RGB")
    except Exception:
        return img


def clean_copy(img: Image.Image) -> Image.Image:
    """A brand-new image holding only the pixels (nothing from .info survives)."""
    out = Image.new("RGB", img.size)
    out.paste(img)
    return out


def process(path: Path, dest: Path, max_edge: int, quality: int) -> tuple[int, int, bool]:
    with Image.open(path) as im:
        gps = has_gps(im)
        im = ImageOps.exif_transpose(im)  # applies orientation and drops the tag
        if im.mode in ("RGBA", "LA") or (im.mode == "P" and "transparency" in im.info):
            rgba = im.convert("RGBA")
            bg = Image.new("RGB", rgba.size, "white")
            bg.paste(rgba, mask=rgba.split()[-1])
            im = bg
        else:
            im = to_srgb(im)
            im = im.convert("RGB")
        w, h = im.size
        long_edge = max(w, h)
        if long_edge > max_edge:
            scale = max_edge / long_edge
            im = im.resize((max(1, round(w * scale)), max(1, round(h * scale))), Image.LANCZOS)
        out = clean_copy(im)
    out.save(dest, "JPEG", quality=quality, optimize=True, progressive=True)  # no exif=/icc_profile= on purpose
    return out.size[0], out.size[1], gps


def verify_clean(dest: Path) -> None:
    data = dest.read_bytes()
    for needle in (b"Exif\x00", b"http://ns.adobe.com/xap", b"ICC_PROFILE", b"Photoshop 3.0"):
        if needle in data:
            raise RuntimeError(f"metadata marker {needle!r} found in {dest.name}; refusing to keep it")
    with Image.open(dest) as chk:
        if len(chk.getexif()) or chk.info.get("icc_profile") or chk.info.get("comment"):
            raise RuntimeError(f"metadata found in {dest.name}; refusing to keep it")


def main() -> int:
    ap = argparse.ArgumentParser(description="Prepare photos (rotate, strip metadata, resize, JPEG q85) for the site.")
    ap.add_argument("input_dir", type=Path, help="folder with the original photos")
    ap.add_argument("slug", help="entry slug (kebab-case), e.g. scada-gk3-audit")
    ap.add_argument("--section", choices=SECTIONS, default="projects")
    ap.add_argument("--max-edge", type=int, default=MAX_EDGE, help=f"long edge cap in px (default {MAX_EDGE})")
    ap.add_argument("--quality", type=int, default=QUALITY, help=f"JPEG quality (default {QUALITY})")
    ap.add_argument("--out-root", type=Path, default=REPO_ROOT, help=argparse.SUPPRESS)  # for tests
    args = ap.parse_args()

    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", args.slug):
        sys.exit(f"Slug must be kebab-case (lowercase letters, digits, hyphens): {args.slug!r}")
    if not args.input_dir.is_dir():
        sys.exit(f"Input folder not found: {args.input_dir}")

    files = sorted(p for p in args.input_dir.iterdir() if p.is_file() and p.suffix.lower() in EXTS)
    if not files:
        sys.exit(f"No images ({', '.join(sorted(EXTS))}) in {args.input_dir}")

    out_dir = args.out_root / "src" / "assets" / args.section / args.slug
    out_dir.mkdir(parents=True, exist_ok=True)

    done: list[str] = []
    used: set[str] = set()
    gps_count = 0
    for p in files:
        if p.suffix.lower() in (".heic", ".heif") and not HEIF_OK:
            print(f"SKIPPED {p.name}: HEIC needs pillow-heif (pip install pillow-heif)")
            continue
        base = kebab(p.stem)
        name, n = base, 2
        while name in used:
            name, n = f"{base}-{n}", n + 1
        used.add(name)
        dest = out_dir / f"{name}.jpg"
        try:
            w, h, gps = process(p, dest, args.max_edge, args.quality)
            verify_clean(dest)
        except Exception as e:  # keep going, report at the end
            print(f"FAILED  {p.name}: {e}")
            if dest.exists():
                dest.unlink()
            continue
        gps_count += gps
        kb = dest.stat().st_size / 1024
        print(f"OK      {p.name} -> {dest.name}  {w}x{h}  {kb:.0f} KB" + ("  (GPS location removed)" if gps else ""))
        done.append(dest.name)

    if not done:
        return 1
    print(f"\n{len(done)} image(s) written to {out_dir}")
    if gps_count:
        print(f"{gps_count} image(s) contained GPS coordinates; they are gone from the output.")
    print("\nPaste into the frontmatter of src/content/%s/%s/index.md (fill alt and caption in EN and FR):\n" % (args.section, args.slug))
    ref = lambda f: f'"@assets/{args.section}/{args.slug}/{f}"'  # quoted: a bare @ is not valid YAML
    if args.section == "projects":
        print("cover: " + ref(done[0]) + "\ngallery:")
        for f in done:
            print(f'  - image: {ref(f)}\n    alt: {{ en: "", fr: "" }}\n    caption: {{ en: "", fr: "" }}')
        print("# Technical drawings go under `drawings:` with the same shape (crop the client title block first).")
    else:
        print("cover: " + ref(done[0]))
        print("# other images, if you need them elsewhere:")
        for f in done[1:]:
            print(f"#   {ref(f)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
