import math
import serial
import serial.tools.list_ports
import time

class GPS:
    """
    Gère la communication avec le module GPS et effectue
    les calculs de distance et d'orientation.
    """
    def __init__(self):
        """
        Initialise le module GPS en recherchant automatiquement le port série disponible.
        
        raise RuntimeError : Si aucun module GPS n'est détecté.
        """
        print("Initialisation du GPS")
        self.gps_serial = self.port()
        if self.gps_serial is None:
            raise RuntimeError("GPS non disponible")

    def convertir_ddmm(self, valeur, orientation):
        """
        Convertit les coordonnées du format NMEA (DDMM.MMMM) en degrés décimaux.
        
        Exemple: 4850.5000 N -> 48.841666
        paramètre valeur : Chaîne de caractères de la coordonnée brute.
        paramètre orientation : 'N', 'S', 'E' ou 'W'.
        return : Float représentant la coordonnée en degrés décimaux.
        """
        print("Conversion de la coordonnée")
        valeur = float(valeur)
        degres = int(valeur // 100)
        minutes = valeur - degres * 100
        coord = degres + minutes / 60
        
        # Inversion pour le Sud ou l'Ouest
        if orientation in ['S', 'W']:
            coord = -coord
        return coord

    def extraire_position_GPGGA(self, trame):
        """
        Analyse une trame NMEA de type $GPGGA pour extraire la position.
        
        paramètre trame : La ligne de texte brute lue sur le port série.
        return : Tuple (latitude, longitude) ou None si le signal est invalide.
        """
        print("Extraction de la position")
        champs = trame.split(",")
        # Signal invalide
        if champs[6] == "0":
            return None
        latitude = self.convertir_ddmm(champs[2], champs[3])
        longitude = self.convertir_ddmm(champs[4], champs[5])
        return latitude, longitude
    
    def get_position_robot(self, timeout = 10):
        """
        Lit les données série jusqu'à trouver une trame GPGGA valide.
        
        paramètre timeout : Temps maximum d'attente en secondes.
        return : Tuple (lat, lon) ou None si expiration du délai.
        """
        print("Récupération de la position du robot")
        start_time = time.time()

        while time.time() - start_time < timeout:
            trame = self.gps_serial.readline().decode("ascii", errors="ignore").strip()
            if trame.startswith("$GPGGA"):
                print("Trame GPGGA : ", trame)
                position = self.extraire_position_GPGGA(trame)
                if position:
                    return position
        print("Aucune trame GPGGA valide reçue dans le délai imparti, position GPS non disponible")
        return None

    def distance_2pGPS(self, coord1, coord2):
        """
        Calcule la distance en mètres entre deux points GPS.
        
        paramètre coord1 : Tuple (lat, lon) du point A.
        paramètre coord2 : Tuple (lat, lon) du point B.
        return : Distance en mètres.
        """
        print(f"Calcule la distance 2pGPS entre {coord1} et {coord2}")
        la1 = math.radians(coord1[0])
        la2 = math.radians(coord2[0])
        lon1 = math.radians(coord1[1])
        lon2 = math.radians(coord2[1])
        valeur = (
        math.sin(la1) * math.sin(la2) +
        math.cos(la1) * math.cos(la2) * math.cos(lon1 - lon2)
        )
        valeur = max(-1.0, min(1.0, valeur))
        dis = 6371009 * math.acos(valeur)
        return dis

    def get_orientation(self, coord1, coord2):
        """
        Calcule l'angle par rapport au Nord pour aller du point 1 au point 2.
        
        paramètre coord1 : Tuple (lat, lon) de départ.
        paramètre coord2 : Tuple (lat, lon) d'arrivée.
        return : Angle en degrés entre 0 et 360 (0 = Nord).
        """
        print(f"Calcule l'orientation entre {coord1} et {coord2}")
        la1 = math.radians(coord1[0])
        la2 = math.radians(coord2[0])
        lon1 = math.radians(coord1[1])
        lon2 = math.radians(coord2[1])

        longDelta = lon2 - lon1
        y = math.sin(longDelta) * math.cos(la2)
        x = math.cos(la1) * math.sin(la2) - math.sin(la1) * math.cos(la2) * math.cos(longDelta)

        angle = math.atan2(y, x) * 360 / (2 * math.pi)
        while angle < 0:
            angle += 360

        direction = angle % 360
        return direction
    
    def port(self):
        """
        Détecte automatiquement le port série utilisé par le module GPS.
        
        return : Objet serial.Serial configuré, ou None si aucun port trouvé.
        """
        print("Recherche du port GPS")
        ports = list(serial.tools.list_ports.comports())
        if not ports:
            print("Aucun GPS détecté")
            return None
        port = ports[0].device
        print("Port GPS trouvé :", port)
        gps_serial = serial.Serial(port, 4800, timeout=1)
        return gps_serial

    def attendre_position(self, message="Attente signal GPS..."):
        """
        Attend que le GPS renvoie une position valide et envoie un message pendant ce temps.
        
        paramètre message: Message à afficher pendant l'attente.
        return : Tuple (latitude, longitude).
        """
        print(message)
        while True:
            position = self.get_position_robot(timeout=10)
            if position is not None:
                return position
            print("GPS indisponible, nouvelle tentative dans 3s...")
            time.sleep(3)

    def angle_depart(self, robot):
        """
        Calcule l'orientation initiale du robot par rapport au nord.
        Le robot avance pendant 3 secondes pour comparer deux positions successives.
        
        paramètre robot : Instance de l'objet Robot.
        return : Orientation de départ par rapport au nord en degrés.
        """
        print("Calibration de l'orientation de départ du robot")
        position1 = self.attendre_position()

        robot.avant()
        time.sleep(3.0)
        robot.arret()

        position2 = self.attendre_position()

        orientation_depart = self.get_orientation(position1, position2)
        print("Orientation de départ :", orientation_depart)
        return orientation_depart

    def calcul_orientation_deplacement(self, pos1, pos2):
        """
        Calcule l'angle de déplacement entre deux points.
        """
        print("Calcule l'orientation de déplacement entre deux points")
        return self.get_orientation(pos1, pos2)