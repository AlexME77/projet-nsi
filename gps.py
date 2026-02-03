import math

def convertir_ddmm(valeur, orientation):
    valeur = float(valeur)
    degres = int(valeur // 100)
    minutes = valeur - degres * 100
    coord = degres + minutes / 60
    if orientation in ['S', 'W']:
        coord = -coord
    return coord


def extraire_position_GPRMC(trame):
    champs = trame.split(",")
    if champs[2] != "A":
        return None
    latitude = convertir_ddmm(champs[3], champs[4])
    longitude = convertir_ddmm(champs[5], champs[6])
    return latitude, longitude

def extraire_position_GPGGA(trame):
    champs = trame.split(",")
    # Vérifier que le signal est valide
    if champs[6] == "0":
        return None
    latitude = convertir_ddmm(champs[2], champs[3])
    longitude = convertir_ddmm(champs[4], champs[5])
    return latitude, longitude



def calculer_orientation_voulue(position, destination):
    """
    Calcule l'orientation (en degrés) à suivre pour aller
    de la position actuelle vers la destination
    """
    lat1, lon1 = position
    lat2, lon2 = destination
    delta_lat = lat2 - lat1
    delta_lon = lon2 - lon1
    angle_rad = math.atan2(delta_lon, delta_lat)
    angle_deg = math.degrees(angle_rad)
    if angle_deg < 0:
        angle_deg += 360
    return angle_deg

def calculer_correction(orientation_actuelle, orientation_voulue):
    angle = orientation_voulue - orientation_actuelle
    if angle > 180:
        angle -= 360
    elif angle < -180:
        angle += 360
    return angle