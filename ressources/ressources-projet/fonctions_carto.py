from math import *

class GPS:

    #fonction calcul de la distance entre deux points GPS en mètres
    def distance_2pGPS(coord1,coord2):
        la1=radians(coord1[0])
        la2=radians(coord2[0])
        lon1=radians(coord1[1])
        lon2=radians(coord2[1])
        dis=6371009*acos((sin(la1)*sin(la2)+cos(la1)*cos(la2)*cos(lon1-lon2)))
        return dis

    #fonction de calculs d'orientation d'une droite passant par deux points GPS par rapport à la direction Nord
    def orientation(coord1,coord2):
        la1=radians(coord1[0])
        la2=radians(coord2[0])
        lon1=radians(coord1[1])
        lon2=radians(coord2[1])
        longDelta = lon2-lon1
        y= sin(longDelta)*cos(la1)
        x= cos(la1)*sin(la2)-sin(la1)*cos(la2)*cos(longDelta)
        angle = atan2(y, x)*360/(2*pi)
        while angle < 0:
            angle+=360
        direction=360-(float(angle) % 360)
        return direction