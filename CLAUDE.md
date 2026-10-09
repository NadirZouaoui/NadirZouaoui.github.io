# CLAUDE.md: nadirzouaoui.github.io

Personal portfolio of Nadir Zouaoui (electrical engineer), live at https://nadirzouaoui.github.io/.
Astro (static output) deployed to GitHub Pages by `.github/workflows/deploy.yml` on every push to `main`.
Bilingual EN/FR on the same URL. Plain, white, professional design; no heavy client JS (vanilla scripts only).

**Plan, status, open questions and media locations for the ongoing upgrade: `docs/PLAN.md`. Read it at the start of every session.**

## Hard rules (read first)

1. **Never push to `main`.** Work on a branch, open a PR (draft if unfinished). Before pushing from a shallow clone run `git fetch origin main`.
2. **The production CV must not change**: `/`, `/?lang=fr`, `/Nadir-Zouaoui-CV-EN.pdf`, `/Nadir-Zouaoui-CV-FR.pdf`, `/og.png` keep working. The CV print output (`@media print`, `@page`) must stay identical; printed CVs carry a QR code to `/`.
3. **No ROAR Training Solutions logos or branding** in any image. Text mentions that the CV already makes are fine.
4. **Strip metadata (EXIF/GPS) from every photo.** The repo is public. Always process photos with `tools/media/prep_images.py`; never commit originals.
5. **Critical infrastructure (for example Sonatrach sites)**: show equipment close-ups only. No station names, no identifying wide shots, no coordinates, no signage or tags that name the site.
6. **Crop client title blocks** (cartouches) out of drawings before adding them.
7. **Drafts never go to production.** `draft: true` is the default. A production build contains only published entries; with zero published entries the site is the CV plus the 404 page, and no nav links appear.
8. Keep the design tokens exactly: `--ink:#1b2430; --muted:#5d6874; --rule:#dde1e6; --accent:#1f3a5f` and the system font stack. Content pages use a wider container (72rem) than the CV (46rem).

## Architecture

```
src/
  pages/index.astro            the CV (1:1 port of the original page; its CSS is `<style is:global>` in that file)
  pages/404.astro
  pages/projects/[...slug].astro     /projects/ AND /projects/<slug>/ from one route; returns NO paths when there is
  pages/simulators/[...slug].astro   no visible entry, so no empty section page is ever built
  views/                       ProjectsIndex, ProjectDetail, SimulatorsIndex, SimulatorDetail (page templates)
  layouts/Base.astro           <head> (title, description, canonical, OG/Twitter; defaults = the CV's), SiteNav, LangScript
  components/                  Lang, LangScript, LangSwitch, SiteNav, ProjectLink, ProjectCard, SimulatorCard, Facts,
                               Gallery, DrawingStrip, Thumb, Lightbox, Clip, Prose
  content.config.ts            collection schemas (projects, simulators + their French bodies)
  content/projects/<slug>/{index.md,index.fr.md}
  content/simulators/<slug>/{index.md,index.fr.md}
  lib/content.ts               getProjects/getSimulators (draft filter), renderBilingual, labels
  assets/                      images processed by Astro (portrait.jpg, projects/<slug>/, simulators/<slug>/)
  styles/site.css              shared tokens/base (loaded everywhere); styles/content.css for Projects/Simulators pages
public/                        copied as-is: the two CV PDFs, og.png, media/<section>/<slug>/ (encoded clips + posters)
tools/media/                   prep_images.py, encode_clip.py (+ README)
tools/dev/with-drafts.mjs      cross-platform "build/preview with drafts"
astro.config.mjs               also holds the `prune-unpublished` integration (see "Drafts" below)
```

### Language mechanism

Both languages are in the HTML; `html[data-lang="en"] [lang="fr"], html[data-lang="fr"] [lang="en"] {display:none}` shows one.
`LangScript.astro` (in every page's `<head>` through Base) picks the language: `?lang=en|fr`, then `localStorage` key `lang`,
then `navigator.language`; it switches `<html lang>`, `document.title`, any `[data-set="en|fr"]` button, `alt` on elements with
`data-alt-en/-fr`, and `aria-label` on elements with `data-label-en/-fr`.
- Inline text: `<Lang en="..." fr="..." />` (never write the two `<span lang>` by hand).
- Images: pass `data-alt-en` and `data-alt-fr` next to `alt` (see ProjectCard).
- Do not add CSS that sets `display` on elements that carry a `lang` attribute (it would beat the hide rule).

### Nav and CV hook

`SiteNav` lists CV / Projects / Simulators; an item shows only if its collection has a visible entry, and the whole row is omitted
when only the CV exists. `ProjectLink` renders nothing unless a published project matches. It is already placed on the CV bullets:

| `cvAnchor` value | CV entry |
|---|---|
| `scada-sonatrach` | RMBTECH: SCADA for Sonatrach gas pipelines |
| `critical-equipment-atex` | RMBTECH: rectifier 8500 A and ATEX Ex "p" cabinet |
| `bossar-rehabilitation` | RMBTECH: BOSSAR packaging machine |
| `silo-mesra` | RMBTECH: OAIC silo SCADA |
| `proskid-dosing-skids` | PROSKID: 27 Milton Roy dosing skids |
| `atex-ex-d-enclosure` | PROSKID: Ex "d" enclosure |
| `ifri-pv` | Freelance: 5.4 MW IFRI PV |
| `roar-3d-training` | Freelance: 3D training modules |

Set `cvAnchor: <value>` in a project's frontmatter and publish it; the "See project" link appears on that CV bullet (screen only, never printed).
To add a hook elsewhere: `<ProjectLink anchor="..." />` at the end of an `<li>` in `src/pages/index.astro` (or `slug="<project-slug>"`).

## Adding a project

1. Photos: `python tools/media/prep_images.py <raw_folder> <slug>` (writes `src/assets/projects/<slug>/`, prints YAML to paste).
2. Clips (optional): `python tools/media/encode_clip.py <raw.mov> projects/<slug>/hero --start 5 --end 17` (writes `public/media/projects/<slug>/`).
3. Create `src/content/projects/<slug>/index.md` (copy `sample-project`). Frontmatter fields: `draft`, `order`, `title{en,fr}`, `summary{en,fr}`, `client`,
   `role{en,fr}`, `period`, `location` (string, or `{en,fr}`), `domains` (oil-gas, atex, solar-pv, automation, scada), `tools[]`, `keyFigure{value,label{en,fr}}`, `cover`, `coverAlt`,
   `heroClip{src,poster,ratio}` (optional; replaces the cover as hero; `ratio` like `"3 / 4"` for a clip that is not 16:9), `heroSide[]` (optional, up to two landscape pictures stacked beside a portrait `heroClip` so the hero reads as one landscape block; same fields as a gallery item), `gallery[]`, `drawings[]` (each `image`, `alt{en,fr}`, `caption{en,fr}`),
   `videos[]` (`src`, `poster`, `ratio`, `caption{en,fr}`), `cvAnchor`. The slug is the folder name. Images are referenced as `"@assets/projects/<slug>/<file>.jpg"` (quote it: a bare `@` is invalid YAML).
4. **Bilingual body**: `index.md` body = English, `index.fr.md` (same folder) body = French, no frontmatter. Use the same three `##` sections in both:
   Context / What I did / Result (Contexte / Ce que j'ai fait / Résultat). If `index.fr.md` is missing the French view falls back to English and the build warns.
   Everything else (titles, summaries, captions, alt) is bilingual in the frontmatter. Fill alt text in both languages (the build warns on empty alt of non-draft entries).
5. Preview with drafts, check, then set `draft: false`.

## Adding a simulator

Same flow with `src/content/simulators/<slug>/`: `status` (delivered | in-development), `tech[]`, `learningGoal{en,fr}`,
`clips[]` (`slug`, `title`, `caption`, `src`, `poster`, `duration`), `underTheHood[]` (each `{en, fr}`), optional `cover`
(otherwise the first clip poster is the card image). `index.md` / `index.fr.md` bodies are the introduction. Clips: `encode_clip.py <raw> simulators/<slug>/<clip-name>`.
The page ends with "Request a live demo" (mailto nadir.zouaoui@hotmail.com).

## Drafts

`draft` defaults to `true`. Drafts are visible in `npm run dev`, and in `npm run build:drafts` / `npm run preview:drafts`
(these build into `dist-drafts/`, which is git-ignored; never deploy it). Draft pages carry `noindex` and a banner.
`sample-project` and `sample-simulator` are placeholder drafts that exercise every template block: delete them (folder in `src/content`,
`src/assets/<section>/<slug>`, `public/media/<section>/<slug>`) once real content exists, or keep them as a regression fixture.
After every production build the `prune-unpublished` integration deletes (a) `dist/media/<section>/<slug>/` of every entry that is not explicitly
`draft: false`, and (b) unreferenced image files in `dist/_astro/` (Astro emits the original of every content `image()` even for drafts).

## Components worth knowing

- `Gallery` is a strict grid of equal tiles. The tile shape follows the majority of the photos (portrait 3:4 or landscape 4:3); in a portrait grid a landscape photo spans two columns. Thumbnails are cropped to the tile, the lightbox shows the whole photo. Photos stay in order; a row that is not full is centred.
- The `videos` of a project page sit in one row, each clip with its own `ratio`, at one shared height; a row that is not full is centred too. `ProjectCard` crops to 8:5, so pick a landscape `cover`.
- `Gallery` + `DrawingStrip` render `Thumb` buttons; one `<Lightbox />` per page opens them (native `<dialog>`, arrows/Home/End/Esc, focus trap, swipe, focus returns to the thumbnail).
- `Clip`: `<video muted loop playsinline preload="none" poster>`; plays only while in the viewport (IntersectionObserver); with `prefers-reduced-motion` it never autoplays and shows a large Play button; there is always a Play/Pause button. Never add `autoplay` or audio.
- Images use Astro `<Picture>` (AVIF/WebP + JPEG fallback, lazy). Hero images are `loading="eager"`.

## Verifying changes

```
npm install
npm run check          # astro check (types)
npm run build          # production build; must list only /index.html and /404.html while nothing is published
npm run build:drafts   # includes drafts -> dist-drafts/
```
Then compare with Playwright (Chromium is preinstalled in the agent sandbox at /opt/pw-browsers; `PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers`, do not run `playwright install`):
- CV regression: serve the original page (`git show 0c05d84:index.html`, plus the PDFs and og.png) and the new `dist/` on two ports; screenshot `/?lang=en` and `/?lang=fr` at 1280 and 390 px, run `page.pdf()` with print media for both, and pixel-diff. Only the portrait pixels may differ (re-encoded JPEG). Check `scrollWidth <= 375` at 375 px and no console errors.
- New pages: screenshot the `dist-drafts` pages at 1280 and 390 px, test the lightbox (Enter, arrows, Esc, Tab trap), the domain chips, and `prefers-reduced-motion`. Note Playwright's Chromium cannot decode H.264, so stub `HTMLMediaElement.play` to test the Clip logic.
- Check no `<img>` without `alt`, and that no photo contains EXIF (`exiftool` or Pillow `getexif()`).
