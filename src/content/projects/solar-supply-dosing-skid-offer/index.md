---
draft: true
order: 30
title:
  en: Stand-alone solar power supply for chemical-injection skids
  fr: Alimentation solaire autonome pour skids d'injection chimique
summary:
  en: "24 V DC solar supplies for chemical dosing skids and for their RTU: array on a retractable pole, MPPT charge controller, battery bank and distribution, drawn as system diagrams for two versions."
  fr: "Alimentations solaires 24 V DC pour des skids de dosage chimique et pour leur RTU : champ sur mât escamotable, régulateur de charge MPPT, parc de batteries et distribution, dessinées sous forme de synoptiques pour deux versions."
client: PROSKID
role:
  en: Lead Electrical Engineer, PROSKID
  fr: Ingénieur électricien principal, PROSKID
period: "2023"
location:
  en: Algeria
  fr: Algérie
domains: [solar-pv]
tools: [QElectroTech]
keyFigure:
  value: 1.3 kWp
  label:
    en: 4 × 325 Wp array, 24 V battery bank of 570 Ah
    fr: 4 × 325 Wc, parc de batteries 24 V de 570 Ah
cover: "@assets/projects/solar-supply-dosing-skid-offer/01-skid-solar-supply-synoptic.jpg"
coverAlt:
  en: System diagram of a solar power supply for a dosing skid, from the panels on a pole to the charge controller, battery bank and 24 V output (labels in French)
  fr: Synoptique d'une alimentation solaire pour skid de dosage, des panneaux sur mât au régulateur de charge, au parc de batteries et à la sortie 24 V
drawings:
  - image: "@assets/projects/solar-supply-dosing-skid-offer/01-skid-solar-supply-synoptic.jpg"
    alt:
      en: System diagram of the skid version, with four solar panels on a pole, a disconnect and surge-protection box, an MPPT charge controller, two bus bars, a battery bank, a battery controller and a DC/DC converter feeding a 24 V output (labels in French)
      fr: Synoptique de la version skid, avec quatre panneaux sur mât, un coffret de sectionnement et parafoudre, un régulateur de charge MPPT, deux jeux de barres, un parc de batteries, un contrôleur de batteries et un convertisseur DC/DC alimentant une sortie 24 V
    caption:
      en: "Skid version: 4 × 325 Wp, MPPT 150 V / 70 A, 12 × 2 V / 570 Ah, DC/DC 24 V / 24 V 240 W (labels in French)."
      fr: "Version skid : 4 × 325 Wc, MPPT 150 V / 70 A, 12 × 2 V / 570 Ah, DC/DC 24 V / 24 V 240 W."
  - image: "@assets/projects/solar-supply-dosing-skid-offer/02-rtu-solar-supply-synoptic.jpg"
    alt:
      en: System diagram of the RTU version, with two solar panels, the same charge controller, a smaller battery bank, a DC/DC converter and an AC/DC converter fed from a 230 VAC input (labels in French)
      fr: Synoptique de la version RTU, avec deux panneaux, le même régulateur de charge, un parc de batteries plus petit, un convertisseur DC/DC et un convertisseur AC/DC alimenté par une entrée 230 VAC
    caption:
      en: "RTU version: 2 × 325 Wp, 12 × 2 V / 400 Ah, DC/DC 110 W, and an AC/DC converter 230 V / 24 V 25 A (labels in French)."
      fr: "Version RTU : 2 × 325 Wc, 12 × 2 V / 400 Ah, DC/DC 110 W et convertisseur AC/DC 230 V / 24 V 25 A."
  - image: "@assets/projects/solar-supply-dosing-skid-offer/03-skid-array-protection-and-charge-controller.jpg"
    alt:
      en: Detail of the skid diagram, with solar panels on a pole, the disconnect and surge-protection box, the MPPT charge controller and the two protective devices, and the cable section written on each run (labels in French)
      fr: Détail du synoptique du skid, avec panneaux sur mât, coffret de sectionnement et parafoudre, régulateur de charge MPPT et les deux protections, et la section de chaque câble
    caption:
      en: From the array to the bus bar, with cable sections of 4, 6 and 16 mm² and protections of 40 A and 20 A (labels in French).
      fr: Du champ au jeu de barres, avec des câbles de 4, 6 et 16 mm² et des protections de 40 A et 20 A.
  - image: "@assets/projects/solar-supply-dosing-skid-offer/04-skid-battery-bank-and-battery-controller.jpg"
    alt:
      en: Detail of the skid diagram, with twelve 2 V cells in two rows connected in series, a battery controller with a temperature sensor, and a fused knife disconnect to the bus bars (labels in French)
      fr: Détail du synoptique du skid, avec douze éléments de 2 V en deux rangées reliés en série, un contrôleur de batteries avec sonde de température et un inter-sectionneur à fusibles couteau vers les jeux de barres
    caption:
      en: Battery bank of 12 × 2 V / 570 Ah with its controller, temperature sensor and fused disconnect (labels in French).
      fr: Parc de batteries 12 × 2 V / 570 Ah avec son contrôleur, sa sonde de température et son sectionneur à fusibles.
---

## Context

Chemical anticorrosion dosing skids on remote sites need a 24 V DC supply from solar power, and so does the RTU that monitors them. For a technical offer, PROSKID needed a stand-alone solar supply defined for each of the two.

The design is documented in a two-sheet system diagram dated 03/10/2023, one sheet per version. The skid version has four 325 Wp monocrystalline modules on a retractable galvanised steel pole built into the solar skid, 10 m high when installed. The RTU version has two modules on the same kind of pole.

## What I did

- Defined the architecture of the supply for the two versions: array, disconnect and surge-protection box, MPPT charge controller, battery bank, battery controller and a DC/DC converter for the 24 V output.
- Set the rating of each component: MPPT charge controller 150 V / 70 A, DC/DC converter 24 V / 24 V 240 W and a 12 × 2 V / 570 Ah battery bank for the skid; 110 W and 12 × 2 V / 400 Ah for the RTU.
- Chose the cable sections (4, 6, 16 and 25 mm² on the skid version) and the protections on each run (40 A and 20 A on the skid version, 20 A and 10 A on the RTU version).
- Added battery temperature sensing, a communication box with an RJ45 link to the RTU, and a local HMI mounted on the cabinet door.
- For the RTU version, added an AC/DC converter (230 V / 24 V, 25 A) fed from a 230 VAC input. The battery enclosure is marked out of scope on that sheet.
- Drew both sheets in QElectroTech.

## Result

Two system diagrams for the technical offer, one per version, with the components, ratings and cable sections defined. This was a design for an offer; I do not know whether the supplies were built.
