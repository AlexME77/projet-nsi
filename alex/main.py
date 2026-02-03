from robot import Robot
import time

def main():
    robot = Robot()
    robot.set_settings(40)

    while True:
        robot.avant()
        time.sleep(1)

if __name__ == "__main__":
    main()