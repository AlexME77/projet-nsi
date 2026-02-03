from robot import Robot
import time
import RPi.GPIO as GPIO
GPIO.setwarnings(False)

def main():
    robot = Robot()
    robot.set_settings(40)

    try:
        while True:
            distance = robot.distance_obstacle()
            if distance < 20:
                robot.arret()
                time.sleep(1)
                robot.arriere()
                time.sleep(1)
                robot.droite()
                time.sleep(1)
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
#    main()
    while True:
        test = Robot()
        print(test.distance_obstacle())
        time.sleep(1)