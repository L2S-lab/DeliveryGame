from connect import connect
from detection import go_to_ball
from search_ball import turn_till_detect_ball
from control_arm import set_default_state_gripper, catch, initiate_pos, drop_ball
from movement_marker import go_to_marker
from robomaster import led


if __name__ == "__main__":
    #FOR A CONNECTION WITH WIFI, USE CONN_TYPE = "ap" and sn=None
    conn_type = "ap"
    sn = None
    ######################################################################
    #audio parameters : "francais", "english" ou None
    audio = "francais"
    ######################################################################
    ep_robot = connect(conn_type, sn)
    ep_robot.camera.start_video_stream(display=False)
    if audio=="francais":ep_robot.play_audio(filename="TheGame/audio/francais/start.wav").wait_for_completed()
    if audio=="english":ep_robot.play_audio(filename="TheGame/audio/english/start.wav").wait_for_completed()

    ep_led = ep_robot.led

    for _ in range(2):
        print("Début de la boucle")
        if audio=="francais":ep_robot.play_audio(filename="TheGame/audio/francais/position.wav").wait_for_completed()
        ep_led.set_led(comp=led.COMP_BOTTOM_ALL, r=255, g=0, b=0, effect=led.EFFECT_ON)
        set_default_state_gripper(ep_robot)
        print("Fin de l'initialisation de la position du bras robotique")
        if audio=="francais":ep_robot.play_audio(filename="TheGame/audio/francais/cherche.wav").wait_for_completed()
        if audio=="english":ep_robot.play_audio(filename="TheGame/audio/english/before_find.wav").wait_for_completed()
        ep_led.set_led(comp=led.COMP_BOTTOM_ALL, r=255, g=0, b=0, effect=led.EFFECT_BREATH)
        total_angle = turn_till_detect_ball(ep_robot)
        print("Balle détectée !")
        if audio=="francais":ep_robot.play_audio(filename="TheGame/audio/francais/go_to_ball.wav").wait_for_completed()
        ep_led.set_led(comp=led.COMP_BOTTOM_ALL, r=0, g=255, b=0, effect=led.EFFECT_ON)
        go_to_ball(ep_robot)
        print("Fin du déplacement jusqu'à la balle")
        ep_led.set_led(comp=led.COMP_BOTTOM_ALL, r=0, g=255, b=0, effect=led.EFFECT_BREATH)
        catch(ep_robot)
        print("Attrappé la balle")
        initiate_pos(ep_robot)
        print(total_angle)
        if audio=="english":ep_robot.play_audio(filename="TheGame/audio/english/got_the_ball.wav").wait_for_completed()
        if audio=="francais":ep_robot.play_audio(filename="TheGame/audio/francais/go_to_box.wav").wait_for_completed()
        ep_led.set_led(comp=led.COMP_BOTTOM_ALL, r=255, g=0, b=0, effect=led.EFFECT_BREATH)
        ep_robot.chassis.move(z=180+total_angle, z_speed=60).wait_for_completed()
        print("Entrée dans go_to_marker")
        ep_led.set_led(comp=led.COMP_BOTTOM_ALL, r=0, g=0, b=255, effect=led.EFFECT_ON)
        go_to_marker(ep_robot)
        print("sortie de go to marker")
        if audio=="francais":ep_robot.play_audio(filename="TheGame/audio/francais/depose.wav").wait_for_completed()
        if audio=="english":ep_robot.play_audio(filename="TheGame/audio/english/delivery_completed.wav").wait_for_completed()

        ep_led.set_led(comp=led.COMP_BOTTOM_ALL, r=0, g=0, b=255, effect=led.EFFECT_BREATH)
        drop_ball(ep_robot)
        ep_led.set_led(comp=led.COMP_BOTTOM_ALL, r=255, g=0, b=0, effect=led.EFFECT_ON)
        ep_robot.chassis.move(x=-0.10, xy_speed=0.3).wait_for_completed()
        ep_robot.chassis.move(z=180, z_speed=60).wait_for_completed()
        print("Fin de la boucle")

    if audio=="francais":ep_robot.play_audio(filename="TheGame/audio/francais/finish.wav").wait_for_completed()
    if audio=="english":ep_robot.play_audio(filename="TheGame/audio/english/finish.wav").wait_for_completed()

    #Dance : 
    # if audio=="english" or audio=="francais":ep_robot.play_audio(filename="TheGame/audio/Champions.wav").wait_for_completed()

    for _ in range(2):
        ep_robot.chassis.move(z=-30, z_speed=150).wait_for_completed()
        ep_robot.chassis.move(z=30, z_speed=150).wait_for_completed()

    ep_robot.camera.stop_video_stream()
    ep_robot.close()
