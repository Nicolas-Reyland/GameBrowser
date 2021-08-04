# GameBrowser ⚠️ french project ⚠️
🥖 This project is made for french speakers. The GUI is in french, so I figured the README should be in french too. 🥖

Un programme pour parcourir et lancer vos jeux (ou programmes), puis suivre leur performances. Tout ceci, en utilisant bien moins de resources que les programmes typiques de ce type.

## Installation
Vous aurez besoin de Python3+ et de pip d'installé.

D'abord, installez les dépendences python:
```
pip install -r requirements.txt
```

Vous pouvez également installer les dépendences additionnelles pour de meilleures performances.
```
pip install -r additional-requirements.txt
```

Pour lancer l'application, on peut simplement lancer la commande suivante:
```
python main.pyw
```

Une meilleure pratique serait de créer un racouricis Windows et de lancer le fichier 'main.pyw' avec le programme 'pythonw' (et non 'python'), qui est installé lors de l'installation de python. Vous pouvez utiliser l'icône de votre choix, mais je vous en ait préparé une au besoin (le fichier en .ico).

## Utilisation
L'interface est assez intuitive, pour ce qui concerne un usage classique et peu avancé. Il y a cependant une barre blanche de recherche en haut, dans laquelle vous pouvez soit recherchez vos jeux (par nom), soit entrer des petites commandes bien utiles.

### Recherche
Pour rechercher un de vos jeux, vous n'avez qu'à commencer à taper son nom dans la barre en haut de l'interface. Même si vous faites une faute de frappe, ça ne devrait pas impacter les résultats affichés.

### Commandes
Tout d'abord, les commandes commencent par le caractère `!`. Il est donc déconseillé de nommer un jeu avec un nom commençant par le point d'exclamation.

#### Commande !help
Pour optenir le l'aide, il existe la commande `!help`, qui vous affiche, entre autres,  la listes des commandes possibles. Pour avoir de l'aide sur l'utilisation d'une commande, il faut écrire `!help nom-de-la-commande`.

#### Commandes classiques et Modules
Lorsque vous verrez les pages d'aide des différentes commandes, vous verrez que certaines sont commandes dites classqies, et que d'autres sont des modules. Pour utiliser une commande classique, il faut simplement écrire `!nom-de-cmd arg1 arg2 ...`. Pour utiliser une commande d'un module (un module a des sous-commandes), il faut ècrire quelque-chose comme `!nom-de-module sous-commande arg1 arg2 ...`.


