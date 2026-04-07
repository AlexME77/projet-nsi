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
    robot.set_settings(100)

    gps = GPS()
    db = Database()

    nav = NavigationRobot(robot, gps, db)

    return robot, gps, db, nav


def boucle_principale():
    robot = None

    try:
        robot, gps, db, nav = initialiser_systeme()
        print("Service robot prêt. En attente de commande...")

        while True:
            commande = db.get_commande()

            if commande is None:
                print("Aucune commande trouvée dans la base.")
                time.sleep(1)
                continue

            action = commande["action"]
            nom_parcours = commande["nom_parcours"]

            if action == "start":
                print(f"Commande START reçue pour le parcours : {nom_parcours}")

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

            elif action == "stop":
                print("Commande STOP reçue.")
                try:
                    robot.arret()
                except Exception as e:
                    print(f"Erreur lors de l'arrêt du robot : {e}")
                finally:
                    db.set_commande("idle", None)
                    print("Robot arrêté. Retour à l'état idle.")

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
    boucle_principale()