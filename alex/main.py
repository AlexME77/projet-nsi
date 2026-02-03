from robot import Robot
import time

def main():
    robot = Robot()
    robot.set_settings(40)

    while True:
        distance = robot.distance_obstacle()
        if distance < 20:
            robot.arret()
            time.sleep(1)
            robot.recule()
            time.sleep(1)
            robot.droite()
            time.sleep(1)
        else:
            robot.avant()
            time.sleep(1)
        time.sleep(0.1)

if __name__ == "__main__":
    main()