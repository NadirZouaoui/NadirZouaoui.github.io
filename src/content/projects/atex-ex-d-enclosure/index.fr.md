## Contexte

PROSKID a réalisé pour GCB (ENGCB) un skid d'injection chimique qui dose un inhibiteur de corrosion (Chimec) dans un gazoduc. Ses trois pompes doseuses sont alimentées et commandées depuis une seule armoire antidéflagrante montée sur le skid, de marquage Ex d IIB+H2 T5 Gb, Ex tb IIIC T100 °C Db, IP66.

Le fabricant de l'armoire, ATEX System, usine la porte et les entrées de câbles et monte les appareils de porte certifiés selon le plan fourni par l'acheteur. Une armoire antidéflagrante ne peut pas être percée après coup sans perdre sa certification : l'implantation devait donc être définitive avant la commande. Le matériel interne, son montage et tout le câblage relevaient de PROSKID.

La commande est en logique câblée à relais, sans automate. En mode local, chaque pompe se démarre et s'arrête depuis la porte. En mode distant, les ordres viennent de la RTU du site, qui reçoit aussi l'état des pompes. Les voyants de la porte donnent le retour d'information local.

## Ce que j'ai fait

J'ai pris en charge l'armoire de la spécification aux essais :

- Spécification et approvisionnement : armoire, appareils de porte et entrées de câbles définis avec le fabricant, composants internes approvisionnés.
- Étude électrique sous EPLAN Electric P8 : schémas de puissance, schémas de commande et implantation de la porte.
- Implantation 3D sous EPLAN Pro Panel avant la livraison : platine, goulottes, rails DIN et borniers positionnés dans le modèle, que le montage a ensuite suivi.
- Logique de commande à relais : marche et arrêt par pompe avec auto-maintien du contacteur, sélection local ou distant, arrêt d'urgence et signaux d'état vers la RTU.
- Montage et câblage de la platine et de la porte.
- Un banc de test jouant le rôle de la RTU, réalisé pour vérifier les ordres à distance et les retours d'état.

## Résultat

L'armoire a été montée et câblée conformément au modèle EPLAN, puis mise sous tension et testée, y compris la commande à distance à l'aide du banc de test RTU. Depuis la porte, l'opérateur démarre et arrête chaque pompe, choisit la commande locale ou distante, et lit la présence de chaque phase, la marche et le défaut de chaque pompe ainsi que le niveau de liquide bas.
