from robot import Robot
import time
import RPi.GPIO as GPIO
GPIO.setwarnings(False)

def eviter_obstacle(robot):
    robot.arret()
    time.sleep(1)
    robot.arriere()
    time.sleep(1)
    robot.droite()
    time.sleep(1)
    robot.avant()
    time.sleep(1)

def main():
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

if __name__ == "__main__":
    main()
