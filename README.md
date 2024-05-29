# DeliveryGame
[English version below]
## But du Jeu

Il s'agit d'un jeu de livraison entre un robot DJI ROBOMASTER EP contrôlé manuellement par une personne (clavier ou manette) et un robot DJI ROBOMASTER EP controlé automatiquement grâce à un cote Python. L'objectif est de récupérer deux balles de tennis et de les ramener dans un panier.

## Mise en place du jeu

Le matériel nécessaire à la mise en place du jeu est le suivant :

- 2 DJI ROBOMASTER EP
- 4 balles de tennis
- 2 paniers : des cartons feront l'affaire
- des marqueurs DJI

Chaque robot doit faire à deux balles de tennis et derrière le robot doit se situer la boite en carton avec le marqueur. 

Pour faire fonctionner le robot controlé automatiquement :

- Lancer le programme `main.py` qui se situe dans le dossier `TheGame`.
Il est possible de configurer la langue dans laquelle le son est émis.

Pour faire fonctionner le robot controlé manuellement :

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

Each robot must play with two tennis balls and behind the robot must be the cardboard box with the marker. 

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
