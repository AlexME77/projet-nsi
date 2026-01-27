from flask import Flask, request
import sqlite3

app = Flask(__name__)

DB_PATH = "../database/parcours.db" #chemin relatif à server.py

def connecter_db():
    return sqlite3.connect(DB_PATH)

@app.route("/ajouter_point", methods=["GET"])
def ajouter_point():
# On récupère toutes les colonnes de la base de données
    nom_parcours = request.args.get("nom_parcours")
    ordre = request.args.get("ordre")
    latitude = request.args.get("latitude")
    longitude = request.args.get("longitude")
    conn = connecter_db()
    curseur = conn.cursor()

# On insère les valeurs dans la base de données
    curseur.execute("""
        INSERT INTO points (nom_parcours, ordre, latitude, longitude)
        VALUES (?, ?, ?, ?)
    """, (nom_parcours, ordre, latitude, longitude))

    conn.commit()
    conn.close()
    
    return "Point ajouté avec succès"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
