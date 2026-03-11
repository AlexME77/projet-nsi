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

    robot = Robot()
    robot.set_settings(50)
    nom_parcours="test"

    #recupération du parcours depuis la base de données
    points_parcours = []
    for i in range(len(lire_destination(nom_parcours))): # à remplacer par la vraie valeur du nombre de points dans le parcours
        points_parcours.append(coord_destination(nom_parcours, ordre=i))

    try:
        navigation(robot, points_parcours)

    except KeyboardInterrupt:
        print("Arrêt du programme par l'utilisateur")
    
    finally:
        robot.arret()
        GPIO.cleanup()
        print("GPIO nettoyé et arrêt du robot")
        

if __name__ == "__main__":
    main()
