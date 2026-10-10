---
draft: true
order: 20
title:
  en: "HV substation switching"
  fr: "Manœuvres HT en poste"
summary:
  en: "First-person exercise in a 34.5 kV / 4.8 kV substation. The trainee writes the switching sheet, isolates a transformer bank, proves it dead, repairs it and restores supply. Each part is assessed and the result is reported to the LMS."
  fr: "Exercice à la première personne dans un poste 34,5 kV / 4,8 kV. Le stagiaire rédige la fiche de manœuvres, consigne un transformateur, vérifie l'absence de tension, le répare et rétablit l'alimentation. Chaque partie est évaluée et le résultat est transmis au LMS."
status: delivered
tech: ["Godot 4", "Blender", "SCORM 1.2", "HTML5"]
cover: "@assets/simulators/hv-substation-switching/yard.jpg"
coverAlt:
  en: "First-person view of the substation yard with a high-voltage tester in hand and the task list on screen"
  fr: "Vue à la première personne de la cour du poste, détecteur de tension HT en main et liste des tâches à l'écran"
learningGoal:
  en: "Plan and carry out an isolation and a restoration in the correct order, under an access permit and a test permit, and prove the equipment dead before working on it."
  fr: "Préparer et exécuter une consignation puis une remise en service dans le bon ordre, sous permis d'accès et permis d'essai, et vérifier l'absence de tension avant d'intervenir."
heroClip:
  src: /media/simulators/hv-substation-switching/hero.mp4
  poster: /media/simulators/hv-substation-switching/hero.jpg
clips:
  - slug: brief-schematic
    title: { en: "Brief and single-line diagram", fr: "Consigne et schéma unifilaire" }
    caption: { en: "The exercise opens on the fault to deal with and the diagram of the substation.", fr: "L'exercice s'ouvre sur le défaut à traiter et le schéma du poste." }
    src: /media/simulators/hv-substation-switching/brief-schematic.mp4
    poster: /media/simulators/hv-substation-switching/brief-schematic.jpg
    duration: "0:07"
  - slug: switching-sheet
    title: { en: "Writing the switching sheet", fr: "Rédaction de la fiche de manœuvres" }
    caption: { en: "Each apparatus is dragged into a step and given its operation, for the isolation and then for the restoration.", fr: "Chaque appareil est glissé dans une étape et reçoit sa manœuvre, pour la consignation puis pour la remise en service." }
    src: /media/simulators/hv-substation-switching/switching-sheet.mp4
    poster: /media/simulators/hv-substation-switching/switching-sheet.jpg
    duration: "0:10"
  - slug: mimic-panel
    title: { en: "Switching on the mimic panel", fr: "Manœuvres sur le synoptique" }
    caption: { en: "The breakers are operated on the panel, with the trainee's own sheet beside it.", fr: "Les disjoncteurs sont manœuvrés sur le tableau, la fiche du stagiaire affichée à côté." }
    src: /media/simulators/hv-substation-switching/mimic-panel.mp4
    poster: /media/simulators/hv-substation-switching/mimic-panel.jpg
    duration: "0:08"
  - slug: permits
    title: { en: "Access and test permits", fr: "Permis d'accès et permis d'essai" }
    caption: { en: "The trainee signs on to each permit before entering the yard.", fr: "Le stagiaire signe chaque permis avant d'entrer dans la cour." }
    src: /media/simulators/hv-substation-switching/permits.mp4
    poster: /media/simulators/hv-substation-switching/permits.jpg
    duration: "0:05"
  - slug: hv-tester
    title: { en: "Proving dead", fr: "Vérification d'absence de tension" }
    caption: { en: "Each phase of the transformer is tested with the HV tester until all three read dead.", fr: "Chaque phase du transformateur est contrôlée au détecteur HT jusqu'à ce que les trois soient hors tension." }
    src: /media/simulators/hv-substation-switching/hv-tester.mp4
    poster: /media/simulators/hv-substation-switching/hv-tester.jpg
    duration: "0:10"
  - slug: repair
    title: { en: "Inspection and repair", fr: "Inspection et réparation" }
    caption: { en: "The transformer is inspected, the leak is found and repaired.", fr: "Le transformateur est inspecté, la fuite est trouvée puis réparée." }
    src: /media/simulators/hv-substation-switching/repair.mp4
    poster: /media/simulators/hv-substation-switching/repair.jpg
    duration: "0:11"
  - slug: sign-off-reverse
    title: { en: "Sign-off and restoration", fr: "Clôture du permis et remise en service" }
    caption: { en: "The access permit is signed off, then the reverse sequence is switched on the panel.", fr: "Le permis d'accès est clôturé, puis la séquence inverse est exécutée sur le tableau." }
    src: /media/simulators/hv-substation-switching/sign-off-reverse.mp4
    poster: /media/simulators/hv-substation-switching/sign-off-reverse.jpg
    duration: "0:15"
grading:
  pictures:
    - image: "@assets/simulators/hv-substation-switching/assessment-failed.jpg"
      alt:
        en: "Assessment summary screen marked failed, with the four parts, the reason for each and a chronological log of the trainee's actions"
        fr: "Écran de synthèse d'évaluation en échec, avec les quatre parties, le motif de chacune et le journal chronologique des actions du stagiaire"
      caption:
        en: "A failed attempt: each of the four parts carries its reason, and the log names every error."
        fr: "Une tentative échouée : chacune des quatre parties porte son motif, et le journal nomme chaque erreur."
    - image: "@assets/simulators/hv-substation-switching/assessment-passed.jpg"
      alt:
        en: "Assessment summary screen marked passed, with the four parts passed and the submitted switching sequences in the log"
        fr: "Écran de synthèse d'évaluation réussie, avec les quatre parties validées et les séquences de manœuvres soumises dans le journal"
      caption:
        en: "A passed attempt, with the submitted sheet recorded in the log."
        fr: "Une tentative réussie, avec la fiche soumise consignée dans le journal."
    - image: "@assets/simulators/hv-substation-switching/correct-sequence.jpg"
      alt:
        en: "Screen showing the standard operating procedure: the correct forward and reverse switching sequences and the permit steps"
        fr: "Écran présentant la procédure de référence : les séquences de manœuvres aller et retour correctes et les étapes des permis"
      caption:
        en: "After the attempt, the correct sequence is shown with the purpose of each step."
        fr: "Après la tentative, la séquence correcte est affichée avec le rôle de chaque étape."
    - image: "@assets/simulators/hv-substation-switching/switching-sheet.jpg"
      alt:
        en: "Switching sheet on a clipboard, with numbered steps, the operation chosen for each and the list of apparatus to drag in"
        fr: "Fiche de manœuvres sur un porte-bloc, avec les étapes numérotées, la manœuvre choisie pour chacune et la liste des appareils à glisser"
      caption:
        en: "The sheet is written by the trainee and is itself assessed."
        fr: "La fiche est rédigée par le stagiaire et fait elle-même l'objet de l'évaluation."
  points:
    - en: "Four parts are assessed separately: writing the switching sheet, forward switching (isolation), permits with test for dead and repair, and reverse switching (restoration)."
      fr: "Quatre parties sont évaluées séparément : rédaction de la fiche de manœuvres, manœuvres aller (consignation), permis avec vérification d'absence de tension et réparation, manœuvres retour (remise en service)."
    - en: "The sheet written by the trainee is checked against the sequence rules, and a wrong order is named in the log."
      fr: "La fiche rédigée par le stagiaire est contrôlée par rapport aux règles de séquence, et un ordre incorrect est signalé dans le journal."
    - en: "The log records every operation in time order, including operating the wrong apparatus, switching before the access permit is signed on, and steps left out."
      fr: "Le journal consigne chaque manœuvre dans l'ordre chronologique, y compris la manœuvre d'un mauvais appareil, une manœuvre avant la signature du permis d'accès et les étapes omises."
    - en: "Completion status, score and the log are sent to the LMS through SCORM 1.2."
      fr: "Le statut, la note et le journal sont transmis au LMS par SCORM 1.2."
gallery:
  - image: "@assets/simulators/hv-substation-switching/single-line-diagram.jpg"
    alt: { en: "Single-line diagram of the substation with the faulty transformer bank circled", fr: "Schéma unifilaire du poste, le transformateur en défaut entouré" }
    caption: { en: "Single-line diagram of the training substation.", fr: "Schéma unifilaire du poste d'entraînement." }
  - image: "@assets/simulators/hv-substation-switching/mimic-panel.jpg"
    alt: { en: "Mimic panel with trip, close and earth switches and indicator lamps, the switching sheet displayed beside it", fr: "Synoptique avec commutateurs déclenchement, enclenchement et mise à la terre et voyants, la fiche de manœuvres affichée à côté" }
    caption: { en: "Mimic panel with the switching sheet.", fr: "Synoptique avec la fiche de manœuvres." }
  - image: "@assets/simulators/hv-substation-switching/equipment-live.jpg"
    alt: { en: "HV tester held at a breaker with a red warning that the equipment is live", fr: "Détecteur HT présenté sur un disjoncteur, avec un avertissement rouge indiquant que l'équipement est sous tension" }
    caption: { en: "Testing equipment that is still live.", fr: "Contrôle d'un équipement encore sous tension." }
  - image: "@assets/simulators/hv-substation-switching/phase-dead.jpg"
    alt: { en: "HV tester at the transformer with a green message that the second of three phases is dead", fr: "Détecteur HT au transformateur, avec un message vert indiquant que la deuxième phase sur trois est hors tension" }
    caption: { en: "Proving dead, phase by phase.", fr: "Vérification d'absence de tension, phase par phase." }
  - image: "@assets/simulators/hv-substation-switching/transformer-repaired.jpg"
    alt: { en: "Transformer in the yard with a message that it has been repaired", fr: "Transformateur dans la cour, avec un message indiquant qu'il est réparé" }
    caption: { en: "Repair completed.", fr: "Réparation terminée." }
  - image: "@assets/simulators/hv-substation-switching/yard.jpg"
    alt: { en: "Substation yard seen in first person, HV tester in hand, task list on screen", fr: "Cour du poste à la première personne, détecteur HT en main, liste des tâches à l'écran" }
    caption: { en: "The yard, with the task list.", fr: "La cour, avec la liste des tâches." }
underTheHood:
  - en: "Modelled in Blender and built in Godot 4. The same project is exported to HTML5 for the browser and to Windows."
    fr: "Modélisé dans Blender et réalisé avec Godot 4. Le même projet est exporté en HTML5 pour le navigateur et pour Windows."
  - en: "The state of each breaker on the mimic panel decides which equipment in the yard is live."
    fr: "L'état de chaque disjoncteur du synoptique détermine quels équipements de la cour sont sous tension."
  - en: "Switching sheets and permits carry their own numbers, and an attempt to switch without a signed permit is recorded and assessed."
    fr: "Les fiches de manœuvres et les permis portent leurs propres numéros, et une tentative de manœuvre sans permis signé est consignée et évaluée."
  - en: "Packaged as a SCORM 1.2 module that runs inside the LMS with nothing to install."
    fr: "Livré sous forme de module SCORM 1.2 qui s'exécute dans le LMS, sans installation."
---

A transformer bank in a 34.5 kV / 4.8 kV substation has a fault. The trainee writes the switching sheet, isolates and earths the bank from the control room, signs on to the permits, proves the transformer dead in the yard, repairs it, then restores supply in the reverse order.

The module was made for an Australian registered training organisation, which uses it to assess HV switching competency. The substation and its diagram are a training layout, not a real site.
