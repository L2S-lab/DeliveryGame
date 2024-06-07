# DeliveryGame
[English version below]
## But du Jeu

Il s'agit d'un jeu de livraison entre un robot DJI ROBOMASTER EP contrôlé manuellement par une personne (clavier ou manette) et un robot DJI ROBOMASTER EP controlé automatiquement grâce à un cote Python. L'objectif est de récupérer deux balles de tennis et de les ramener dans un panier.

## Installation de l'environnement Python

Installation de Python : 
- Avoir python 3.7 ou 3.8 installé sur son ordinateur. Vérification possible avec :
``py --list``
Si ça n'est pas le cas, installer la version voulue depuis https://www.python.org/downloads/

Mise en place de l'environnement virtuel et installation du package robomaster : 

- Se placer à l'endroit voulu pour créer l'environnement virtuel puis exécuter la commande :
``py -3.7 -m venv .venv``. Cela va créer un nouvel environnement virtuel python avec la version donnée.

- Une fois dans cet environnement virtuel, on peut installer l'ensemble des modules nécessaires avec la commande :
``pip install -r requirements.txt``

- Pour activer l'environnement, utiliser la commande 
``.\/.venv/Scripts/activate``
- Pour quitter l'environnement virtuel, utiliser la commande 
``deactivate``

En cas d'erreur, tuer le terminal permet de déconnecter l'environnement virtuel.

## Mise en place du jeu

Le matériel nécessaire à la mise en place du jeu est le suivant :

- 2 DJI ROBOMASTER EP
- 4 balles de tennis
- 2 paniers : des cartons feront l'affaire
- des marqueurs DJI

Chaque robot doit faire face à deux balles de tennis et derrière le robot doit se situer la boite en carton avec le marqueur. 

Pour se connecter aux robots : 

- Allumer les robots puis mettre l'interrupteur de connexion sur le mode direct (icone avec le téléphone)
- Se connecter au WIFI du robot sur son ordinateur
- Le mot de passe se trouve sur l'étiquette du robot

Pour faire fonctionner le robot contrôlé automatiquement :

- Lancer le programme `main.py` qui se situe dans le dossier `TheGame`.
Il est possible de configurer la langue dans laquelle le son est émis.

Pour faire fonctionner le robot contrôlé manuellement :

- Brancher une manette de jeu à votre ordinateur.
- Lancer le programme `control_manette.py` dans le dossier `ControlRobot`.


## Aspect pédagogique du jeu

Les étudiants ont la possibilité de régler le PID qui permet au robot d'aller vers le marqueur. 

Pour cela, il faut :

- Mettre le robot en face du marqueur. Il peut être décalé sur le côté.
- Lancer le programme `setting_pi.py` dans le dossier `PedagoTools`.
- Régler les coefficients, appuyer sur start et recommencer à l'infini jusqu'à que le PID soit bien réglé.

---------------------------------------------------------------------------------------------------------------------------------------
English Version
## Goal of the game

This is a delivery game between a DJI ROBOMASTER EP robot controlled manually by a person (keyboard or joystick) and a DJI ROBOMASTER EP robot controlled automatically using a Python code. The aim is to retrieve two tennis balls and return them to a basket.

## Setting up the game

The equipment needed to set up the game is as follows:

- 2 DJI ROBOMASTER EP
- 4 tennis balls
- 2 baskets: cardboard boxes will do
- DJI markers

Each robot must be in front of two tennis balls and behind the robot must be the cardboard box with the marker. 

To make the automatically controlled robot work :

- Run the `main.py` program which is located in the `TheGame` folder.
It is possible to configure the language in which the sound is emitted.

To operate the robot manually :

- Connect a game controller to your computer.
- Run the `control_manette.py` program in the `ControlRobot` folder.


## Educational aspect of the game

The students can set the PID that allows the robot to move towards the marker. 

To do this, they must :

- Place the robot in front of the marker. It can be moved to the side.
- Run the `setting_pi.py` program in the `PedagoTools` folder.
- Set the coefficients, press start and repeat ad infinitum until the PID is set correctly.
