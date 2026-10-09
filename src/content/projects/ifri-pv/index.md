---
draft: true
order: 20
title:
  en: Electrical design of a 5.4 MW rooftop solar plant with zero export
  fr: Étude électrique d'une centrale solaire en toiture de 5,4 MW sans injection
summary:
  en: "Design of a 5.4 MW AC self-consumption plant on the roofs of several production buildings: 36 inverters of 150 kW, a fuse-free DC architecture justified by calculation, injection on existing LV boards and a yield study per zone."
  fr: "Étude d'une centrale d'autoconsommation de 5,4 MW AC sur les toitures de plusieurs bâtiments de production : 36 onduleurs de 150 kW, une architecture DC sans fusible justifiée par le calcul, injection sur les TGBT existants et étude de productible par zone."
client: SARL Ibrahim & Fils (IFRI)
role:
  en: Freelance electrical design engineer
  fr: Ingénieur d'études électriques, freelance
period: "2026"
location:
  en: Akbou, Béjaïa, Algeria
  fr: Akbou, Béjaïa, Algérie
domains: [solar-pv]
tools: [SketchUp, Archelios Pro, Blender]
keyFigure:
  value: 5.4 MW AC
  label:
    en: 36 × 150 kW inverters, zero export
    fr: 36 onduleurs de 150 kW, sans injection
cover: "@assets/projects/ifri-pv/07-array-rows-standing-seam.jpg"
coverAlt:
  en: Rows of solar modules on a metal roof under a low sun, with a roof valley on the left and hills on the horizon
  fr: Rangées de modules solaires sur une toiture métallique sous un soleil bas, avec un chéneau à gauche et des collines à l'horizon
gallery:
  - image: "@assets/projects/ifri-pv/01-crane-lifting-pallet.jpg"
    alt:
      en: Night view from a roof of a crane lifting a pallet, with modules laid in the foreground, workers in high-visibility vests and floodlights behind
      fr: Vue de nuit depuis une toiture d'une grue qui hisse une palette, avec des modules posés au premier plan, des ouvriers en gilet haute visibilité et des projecteurs derrière
    caption:
      en: A pallet lifted onto the roof by crane, at night.
      fr: Une palette hissée sur la toiture par une grue, de nuit.
  - image: "@assets/projects/ifri-pv/02-rails-and-clamps.jpg"
    alt:
      en: Metal rail and clamps on a metal roof between two rows of modules, with module leads hanging loose
      fr: Rail métallique et brides sur une toiture métallique entre deux rangées de modules, avec des câbles de modules pendants
    caption:
      en: Rail and clamps between two module rows.
      fr: Rail et brides entre deux rangées de modules.
  - image: "@assets/projects/ifri-pv/03-meter-and-mc4-leads.jpg"
    alt:
      en: Orange clamp meter with a test probe held by a gloved hand on a module frame, and a bundle of black MC4 leads beside it, at night
      fr: Pince multimètre orange avec une pointe de touche tenue par une main gantée sur le cadre d'un module, et un faisceau de câbles MC4 noirs à côté, de nuit
    caption:
      en: Clamp meter and MC4 leads on a module, at night.
      fr: Pince multimètre et câbles MC4 sur un module, de nuit.
  - image: "@assets/projects/ifri-pv/04-cable-on-rail-clip.jpg"
    alt:
      en: White cable running along a module frame and past a galvanised rail clip on the roof
      fr: Câble blanc longeant le cadre d'un module et passant près d'une patte de rail galvanisée sur la toiture
    caption:
      en: Cable run along the module frame at a rail clip.
      fr: Câble le long du cadre du module, au niveau d'une patte de rail.
  - image: "@assets/projects/ifri-pv/05-night-works-roof.jpg"
    alt:
      en: Night view along a metal roof towards a parapet wall, with a few modules laid at the far end and two workers in high-visibility vests under floodlights
      fr: Vue de nuit le long d'une toiture métallique vers un acrotère, avec quelques modules posés au fond et deux ouvriers en gilet haute visibilité sous des projecteurs
    caption:
      en: Work on the roof at night, under floodlights.
      fr: Travaux sur la toiture de nuit, sous projecteurs.
  - image: "@assets/projects/ifri-pv/06-dusk-modules.jpg"
    alt:
      en: Rows of modules covering a roof at dusk, with hills and distant lights on the horizon
      fr: Rangées de modules couvrant une toiture au crépuscule, avec des collines et des lumières lointaines à l'horizon
    caption:
      en: Module rows at dusk.
      fr: Rangées de modules au crépuscule.
drawings:
  - image: "@assets/projects/ifri-pv/01-typical-150kw-block.jpg"
    alt:
      en: Typical 150 kW block diagram, with seven MPPT inputs of two strings each feeding a SUN2000-150K inverter, a 250 A breaker to the 400 V cabinet busbar, equipment tables and the note on the fuse-free DC architecture (labels in French)
      fr: Schéma du bloc type de 150 kW, avec sept entrées MPPT de deux chaînes chacune vers un onduleur SUN2000-150K, un disjoncteur 250 A vers le jeu de barres de l'armoire 400 V, les tableaux de caractéristiques et la note sur l'architecture DC sans fusible
    caption:
      en: Typical 150 kW block, with the note justifying the fuse-free DC side (labels in French).
      fr: Bloc type de 150 kW, avec la note qui justifie le côté DC sans fusible.
  - image: "@assets/projects/ifri-pv/02-module-layout-one-zone.jpg"
    alt:
      en: Module layout plan of one roof zone, with four colour-coded inverter groups of 14 strings each, obstacles, dimensions and a legend (labels in French)
      fr: Plan de calepinage des modules d'une zone de toiture, avec quatre groupes d'onduleur de 14 chaînes chacun en couleurs, les obstacles, les cotes et une légende
    caption:
      en: Module layout study for one roof zone (labels in French).
      fr: Étude de calepinage des modules pour une zone de toiture.
cvAnchor: ifri-pv
---

## Context

SARL Ibrahim & Fils (IFRI) is equipping the roofs of several production buildings at its Akbou site with a photovoltaic plant for self-consumption. The plant never exports: the inverters feed the existing low-voltage main boards of the buildings and the energy is consumed on site.

The design set describes a plant of 5 400 kW AC made of 36 Huawei SUN2000-150K inverters (150 kW each) and JinkoSolar Tiger Neo 635 Wp bifacial modules, grouped in 12 zones, each with its own 400 V AC cabinet. The cabinets connect to 11 injection points on the existing boards. A battery storage of 10 × 241 kWh is shown on the diagrams as outside the scope of this package.

## What I did

I worked on the electrical design and the energy study, from the roof layout to the single-line diagrams:

- Module layout (calepinage) of the 635 Wp modules on the roofs, taking shading, access and cable paths into account.
- Stringing and DC/AC ratio, and zoning of the roofs into 150 kW inverter blocks.
- Typical 150 kW block: 7 MPPT inputs of 2 strings each, and an ABB XT4N 250 breaker on the AC output.
- Fuse-free DC architecture, justified by the reverse current: 1.25 × 17.96 = 22.45 A against the 35 A series-fuse rating of the module (IEC 62548, IEC 60364-7-712).
- Injection on the existing LV boards: single-line diagrams, breaker sizing, AC and DC cable sections and voltage drop.
- Connection points for the battery storage shown on the single-line diagrams; the storage itself is outside this package.
- Analysis of the site load profile and power quality.
- Yield study with Archelios Pro for each zone, with P50 and P90 values and the performance ratio.

## Result

The design set was issued as a dossier of 17 single-line diagram sheets (revision D, 27 July 2026): general diagram, typical 150 kW block, one sheet per injection point and the recap of the AC feeders.

The yield study of one zone of about 600 kWp (954 modules, four inverters, east-west at 5°) gives a first-year AC yield of 1 404 kWh/kWp at P50 and 1 288 kWh/kWp at P90, with a performance ratio of 83.18 %.

The photos show the installation under way on the roofs in August and September 2026.
