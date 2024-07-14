from connect import connect
from detection import go_to_ball
from search_ball import turn_till_detect_ball
from control_arm import set_default_state_gripper, catch, initiate_pos, drop_ball
from movement_marker import go_to_marker
from robomaster import led
import argparse


if __name__ == "__main__":
    #FOR A CONNECTION WITH WIFI, USE CONN_TYPE = "ap" and sn=None
    sn = None
    ######################################################################
    #audio parameters : "francais", "english" ou None
    parser = argparse.ArgumentParser(description='Select audio language.')
    parser.add_argument('--language', choices=['fr', 'en'], default='fr', help='Select audio language (fr or en)')
    parser.add_argument('--conn_type', choices=['ap', 'sta'], default='ap', help='Select connection type (ap for direct connection or sta for connection through a router)')
    parser.add_argument('--nb_balls', type=int, default=2, help='Number of balls to deliver (default: 2), put -1 for infinite (not recommended)')
    args = parser.parse_args()
    audio = args.language
    conn_type = args.conn_type
    nb_balls = args.nb_balls
    if conn_type == "sta":
        sn = input("Enter the serial number of your robot: ")
        if sn is None:
            raise ValueError("Serial number is required for connection type 'sta'")
    ######################################################################
    ep_robot = connect(conn_type, sn)
    ep_robot.camera.start_video_stream(display=False)
    if audio=="fr":ep_robot.play_audio(filename="TheGame/audio/francais/start.wav").wait_for_completed()
    if audio=="en":ep_robot.play_audio(filename="TheGame/audio/english/start.wav").wait_for_completed()

    ep_led = ep_robot.led

    for _ in range(nb_balls):
        if audio=="fr":ep_robot.play_audio(filename="TheGame/audio/francais/position.wav").wait_for_completed()
        ep_led.set_led(comp=led.COMP_BOTTOM_ALL, r=255, g=0, b=0, effect=led.EFFECT_ON)
        set_default_state_gripper(ep_robot)
        if audio=="fr":ep_robot.play_audio(filename="TheGame/audio/francais/cherche.wav").wait_for_completed()
        if audio=="en":ep_robot.play_audio(filename="TheGame/audio/english/before_find.wav").wait_for_completed()
        ep_led.set_led(comp=led.COMP_BOTTOM_ALL, r=255, g=0, b=0, effect=led.EFFECT_BREATH)
        total_angle = turn_till_detect_ball(ep_robot)
        if audio=="fr":ep_robot.play_audio(filename="TheGame/audio/francais/go_to_ball.wav").wait_for_completed()
        ep_led.set_led(comp=led.COMP_BOTTOM_ALL, r=0, g=255, b=0, effect=led.EFFECT_ON)
        go_to_ball(ep_robot)
        ep_led.set_led(comp=led.COMP_BOTTOM_ALL, r=0, g=255, b=0, effect=led.EFFECT_BREATH)
        catch(ep_robot)
        initiate_pos(ep_robot)
        if audio=="en":ep_robot.play_audio(filename="TheGame/audio/english/got_the_ball.wav").wait_for_completed()
        if audio=="fr":ep_robot.play_audio(filename="TheGame/audio/francais/go_to_box.wav").wait_for_completed()
        ep_led.set_led(comp=led.COMP_BOTTOM_ALL, r=255, g=0, b=0, effect=led.EFFECT_BREATH)
        ep_robot.chassis.move(z=180+total_angle, z_speed=60).wait_for_completed()
        ep_led.set_led(comp=led.COMP_BOTTOM_ALL, r=0, g=0, b=255, effect=led.EFFECT_ON)
        go_to_marker(ep_robot)
        if audio=="fr":ep_robot.play_audio(filename="TheGame/audio/francais/depose.wav").wait_for_completed()
        if audio=="en":ep_robot.play_audio(filename="TheGame/audio/english/delivery_completed.wav").wait_for_completed()

        ep_led.set_led(comp=led.COMP_BOTTOM_ALL, r=0, g=0, b=255, effect=led.EFFECT_BREATH)
        drop_ball(ep_robot)
        ep_led.set_led(comp=led.COMP_BOTTOM_ALL, r=255, g=0, b=0, effect=led.EFFECT_ON)
        ep_robot.chassis.move(x=-0.10, xy_speed=0.3).wait_for_completed()
        ep_robot.chassis.move(z=180, z_speed=60).wait_for_completed()
        
    if audio=="fr":ep_robot.play_audio(filename="TheGame/audio/francais/finish.wav").wait_for_completed()
    if audio=="en":ep_robot.play_audio(filename="TheGame/audio/english/finish.wav").wait_for_completed()

    #Dance : 
    if audio=="en" or audio=="fr":ep_robot.play_audio(filename="TheGame/audio/Champions.wav").wait_for_completed()

    for _ in range(nb_balls):
        ep_robot.chassis.move(z=-30, z_speed=150).wait_for_completed()
        ep_robot.chassis.move(z=30, z_speed=150).wait_for_completed()

    ep_robot.camera.stop_video_stream()
    ep_robot.close()
