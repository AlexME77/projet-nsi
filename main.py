# Réalisé par : Alexandre Mai--Emery, Mickaël Mai--Emery
import RPi.GPIO as GPIO

from robot import Robot
from navigation_robot import NavigationRobot
from gps import GPS
from database import Database


def initialiser_systeme():
    '''
    Initialise le système en configurant les GPIO, en créant les instances de Robot, GPS et Database
    Retourne les instances créées

    Réalisé par : Alexandre Mai--Emery
    '''
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    robot = Robot()
    gps = GPS()
    db = Database()
    return robot, gps, db

def main():

    # Alexandre : Initialisation du système
    robot = None

    try:
        robot, gps, db = initialiser_systeme()

        # Mickaël : Récupération de la commande dans la base de données
        commande = db.get_commande()
        action = commande['action'] if commande else None
        if action != "start":
            print("Aucune commande de démarrage trouvée, fin du service robot.")
            return

        # Alexandre et Mickaël : Navigation vers les points du parcours
        try:
            nom_parcours = commande["nom_parcours"]
            if not nom_parcours:
                raise ValueError("Nom de parcours manquant")
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
