<?php
include("db.php");

$message = "";
$parcours_selectionne = "";

if (isset($_GET["nom_parcours"])) {
    $parcours_selectionne = $_GET["nom_parcours"];
}

if (isset($_POST["id"])) {
    $id = $_POST["id"];

    $requete = "DELETE FROM points WHERE id = $id";
    $resultat = $db->exec($requete);

    if ($resultat) {
        $message = "Point supprimé";
    } else {
        $message = "Erreur lors de la suppression";
    }
}
?>

<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<title>Supprimer un point</title>
<link rel="stylesheet" href="style.css">
</head>
<body>

<div class="container">
<h1>Supprimer un point</h1>

<p><a href="index.php">← Retour au menu</a></p>

<form action="supprimer.php" method="get">
<label>Choisir un parcours :</label>
<select name="nom_parcours" required>
<option value="">-- Choisir un parcours --</option>

<?php

$parcours = $db->query("SELECT DISTINCT nom_parcours FROM points ORDER BY nom_parcours");

while ($ligne = $parcours->fetchArray()) {
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
<form action="supprimer.php" method="post">
<label>Choisir un point :</label>
<select name="id" required>
<?php

$points = $db->query("SELECT id, ordre, latitude, longitude FROM points WHERE nom_parcours = '$parcours_selectionne' ORDER BY ordre");

while ($point = $points->fetchArray()) {
    echo "<option value=\"" . $point["id"] . "\">";
    echo "Point " . $point["ordre"] . " (" . $point["latitude"] . ", " . $point["longitude"] . ")";
    echo "</option>";
}
?>
</select>

<br><br>

<input type="submit" value="Supprimer le point" class="danger">
</form>
<?php
}
?>

<p class="note"><?php echo $message; ?></p>
</div>

</body>
</html>