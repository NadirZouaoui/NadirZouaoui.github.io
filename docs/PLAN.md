# Portfolio upgrade: plan and handoff

Source of truth for the portfolio upgrade. Read this together with `CLAUDE.md` (architecture and hard rules).
Last updated 2026-10-09.

## Goals
1. Photos and graphics for delivered projects (case studies under `/projects/`).
2. A separate **Simulators** section for the 3D training work, shown as short clips (`/simulators/`).

## Decisions (locked)
| Topic | Decision |
|---|---|
| Stack | Astro, static, deployed by GitHub Actions |
| Look | Same plain white style everywhere (tokens in `CLAUDE.md`) |
| Languages | EN/FR on the same URL (existing toggle) |
| Simulators | **Clips only.** No playable builds online; live demos in person or on request |
| First case study | ATEX Ex "d" flameproof enclosure, GCB skid (PROSKID job 2202) |

## Status
- [x] **Phase 1: scaffold + CV port.** Draft PR #1 (`astro-site`). CV verified 1:1 (screen EN/FR at 1280/390 px, print PDF; only the portrait re-encode differs).
- [x] **Phase 2: content model, components, media tools.** In the same PR. Draft samples: `sample-project`, `sample-simulator`.
- [ ] **Go live:** Settings → Pages → Source: **GitHub Actions**, THEN merge PR #1. (Merging first would serve the raw Astro source.)
- [~] **Phase 3: ATEX Ex "d" case study (the pilot).** Reviewed in five rounds; Nadir approved the result on 2026-10-09 ("Pilot looks good"). Still `draft: true` in draft PR #2 (`phase-3-atex` into `astro-site`): setting `draft: false` and merging are the next steps, on his go-ahead. Content in `src/content/projects/atex-ex-d-enclosure/`, media in `src/assets/projects/atex-ex-d-enclosure/` and `public/media/projects/atex-ex-d-enclosure/`. Branch `phase-3-atex`, draft PR into `astro-site`.
- [ ] **Phase 4: Simulators.** Waiting for clips.
- [ ] **Phase 5: more case studies** as media arrives.
- [ ] **Phase 6: polish.** Per-page OG images, sitemap, performance pass, link check.

## Nadir's answers (Phase 3)
1. **Function:** the skid doses a chemical corrosion inhibitor (Chimec) into a gas pipeline. The enclosure is both the power panel and the control panel for 3 dosing pumps. There is no PLC: it is hard-wired relay logic. Local and remote command, with status feedback to the site RTU; the door pilot lights are the local feedback. (The door has 19 devices: 10 pilot lights, 6 pushbuttons, a local/remote selector, an ON/OFF switch, an emergency stop.)
2. **Ex marking, IP, maker:** only what the supplier documents state (`Consultation Atex System UCP\Fichiers reçus\Rev 4\`): Ex d IIB+H2 T5 Gb, Ex tb IIIC T100 °C Db, IP66 (quotation, p.1).
3. **Period:** August to October 2024. No FAT/SAT, commissioning, delivery or site installation is claimed.
4. **Proud of:** everything planned in EPLAN (Electric P8 + Pro Panel 3D layout) before the enclosure arrived; did everything alone, from sourcing to design to wiring. He also built a test-bench enclosure playing the RTU to test the remote operation (photos at the end of the gallery, video in `videos[]`).

Confirmed by Nadir on review (2026-10-09): the period 08/2024 - 10/2024; naming Chimec in the copy; the "PLC" labels and instrument tags visible in the hero's EPLAN frames are fine.

Still open, for Nadir to confirm (listed in the build report):
- The location "Algeria" (no document states it).
- Enclosure dimensions differ between the supplier documents (CCF16G 550x800x245 in the technical sheet, CCF16BG 500x800x360 in the quotation), and the isolator rating differs (S0 16 A in the schematic, 32 A in the technical sheet). Neither is used in the copy.
- Whether naming the enclosure maker is wanted (not named in the copy).
- Photos 14 to 16 show a leg in trousers (no face). Photo 16 is a workshop shot, cropped to the enclosure and the test bench (background signage and the pump removed). Photo 01 is cropped above the title block of the printed drawing.
- The three EPLAN Pro Panel 3D screenshots are small (about 500 x 750 px); larger exports would look better in the lightbox.
- The hero is `2202 building.mp4` (Nadir's LinkedIn edit: EPLAN first, then the build), with the EPLAN part (0 to 12.37 s) at 2x, encoded by hand with ffmpeg using the `encode_clip.py` settings because the tool has one speed for the whole clip. Its schematic frames show the remote system labelled "PLC" and instrument tag numbers. It is portrait (3:4) and the hero frame follows that ratio; two landscape pictures (`heroSide`: photo 01 and the door layout drawing) are stacked beside it so the hero reads as one landscape block. The card cover is photo 01 (landscape: empty enclosure and the drawing). Nadir removed the photo "Wiring behind the door" (2026-10-09).
Schematics used: `D:\Nadir\Documents\Work\Proskid\NZO\2202\SCHEMAS ELECTRIQUES\2202 SKID GCB.pdf` (p.12 power, p.13-15 control, p.16-17 layout). Page 15 mentions a PLC and a site tag, so it is not published.

## Building on Nadir's PC
- Shell is Git Bash. The system Node is 22.11, too old for Astro. Put Node 24 first: `export PATH="/c/Users/Nadir/AppData/Local/ms-playwright-go/1.57.0:$PATH"`, set `NPMCLI="C:/Program Files/nodejs/node_modules/npm/bin/npm-cli.js"`, and run npm as `node "$NPMCLI" run <script>`. Shell state does not persist between commands, so start every command with these.
- `gh` is logged in as NadirZouaoui.
- `ffmpeg`/`ffprobe` are not on PATH. They live in `/c/Program Files/Shutter Encoder/Library/`; run `export PATH="/c/Program Files/Shutter Encoder/Library:$PATH"` before `encode_clip.py`.
- Python 3.13 with Pillow and PyMuPDF. Use `python -I -X utf8` when printing PDF text (accents otherwise raise UnicodeEncodeError). For multi-line files, use the editor tools instead of shell heredocs.
- Screenshots: headless Microsoft Edge (`--screenshot`, `--window-size`), served from a local `http.server`. Stop the server afterwards.
- Raw material is staged outside the repo in `D:\Nadir\Documents\Portfolio\media-src\<slug>\` and only the processed output is written into the repo.
- Portrait media: `Clip` uses a 16/9 frame unless the entry gives `ratio` (printed by `encode_clip.py`; without it a portrait video is pillarboxed). `Gallery` is a strict grid whose tile shape follows the majority of the photos (portrait tiles here; landscape photos span two columns). Nadir tried justified rows (commit `b5122e9`) and found the strict grid more professional. The project `videos` keep each clip's ratio at one shared height. `ProjectCard` crops to 8:5, so pick a landscape photo as `cover`.
- Local preview: a plain `http.server` lets the browser replay an old clip from its cache when a file is re-encoded under the same name. Serve with `Cache-Control: no-store` or hard-reload.

## Lessons from the pilot review (apply to every later case study)
What Nadir asked for while reviewing the ATEX page. Follow these from the first draft.
- **Copy:** factual and sober. No sales wording ("the client needed one enclosure"), no boasting ("I did the whole job alone"): state the scope as a plain list of what he did. Say what the equipment is for in one sentence.
- **Key figure:** something an engineer finds meaningful (a rating, a power, a standard), not a count of parts.
- **Hero:** prefer a video Nadir edited himself when one exists (here his LinkedIn edit). The poster is the clip's first frame. A portrait clip gets two landscape pictures stacked beside it (`heroSide`) so the hero reads as one landscape block.
- **Order of sections:** drawings before photos.
- **Card cover:** a landscape photo (the card crops to 8:5).
- **Photos:** strict grid with aligned tiles (he found justified rows less professional); a row that is not full is centred. Keep the selection tight; he removed a close-up that added nothing.
- **Preview:** serve `dist-drafts` with `Cache-Control: no-store` and give him the local URL after each change; he reviews in the browser and answers in short rounds.
- **Process:** show him the first draft early. Ask about facts no document states (location, dates, whether a name may be published) instead of guessing; list what is still open in the PR.

## Media locations (Nadir's PC)
| Project | Where | Notes |
|---|---|---|
| ATEX Ex "d" enclosure (2202) | `D:\Nadir\Documents\Work\Proskid\NZO\2202\Photos\` | ~75 photos. **`2202 building.mp4` = Nadir's edit (EPLAN, then the build) → hero clip**, EPLAN part at 2x. `1~2.mp4` = timelapse of the panel build (not used). 4 EPLAN Pro Panel screen recordings (`EPLAN Pro Panel 2022 - …mp4`), `2202 building_1.mp4` (lower-quality copy), `Screenshot (11–26).png` = EPLAN 3D layout. Best shots seen: `1.jpg` (empty box + drawing), `10.jpg`, `15.jpg`, `21.jpg`, `24.jpg`, `PXL_20241030_144844635.jpg` (wiring close-up), `o1.jpg` (finished door, lights on), `p (13).jpg`, `p (17).jpg`, `p (5).jpg` |
| Skid 3D animation (2204) | `…\Proskid\NZO\2204\Animation 3D\2204 Animation 3D.mp4` | 41 MB |
| IFRI 5.4 MW rooftop (Akbou) | `D:\Nadir\Documents\Work\Freelance\Walid\Ifri\Photos\` (20), `Schemas Electriques\`, calepinage | Night works, string testing, rooftop rows |
| At Pharma PV + BESS | `…\Freelance\Walid\At Pharma\Renders\` | 17 Blender renders |
| Sungy PV designs | `D:\Nadir\Documents\Work\Sungy\` | Arkad, Ifni, ASL, SGA HMD façade, 305.2 kWc aerial |
| MHR solar skid / genset cabinet / Villa Draria | `…\Freelance\MHR\Renders\`, `…\Walid\Armoire genset\Photos\`, `…\Walid\Villa Draria Sebala\SLD\` | Supporting only (small WhatsApp photos) |
| Simulators (Godot projects) | `D:\Nadir\Documents\Work\Freelance\HV Exercices Simulations\` | `3D Substation\`, `LVR CPR\`, `2D HV Switching Exercices\`. `scorm_build\index.png` is the ROAR logo: never use it |
| Milton Roy skids ×27, GK3 survey, ALRAR | Nadir's phone | Suggested drop folder: `D:\Nadir\Documents\Portfolio\media-src\<slug>\` |
| GP2Z Ex "p", 8500 A rectifier, BOSSAR/GBFoods, OAIC silo, thesis microgrid | Unknown (hard drive?) | Ask Nadir |

Do not use anything in `D:\Nadir\Documents\Work\RMBTech\` except project media Nadir points to explicitly (that folder holds contracts and HR paperwork).

## Simulator clip lists (Phase 4)
Recording: OBS at 1080p, clean UI, no ROAR branding, one action per clip, 8–20 s. Encode with `tools/media/encode_clip.py`.
- **Substation switching (3D):** walk the yard · drag-and-drop switching sheet · access and test permits (SS/AC IDs) · HV tester self-test and prove-dead · operating with the live schematic map · grading, debrief and fail screen
- **LV Rescue + CPR:** kit check (6 of 16) · naming the kit · hazard ID and ISOLATE HERE sign · the incident (arc FX) · gloves and crook rescue (20 s) · drag to safety and isolate · primary survey · compressions (rate/depth, metronome) · AED pads and shock · debrief (correct vs actual order)
- **Test & Tag (Seaward PAT tester):** in development
- **2D HV switching exercises:** MCC exercise, HV ABS assessment, Exercise 3
- "Under the hood": Blender → Godot 4 (Compatibility renderer), procedure-driven weighted scoring, SCORM 1.2 reporting, headless regression tests.
Source notes: `LVR CPR\lvr-cpr\PROJECT_STATUS.md`, `3D Substation\substation-3d-training\behance_project.md`.

## Phase 3 brief (ATEX Ex "d" case study)
1. Branch from `astro-site` (or `main` after merge).
2. Pick ~15 photos telling the build story (empty enclosure + drawing → mounting rails → wiring → finished door lit). Pick 3–4 EPLAN Pro Panel screenshots for the drawings strip, and crop client title blocks. Process them with `prep_images.py <folder> atex-ex-d-enclosure`.
3. Hero: `2202 building.mp4` with the EPLAN part at 2x (see the open points above), as a loop under 6 MB. Optional extra videos: one EPLAN 3D layout recording, trimmed.
4. Write `index.md` / `index.fr.md` (Context / What I did / Result), facts (client GCB/ENGCB, role Lead Electrical Engineer, PROSKID, period, tools EPLAN Electric P8 + Pro Panel), `keyFigure`, `domains: [oil-gas, atex]`, `cvAnchor: atex-ex-d-enclosure`. Keep the copy factual and short. Nadir reviews before `draft: false`.
5. Verify per `CLAUDE.md` (CV unchanged, EXIF stripped, screenshots at 1280/390 EN/FR). Open a PR.
