import time
import RPi.GPIO as GPIO

from robot import Robot
from controle.navigation_robot import NavigationRobot
from gps.gps import GPS
from gps.database import Database


def initialiser_systeme():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    robot = Robot()
    gps = GPS()
    db = Database()
    return robot, gps, db

def main():

    robot = None

    try:
        robot, gps, db = initialiser_systeme()

        commande = db.get_commande()
        action = commande['action'] if commande else None
        if action != "start":
            print("Aucune commande de démarrage trouvée, fin du service robot.")
            return

        try:
            nom_parcours = commande["nom_parcours"]
            if not nom_parcours:
                print("Nom de parcours manquant, arrêt.")
                return
            nav = NavigationRobot(robot, gps, db)
            points_parcours = db.get_points_parcours(nom_parcours)
            nav.navigation(points_parcours)
            
        except Exception as e:
            print(f"Erreur pendant la navigation : {e}")
        finally:
            db.set_commande("idle", None)
            print("Retour de la commande à l'état idle.")
            robot.arret()

    except KeyboardInterrupt:
        print("Arrêt manuel du service robot par l'utilisateur.")

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
