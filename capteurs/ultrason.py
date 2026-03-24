import RPi.GPIO as GPIO
import time

class CapteurUltrason:

    def __init__(self, trig=2, echo=3):
        self.trig = trig
        self.echo = echo

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.trig, GPIO.OUT)
        GPIO.setup(self.echo, GPIO.IN)

    def mesurer_distance(self):
        GPIO.output(self.trig, True)
        time.sleep(0.00001)
        GPIO.output(self.trig, False)

        start = time.time()
        stop = time.time()

        timeout = time.time() + 0.02  # 20 ms max
        while GPIO.input(self.echo) == 0:
            start = time.time()
            if start > timeout:
                return None  # erreur

        timeout = time.time() + 0.02  # 20 ms max
        while GPIO.input(self.echo) == 1:
            start = time.time()
            if start > timeout:
                return None  # erreur

        duree = stop - start
        distance = (duree * 34300) / 2
        return distance
