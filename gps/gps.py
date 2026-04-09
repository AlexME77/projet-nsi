import math
import serial
import serial.tools.list_ports
import time

class GPS:

    def __init__(self):
        print("Initialisation du GPS")
        self.gps_serial = self.port()
        if self.gps_serial is None:
            raise RuntimeError("GPS non disponible")

    def convertir_ddmm(self, valeur, orientation):
        print("Conversion de la coordonnée")
        valeur = float(valeur)
        degres = int(valeur // 100)
        minutes = valeur - degres * 100
        coord = degres + minutes / 60
        if orientation in ['S', 'W']:
            coord = -coord
        return coord

    def extraire_position_GPGGA(self, trame):
        print("Extraction de la position")
        champs = trame.split(",")
        # Signal invalide
        if champs[6] == "0":
            return None
        latitude = self.convertir_ddmm(champs[2], champs[3])
        longitude = self.convertir_ddmm(champs[4], champs[5])
        return latitude, longitude
    
    def get_position_robot(self, timeout = 10):
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
        print(message)
        while True:
            position = self.get_position_robot(timeout=10)
            if position is not None:
                return position
            print("GPS indisponible, nouvelle tentative dans 3s...")
            time.sleep(3)

    def angle_depart(self, robot):
        "Calibration du robot pour avoir son orientation de départ par rapport au Nord"
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
        print("Calcule l'orientation de déplacement entre deux points")
        return self.get_orientation(pos1, pos2)