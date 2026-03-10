import sqlite3

def lire_destination(nom_parcours, ordre):
    """
    Récupère les coordonnées GPS (latitude, longitude)
    d'un point du parcours depuis la base de données
    """
    conn = sqlite3.connect("gps/parcours.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT latitude, longitude FROM points WHERE nom_parcours=? AND ordre=?",
        (nom_parcours, ordre)
    )
    resultat = cursor.fetchone()
    conn.close()
    if resultat is None:
        return None
    return resultat  # (latitude, longitude)