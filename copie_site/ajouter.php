<?php
include("db.php");

$message = "";
$parcours_selectionne = "";

if (isset($_GET["nom_parcours"])) {
    $parcours_selectionne = $_GET["nom_parcours"];
}

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $nom_parcours = $_POST["nom_parcours"];
    $ordre = $_POST["ordre"];
    $latitude = $_POST["latitude"];
    $longitude = $_POST["longitude"];

    $stmt = $db->prepare("INSERT INTO points (nom_parcours, ordre, latitude, longitude) VALUES (:nom_parcours, :ordre, :latitude, :longitude)");
    $stmt->bindValue(":nom_parcours", $nom_parcours, SQLITE3_TEXT);
    $stmt->bindValue(":ordre", $ordre, SQLITE3_INTEGER);
    $stmt->bindValue(":latitude", $latitude, SQLITE3_FLOAT);
    $stmt->bindValue(":longitude", $longitude, SQLITE3_FLOAT);

    $resultat = $stmt->execute();

    if ($resultat) {
        $message = "Point ajouté.";
        $parcours_selectionne = $nom_parcours;
    } else {
        $message = "Erreur lors de l'ajout : " . $db->lastErrorMsg();
    }
}

if ($parcours_selectionne != "") {
    $stmt_points = $db->prepare("SELECT id, nom_parcours, ordre, latitude, longitude FROM points WHERE nom_parcours = :nom_parcours ORDER BY ordre");
    $stmt_points->bindValue(":nom_parcours", $parcours_selectionne, SQLITE3_TEXT);
    $points = $stmt_points->execute();
} else {
    $points = $db->query("SELECT id, nom_parcours, ordre, latitude, longitude FROM points ORDER BY nom_parcours, ordre");
}
?>
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Ajouter un point</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>

<div class="container">
    <h1>Ajouter un point</h1>
    <p><a href="index.php">← Retour au menu</a></p>

    <form action="ajouter.php" method="get">
        <label>Voir les points du parcours :</label>
        <select name="nom_parcours">
            <option value="">-- Tous les parcours --</option>
            <?php
            $parcours = $db->query("SELECT DISTINCT nom_parcours FROM points ORDER BY nom_parcours");
            while ($ligne = $parcours->fetchArray(SQLITE3_ASSOC)) {
                echo "<option value=\"" . $ligne["nom_parcours"] . "\"";
                if ($ligne["nom_parcours"] == $parcours_selectionne) {
                    echo " selected";
                }
                echo ">" . $ligne["nom_parcours"] . "</option>";
            }
            ?>
        </select>
        <input type="submit" value="Afficher">
    </form>

    <br>

    <label>Points enregistrés :</label>
    <select>
        <?php
        while ($point = $points->fetchArray(SQLITE3_ASSOC)) {
            echo "<option>";
            echo $point["nom_parcours"] . " - point " . $point["ordre"];
            echo " (" . $point["latitude"] . ", " . $point["longitude"] . ")";
            echo "</option>";
        }
        ?>
    </select>

    <br><br>

    <form action="ajouter.php" method="post">
        <label>Nom du parcours :</label>
        <input type="text" name="nom_parcours" required>

        <label>Ordre du point :</label>
        <input type="number" name="ordre" required>

        <label>Latitude :</label>
        <input type="number" step="any" name="latitude" required>

        <label>Longitude :</label>
        <input type="number" step="any" name="longitude" required>

        <input type="submit" value="Ajouter le point">
    </form>

    <p class="note"><?php echo $message; ?></p>
</div>

</body>
</html>