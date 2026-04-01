<?php
include("db.php");

$parcours_selectionne = "";

if (isset($_GET["nom_parcours"])) {
    $parcours_selectionne = $_GET["nom_parcours"];
}

$parcours = $db->query("SELECT DISTINCT nom_parcours FROM points ORDER BY nom_parcours");

if ($parcours_selectionne != "") {
    $stmt = $db->prepare("SELECT id, nom_parcours, ordre, latitude, longitude FROM points WHERE nom_parcours = :nom_parcours ORDER BY ordre");
    $stmt->bindValue(":nom_parcours", $parcours_selectionne, SQLITE3_TEXT);
    $points = $stmt->execute();
} else {
    $points = $db->query("SELECT id, nom_parcours, ordre, latitude, longitude FROM points ORDER BY nom_parcours, ordre");
}
?>
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Robot - Accueil</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>

<div class="container">
    <h1>Menu principal</h1>

    <form action="index.php" method="get">
        <label>Choisir un parcours :</label>
        <select name="nom_parcours" required>
            <option value="">-- Choisir un parcours --</option>
            <?php
            $parcours2 = $db->query("SELECT DISTINCT nom_parcours FROM points ORDER BY nom_parcours");
            while ($ligne = $parcours2->fetchArray(SQLITE3_ASSOC)) {
                echo "<option value=\"" . $ligne["nom_parcours"] . "\"";
                if ($ligne["nom_parcours"] == $parcours_selectionne) {
                    echo " selected";
                }
                echo ">" . $ligne["nom_parcours"] . "</option>";
            }
            ?>
        </select>
        <input type="submit" value="Afficher les points">
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

    <form action="lancer.php" method="post">
        <label>Parcours à lancer :</label>
        <select name="nom_parcours" required>
            <?php
            $parcours3 = $db->query("SELECT DISTINCT nom_parcours FROM points ORDER BY nom_parcours");
            while ($ligne = $parcours3->fetchArray(SQLITE3_ASSOC)) {
                echo "<option value=\"" . $ligne["nom_parcours"] . "\"";
                if ($ligne["nom_parcours"] == $parcours_selectionne) {
                    echo " selected";
                }
                echo ">" . $ligne["nom_parcours"] . "</option>";
            }
            ?>
        </select>
        <input type="submit" value="Lancer le robot">
    </form>

    <br>

    <form action="stop.php" method="post">
        <input type="submit" value="Arrêter le robot" class="danger">
    </form>

    <br><br>

    <ul>
        <li><a href="ajouter.php">Ajouter un point</a></li>
        <li><a href="modifier.php">Modifier un point</a></li>
        <li><a href="supprimer.php">Supprimer un point</a></li>
    </ul>
</div>

</body>
</html>