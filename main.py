from robot import Robot
from controle.navigation_robot import *
import RPi.GPIO as GPIO
GPIO.setwarnings(False)
import serial
import serial.tools.list_ports
from gps.gps import GPS
from gps.database import coord_destination
import time

def main(nom_parcours):

    robot = Robot()
    robot.set_settings(50)

    #recupération du parcours depuis la base de données

    try:
        navigation(robot, nom_parcours=nom_parcours)

    except KeyboardInterrupt:
        print("Arrêt du programme par l'utilisateur")
    
    finally:
        robot.arret()
        print("Arrêt du robot")
        GPIO.cleanup()
        print("GPIO nettoyé")

if __name__ == "__main__":
    main("test")
