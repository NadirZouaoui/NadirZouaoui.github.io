## Contexte

Sur site isolé, un skid de dosage chimique anticorrosion doit être alimenté en 24 V DC par une installation solaire, tout comme la RTU qui le supervise. Pour une offre technique, PROSKID avait besoin de définir une alimentation solaire autonome pour chacun des deux.

L'étude est documentée dans un synoptique de deux feuilles daté du 03/10/2023, une feuille par version. La version skid comprend quatre modules monocristallins de 325 Wc sur un mât escamotable en acier galvanisé intégré au skid solaire, d'une hauteur de 10 m une fois déployé. La version RTU comprend deux modules sur le même type de mât.

## Ce que j'ai fait

- Définition de l'architecture de l'alimentation pour les deux versions : champ photovoltaïque, coffret de sectionnement et parafoudre, régulateur de charge MPPT, parc de batteries, contrôleur de batteries et convertisseur DC/DC pour la sortie 24 V.
- Choix des caractéristiques de chaque composant : régulateur de charge MPPT 150 V / 70 A, convertisseur DC/DC 24 V / 24 V 240 W et parc de batteries 12 × 2 V / 570 Ah pour le skid ; 110 W et 12 × 2 V / 400 Ah pour la RTU.
- Choix des sections de câbles (4, 6, 16 et 25 mm² sur la version skid) et des protections de chaque départ (40 A et 20 A sur la version skid, 20 A et 10 A sur la version RTU).
- Ajout d'une sonde de température des batteries, d'un boîtier de communication avec liaison RJ45 vers la RTU et d'un HMI local en façade de l'armoire.
- Pour la version RTU, ajout d'un convertisseur AC/DC (230 V / 24 V, 25 A) alimenté par une entrée 230 VAC. Le local batteries est marqué hors périmètre sur cette feuille.
- Dessin des deux feuilles sous QElectroTech.

## Résultat

Deux synoptiques pour l'offre technique, un par version, avec les composants, leurs caractéristiques et les sections de câbles définis. Il s'agissait d'une étude pour une offre ; je ne sais pas si ces alimentations ont été réalisées.
