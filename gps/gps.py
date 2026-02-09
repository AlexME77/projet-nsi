from math import *
import math

class GPS:
    
    def convertir_ddmm(valeur, orientation):
        valeur = float(valeur)
        degres = int(valeur // 100)
        minutes = valeur - degres * 100
        coord = degres + minutes / 60
        if orientation in ['S', 'W']:
            coord = -coord
        return coord

    def extraire_position_GPGGA(trame):
        champs = trame.split(",")
        # Signal invalide
        if champs[6] == "0":
            return None
        latitude = GPS.convertir_ddmm(champs[2], champs[3])
        longitude = GPS.convertir_ddmm(champs[4], champs[5])
        return latitude, longitude
    
    def lire_position_GPS(gps):
        """
        Lit les trames jusqu'à obtenir une position GPS valide (GPGGA)
        """
        while True:
            trame = gps.readline().decode("ascii", errors="ignore").strip()
            if trame.startswith("$GPGGA"):
                print(trame)
                position = GPS.extraire_position_GPGGA(trame)
                if position is None:
                    print("Position GPS invalide")
                return position

    def distance_2pGPS(coord1, coord2):
        la1 = radians(coord1[0])
        la2 = radians(coord2[0])
        lon1 = radians(coord1[1])
        lon2 = radians(coord2[1])
        dis = 6371009 * acos(
            sin(la1) * sin(la2) +
            cos(la1) * cos(la2) * cos(lon1 - lon2)
        )
        return dis  # en mètres

    def orientation(coord1, coord2):
        la1 = radians(coord1[0])
        la2 = radians(coord2[0])
        lon1 = radians(coord1[1])
        lon2 = radians(coord2[1])

        longDelta = lon2 - lon1
        y = sin(longDelta) * cos(la1)
        x = cos(la1) * sin(la2) - sin(la1) * cos(la2) * cos(longDelta)

        angle = atan2(y, x) * 360 / (2 * pi)
        while angle < 0:
            angle += 360

        direction = 360 - (angle % 360)
        return direction