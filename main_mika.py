import serial
import serial.tools.list_ports
from gps.gps import GPS
from gps.database import lire_destination
import time

if __name__ == '__main__':
    
    ports = list(serial.tools.list_ports.comports())
    if not ports:
        print("Aucun port série détecté")
        exit()
    port = ports[0].device
    print("Port GPS détecté :", port)
    gps_serial = serial.Serial(port, 4800, timeout=1)
    
    
    print("Calibration orientation...")
    try:
        from robot import *
        robot_disponible = True
        robot = robot.Robot()
    except ModuleNotFoundError:
        print ("RPi.GPIO non disponible (mode PC)")
        robot_disponible = False
        orientation_depart = None
        
    if robot_disponible :
        position1 = GPS.lire_position_GPS(gps_serial)
        robot.avant()
        time.sleep(0.5)
        robot.arret()
        position2 = GPS.lire_position_GPS(gps_serial)
        orientation_depart = GPS.orientation(position1, position2)
        print("Orientation de départ :", orientation_depart)
    else:
        orientation_depart = None
        print("Calibration ignorée (mode PC)")
    
    ordre = 1
    seuil = 2.0
    
    while True:
        trame = gps_serial.readline().decode("ascii", errors="ignore").strip()
        if not trame.startswith("$GPGGA"):
            continue
        print(trame)
        
        position = GPS.extraire_position_GPGGA(trame)
        if position is None:
            print("Position GPS invalide")
            continue
        #print("Position actuelle :", position)
        
        destination = lire_destination("test", ordre)
        #print("Destination :", destination)
        if destination is None:
            print("Parcours terminé")
            break
        
        orientation_voulue = GPS.orientation(position, destination)
        #print("Orientation cible : ", round(orientation_voulue, 2), "°")
        
        distance_reste = GPS.distance_2pGPS(position, destination)
        #print("Distance restante :", round(distance_reste, 2), "m")
                
        # Vérifier si le point est atteint
        if distance_reste < seuil:
            print("Point atteint")
            ordre += 1