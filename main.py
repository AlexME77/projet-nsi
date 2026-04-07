from robot import Robot
from controle.navigation_robot import NavigationRobot
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
from gps.gps import GPS
from gps.database import Database

def main():
    
    print("Initialisation du robot...")
    robot = Robot()
    robot.set_settings(100)

    gps = GPS()

    db = Database()

    try:
        nav = NavigationRobot(robot, gps, db)
    except RuntimeError as e:
        print(e)
        robot.cleanup()
        GPIO.cleanup()
        return

    commande = db.get_commande()
    action = commande[0] if commande else None
    if action != "start":
        print("Aucun parcours à lancer")
        return

    try:
        print("Récupération des coordonnées du parcours...")
        points_parcours = db.coord_destination()
        print("Démarrage de la navigation...")
        nav.navigation(points_parcours)

    except KeyboardInterrupt:
        print("Arrêt du programme par l'utilisateur")
    
    finally:
        robot.cleanup()
        GPIO.cleanup()
        print("GPIO nettoyé")

if __name__ == "__main__":
    main()