## Contexte

GCB (ENGCB) avait besoin d'une seule armoire servant à la fois de coffret de puissance et de coffret de commande pour les trois pompes doseuses d'un skid d'inhibiteur de corrosion réalisé par PROSKID. L'armoire est prévue pour les atmosphères explosives : le devis du fabricant indique Ex d IIB+H2 T5 Gb, Ex tb IIIC T100 °C Db, IP66. Le fabricant a fourni l'armoire ; le câblage et l'intégration revenaient à PROSKID.

La logique est à relais câblés. Chaque pompe se démarre et s'arrête en local depuis la porte, ou bien un sélecteur donne la main à la RTU du site, qui reçoit aussi l'état de chaque pompe. Les voyants en face avant donnent le retour d'information local.

## Ce que j'ai fait

- J'ai tout fait seul, de l'approvisionnement des composants à l'étude puis au câblage.
- J'ai dessiné les schémas de puissance, les schémas de commande et l'implantation de la porte sous EPLAN Electric P8.
- J'ai implanté la platine et la porte sous EPLAN Pro Panel 3D avant l'arrivée de l'armoire, de sorte que la position de chaque composant était arrêtée avant tout montage.
- J'ai câblé la commande en logique à relais : un bouton marche et un bouton arrêt par pompe, un contact d'auto-maintien du contacteur, un sélecteur local ou distant et un arrêt d'urgence.
- J'ai monté et câblé à la main les composants sur la platine et à l'arrière de la porte.
- J'ai réalisé un coffret de test qui joue le rôle de la RTU, pour essayer la commande à distance.

## Résultat

Une armoire antidéflagrante complète de puissance et de commande pour trois pompes, étudiée sous EPLAN avant l'arrivée du matériel et câblée à la main. Sa porte comporte 19 appareils : 10 voyants, 6 boutons-poussoirs, un sélecteur local ou distant, un interrupteur ON/OFF et un arrêt d'urgence. Les voyants indiquent la présence de chaque phase, l'état de marche et de défaut de chaque pompe, et un niveau de liquide bas. La commande à distance a été essayée sur le banc de test RTU.
