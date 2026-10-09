# Media tools

Two small Python 3 scripts that turn raw photos and videos into web-ready files. They work on Windows, macOS and Linux.
The repository is **public**, so these scripts also strip all metadata (GPS location, camera, dates) from everything they write.

Keep the raw originals OUTSIDE the repository, for example:

```
D:\Nadir\Documents\Portfolio\media-src\<slug>\
```

## One-time setup (Windows)

```powershell
pip install pillow            # required by prep_images.py
pip install pillow-heif       # optional: iPhone .heic photos
winget install Gyan.FFmpeg    # required by encode_clip.py (then open a NEW terminal)
```

Run the scripts from the repository root (the folder that contains `package.json`).

## `prep_images.py`: photos

```
python tools/media/prep_images.py <input_dir> <slug> [--section projects|simulators]
```

Windows example:

```powershell
python tools\media\prep_images.py "D:\Nadir\Documents\Portfolio\media-src\scada-gk3-audit" scada-gk3-audit
python tools\media\prep_images.py "D:\Nadir\Documents\Portfolio\media-src\substation-sim" substation-sim --section simulators
```

For every image it: rotates it upright (EXIF orientation), removes ALL metadata, caps the long edge at 2400 px,
saves JPEG quality 85 with a kebab-case file name, and writes it to `src/assets/<section>/<slug>/`.
It then prints a YAML snippet (`cover:` and `gallery:` with empty `alt`/`caption`) to paste into
`src/content/<section>/<slug>/index.md`. Fill alt text and captions in English and French.
It reports every file that contained GPS coordinates.

Drawings (single-line diagrams, layouts): crop out the client title block in an image editor first, then run the
script, and paste the printed items under `drawings:` instead of `gallery:`.

## `encode_clip.py`: video clips

```
python tools/media/encode_clip.py <input> <section>/<slug>/<name> [--start s] [--end s] [--speed N] [--width 1280] [--poster-at s]
```

Windows examples:

```powershell
# a 12 s excerpt as the hero clip of a project
python tools\media\encode_clip.py "D:\Nadir\Documents\Portfolio\media-src\scada-gk3-audit\walk.mov" projects/scada-gk3-audit/hero --start 12 --end 24 --poster-at 3

# a 3 minute screen recording of a simulator, as a 15x timelapse
python tools\media\encode_clip.py "D:\Nadir\Documents\Portfolio\media-src\substation-sim\run1.mp4" simulators/substation-sim/isolation --speed 15
```

Output: `public/media/<section>/<slug>/<name>.mp4` (H.264, yuv420p, CRF 26, no audio, `+faststart`, max width 1280,
60 fps footage reduced to 30 fps, metadata stripped) and a poster `<name>.jpg` next to it.
`--poster-at` is in seconds of the OUTPUT clip. The script warns when a file is over 6 MB: shorten it, use
`--width 960`, speed it up, or raise `--crf` (28 to 30). It prints the `src:`, `poster:` and `ratio:` lines to use in the frontmatter (`ratio` lets a project page give a portrait clip a portrait frame).

## After running

1. Edit the entry's frontmatter and body (see `CLAUDE.md`, "Adding a project / simulator").
2. Preview with drafts visible: `npm run dev`, or `npm run preview:drafts` (builds into `dist-drafts/` and serves it).
3. Set `draft: false` when the entry is ready, commit, open a PR.
