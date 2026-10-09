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
- [x] **Go live:** done 2026-10-09. Pages source set to **GitHub Actions**, then PR #1 merged into `main`. Live checks passed: `/`, `/?lang=fr`, both CV PDFs and `/og.png` (byte-identical to the build), `/projects/`, the ATEX page and its media; sample pages and source files return 404. New work now branches from `main`, one PR per change.
- [x] **Phase 3: ATEX Ex "d" case study (the pilot).** Reviewed in five rounds; Nadir approved the result on 2026-10-09. Published (`draft: false`) and PR #2 (`phase-3-atex`) merged into `astro-site` on 2026-10-09; live since PR #1 was merged the same day. Content in `src/content/projects/atex-ex-d-enclosure/`, media in `src/assets/projects/atex-ex-d-enclosure/` and `public/media/projects/atex-ex-d-enclosure/`. Branch `phase-3-atex`, draft PR into `astro-site`.
- [ ] **Phase 4: Simulators.** Waiting for clips.
- [ ] **Phase 5: more case studies.** In progress, one draft PR each, entries stay `draft: true` until Nadir has read them. See "Phase 5 queue" below.
- [x] **Phase 6: polish.** PR #4 merged 2026-10-09 and verified live: `/sitemap.xml` (published pages only), `/robots.txt`, per-page share image (1200x630, from the cover), preload of the hero poster, `npm run check:links`. The CV page stayed byte-identical. Lighthouse on the local build: CV and `/projects/` 100 on all four, ATEX page 89 for performance (the 4.9 MB hero clip is the largest paint). Not done: no favicon (adding one changes the CV head); the Fiverr and LinkedIn links refuse automated checks, test them by hand.

## Phase 5 queue (decided 2026-10-09 from the media on Nadir's PC)
1. **IFRI 5.4 MW rooftop PV** (`ifri-pv`): **published 2026-10-09** (PR #5 merged), branch `phase-5-ifri-pv`. Source `Work\Freelance\Walid\Ifri\`. All figures come from the single-line diagram dossier revision D (27/07/2026) and the Archelios Pro report of one zone; the scope of work and the load study give older figures (20 or 14 injection points), do not use them. No claim of commissioning. Open questions are listed in the PR. The page has an optional `hero` / `heroAlt` frontmatter field (schema in `src/content.config.ts`, used by `src/views/ProjectDetail.astro`, falls back to `cover`): the dusk photo is the hero, `cover` stays the card and share image. Drawings: site plan, general single-line diagram, two injection-point sheets, AC feeders recap (SLD Ind D) and the latest layouts of KSB (Rev K), Tetra and Canette (Rev I), Sidel 1 (Rev C), Sidel 2 (Rev D). Production section from the two Archelios reports that exist (Tetra and Canette, KSB). Open point for Nadir: the SLD shows 9 inverters / 1 350 kW AC for KSB 182 + KSB 1833, while the KSB layout Rev K and the Archelios report give 8 inverters / 1 280.16 kWp; the Sidel 1 layout states 866 A where the SLD states 962 A.
2. **Solar supply for dosing skids, offer-stage design** (`solar-supply-dosing-skid-offer`): draft PR #7, branch `phase-5-proskid-solar-skids`. Source `Work\Proskid\NZO\Skids solaires HRM\23-028-ELE-GAD-001_01.pdf` (two system diagrams, author NZO, 03/10/2023). Nadir, 2026-10-09: this offer is **not** the 27 Milton Roy skids mission, PROSKID did not supply these skids, and he does not know whether they were built. Thin page (no photo, no outcome): keep as a draft, publish only if Nadir wants it, or fold it into another page.
3. **Cable trays and power routing on the GCB dosing skid** (`gcb-skid-cabling`): **published 2026-10-09** (PR #8 merged), branch `phase-5-gcb-skid-cabling`. Same skid (2202) as the Ex d enclosure pilot. Nadir, 2026-10-09: the skid was modelled in SolidWorks; he rebuilt it in Blender with added detail, designed the cable trays and the power routing from the enclosure to the pumps, and made the animation, which was shown to the client to present progress. Source `Work\Proskid\NZO\2202\3D\` and `2202\SCHEMAS ELECTRIQUES\`. The page also shows the enclosure power schematic. The `atex-ex-d-enclosure` page now links to it.
4. **At Pharma PV + storage visualisation** (`at-pharma-pv-visualisation`): **published 2026-10-09** (PR #9 merged), branch `phase-5-at-pharma-visualisation`. Source `Work\Freelance\Walid\At Pharma\Renders\`. Scope is visualisation only (quote of 28/07/2024, never publish its prices). Views on satellite imagery and the site plan are not used. The cover is the roof inverter render; three interior renders of the technical room were added.
5. **27 Milton Roy dosing skids mission** (`proskid-dosing-skids`, the CV anchor of that bullet): not started. Waiting for Nadir's pictures of the mission. The Milton Roy drawings are the manufacturer's, not Nadir's. `23-040` and `2403` are critical infrastructure: equipment close-ups only.

Public text (captions, alt text, body) describes the work only: no processing or internal notes (duration, audio removed, cropping, what was left out). Such notes go in the PR.

Open questions for Nadir are listed in each draft PR.

Left out for now: Sungy (renders only, a bank's sign in some), MHR (800x600 images), the genset cabinet (WhatsApp-size photos), the private villa.

Preview of drafts: `npm run build:drafts`, then serve `dist-drafts/` with a no-cache server. Each draft lives on its own branch, so a preview of all of them needs a local throwaway branch that merges the draft branches (never pushed).

## Nadir's answers (Phase 3)
1. **Function:** the skid doses a chemical corrosion inhibitor (Chimec) into a gas pipeline. The enclosure is both the power panel and the control panel for 3 dosing pumps. There is no PLC: it is hard-wired relay logic. Local and remote command, with status feedback to the site RTU; the door pilot lights are the local feedback. (The door has 19 devices: 10 pilot lights, 6 pushbuttons, a local/remote selector, an ON/OFF switch, an emergency stop.)
2. **Ex marking, IP, maker:** only what the supplier documents state (`Consultation Atex System UCP\Fichiers reçus\Rev 4\`): Ex d IIB+H2 T5 Gb, Ex tb IIIC T100 °C Db, IP66 (quotation, p.1).
3. **Period:** August to October 2024. No FAT/SAT, commissioning, delivery or site installation is claimed.
4. **Proud of:** everything planned in EPLAN (Electric P8 + Pro Panel 3D layout) before the enclosure arrived; did everything alone, from sourcing to design to wiring. He also built a test-bench enclosure playing the RTU to test the remote operation (photos at the end of the gallery, video in `videos[]`).

Confirmed by Nadir on review (2026-10-09): the period 08/2024 - 10/2024; naming Chimec in the copy; the "PLC" labels and instrument tags visible in the hero's EPLAN frames are fine.

Answered by Nadir before publishing (2026-10-09):
- Location: "Algiers, Algeria" / "Alger, Algérie" (`location` now accepts a string or `{en,fr}`).
- The enclosure maker is named once in the Context section: ATEX System (from the supplier quotation).
- Photos 14 to 16 (a leg in trousers, no face; photo 16 cropped to the enclosure and the test bench) are published as they are. Photo 01 is cropped above the title block of the printed drawing.
- The three EPLAN Pro Panel 3D screenshots are small (about 500 x 750 px): published as they are, to be replaced when Nadir makes larger exports.
- The CV shows a single EN/FR switch: its own switch is hidden on screen whenever the nav row is rendered (CSS in `src/pages/index.astro`).

Notes kept for reference:
- Enclosure dimensions differ between the supplier documents (CCF16G 550x800x245 in the technical sheet, CCF16BG 500x800x360 in the quotation), and the isolator rating differs (S0 16 A in the schematic, 32 A in the technical sheet). Neither is used in the copy.
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
