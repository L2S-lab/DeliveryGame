#import faulthandler
#faulthandler.enable()
try:
    from .connect import connect
    from .detection import remain_in_speed_bounds_x, remain_in_speed_bounds_y, delta_to_self, detect_ball, CAMERA_SCREEN_WIDTH, CAMERA_SCREEN_HEIGHT
    from .control_arm import set_default_state_gripper, catch, initiate_pos, drop_ball
    from .movement_marker import MarkerInfo
except ImportError:
    from connect import connect
    from detection import remain_in_speed_bounds_x, remain_in_speed_bounds_y, delta_to_self, detect_ball, CAMERA_SCREEN_WIDTH, CAMERA_SCREEN_HEIGHT
    from control_arm import set_default_state_gripper, catch, initiate_pos, drop_ball
    from movement_marker import MarkerInfo

from robomaster import led
import argparse, cv2
import time
from sys import exit

FREQUENCY = 10

class DeliveryRobot:
    def __init__(self, lang="fr", conn_type="ap", sn=None, nb_balls=2, silent=False):
        self.status = "WAITING"
        self.audio = lang
        self.conn_type = conn_type
        self.nb_balls = nb_balls
        self.sn = sn
        self.silent = silent
        if conn_type == "sta" and (self.sn is None or self.sn == ""):
            raise ValueError("Serial number is required for connection type 'sta'")
        self.ep_robot = connect(conn_type, sn)
        self.ep_led = self.ep_robot.led
        self.ep_camera = self.ep_robot.camera
        self.ep_gripper = self.ep_robot.gripper
        self.ep_arm = self.ep_robot.robotic_arm
        self.ep_chassis = self.ep_robot.chassis
        self.ep_vision = self.ep_robot.vision
        self.start_time = None
        self.time_pos = 0
        self.time_neg = 0
        self.total_angle = 0
        self.integral_x = 0
        self.integral_y = 0
        self.img = None
        self._kp_x, self._ki_x = 3.0 , 0.038
        self._kp_y, self._ki_y = 5.0, 0.038
        self.track_ball = True
        self.markers = []
        self.marker_info = None
        #Détecter si la balle est dans la pince
        #Les valeurs on été choisies empiriquement
        self.x_min = int(CAMERA_SCREEN_WIDTH * 0.38)  # Exclure 38% de la largeur de l'image du côté gauche
        self.x_max = int(CAMERA_SCREEN_WIDTH * 0.62)  # Exclure 38% de la largeur de l'image du côté droit 
        self.y_min = int(CAMERA_SCREEN_HEIGHT * 0.7) # Commencer à 70% de la hauteur de l'image
        self.y_max = int(CAMERA_SCREEN_HEIGHT)
        self.count = 0

    def __del__(self):
        self.close()

    @property
    def kp_x(self):
        return self._kp_x
    @kp_x.setter
    def kp_x(self, value):
        self._kp_x = value

    @property
    def ki_x(self):
        return self._ki_x
    @ki_x.setter
    def ki_x(self, value):
        self._ki_x = value

    @property
    def kp_y(self):
        return self._kp_y
    @kp_y.setter
    def kp_y(self, value):
        self._kp_y = value
    
    @property
    def ki_y(self):
        return self._ki_y
    @ki_y.setter
    def ki_y(self, value):
        self._ki_y = value

    def close(self):
        try:
            self.ep_camera.stop_video_stream()
        except Exception as e:
            print("Error stopping video stream", e)
        self.ep_robot.close()
        exit(0)

    def start(self):
        print("Starting the game")
        self.ep_camera.start_video_stream(display=False)
        if not self.silent and self.audio=="fr":self.ep_robot.play_audio(filename="TheGame/audio/francais/start.wav").wait_for_completed()
        if not self.silent and self.audio=="en":self.ep_robot.play_audio(filename="TheGame/audio/english/start.wav").wait_for_completed()
        self.ep_led.set_led(comp=led.COMP_BOTTOM_ALL, r=255, g=0, b=0, effect=led.EFFECT_ON)
        self.status = "SEARCHING"
        while True:
            print(f"{self.count=}")
            if self.count == self.nb_balls:
                break
            self.start_time = time.time()
            self.time_pos = 0
            self.time_neg = 0
            self.total_angle = 0
            self.integral_x = 0
            self.integral_y = 0

            if self.status == "SEARCHING":
                set_default_state_gripper(self.ep_gripper, self.ep_arm)
                if not self.silent and self.audio=="fr":self.ep_robot.play_audio(filename="TheGame/audio/francais/cherche.wav").wait_for_completed()
                if not self.silent and self.audio=="en":self.ep_robot.play_audio(filename="TheGame/audio/english/before_find.wav").wait_for_completed()
                self.ep_led.set_led(comp=led.COMP_BOTTOM_ALL, r=255, g=0, b=0, effect=led.EFFECT_BREATH)
                self.total_angle = self.search_ball()
                cv2.destroyAllWindows()
            if self.status == "FOUND":
                if not self.silent and self.audio=="fr":self.ep_robot.play_audio(filename="TheGame/audio/francais/go_to_ball.wav").wait_for_completed()
                self.ep_led.set_led(comp=led.COMP_BOTTOM_ALL, r=0, g=255, b=0, effect=led.EFFECT_ON)
                self.go_to_ball()
                cv2.destroyAllWindows()
            if self.status == "CATCHING":
                self.ep_led.set_led(comp=led.COMP_BOTTOM_ALL, r=0, g=255, b=0, effect=led.EFFECT_BREATH)
                catch(self.ep_gripper)
                initiate_pos(self.ep_arm)
                if not self.silent and self.audio=="fr":self.ep_robot.play_audio(filename="TheGame/audio/francais/go_to_box.wav").wait_for_completed()
                if not self.silent and self.audio=="en":self.ep_robot.play_audio(filename="TheGame/audio/english/go_to_box.wav").wait_for_completed()
                self.ep_led.set_led(comp=led.COMP_BOTTOM_ALL, r=255, g=0, b=0, effect=led.EFFECT_BREATH)
                #self.ep_chassis.move(z=self.total_angle, z_speed=60).wait_for_completed()
                self. ep_led.set_led(comp=led.COMP_BOTTOM_ALL, r=0, g=0, b=255, effect=led.EFFECT_ON)
                self.status = "DELIVERING"
            if self.status == "DELIVERING":
                self.go_to_marker()
                cv2.destroyAllWindows()
                if not self.silent and self.audio=="fr":self.ep_robot.play_audio(filename="TheGame/audio/francais/depose.wav").wait_for_completed()
                if not self.silent and self.audio=="en":self.ep_robot.play_audio(filename="TheGame/audio/english/delivery_completed.wav").wait_for_completed()
                self.ep_led.set_led(comp=led.COMP_BOTTOM_ALL, r=0, g=0, b=255, effect=led.EFFECT_BREATH)
                drop_ball(self.ep_gripper, self.ep_arm)
                self.ep_led.set_led(comp=led.COMP_BOTTOM_ALL, r=255, g=0, b=0, effect=led.EFFECT_ON)
                self.ep_chassis.move(x=-0.10, xy_speed=0.3).wait_for_completed()
                self.ep_chassis.move(z=180, z_speed=60).wait_for_completed()
                self.status = "SEARCHING"
                self.count += 1
                if not self.silent and self.audio=="fr":self.ep_robot.play_audio(filename="TheGame/audio/francais/finish.wav").wait_for_completed()
                if not self.silent and self.audio=="en":self.ep_robot.play_audio(filename="TheGame/audio/english/finish.wav").wait_for_completed()
        if not self.silent:self.ep_robot.play_audio(filename="TheGame/audio/Champions.wav").wait_for_completed()

    def search_ball(self):
        start_time = time.time()
        while True:
            try: 
                self.img = self.ep_camera.read_cv2_image(strategy="newest", timeout=3)
            except KeyboardInterrupt:
                cv2.destroyAllWindows()
                self.close()
                break
            except Exception as e:
                print("erreur connexion camera ", e)
                continue
            if self.img is not None:
                if self.status == "SEARCHING":
                    ball_on_screen, x, y, radius = detect_ball(self.img)
                    if ball_on_screen:
                        # Afficher un cercle à l'écran autour de la balle
                        cv2.circle(self.img, (int(x), int(y)), int(radius), (0,255,255), 2)
                        if x - CAMERA_SCREEN_WIDTH/2 >= 100:
                            self.turn()
                            self.time_pos += time.time() - self.start_time
                            self.start_time = time.time()
                        elif CAMERA_SCREEN_WIDTH/2 - x >= 100:
                            self.turn(-1)
                            self.time_neg += time.time() - self.start_time
                            self.start_time = time.time()
                        else:
                            time.sleep(0.1)
                            total_angle = 10 * (self.time_pos - self.time_neg)
                            self.status = "FOUND"
                            return total_angle
                    else:
                        self.turn()
                        self.time_pos += time.time() - self.start_time
                        self.start_time = time.time()
                    if self.status == "SEARCHING":
                        k = cv2.waitKey(1)
                        if k == ord('q'):
                            cv2.destroyAllWindows()
                            break
                        cv2.imshow("Searching for a ball", cv2.cvtColor(self.img, cv2.COLOR_BGR2HSV))
            time.sleep(0.05)
            if time.time() - start_time > 30:
                print("Je n'ai pas trouvé de balle, j'ai terminé")
                self.close()
                exit(1)
    
    def go_to_ball(self):
        self.track_ball = True
        count = 0
        while True:
            try: 
                self.img = self.ep_camera.read_cv2_image(strategy="newest", timeout=3)
            except KeyboardInterrupt:
                cv2.destroyAllWindows()
                self.close()
                break
            except Exception as e:
                print("erreur connexion camera ", e)
                continue
            if self.img is not None:
                height, width, _ = self.img.shape

                # Coordonnées du coin supérieur gauche et du coin inférieur droit du rectangle
                x1 = int(width * 0.38)  # Exclure 10% de la largeur de l'image du côté gauche
                x2 = int(width * 0.62)  # Exclure 10% de la largeur de l'image du côté droit
                y1 = int(height)  # Commencer à 80% de la hauteur de l'image
                y2 = int(height * 0.75)  # Monter jusqu'à 60% de la hauteur de l'image

                # Dessiner le rectangle sur l'image
                cv2.rectangle(self.img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                
                if self.track_ball:
                    ball_on_screen, x, y, radius = detect_ball(self.img)

                    if ball_on_screen:
                        count = self.on_detect_ball( x, y, radius, count)
                        # Afficher un cercle autour de la balle
                        cv2.circle(self.img, (int(x), int(y)), int(radius), (0,255,255), 2)
                        cv2.circle(self.img, (int(x), int(y)), 5, (255,0,0), 2)
                else:
                    self.status = "CATCHING"
                    break
                k = cv2.waitKey(1)
                if k == ord('q'):
                    cv2.destroyAllWindows()
                    break
                cv2.imshow("Detect a Tennis Ball", cv2.cvtColor(self.img, cv2.COLOR_BGR2HSV))  
            time.sleep(0.1)

    def go_to_marker(self):
        self.markers.clear()
        start_time = time.time()
        while len(self.markers)==0:
            self.ep_vision.sub_detect_info(name="marker", callback=self.on_detect_marker)
            #print("Je n'ai pas détecté de marqueur, j'avance")
            if len(self.markers)!=0:
                break
            elif time.time() - start_time <30:
                self.ep_chassis.drive_speed(z=20, timeout=0.5)
            else:
                print("Je n'ai pas détecté de marqueur,  j'ai terminé")
                self.close()
                exit(1)
            #else:
            #    self.ep_chassis.move(x=0.5, y=0, xy_speed=1).wait_for_completed()
            #    time.sleep(0.5)
            #    start_time = time.time()

        print("sortie du while, début du mvt")
        while True :
            info, x, y, w, h = self.markers[-1]._info, self.markers[-1]._x, self.markers[-1]._y, self.markers[-1]._w, self.markers[-1]._h
            try: 
                self.img = self.ep_camera.read_cv2_image(strategy="newest", timeout=3)
            except KeyboardInterrupt:
                cv2.destroyAllWindows()
                self.close()
                break
            except Exception as e:
                print("erreur connexion camera ", e)
                continue
            if self.img is not None:
                cv2.rectangle(self.img, self.markers[-1].pt1, self.markers[-1].pt2, (255, 255, 255))
                cv2.putText(self.img, self.markers[-1].text, self.markers[-1].center, cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 3)
                cv2.imshow("Markers", self.img)
                k = cv2.waitKey(1)
                if k == ord('q'):
                    cv2.destroyAllWindows()
                    break

                delta_x, delta_y = self.markers[-1].delta_to_self()
                #print(f"X  : {delta_x} et Y : {delta_y}")
                #print(f"X_center  : {x} et Y_center : {y}")
                error_x = delta_x - 0.45
                error_y = delta_y

                self.integral_x += error_x / FREQUENCY
                #derivative_x = (error_x - prev_error_x) * FREQUENCY
                output_x = self.kp_x * error_x + self.ki_x * self.integral_x 

                # Calculer les termes PI pour var_y
                self.integral_y += error_y / FREQUENCY
                #derivative_y = (error_y - prev_error_y) * FREQUENCY
                output_y = self.kp_y * error_y + self.ki_y * self.integral_y

                x_speed = remain_in_speed_bounds_x(output_x)
                y_speed = remain_in_speed_bounds_y(output_y)

                self.ep_chassis.drive_speed(x=x_speed, y=y_speed, z=0, timeout=1/FREQUENCY)

                if abs(error_x) < 0.1 and abs(error_y) < 0.07:
                    break
            time.sleep(0.1)
    
    def on_detect_marker(self, marker_info):
        number = len(marker_info)
        if number == 0:
            return
        for i in range(number):
            x, y, w, h, info = marker_info[i]
            self.marker_info = MarkerInfo(x, y, w, h, info)
            self.markers.append(self.marker_info)

    def on_detect_ball(self, x, y, radius, count):
        """Calcul du contrôleur PI à partir des données de la balle détectée"""
        var_x, var_y = delta_to_self(x, y, radius)
        error_x = var_x - 0.2    #Pour compenser des erreurs d'approximation
        error_y = var_y - 0      #Valeurs empiriques

        
        if self.x_min <= int(x) <= self.x_max and self.y_min <= int(y) <= self.y_max:
            self.ep_chassis.drive_speed(x=0, y=0, z=0, timeout=1/FREQUENCY)
            count += 1
            if count == 10:
                self.track_ball = False
        else:
            count = 0

            # Calculer les termes PI pour var_x
            self.integral_x += error_x / FREQUENCY
            #derivative_x = (error_x - prev_error_x) * FREQUENCY
            output_x = self.kp_x * error_x + self.ki_x * self.integral_x 

            # Calculer les termes PI pour var_y
            self.integral_y += error_y / FREQUENCY
            #derivative_y = (error_y - prev_error_y) * FREQUENCY
            output_y = self.kp_y * error_y + self.ki_y * self.integral_y

            x_speed = remain_in_speed_bounds_x(output_x)
            y_speed = remain_in_speed_bounds_y(output_y)
            # Appliquer la commande de contrôle
            self.ep_chassis.drive_speed(x=x_speed, y=y_speed, z=0, timeout=1/FREQUENCY)
        return count

    def turn(self, direction=1):
        if direction not in [1, -1]:
            direction = abs(direction)/direction
        self.ep_chassis.drive_speed(z=direction*10, timeout=0.5)






if __name__ == "__main__":
    #FOR A CONNECTION WITH WIFI, USE CONN_TYPE = "ap" and sn=None

    ######################################################################
    #audio parameters : "francais", "english" ou None
    parser = argparse.ArgumentParser(description='Select audio language.')
    parser.add_argument('--language', choices=['fr', 'en'], default='fr', help='Select audio language (fr or en)')
    parser.add_argument('--silent', action='store_true', help='Silent mode (no audio)')
    parser.add_argument('--conn_type', choices=['ap', 'sta'], default='ap', help='Select connection type (ap for direct connection or sta for connection through a router)')
    parser.add_argument('--nb_balls', type=int, default=1, help='Number of balls to deliver (default: 2), put -1 for infinite (not recommended)')
    parser.add_argument('--kp_x', type=float, default=3.0, help='Proportional gain for x')
    parser.add_argument('--ki_x', type=float, default=0.038, help='Integral gain for x')
    parser.add_argument('--kp_y', type=float, default=5.0, help='Proportional gain for y')
    parser.add_argument('--ki_y', type=float, default=0.038, help='Integral gain for y')
    args = parser.parse_args()
    audio = args.language
    conn_type = args.conn_type
    nb_balls = args.nb_balls
    silent = args.silent
    
    #test
    silent = True 
    nb_balls = -1
    conn_type = "ap"

    print("Silent mode: ", silent)
    game = DeliveryRobot(lang=audio, conn_type=conn_type, nb_balls=nb_balls, silent=silent)
    game.kp_x = args.kp_x
    game.ki_x = args.ki_x
    game.kp_y = args.kp_y
    game.ki_y = args.ki_y
    game.start()
    
    #test
    #game.search_ball()
    #game.go_to_ball()
    #game.go_to_marker()
    #atexit.register(game.close)
    game.close()
    










































    # for _ in range(nb_balls):

    #     STATUS = "SEARCHING"
    #     while True:
    #         try: 
    #             img = ep_camera.read_cv2_image(strategy="newest", timeout=3)
    #         except KeyboardInterrupt:
    #             ep_robot.camera.stop_video_stream()
    #             ep_robot.close()
    #             cv2.destroyAllWindows()
    #             break
    #         except Exception as e:
    #             print("erreur connexion camera ", e)
    #             continue
    #         k = cv2.waitKey(1)
    #         if k == ord('q'):
    #             ep_robot.camera.stop_video_stream()
    #             ep_robot.close()
    #             cv2.destroyAllWindows()
    #             break
    #         if img is not None:
    #             if STATUS == "SEARCHING":
    #                 ball_on_screen, x, y, radius, _ = detect_ball(img)
    #                 if ball_on_screen:
    #                     # Afficher un cercle à l'écran autour de la balle
    #                     cv2.circle(img, (int(x), int(y)), int(radius), (0,255,255), 2)
    #                     if x - CAMERA_SCREEN_WIDTH/2 >= 100:
    #                         turn(ep_robot)
    #                         time_pos += time.time() - start_time
    #                         start_time = time.time()
    #                     elif CAMERA_SCREEN_WIDTH/2 - x >= 100:
    #                         turn(ep_robot, -1)
    #                         time_neg += time.time() - start_time
    #                         start_time = time.time()
    #                     else:
    #                         cv2.destroyAllWindows()
    #                         time.sleep(0.5)
    #                         total_angle = 10 * (time_pos - time_neg)
    #                         STATUS = "FOUND"
    #                 else:
    #                     turn(ep_robot)
    #                     time_pos += time.time() - start_time
    #                     start_time = time.time()
    #                 if STATUS == "SEARCHING":
    #                     cv2.imshow("Searching for a ball", img)
                
    #             elif STATUS == "FOUND":
    #                 print("Ball found")
    #                 #break
    #                 #if audio=="fr":ep_robot.play_audio(filename="TheGame/audio/francais/go_to_ball.wav").wait_for_completed()
    #                 ep_led.set_led(comp=led.COMP_BOTTOM_ALL, r=0, g=255, b=0, effect=led.EFFECT_ON)
    #                 reached = go_to_ball(img, ep_robot)
    #                 if not reached:
    #                     cv2.destroyAllWindows()
        
        
        # ep_led.set_led(comp=led.COMP_BOTTOM_ALL, r=0, g=255, b=0, effect=led.EFFECT_BREATH)
        # catch(ep_robot)
        # initiate_pos(ep_robot)
        # #if audio=="en":ep_robot.play_audio(filename="TheGame/audio/english/got_the_ball.wav").wait_for_completed()
        # #if audio=="fr":ep_robot.play_audio(filename="TheGame/audio/francais/go_to_box.wav").wait_for_completed()
        # ep_led.set_led(comp=led.COMP_BOTTOM_ALL, r=255, g=0, b=0, effect=led.EFFECT_BREATH)
        # ep_chassis.move(z=180+total_angle, z_speed=60).wait_for_completed()
        # ep_led.set_led(comp=led.COMP_BOTTOM_ALL, r=0, g=0, b=255, effect=led.EFFECT_ON)
        # go_to_marker(ep_robot)
        # #if audio=="fr":ep_robot.play_audio(filename="TheGame/audio/francais/depose.wav").wait_for_completed()
        # #if audio=="en":ep_robot.play_audio(filename="TheGame/audio/english/delivery_completed.wav").wait_for_completed()
# 
        # ep_led.set_led(comp=led.COMP_BOTTOM_ALL, r=0, g=0, b=255, effect=led.EFFECT_BREATH)
        # drop_ball(ep_robot)
        # ep_led.set_led(comp=led.COMP_BOTTOM_ALL, r=255, g=0, b=0, effect=led.EFFECT_ON)
        # ep_chassis.move(x=-0.10, xy_speed=0.3).wait_for_completed()
        # ep_chassis.move(z=180, z_speed=60).wait_for_completed()
        # 
    #if audio=="fr":ep_robot.play_audio(filename="TheGame/audio/francais/finish.wav").wait_for_completed()
    #if audio=="en":ep_robot.play_audio(filename="TheGame/audio/english/finish.wav").wait_for_completed()

    #Dance : 
    #if audio=="en" or audio=="fr":ep_robot.play_audio(filename="TheGame/audio/Champions.wav").wait_for_completed()

    #for _ in range(2):
    #    ep_chassis.move(z=-30, z_speed=150).wait_for_completed()
    #    ep_chassis.move(z=30, z_speed=150).wait_for_completed()

    # ep_robot.camera.stop_video_stream()
    # ep_robot.close()
