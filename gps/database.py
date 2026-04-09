import sqlite3

class Database:

    def __init__(self, database_path="/var/www/html/database/parcours.db"):
        print("Initialisation de la base de données")
        self.path = database_path

    def _connect(self):
        return sqlite3.connect(self.path, timeout=5)

    def get_commande(self):
        conn = self._connect()
        cur = conn.cursor()
        cur.execute("SELECT action, nom_parcours FROM commande WHERE id = 1")
        row = cur.fetchone()
        conn.close()

        if row is None:
            print("Aucune commande trouvée")
            return None

        return {
            "action": row[0],
            "nom_parcours": row[1]
        }

    def set_commande(self, action, nom_parcours=None):
        print(f"Changement de commande : action={action}, nom_parcours={nom_parcours}")
        conn = self._connect()
        cur = conn.cursor()
        cur.execute(
            "UPDATE commande SET action = ?, nom_parcours = ? WHERE id = 1",
            (action, nom_parcours)
        )
        conn.commit()
        conn.close()

    def get_points_parcours(self, nom_parcours):
        print(f"Récupération des points du parcours '{nom_parcours}'")
        if not nom_parcours:
            raise ValueError("Nom de parcours vide")

        conn = self._connect()
        cur = conn.cursor()
        cur.execute(
            """
            SELECT latitude, longitude
            FROM points
            WHERE nom_parcours = ?
            ORDER BY ordre
            """,
            (nom_parcours,)
        )
        points = cur.fetchall()
        conn.close()

        if not points:
            raise ValueError(f"Aucun point trouvé pour le parcours '{nom_parcours}'")

        return points

    def stop_demande(self):
        commande = self.get_commande()
        if commande is None:
            return False
        return commande["action"] == "stop"
