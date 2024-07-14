# DeliveryGame

## Requirements

### Windows

- Python 3.8 only
- Download Python3.8 from Microsoft windows store.
- Open windows powershell and run following line by line
```
git clone https://github.com/L2S-lab/DeliveryGame.git
cd DeliveryGame
python3.8 -m venv .venv 
.\.venv\Scripts\activate 
pip install -r requirements.txt
```
- For error in activating venv, excecute the following
```
# Secure but annoying way, need to run on each terminal
Set-ExecutionPolicy Unrestricted -Scope Process

# Not so secure way but onnly need to run once for user
Set-ExecutionPolicy Unrestricted -Force -Scope CurrentUser
```

### Linux

- For Python 3 only,
```
sudo apt install python3-venv libopus-dev -y
git clone https://github.com/L2S-lab/DeliveryGame.git
cd DeliveryGame
python3 -m venv .venv
source .venv/bin/activate
pip install git+https://github.com/aarsht7/RoboMaster-SDK.git@master
pip install git+https://github.com/aarsht7/RoboMaster-SDK.git@libmedia_codec
pip install -r requirements.txt
```
### MacOs

Haven't tried on MacOS but follow the linux version. It should be something similar.

If you try on Mac, please report any error or feedback.


## Goal of the game

This is a delivery game between a DJI ROBOMASTER EP robot controlled manually by a person (keyboard or joystick) and a DJI ROBOMASTER EP robot controlled automatically using a Python code. The aim is to retrieve two tennis balls and return them to a basket.

### Setting up the game

The hardware required to set up the game is as follows:

- 2 DJI ROBOMASTER EP
- 4 tennis balls
- 2 baskets: cardboard boxes will do
- DJI markers
- two computers
- une manette 8-bitdo sn30 pro

Each robot must face two tennis balls and behind the robot must be the cardboard box with the marker. 

Diagram of how to set up the game :   

![Schéma jeu](https://github.com/comoxx/DeliveryGame/assets/93337725/c95afe61-1f57-4ff4-9317-bffa23e5b58d)


To connect to the robots : 

- Turn on the robots, then set the connection switch to direct mode (icon with the telephone).
- Connect to the robot's WIFI on your computer
- The password can be found on the robot label

To operate the automatically controlled robot :

- Use the command `python .\TheGame\main.py ` to start the game.You can configure the language in which the sound is emitted.

To run the manually controlled robot:
- Connect a game controller to your computer.
- Run the `control_manette.py` program in the `ControlRobot` folder.


### Educational aspect of the game

The students can set the PID that allows the robot to move towards the marker. 

To do this, they must :

- Place the robot in front of the marker. It can be moved to the side.
- Run the `setting_pi.py` program in the `PedagoTools` folder.
- Set the coefficients, press start and repeat ad infinitum until the PID is set correctly.
