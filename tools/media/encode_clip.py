#!/usr/bin/env python3
"""Encode a short web clip (H.264, no audio) plus a poster image for the portfolio site.

    python tools/media/encode_clip.py <input> <section>/<slug>/<name> [--start s] [--end s] [--speed N]
                                      [--width 1280] [--poster-at s]

Example:
    python tools/media/encode_clip.py raw.mov projects/scada-gk3-audit/hero --start 12 --end 24 --poster-at 3

Output goes to public/media/<section>/<slug>/<name>.mp4 and <name>.jpg (the poster). Video is H.264
yuv420p, CRF 26, no audio, +faststart, max width 1280. All source metadata (GPS, device, dates) is
stripped. A timelapse is made with --speed (8 = eight times faster). Warns above 6 MB.

Needs ffmpeg (and ffprobe) on PATH.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SECTIONS = ("projects", "simulators")
MAX_MB = 6.0
KEBAB = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")

MISSING_FFMPEG = """ffmpeg was not found on your PATH.
Install it, then open a NEW terminal window:
  Windows (winget):      winget install Gyan.FFmpeg
  Windows (Chocolatey):  choco install ffmpeg
  Windows (manual):      download a build from https://www.gyan.dev/ffmpeg/builds/ , unzip it,
                         and add its "bin" folder to the PATH environment variable
  macOS:                 brew install ffmpeg
  Linux (Debian/Ubuntu): sudo apt install ffmpeg
Check with:  ffmpeg -version"""


def run(cmd: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")


def probe_fps(ffprobe: str | None, src: Path) -> float | None:
    if not ffprobe:
        return None
    r = run([ffprobe, "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=r_frame_rate", "-of", "json", str(src)])
    try:
        num, den = json.loads(r.stdout)["streams"][0]["r_frame_rate"].split("/")
        return float(num) / float(den) if float(den) else None
    except Exception:
        return None


def main() -> int:
    ap = argparse.ArgumentParser(description="Encode a web clip + poster with ffmpeg.")
    ap.add_argument("input", type=Path, help="source video (mp4, mov, mkv, ...)")
    ap.add_argument("target", help="<section>/<slug>/<name>, e.g. projects/scada-gk3-audit/hero")
    ap.add_argument("--start", type=float, default=None, help="start time in the source, seconds")
    ap.add_argument("--end", type=float, default=None, help="end time in the source, seconds")
    ap.add_argument("--speed", type=float, default=1.0, help="speed factor via setpts: 8 = timelapse x8, 0.5 = slow motion")
    ap.add_argument("--width", type=int, default=1280, help="max output width in px (default 1280; never upscales)")
    ap.add_argument("--poster-at", type=float, default=None, help="poster frame time in seconds of the OUTPUT clip (default: 1 s or the middle if shorter)")
    ap.add_argument("--crf", type=int, default=26, help="x264 quality, lower = better and bigger (default 26)")
    ap.add_argument("--out-root", type=Path, default=REPO_ROOT, help=argparse.SUPPRESS)  # for tests
    args = ap.parse_args()

    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        print(MISSING_FFMPEG, file=sys.stderr)
        return 2
    ffprobe = shutil.which("ffprobe")

    if not args.input.is_file():
        sys.exit(f"Input file not found: {args.input}")
    parts = [p for p in args.target.replace("\\", "/").strip("/").split("/") if p]
    if len(parts) != 3 or parts[0] not in SECTIONS or not all(KEBAB.match(p) for p in parts[1:]):
        sys.exit("Target must be <section>/<slug>/<name> with section in %s and kebab-case slug and name\n"
                 "  e.g. projects/scada-gk3-audit/hero" % "|".join(SECTIONS))
    section, slug, name = parts
    if args.speed <= 0:
        sys.exit("--speed must be > 0")
    if args.start is not None and args.end is not None and args.end <= args.start:
        sys.exit("--end must be after --start")

    out_dir = args.out_root / "public" / "media" / section / slug
    out_dir.mkdir(parents=True, exist_ok=True)
    mp4 = out_dir / f"{name}.mp4"
    poster = out_dir / f"{name}.jpg"

    cmd = [ffmpeg, "-hide_banner", "-loglevel", "error", "-y"]
    if args.start is not None:
        cmd += ["-ss", f"{args.start}"]
    if args.end is not None:  # -t (duration) is unambiguous when combined with an input -ss
        cmd += ["-t", f"{args.end - (args.start or 0)}"]
    cmd += ["-i", str(args.input)]

    filters = []
    if args.speed != 1.0:
        filters.append(f"setpts=PTS/{args.speed}")
    fps = probe_fps(ffprobe, args.input)
    if fps and fps > 30.5:
        filters.append("fps=30")  # phone 50/60 fps footage doubles the file size for no visible benefit
    filters.append(f"scale=trunc(min({args.width}\\,iw)/2)*2:-2")  # max width, even dimensions, keep aspect
    filters.append("format=yuv420p")
    cmd += ["-vf", ",".join(filters), "-an", "-sn", "-dn", "-map_metadata", "-1", "-map_chapters", "-1",
            "-c:v", "libx264", "-preset", "slow", "-crf", str(args.crf), "-pix_fmt", "yuv420p",
            "-movflags", "+faststart", str(mp4)]

    print("Encoding", mp4)
    r = run(cmd)
    if r.returncode != 0 or not mp4.exists():
        print(r.stderr, file=sys.stderr)
        sys.exit("ffmpeg failed (see above).")

    # duration of the result, to choose a sensible poster frame
    dur = None
    if ffprobe:
        d = run([ffprobe, "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", str(mp4)])
        try:
            dur = float(d.stdout.strip())
        except ValueError:
            pass
    at = args.poster_at if args.poster_at is not None else (min(1.0, dur / 2) if dur else 0.0)
    pr = run([ffmpeg, "-hide_banner", "-loglevel", "error", "-y", "-ss", f"{at}", "-i", str(mp4),
              "-frames:v", "1", "-q:v", "3", "-map_metadata", "-1", str(poster)])
    if pr.returncode != 0 or not poster.exists():
        print(pr.stderr, file=sys.stderr)
        sys.exit("Poster extraction failed. Is --poster-at inside the clip?")

    mb = mp4.stat().st_size / 1024 / 1024
    print(f"OK  {mp4.name}  {mb:.2f} MB" + (f"  {dur:.1f} s" if dur else "") + f"   poster: {poster.name} ({poster.stat().st_size / 1024:.0f} KB)")
    if mb > MAX_MB:
        print(f"\nWARNING: {mb:.1f} MB is above the {MAX_MB:.0f} MB budget. Make it shorter (--start/--end), narrower (--width 960),"
              f" faster (--speed) or raise --crf (28-30).")
    print("\nFrontmatter reference:")
    print(f"  src: /media/{section}/{slug}/{name}.mp4")
    print(f"  poster: /media/{section}/{slug}/{name}.jpg")
    if ffprobe:
        s = run([ffprobe, "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height", "-of", "csv=p=0", str(mp4)])
        try:
            w, h = (int(x) for x in s.stdout.strip().split(",")[:2])
            print(f'  ratio: "{w} / {h}"   # projects only; may be left out for a 16:9 clip')
        except ValueError:
            pass
    return 0


if __name__ == "__main__":
    sys.exit(main())
