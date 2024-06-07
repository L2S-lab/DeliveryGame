# DeliveryGame
[English version below]
## But du Jeu

Il s'agit d'un jeu de livraison entre un robot DJI ROBOMASTER EP contrôlé manuellement par une personne (clavier ou manette) et un robot DJI ROBOMASTER EP controlé automatiquement grâce à un cote Python. L'objectif est de récupérer deux balles de tennis et de les ramener dans un panier.

## Installation de l'environnement Python

Installation de Python : 
- Avoir python 3.7 ou 3.8 installé sur son ordinateur. Vérification possible avec
``py --list``
Si ça n'est pas le cas, installer la version voulue depuis https://www.python.org/downloads/

Mise en place de l'environnement virtuel et installation des packages nécessaires : 

- Se placer à l'endroit voulu pour créer l'environnement virtuel puis exécuter la commande
``py -3.7 -m venv .venv``. Cela va créer un nouvel environnement virtuel python avec la version donnée.

- Pour activer l'environnement, utiliser la commande 
``.\/.venv/Scripts/activate``

- Une fois dans cet environnement virtuel, on peut installer l'ensemble des modules nécessaires avec la commande
``pip install -r requirements.txt``

- Pour quitter l'environnement virtuel, utiliser la commande 
``deactivate``

En cas d'erreur, tuer le terminal permet de déconnecter l'environnement virtuel.

## Mise en place du jeu

Le matériel nécessaire à la mise en place du jeu est le suivant :

- 2 DJI ROBOMASTER EP
- 4 balles de tennis
- 2 paniers : des cartons feront l'affaire
- des marqueurs DJI
- deux ordinateurs
- une manette 8-bitdo sn30 pro

Chaque robot doit faire face à deux balles de tennis et derrière le robot doit se situer la boite en carton avec le marqueur. 

Schéma de mise en place du jeu :   

![Schéma jeu](https://github.com/comoxx/DeliveryGame/assets/93337725/c95afe61-1f57-4ff4-9317-bffa23e5b58d)


Pour se connecter aux robots : 

- Allumer les robots puis mettre l'interrupteur de connexion sur le mode direct (icone avec le téléphone)
- Se connecter au WIFI du robot sur son ordinateur
- Le mot de passe se trouve sur l'étiquette du robot

Pour faire fonctionner le robot contrôlé automatiquement :

- Utiliser la commande `python .\TheGame\main.py ` pour démarrer le jeu.
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
# DeliveryGame
[English version below]
## Goal of the game

This is a delivery game between a DJI ROBOMASTER EP robot controlled manually by a person (keyboard or joystick) and a DJI ROBOMASTER EP robot controlled automatically using a Python code. The aim is to retrieve two tennis balls and return them to a basket.

## Installing the Python environment

Installing Python : 
- Have Python 3.7 or 3.8 installed on your computer. You can check with
py --list
If this is not the case, install the required version from https://www.python.org/downloads/

Setting up the virtual environment and installing the necessary packages: 

- Go to the location where you want to create the virtual environment and run the command
``py -3.7 -m venv .venv``. This will create a new python virtual environment with the given version.

- To activate the environment, use the command 
.\/.venv/Scripts/activate

- Once in this virtual environment, you can install all the necessary modules with the command
pip install -r requirements.txt

- To exit the virtual environment, use the command 
deactivate

In the event of an error, kill the terminal to disconnect the virtual environment.

## Setting up the game

The hardware required to set up the game is as follows:

- 2 DJI ROBOMASTER EP
- 4 tennis balls
- 2 baskets: cardboard boxes will do
- DJI markers
- two computers
Each robot must face two tennis balls and behind the robot must be the cardboard box with the marker. 

Diagram of how to set up the game :   

![Schéma jeu](https://github.com/comoxx/DeliveryGame/assets/93337725/c95afe61-1f57-4ff4-9317-bffa23e5b58d)


To connect to the robots : 

- Turn on the robots, then set the connection switch to direct mode (icon with the telephone).
- Connect to the robot's WIFI on your computer
- The password can be found on the robot label

To operate the automatically controlled robot :

- Use the command `python .\TheGame\main.py ` to start the game.You can configure the language in which the sound is emitted.

To run the manually controlled robot:- Connect a game controller to your computer.
- Run the `control_manette.py` program in the `ControlRobot` folder.


## Educational aspect of the game

The students can set the PID that allows the robot to move towards the marker. 

To do this, they must :

- Place the robot in front of the marker. It can be moved to the side.- Run the `setting_pi.py` program in the `PedagoTools` folder.
- Set the coefficients, press start and repeat ad infinitum until the PID is set correctly.

Translated with DeepL.com (free version)
