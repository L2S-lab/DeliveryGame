# DeliveryGame

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