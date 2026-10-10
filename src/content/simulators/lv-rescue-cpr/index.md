---
draft: true
order: 10
title:
  en: "Low-voltage rescue and CPR"
  fr: "Sauvetage basse tension et RCP"
summary:
  en: "First-person exercise in a switchroom: a worker receives an electric shock at a live board. The trainee prepares the rescue kit, breaks contact, isolates, then carries out CPR and defibrillation. All 26 steps are graded and the result is reported to the LMS."
  fr: "Exercice à la première personne dans un local électrique : un opérateur est électrisé sur un tableau sous tension. Le stagiaire prépare le kit de sauvetage, dégage la victime, consigne, puis réalise la RCP et la défibrillation. Les 26 étapes sont notées et le résultat est transmis au LMS."
status: delivered
tech: ["Godot 4", "Blender", "SCORM 1.2", "HTML5"]
cover: "@assets/simulators/lv-rescue-cpr/incident.jpg"
coverAlt:
  en: "A worker in contact with a live switchboard, a contact clock on screen and the insulated rescue hook in the trainee's hand"
  fr: "Un opérateur en contact avec un tableau sous tension, un chronomètre de contact à l'écran et la perche isolante dans la main du stagiaire"
learningGoal:
  en: "Carry out a low-voltage rescue and resuscitation in the correct order and in time, without becoming a second casualty."
  fr: "Réaliser un sauvetage basse tension et une réanimation dans le bon ordre et dans les temps, sans devenir une seconde victime."
heroClip:
  src: /media/simulators/lv-rescue-cpr/hero.mp4
  poster: /media/simulators/lv-rescue-cpr/hero.jpg
clips:
  - slug: incident
    title: { en: "The incident", fr: "L'accident" }
    caption: { en: "The worker is in contact with the live board. A clock counts the contact time until the trainee breaks it with the insulated rescue hook.", fr: "L'opérateur est en contact avec le tableau sous tension. Un chronomètre compte la durée du contact jusqu'à ce que le stagiaire le dégage avec la perche isolante." }
    src: /media/simulators/lv-rescue-cpr/incident.mp4
    poster: /media/simulators/lv-rescue-cpr/incident.jpg
    duration: "0:10"
  - slug: fatal-error
    title: { en: "A fatal error", fr: "Une erreur fatale" }
    caption: { en: "Touching the casualty bare-handed while still in contact ends the exercise, and the failure is recorded.", fr: "Toucher la victime à mains nues alors qu'elle est encore en contact met fin à l'exercice, et l'échec est enregistré." }
    src: /media/simulators/lv-rescue-cpr/fatal-error.mp4
    poster: /media/simulators/lv-rescue-cpr/fatal-error.jpg
    duration: "0:15"
  - slug: drag-isolate
    title: { en: "Drag clear and isolate", fr: "Dégagement et coupure" }
    caption: { en: "The casualty is dragged to a safe area and the supply is isolated at the breaker.", fr: "La victime est tirée vers une zone sûre et l'alimentation est coupée au disjoncteur." }
    src: /media/simulators/lv-rescue-cpr/drag-isolate.mp4
    poster: /media/simulators/lv-rescue-cpr/drag-isolate.jpg
    duration: "0:15"
  - slug: compressions
    title: { en: "Chest compressions", fr: "Compressions thoraciques" }
    caption: { en: "Thirty compressions, each one measured for depth and rate.", fr: "Trente compressions, chacune mesurée en profondeur et en cadence." }
    src: /media/simulators/lv-rescue-cpr/compressions.mp4
    poster: /media/simulators/lv-rescue-cpr/compressions.jpg
    duration: "0:17"
  - slug: aed-shock
    title: { en: "Stand clear and shock", fr: "Écartez-vous, choc" }
    caption: { en: "The trainee stands clear and delivers the shock.", fr: "Le stagiaire s'écarte et délivre le choc." }
    src: /media/simulators/lv-rescue-cpr/aed-shock.mp4
    poster: /media/simulators/lv-rescue-cpr/aed-shock.jpg
    duration: "0:17"
  - slug: debrief
    title: { en: "Debrief", fr: "Débriefing" }
    caption: { en: "Score, measurements and the step-by-step record of the attempt.", fr: "Note, mesures et relevé étape par étape de la tentative." }
    src: /media/simulators/lv-rescue-cpr/debrief.mp4
    poster: /media/simulators/lv-rescue-cpr/debrief.jpg
    duration: "0:14"
grading:
  pictures:
    - image: "@assets/simulators/lv-rescue-cpr/debrief-score.jpg"
      alt:
        en: "Debrief screen: 97 % against a pass mark of 80 %, elapsed time, 26 of 26 steps, five measurement tiles and the first rows of the step table"
        fr: "Écran de débriefing : 97 % pour un seuil de 80 %, temps écoulé, 26 étapes sur 26, cinq indicateurs mesurés et les premières lignes du tableau des étapes"
      caption:
        en: "Debrief: score against the pass mark, compressions in depth and in rate, pads placed, time to shock."
        fr: "Débriefing : note et seuil de réussite, compressions en profondeur et en cadence, électrodes posées, délai avant le choc."
    - image: "@assets/simulators/lv-rescue-cpr/debrief-steps.jpg"
      alt:
        en: "Step table of the debrief with the time of each action, critical steps marked with a star and one step marked late"
        fr: "Tableau des étapes du débriefing avec l'heure de chaque action, les étapes critiques marquées d'une étoile et une étape notée en retard"
      caption:
        en: "Every step with its time. Critical steps carry a star; here the call for help is marked late."
        fr: "Chaque étape avec son heure. Les étapes critiques portent une étoile ; ici, l'appel des secours est noté en retard."
    - image: "@assets/simulators/lv-rescue-cpr/exercise-failed.jpg"
      alt:
        en: "Exercise failed screen explaining that the trainee touched a casualty still connected to a live conductor"
        fr: "Écran d'échec de l'exercice expliquant que le stagiaire a touché une victime encore reliée à un conducteur sous tension"
      caption:
        en: "A fatal error ends the exercise, states the reason and records the result."
        fr: "Une erreur fatale met fin à l'exercice, en donne la raison et enregistre le résultat."
    - image: "@assets/simulators/lv-rescue-cpr/compressions-gauge.jpg"
      alt:
        en: "Chest compressions in progress with a counter at 13 of 30 and a depth bar"
        fr: "Compressions thoraciques en cours avec un compteur à 13 sur 30 et une barre de profondeur"
      caption:
        en: "Each compression is measured as it is given."
        fr: "Chaque compression est mesurée au moment où elle est faite."
  points:
    - en: "26 steps are graded, each with its own weight. The pass mark is 80 %."
      fr: "26 étapes sont notées, chacune avec sa pondération. Le seuil de réussite est de 80 %."
    - en: "A step done out of order or late keeps only part of its marks. The debrief shows the trainee's order against the correct one."
      fr: "Une étape faite dans le désordre ou en retard ne conserve qu'une partie de ses points. Le débriefing compare l'ordre du stagiaire à l'ordre correct."
    - en: "Seven steps are critical: getting one wrong fails the attempt whatever the score."
      fr: "Sept étapes sont critiques : une erreur sur l'une d'elles entraîne l'échec, quelle que soit la note."
    - en: "A fatal safety error ends the exercise at once."
      fr: "Une erreur de sécurité fatale met fin à l'exercice immédiatement."
    - en: "Compressions are measured one by one for depth and rate, and the time to the first shock is recorded."
      fr: "Les compressions sont mesurées une à une en profondeur et en cadence, et le délai avant le premier choc est enregistré."
    - en: "Completion status, score and the step record are sent to the LMS through SCORM 1.2."
      fr: "Le statut, la note et le relevé des étapes sont transmis au LMS par SCORM 1.2."
gallery:
  - image: "@assets/simulators/lv-rescue-cpr/kit-naming.jpg"
    alt: { en: "Rescue kit laid out on a bench with a menu to name the selected item", fr: "Kit de sauvetage disposé sur un établi, avec un menu pour nommer l'élément sélectionné" }
    caption: { en: "Naming the items of the rescue kit.", fr: "Identification des éléments du kit de sauvetage." }
  - image: "@assets/simulators/lv-rescue-cpr/aed-pads.jpg"
    alt: { en: "Defibrillator beside the casualty with the first pad attached and the second site to select", fr: "Défibrillateur à côté de la victime, première électrode posée et second emplacement à choisir" }
    caption: { en: "Placing the defibrillator pads.", fr: "Pose des électrodes du défibrillateur." }
underTheHood:
  - en: "Modelled in Blender and built in Godot 4 with the Compatibility renderer, so the same project runs in a browser (WebGL 2) and on Windows."
    fr: "Modélisé dans Blender et réalisé avec Godot 4 et son moteur de rendu Compatibility : le même projet fonctionne dans un navigateur (WebGL 2) et sous Windows."
  - en: "The procedure is data: steps, weights, prerequisites and critical steps are defined in one place and can be changed without touching the scene."
    fr: "La procédure est une donnée : étapes, pondérations, prérequis et étapes critiques sont définis à un seul endroit et se modifient sans toucher à la scène."
  - en: "The simulation does not stop the trainee from making a wrong choice. It records it."
    fr: "La simulation n'empêche pas le stagiaire de faire un mauvais choix. Elle l'enregistre."
  - en: "Scoring and SCORM reporting are covered by automated tests and were checked against a test LMS before delivery."
    fr: "La notation et le suivi SCORM sont couverts par des tests automatisés et ont été vérifiés sur un LMS de test avant la livraison."
  - en: "The resuscitation part also exists as a shorter standalone CPR module, built from the same scenario."
    fr: "La partie réanimation existe aussi en module RCP autonome, plus court, réalisé à partir du même scénario."
---

A worker opens a live low-voltage board and receives an electric shock. The trainee has prepared for it: checking and naming the rescue kit, identifying the hazards and marking the isolation point. When the shock happens, the trainee breaks contact with the insulated hook, drags the casualty clear, isolates the supply, calls for help, then carries out CPR and uses the defibrillator until the ambulance arrives.

The module was made for an Australian registered training organisation, which uses it to assess low-voltage rescue and CPR competency.
