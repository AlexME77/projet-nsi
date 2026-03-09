from robot import Robot
from controle.navigation_robot import *
import RPi.GPIO as GPIO
GPIO.setwarnings(False)
#from gps.gps import GPS


angle_actuel = 0
distance_cible = 10

def get_angle_cible():
    return 90

def get_distance_cible():
    global distance_cible
    distance_cible -= 0.1
    return distance_cible

def get_angle_actuel():
    global angle_actuel
    return angle_actuel

def main():
    robot = Robot()
    robot.set_settings(60)

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
