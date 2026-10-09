## Contexte

SARL Ibrahim & Fils (IFRI) équipe les toitures de plusieurs bâtiments de production de son site d'Akbou d'une centrale photovoltaïque en autoconsommation. La centrale n'injecte jamais sur le réseau : les onduleurs alimentent les tableaux généraux basse tension existants des bâtiments et l'énergie est consommée sur place.

Le dossier d'étude décrit une centrale de 5 400 kW AC composée de 36 onduleurs Huawei SUN2000-150K (150 kW chacun) et de modules bifaciaux JinkoSolar Tiger Neo 635 Wc, répartis en 12 zones, chacune avec son armoire AC 400 V. Les armoires se raccordent à 11 points d'injection sur les tableaux existants. Un stockage par batteries de 10 × 241 kWh figure sur les schémas comme hors lot de ce dossier.

## Ce que j'ai fait

J'ai travaillé sur l'étude électrique et l'étude énergétique, du calepinage en toiture aux schémas unifilaires :

- Calepinage des modules de 635 Wc sur les toitures, en tenant compte des ombrages, des accès et des chemins de câbles.
- Composition des chaînes et ratio DC/AC, et découpage des toitures en blocs onduleurs de 150 kW.
- Bloc type de 150 kW : 7 entrées MPPT de 2 chaînes chacune, et un disjoncteur ABB XT4N 250 sur la sortie AC.
- Architecture DC sans fusible, justifiée par le courant inverse : 1,25 × 17,96 = 22,45 A pour un calibre fusible série admissible de 35 A pour le module (IEC 62548, IEC 60364-7-712).
- Injection sur les TGBT existants : schémas unifilaires, dimensionnement des disjoncteurs, sections de câbles AC et DC et chute de tension.
- Points de raccordement du stockage par batteries représentés sur les schémas unifilaires ; le stockage lui-même est hors lot.
- Analyse du profil de charge du site et de la qualité de l'énergie.
- Étude de productible sous Archelios Pro pour chaque zone, avec les valeurs P50 et P90 et le ratio de performance.

## Production

Les rapports Archelios Pro donnent les résultats suivants de première année pour les deux zones étudiées (production AC, orientation est-ouest à 5° d'inclinaison, modules de 635 Wc) :

- **Zone Tetra et Canette :** 605,79 kWc, 954 modules, 4 onduleurs. Productible spécifique de 1 404 kWh/kWc en P50 et de 1 288 kWh/kWc en P90, énergie AC annuelle de 850,5 MWh, ratio de performance de 83,18 %.
- **Zone KSB :** 1 280,16 kWc, 2 016 modules, 8 onduleurs. Productible spécifique de 1 397 kWh/kWc en P50 et de 1 281 kWh/kWc en P90, énergie AC annuelle de 1 789 MWh, ratio de performance de 82,90 %.

## Résultat

Le dossier d'étude a été émis sous forme de 17 feuilles de schémas unifilaires (indice D, 27 juillet 2026) : schéma général, bloc type de 150 kW, une feuille par point d'injection et le récapitulatif des départs AC.

Les études de productible de la zone Tetra et Canette et de la zone KSB sont résumées dans la section Production ci-dessus.

Les photos montrent l'installation en cours sur les toitures en août et septembre 2026.
