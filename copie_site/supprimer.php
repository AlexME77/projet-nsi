<?php
include("db.php");

$message = "";
$parcours_selectionne = "";

if (isset($_GET["nom_parcours"])) {
$parcours_selectionne = $_GET["nom_parcours"];
}

if ($_SERVER["REQUEST_METHOD"] == "POST") {
$id = $_POST["id"];

$stmt = $db->prepare("DELETE FROM points WHERE id = :id");
$stmt->bindValue(":id", $id, SQLITE3_INTEGER);
$resultat = $stmt->execute();

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
<form action="supprimer.php" method="post">
<label>Choisir un point :</label>
<select name="id" required>
<?php
$stmt_points = $db->prepare("SELECT id, ordre, latitude, longitude FROM points WHERE nom_parcours = :nom_parcours ORDER BY ordre");
$stmt_points->bindValue(":nom_parcours", $parcours_selectionne, SQLITE3_TEXT);
$points = $stmt_points->execute();

while ($point = $points->fetchArray(SQLITE3_ASSOC)) {
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