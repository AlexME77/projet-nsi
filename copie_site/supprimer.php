<?php
/**
 * Fichier : supprimer.php
 * Rôle : Permet de supprimer un point précis dans un parcours.
 * Logique : 1. On filtre par parcours. 2. On sélectionne le point à supprimer de la base de données.
 */

// Connexion à la base de données SQLite (via db.php)
include("db.php");

$message = "";
$parcours_selectionne = "";

/**
 * ÉTAPE 1 : CHOIX DU PARCOURS
 * Si l'URL contient un nom de parcours (via le premier formulaire), on le garde en mémoire.
 */
if (isset($_GET["nom_parcours"])) {
    $parcours_selectionne = $_GET["nom_parcours"];
}

/**
 * ÉTAPE 2 : SUPPRESSION DU POINT
 * Si le 2ème formulaire a envoyé un ID en POST, on passe à la suppression du point ciblé dans la base de données.
 */
if (isset($_POST["id"])) {
    $id = $_POST["id"];

    // Requête SQL pour effacer la ligne précise
    $requete = "DELETE FROM points WHERE id = $id";
    $resultat = $db->exec($requete);

    // Check pour voir si la suppression a bien marché
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
// On récupère la liste de tous les parcours sans doublons
$parcours = $db->query("SELECT DISTINCT nom_parcours FROM points ORDER BY nom_parcours");

// On remplit le menu déroulant
while ($ligne = $parcours->fetchArray()) {
    echo "<option value=\"" . $ligne["nom_parcours"] . "\"";

    // Garde le parcours sélectionné affiché si on a déjà fait un choix
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
// Si un parcours est choisi, on affiche la suite pour cibler le point à supprimer
if ($parcours_selectionne != "") {
?>
<form action="supprimer.php" method="post">
<label>Choisir un point :</label>
<select name="id" required>
<?php
// On va chercher uniquement les points du parcours sélectionné
$points = $db->query("SELECT id, ordre, latitude, longitude FROM points WHERE nom_parcours = '$parcours_selectionne' ORDER BY ordre");

// On liste les points dispos pour les supprimer
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