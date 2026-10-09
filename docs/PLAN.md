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
- [ ] **Phase 3: ATEX Ex "d" case study.** Waiting for Nadir's answers (see below).
- [ ] **Phase 4: Simulators.** Waiting for clips.
- [ ] **Phase 5: more case studies** as media arrives.
- [ ] **Phase 6: polish.** Per-page OG images, sitemap, performance pass, link check.

## Open questions for Nadir (Phase 3)
1. What does the enclosure do on the skid (PLC/control of the injection pumps)? What are the 18 pilot lights for?
2. The Ex marking and rating (e.g. Ex d IIB T4 Gb, IP66), and the enclosure maker.
3. Timeline (photos are dated Oct–Nov 2024), and whether it went through FAT/SAT at GCB.
4. What he is proud of (wiring density, EPLAN Pro Panel 3D layout before cutting, etc.).
Schematics that may answer some of this: `D:\Nadir\Documents\Work\Proskid\NZO\2202\SCHEMAS ELECTRIQUES\` (2202 SKID GCB.pdf, 2202-ELE-DIA-022, -GAD-053, -LIS-029, 2202-PLC-LIS-054).

## Media locations (Nadir's PC)
| Project | Where | Notes |
|---|---|---|
| ATEX Ex "d" enclosure (2202) | `D:\Nadir\Documents\Work\Proskid\NZO\2202\Photos\` | ~75 photos. **`1~2.mp4` = timelapse of the panel build → hero clip** (20–30 s loop with `--speed`). 4 EPLAN Pro Panel screen recordings (`EPLAN Pro Panel 2022 - …mp4`), `2202 building*.mp4`, `Screenshot (11–26).png` = EPLAN 3D layout. Best shots seen: `1.jpg` (empty box + drawing), `10.jpg`, `15.jpg`, `21.jpg`, `24.jpg`, `PXL_20241030_144844635.jpg` (wiring close-up), `o1.jpg` (finished door, lights on), `p (13).jpg`, `p (17).jpg`, `p (5).jpg` |
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
3. Hero: the timelapse `1~2.mp4` → `encode_clip.py … projects/atex-ex-d-enclosure/hero --speed N`, as a 20–30 s loop under 6 MB. Optional extra videos: one EPLAN 3D layout recording, trimmed.
4. Write `index.md` / `index.fr.md` (Context / What I did / Result), facts (client GCB/ENGCB, role Lead Electrical Engineer, PROSKID, period, tools EPLAN Electric P8 + Pro Panel), `keyFigure`, `domains: [oil-gas, atex]`, `cvAnchor: atex-ex-d-enclosure`. Keep the copy factual and short. Nadir reviews before `draft: false`.
5. Verify per `CLAUDE.md` (CV unchanged, EXIF stripped, screenshots at 1280/390 EN/FR). Open a PR.
