import cv2, time
from detection import detect_ball, CAMERA_SCREEN_WIDTH

def turn(ep_robot, direction=1):
    if direction not in [1, -1]:
        direction = abs(direction)/direction
    ep_robot.chassis.drive_speed(z=direction*10, timeout=0.5)

def turn_till_detect_ball(ep_robot):
    """Fait tourner le robot sur lui-même jusqu'à détecter une balle et renvoie l'angle de rotation total du robot"""
    ep_camera = ep_robot.camera
    start_time = time.time()
    time_pos = 0
    time_neg = 0
    while True:
        try:
            img = ep_camera.read_cv2_image(strategy="newest", timeout=3)
            cv2.waitKey(10)
        except Exception as e:
            print("erreur connexion camera", e)
            continue
        
        ball_on_screen, x, y, radius, _ = detect_ball(img)
        if ball_on_screen:
            # Afficher un cercle à l'écran autour de la balle
            cv2.circle(img, (int(x), int(y)), int(radius), (0,255,255), 2)
            cv2.imshow("Searching for a ball", img)
            
            if x - CAMERA_SCREEN_WIDTH/2 >= 100:
                turn(ep_robot)
                time_pos += time.time() - start_time
                start_time = time.time()
            elif CAMERA_SCREEN_WIDTH/2 - x >= 100:
                turn(ep_robot, -1)
                time_neg += time.time() - start_time
                start_time = time.time()
            else:
                break
        else:
            turn(ep_robot)
            time_pos += time.time() - start_time
            start_time = time.time()
    end_time = time.time()

    cv2.destroyAllWindows()
    time.sleep(0.5)
    time.sleep(0.1)
    return 10 * (time_pos - time_neg)
