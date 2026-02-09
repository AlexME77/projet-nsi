from robot import Robot
from controle.navigation_robot import navigation
import RPi.GPIO as GPIO
GPIO.setwarnings(False)
from gps.gps import GPS
import time


angle_actuel = 0
distance_cible = 10

def get_angle_cible():
    return 90

def get_distance_cible():
    global distance_cible
    distance_cible -= 0.1
    return distance_cible

def eviter_obstacle(robot):
    robot.arret()
    time.sleep(1)
    robot.arriere()
    time.sleep(1)
    robot.droite()
    time.sleep(1)
    robot.avant()
    time.sleep(1)

def main_temporaire():
    robot = Robot()
    distance_seuil=10
    vitesse=40
    robot.set_settings(vitesse)
    

    try:
        while True:
            distance = robot.distance_obstacle()
            if distance < distance_seuil:
                eviter_obstacle(robot)
            else:
                robot.avant()
                time.sleep(1)
            time.sleep(0.1)
    
    except KeyboardInterrupt:
        print("Arrêt du programme par l'utilisateur")
    
    finally:
        robot.arret()
        GPIO.cleanup()
        print("GPIO nettoyé et arrêt du robot")

def main():
    robot = Robot()
    robot.set_settings(40)

    try:
        navigation(robot, get_angle_cible, get_distance_cible, angle_actuel)

    except KeyboardInterrupt:
        print("Arrêt du programme par l'utilisateur")
    
    finally:
        robot.arret()
        GPIO.cleanup()
        print("GPIO nettoyé et arrêt du robot")

if __name__ == "__main__":
    main()  