# Battlegrounds
- Auteur: NGUYEN Anthony
- E-Mail: nguyen.anthony.dev@gmail.com

## Préambule
Ce jeu à été conçu pour le projet d'ISN du 2ème trimestre 2018-2019. <br>
Toute la progression du jeu peut être suivie dans "Commits". <br>
Les bugs majeurs sont répertoriés dans "Issues". <br>
La progression en todo list est disponible dans "Projects".<br>

Le jeu et le code sont entièrement en anglais afin de respecter un assignement constant des variables. <br>

Un mode pour les daltoniens est disponible (Protanomaly uniquement). <br>
Pour cela, modifier la ligne au début du code ```colorblind = 0``` 0 pour des couleurs normales, 1 pour le mode daltonien.

### Nécéssaire:
    - Python 3.0+
    - TkInter
    - sys
    - os
    
### Contenu:
    - /board.py - Le programme à faire tourner
    - /images - Fichier images contenant un screenshot de chaque hexagone
    - images/colorblind - version daltonien
    
## Règles du jeu et fonctionnement:

### Règles du jeu:
Le jeu fonctionne en tour par tour avec 2 joueurs. <br>
L'objectif du jeu est de capturer la base adverse de l'autre côté du plateau de jeu.<br>
Des obstacles environnementaux sont présents sur le plateau (montagnes, lacs)<br>
Chaque joueur est représenté par une armée de couleur différente.<br>
L'armée est composée d'esquadrons d'unités.<br>

Un esquadron possède donc 4 caractéristiques :
- *Units* : ce sont les points de vie de chaque unité. Par défaut, chaque esquadron est composé de 6 unités.
- *AP (Attack points)* : ce sont les points d'attaque. Lors d'une attaque, ils infligent un nombre x de dégâts à l'ennemi.
- *EP (Energy points)* : ce sont les points d'énergie. Ils déterminent le nombre d'attaque possible.
- *MP (Movement points)* : ce sont les points de mouvements. Ils déterminent le nombre de cases que l'esquadron peut se déplacer.

A chaque tour, le joueur peut déplacer autant d'esquadrons qu'il souhaite.

### Fonctionnement:
- Joueur 1 :
![alt text](https://i.imgur.com/MjvXilA.png) ver. daltonien![alt text](https://i.imgur.com/oH5eb48.png)
- Joueur 2 :
![alt text](https://i.imgur.com/eeafQTs.png) ver. daltonien![alt text](https://i.imgur.com/l9p4QhN.png)
- Objectif :
![alt text](https://i.imgur.com/XLCXeyz.png) ver. daltonien![alt text](https://i.imgur.com/omIGrjL.png)
- Montagne :
![alt text](https://i.imgur.com/CUfK0nf.png) ver. daltonien![alt text](https://i.imgur.com/HamxFE9.png)
- Eau :
![alt text](https://i.imgur.com/vpstBkV.png) ver. daltonien![alt text](https://i.imgur.com/9O5ZomI.png)

Sur le côté gauche, une barre d'information est disponible:

![alt text](https://i.imgur.com/mZrGERK.png)

### Plusieurs informations sont affichées:
>- "Status" permet d'afficher si une action effectuée par l'utilisateur est impossible.
>![alt text](https://i.imgur.com/MPsqPVV.png)
>- "End Turn" permet de passer la main à l'adversaire.
>![alt text](https://i.imgur.com/kICQzwx.png)
>- "Turn of" permet de savoir à qui est le tour.
>![alt text](https://i.imgur.com/NMdMn1x.png)

### D'autres interactions sont possibles:
>- Le mouvement est possible lorsqu'une unité jouable est séléctionnée
>![alt text](https://i.imgur.com/WQuyPtU.png)
>- Une fenêtre pop-up demande si le joueur veut rejouer
>![alt text](https://i.imgur.com/XaKEJm4.png)
