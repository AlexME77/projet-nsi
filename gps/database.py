import sqlite3

def coord_destination(nom_parcours):
    """
    Récupère les coordonnées GPS (latitude, longitude)
    d'un point du parcours depuis la base de données
    """

    print("Connexion à la base de données")
    conn = sqlite3.connect("/var/www/html/robot/database/parcours.db")
    cursor = conn.cursor()
    print("Récupération des coordonnées GPS")
    cursor.execute(
        "SELECT latitude, longitude FROM points WHERE nom_parcours=? ORDER BY ordre",
        (nom_parcours,)
    )
    resultat = cursor.fetchall()
    conn.close()
    print("Déconnexion de la base de données, récupération terminée")

    print("Vérification si la base de données est vide")
    if len(resultat) == 0: 
        raise ValueError(f"Aucun parcours '{nom_parcours}'")
    
    print(f"Les points du parcours sont : {resultat}")
    return resultat  # (latitude, longitude)

if __name__ == '__main__':
    coord_destination('test')
