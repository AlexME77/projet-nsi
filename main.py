from robot import Robot
from controle.navigation_robot import *
import RPi.GPIO as GPIO
GPIO.setwarnings(False)
import serial
import serial.tools.list_ports
from gps.gps import GPS
from gps.database import lire_destination
import time

def main():
    ordre = 1
    seuil = 2.0
    
    robot = Robot()
    robot.set_settings(50)

    try:
        navigation(robot, angle_cible, distance_cible, angle_actuel)

    except KeyboardInterrupt:
        print("Arrêt du programme par l'utilisateur")
    
    finally:
        robot.arret()
        GPIO.cleanup()
        print("GPIO nettoyé et arrêt du robot")
        

if __name__ == "__main__":
    main()
