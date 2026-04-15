# Réalisé par : Alexandre Mai--Emery
import RPi.GPIO as GPIO
import time

class CapteurUltrason:

    def __init__(self, TRIG=3, ECHO=4):
        print("Initialisation du capteur ultrason")
        self.trig = TRIG
        self.echo = ECHO
        GPIO.setup(self.trig, GPIO.OUT)
        GPIO.setup(self.echo, GPIO.IN)
 
    def mesurer_distance(self):
        '''
        Mesure la distance à l'obstacle en utilisant le capteur ultrason
        Retourne la distance en centimètres ou None en cas d'erreur de mesure
        '''
        
        print("Mesure de la distance à l'obstacle")
        
        # Envoi d'une impulsion ultrason
        GPIO.output(self.trig, True)
        time.sleep(0.00001)
        GPIO.output(self.trig, False)
    
        # Attente du début de l'impulsion
        timeout = time.time() + 0.02 
        while GPIO.input(self.echo) == 0:
            if time.time() > timeout:
                return None 
        start = time.time()
    
        # Attente du retour de l'impulsion
        timeout = time.time() + 0.02
        while GPIO.input(self.echo) == 1:
            if time.time() > timeout:
                return None 
        end = time.time()

        # Calcul de la distance en fonction du temps écoulé (différence entre le début et la fin de l'impulsion)
        duree = end - start
        distance = (duree * 34300) / 2
    
        return distance
