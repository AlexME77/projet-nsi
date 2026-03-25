<?php
include("db.php");

$message = "";
$parcours_selectionne = "";
$point_selectionne = null;

if (isset($_GET["nom_parcours"])) {
    $parcours_selectionne = $_GET["nom_parcours"];
}

if (isset($_GET["id"])) {
    $id = $_GET["id"];
    $stmt = $db->prepare("SELECT * FROM points WHERE id = :id");
    $stmt->bindValue(":id", $id, SQLITE3_INTEGER);
    $resultat = $stmt->execute();
    $point_selectionne = $resultat->fetchArray(SQLITE3_ASSOC);

    if ($point_selectionne) {
        $parcours_selectionne = $point_selectionne["nom_parcours"];
    }
}

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $id = $_POST["id"];
    $nom_parcours = $_POST["nom_parcours"];
    $ordre = $_POST["ordre"];
    $latitude = $_POST["latitude"];
    $longitude = $_POST["longitude"];

    $stmt = $db->prepare("
        UPDATE points
        SET nom_parcours = :nom_parcours, ordre = :ordre, latitude = :latitude, longitude = :longitude
        WHERE id = :id
    ");
    $stmt->bindValue(":nom_parcours", $nom_parcours, SQLITE3_TEXT);
    $stmt->bindValue(":ordre", $ordre, SQLITE3_INTEGER);
    $stmt->bindValue(":latitude", $latitude, SQLITE3_FLOAT);
    $stmt->bindValue(":longitude", $longitude, SQLITE3_FLOAT);
    $stmt->bindValue(":id", $id, SQLITE3_INTEGER);

    $resultat = $stmt->execute();

    if ($resultat) {
        $message = "Point modifié.";
    } else {
        $message = "Erreur lors de la modification : " . $db->lastErrorMsg();
    }

    $stmt2 = $db->prepare("SELECT * FROM points WHERE id = :id");
    $stmt2->bindValue(":id", $id, SQLITE3_INTEGER);
    $res2 = $stmt2->execute();
    $point_selectionne = $res2->fetchArray(SQLITE3_ASSOC);

    if ($point_selectionne) {
        $parcours_selectionne = $point_selectionne["nom_parcours"];
    }
}
?>
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Modifier un point</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>

<div class="container">
    <h1>Modifier un point</h1>
    <p><a href="index.php">← Retour au menu</a></p>

    <form action="modifier.php" method="get">
        <label>Choisir un parcours :</label>
        <select name="nom_parcours" required>
            <option value="">-- Choisir un parcours --</option>
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
        <input type="submit" value="Afficher les points">
    </form>

    <br>

    <?php
    if ($parcours_selectionne != "") {
    ?>
        <form action="modifier.php" method="get">
            <input type="hidden" name="nom_parcours" value="<?php echo $parcours_selectionne; ?>">

            <label>Choisir un point :</label>
            <select name="id" required>
                <?php
                $stmt_points = $db->prepare("SELECT id, ordre FROM points WHERE nom_parcours = :nom_parcours ORDER BY ordre");
                $stmt_points->bindValue(":nom_parcours", $parcours_selectionne, SQLITE3_TEXT);
                $points = $stmt_points->execute();

                while ($point = $points->fetchArray(SQLITE3_ASSOC)) {
                    echo "<option value=\"" . $point["id"] . "\">Point " . $point["ordre"] . "</option>";
                }
                ?>
            </select>
            <input type="submit" value="Choisir ce point">
        </form>
    <?php
    }
    ?>

    <br>

    <?php if ($point_selectionne) { ?>
        <form action="modifier.php" method="post">
            <input type="hidden" name="id" value="<?php echo $point_selectionne["id"]; ?>">

            <label>Nom du parcours :</label>
            <input type="text" name="nom_parcours" value="<?php echo $point_selectionne["nom_parcours"]; ?>" required>

            <label>Ordre du point :</label>
            <input type="number" name="ordre" value="<?php echo $point_selectionne["ordre"]; ?>" required>

            <label>Latitude :</label>
            <input type="number" step="any" name="latitude" value="<?php echo $point_selectionne["latitude"]; ?>" required>

            <label>Longitude :</label>
            <input type="number" step="any" name="longitude" value="<?php echo $point_selectionne["longitude"]; ?>" required>

            <input type="submit" value="Modifier le point">
        </form>
    <?php } ?>

    <p class="note"><?php echo $message; ?></p>
</div>

</body>
</html>