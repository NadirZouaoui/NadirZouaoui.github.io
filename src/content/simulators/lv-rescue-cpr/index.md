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
  - slug: kit-naming
    title: { en: "Naming the rescue kit", fr: "Identification du kit de sauvetage" }
    caption: { en: "The trainee selects each item of the rescue kit on the bench and names it from a menu.", fr: "Le stagiaire sélectionne chaque élément du kit de sauvetage sur l'établi et le nomme à partir d'un menu." }
    src: /media/simulators/lv-rescue-cpr/kit-naming.mp4
    poster: /media/simulators/lv-rescue-cpr/kit-naming.jpg
    duration: "0:17"
  - slug: aed-pads
    title: { en: "Defibrillator pads", fr: "Électrodes du défibrillateur" }
    caption: { en: "The two pads are placed on the chest.", fr: "Les deux électrodes sont posées sur le thorax." }
    src: /media/simulators/lv-rescue-cpr/aed-pads.mp4
    poster: /media/simulators/lv-rescue-cpr/aed-pads.jpg
    duration: "0:14"
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
  - image: "@assets/simulators/lv-rescue-cpr/hazard-check.jpg"
    alt: { en: "Hazard checklist with eight statements, four of them ticked, and a Submit assessment button", fr: "Liste de contrôle des dangers de huit propositions dont quatre sont cochées, et un bouton de validation" }
    caption: { en: "Identifying the hazards from a list.", fr: "Identification des dangers dans une liste." }
  - image: "@assets/simulators/lv-rescue-cpr/isolation-sign.jpg"
    alt: { en: "Open breaker panel with an orange isolation sign hung above the breaker and a message confirming the isolation point is marked", fr: "Panneau de disjoncteur ouvert avec un panneau de coupure orange accroché au-dessus du disjoncteur et un message confirmant le repérage du point de coupure" }
    caption: { en: "Marking the isolation point on the breaker.", fr: "Repérage du point de coupure sur le disjoncteur." }
  - image: "@assets/simulators/lv-rescue-cpr/drag-isolate.jpg"
    alt: { en: "Casualty lying on the floor of the switchroom with the labels Drag the casualty to the safe area and Isolate the circuit at the breaker", fr: "Victime allongée sur le sol du local électrique avec les étiquettes Tirer la victime vers la zone sûre et Couper le circuit au disjoncteur" }
    caption: { en: "Dragging the casualty clear.", fr: "Dégagement de la victime." }
  - image: "@assets/simulators/lv-rescue-cpr/isolate-breaker.jpg"
    alt: { en: "Open board with the isolation sign, the label Isolate the circuit at the breaker highlighted and the option Isolate at Breaker Handle", fr: "Tableau ouvert avec le panneau de coupure, l'étiquette Couper le circuit au disjoncteur en surbrillance et l'option Couper à la poignée du disjoncteur" }
    caption: { en: "Isolating the circuit at the breaker.", fr: "Coupure du circuit au disjoncteur." }
  - image: "@assets/simulators/lv-rescue-cpr/primary-survey.jpg"
    alt: { en: "Casualty seen from the head with three action labels on the body: Check for a response, Start compressions, Check the casualty is not on fire", fr: "Victime vue depuis la tête avec trois étiquettes d'action sur le corps : vérifier la réponse, commencer les compressions, vérifier que la victime ne brûle pas" }
    caption: { en: "Primary survey: actions chosen on the casualty.", fr: "Bilan primaire : les actions se choisissent sur la victime." }
  - image: "@assets/simulators/lv-rescue-cpr/breathing-check.jpg"
    alt: { en: "Casualty's face seen from above with the label Check for breathing highlighted on the mouth", fr: "Visage de la victime vu de dessus avec l'étiquette Contrôler la respiration en surbrillance sur la bouche" }
    caption: { en: "Checking for breathing.", fr: "Contrôle de la respiration." }
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
