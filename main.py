from robot import Robot
from controle.navigation_robot import *
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

def main(nom_parcours):

    print("Initialisation du robot...")
    robot = Robot()
    robot.set_settings(100)

    try:
        print("Récupération des coordonnées du parcours...")
        points_parcours = coord_destination(nom_parcours)
        print("Démarrage de la navigation...")
        navigation(robot, points_parcours)

    except KeyboardInterrupt:
        print("Arrêt du programme par l'utilisateur")
    
    finally:
        robot.arret()
        print("Arrêt du robot")
        GPIO.cleanup()
        print("GPIO nettoyé")

if __name__ == "__main__":
    main("test")
