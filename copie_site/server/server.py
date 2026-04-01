from flask import Flask, request
import sqlite3

app = Flask(__name__)

DB_PATH = "../database/parcours.db"

def connecter_db():
    return sqlite3.connect(DB_PATH)

@app.route("/ajouter_point", methods=["GET"])
def ajouter_point():
    # 1) Vérifier présence des champs
    champs = ["nom_parcours", "ordre", "latitude", "longitude"]
    for c in champs:
        if request.args.get(c) is None:
            return f"Erreur : champ manquant -> {c}", 400

    nom_parcours = request.args.get("nom_parcours")

    # 2) Convertir les types (et détecter erreurs)
    try:
        ordre = int(request.args.get("ordre"))
        latitude = float(request.args.get("latitude"))
        longitude = float(request.args.get("longitude"))
    except ValueError:
        return "Erreur : ordre doit être un entier, latitude/longitude des nombres", 400

    # 3) Insérer dans la base
    try:
        conn = connecter_db()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO points (nom_parcours, ordre, latitude, longitude)
            VALUES (?, ?, ?, ?)
        """, (nom_parcours, ordre, latitude, longitude))
        conn.commit()
        conn.close()
    except sqlite3.IntegrityError:
        return "Erreur : ce point (nom_parcours, ordre) existe déjà", 409
    except sqlite3.Error as e:
        return f"Erreur SQLite : {e}", 500

    return "OK : point ajouté", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
