import time
import RPi.GPIO as GPIO

from robot import Robot
from controle.navigation_robot import NavigationRobot
from gps.gps import GPS
from gps.database import Database


def initialiser_systeme():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    print("Initialisation du robot...")
    robot = Robot()
    gps = GPS()
    db = Database()
    return robot, gps, db

def main():
    
    robot = None

    try:
        robot, gps, db = initialiser_systeme()
        nav = NavigationRobot(robot, gps, db)
        print("Service robot prêt. En attente de commande...")
        
        commande = db.get_commande()
        action = commande['action'] if commande else None
        if action != "start":
            print("Aucun parcours à lancer")
            return

            while True:
                nom_parcours = commande["nom_parcours"]
                try:
                    points_parcours = db.get_points_parcours(nom_parcours)
                    print("Démarrage de la navigation...")
                    nav.navigation(points_parcours)
                    print("Navigation terminée.")
                except Exception as e:
                    print(f"Erreur pendant la navigation : {e}")
                finally:
                    db.set_commande("idle", None)
                    print("Retour à l'état idle.")
                    robot.arret()
                    print("Robot arrêté.")
                time.sleep(0.5)

    except KeyboardInterrupt:
        print("Arrêt manuel du service robot.")

    except Exception as e:
        print(f"Erreur fatale : {e}")
        raise

    finally:
        if robot is not None:
            try:
                robot.cleanup()
            except Exception:
                pass

        GPIO.cleanup()
        print("GPIO nettoyé.")


if __name__ == "__main__":
    main()
