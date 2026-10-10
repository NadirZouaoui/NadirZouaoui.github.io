---
# SAMPLE: exercises every block of the simulator template. Delete it (folder + src/assets/simulators/sample-simulator
# + public/media/simulators/sample-simulator) when the first real simulator is published. Draft = never in production.
draft: true
order: 1000
title:
  en: Sample simulator, switchboard isolation
  fr: Simulateur exemple, consignation d'un tableau
summary:
  en: Placeholder text. A first-person 3D exercise that trains one procedure, shown here as short clips.
  fr: Texte de remplissage. Un exercice 3D à la première personne qui entraîne une procédure, présenté ici en courts extraits.
status: in-development
tech: [Godot 4, Blender, SCORM 1.2, WebGL2]
cover: "@assets/simulators/sample-simulator/cover.jpg"
coverAlt:
  en: Placeholder cover image
  fr: Image de couverture factice
learningGoal:
  en: The learner can isolate, prove dead and secure a circuit in the correct order.
  fr: L'apprenant sait consigner, vérifier l'absence de tension et sécuriser un circuit dans le bon ordre.
heroClip:
  src: /media/simulators/sample-simulator/clip-a.mp4
  poster: /media/simulators/sample-simulator/clip-a.jpg
clips:
  - slug: approach
    title: { en: Approach and hazard check, fr: Approche et contrôle des dangers }
    caption: { en: "Placeholder clip.", fr: "Extrait factice." }
    src: /media/simulators/sample-simulator/clip-a.mp4
    poster: /media/simulators/sample-simulator/clip-a.jpg
    duration: "0:04"
    ratio: "16 / 9"
  - slug: isolation
    title: { en: Isolation, fr: Consignation }
    caption: { en: "Placeholder clip.", fr: "Extrait factice." }
    src: /media/simulators/sample-simulator/clip-b.mp4
    poster: /media/simulators/sample-simulator/clip-b.jpg
    duration: "0:04"
  - slug: proving-dead
    title: { en: Proving dead, fr: Vérification d'absence de tension }
    caption: { en: "", fr: "" }
    src: /media/simulators/sample-simulator/clip-c.mp4
    poster: /media/simulators/sample-simulator/clip-c.jpg
underTheHood:
  - en: First-person controller and interaction logic in Godot 4.
    fr: Contrôleur à la première personne et logique d'interaction sous Godot 4.
  - en: Phase-gated procedure checklist that blocks out-of-order steps.
    fr: Checklist de procédure par phases qui bloque les étapes dans le désordre.
  - en: Exported to WebGL2 and packaged as SCORM 1.2 for the client LMS.
    fr: Export WebGL2 et packaging SCORM 1.2 pour le LMS du client.
gallery:
  - image: "@assets/simulators/sample-simulator/cover.jpg"
    alt: { en: Placeholder screenshot, fr: Capture d'écran factice }
    caption: { en: Placeholder screen., fr: Écran factice. }
  - image: "@assets/projects/sample-project/gallery-1.jpg"
    alt: { en: Placeholder screenshot, fr: Capture d'écran factice }
    caption: { en: Placeholder screen., fr: Écran factice. }
grading:
  points:
    - en: Each step is graded against the procedure, with weights and critical steps.
      fr: Chaque étape est notée par rapport à la procédure, avec pondérations et étapes critiques.
    - en: Status, score and step log are reported to the LMS through SCORM.
      fr: Le statut, la note et le journal des étapes sont transmis au LMS par SCORM.
  pictures:
    - image: "@assets/projects/sample-project/drawing-1.jpg"
      alt: { en: Placeholder score report, fr: Rapport de note factice }
      caption: { en: Placeholder result screen., fr: Écran de résultat factice. }
    - image: "@assets/projects/sample-project/drawing-2.jpg"
      alt: { en: Placeholder step log, fr: Journal des étapes factice }
      caption: { en: Placeholder step log., fr: Journal des étapes factice. }
---

Two or three sentences introducing the module: who it is for and what the learner does. This is the **English**
body; the French one lives next to it in `index.fr.md`.
