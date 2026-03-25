import math
import serial
import serial.tools.list_ports
import time
from gps.database import coord_destination

class GPS:

    def __init__(self):
        self.gps_serial = self.port()

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
    
    def get_position_robot(self, timeout = 5):
        """
        Lit les trames jusqu'à obtenir une position GPS valide (GPGGA)
        """
        start_time = time.time()

        while time.time() - start_time < timeout:
            trame = self.gps_serial.readline().decode("ascii", errors="ignore").strip()
            print("Trame brut : ", trame)
            if trame.startswith("$GPGGA"):
                position = self.extraire_position_GPGGA(trame)
                if position:
                    return position
        return None  # échec

    def distance_2pGPS(self, coord1, coord2):
        print(f"Calcule 2pGPS entre {coord1} et {coord2}")
        la1 = math.radians(coord1[0])
        la2 = math.radians(coord2[0])
        lon1 = math.radians(coord1[1])
        lon2 = math.radians(coord2[1])
        dis = 6371009 * math.acos(
            math.sin(la1) * math.sin(la2) +
            math.cos(la1) * math.cos(la2) * math.cos(lon1 - lon2)
        )
        return dis  # en mètres

    def get_orientation(self, coord1, coord2):
        print("Calcule de l'orientation de l'arrivée par rapport au Nord")
        la1 = math.radians(coord1[0])
        la2 = math.radians(coord2[0])
        lon1 = math.radians(coord1[1])
        lon2 = math.radians(coord2[1])

        longDelta = lon2 - lon1
        y = math.sin(longDelta) * math.cos(la1)
        x = math.cos(la1) * math.sin(la2) - math.sin(la1) * math.cos(la2) * math.cos(longDelta)

        angle = math.atan2(y, x) * 360 / (2 * math.pi)
        while angle < 0:
            angle += 360

        direction = 360 - (angle % 360)
        return direction
    
    def port(self):
        print("Regarde si tu es sur le Raspberry et le port usb utilisé")
        ports = list(serial.tools.list_ports.comports())
        if not ports:
            print("Aucun port série détecté")
            exit()
        port = ports[0].device
        print("Port GPS détecté :", port)
        gps_serial = serial.Serial(port, 4800, timeout=1)
        return gps_serial
    
    def angle_depart(self, robot):
        "Calibration du robot pour avoir son orientation de départ par rapport au Nord"
        print("Calibration orientation...")
        position1 = self.get_position_robot()
        if position1 is None:
            print("Erreur GPS (position1)")
            return None
	
        robot.avant()
        time.sleep(0.5)
        robot.arret()

        position2 = self.get_position_robot()
        if position2 is None:
            print("Erreur GPS (position2)")
            return None

        orientation_depart = self.get_orientation(position1, position2)
        print("Orientation de départ :", orientation_depart)

        return orientation_depart
        
    def get_distance_cible(self, points, ordre):
        print("Calcul de la distance du robot par rapport à la cible")
        return self.distance_2pGPS(self.get_position_robot(), points[ordre])

    def correction_orientation(self, points, ordre, orientation_robot):
        "Calcule la correction d'orientation nécessaire pour se diriger vers la cible"
        angle_destination = self.get_orientation(self.get_position_robot(), points[ordre])
        correction = (angle_destination - orientation_robot)

        if correction > 180:
            correction -= 360

        if correction < -180:
            correction += 360

        return correction
