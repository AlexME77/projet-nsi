from robot import Robot
from controle.navigation_robot import *
import RPi.GPIO as GPIO
GPIO.setwarnings(False)
#from gps.gps import GPS

angle_actuel = 0

def main():
    robot = Robot()
    robot.set_settings(50)

    try:
        navigation(robot, get_angle_cible, get_distance_cible, get_angle_actuel)

    except KeyboardInterrupt:
        print("Arrêt du programme par l'utilisateur")
    
    finally:
        robot.arret()
        GPIO.cleanup()
        print("GPIO nettoyé et arrêt du robot")

if __name__ == "__main__":
    main()  
