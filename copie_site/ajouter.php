<?php
/**
 * Fichier : ajouter.php
 * Rôle : Permet de créer un nouveau point GPS et de l'ajouter à un parcours.
 * Affiche aussi la liste des points déjà enregistrés pour vérifier.
 */

include("db.php");

$message = ""; // Stocke le message de réussite ou d'erreur
$parcours_selectionne = ""; // Mémorise le parcours qu'on veut afficher

/**
 * GESTION DU FILTRE (Affichage)
 * Si l'URL contient "?nom_parcours=...", ça veut dire qu'on a utilisé
 * le premier formulaire (en GET) pour filtrer l'affichage.
 */
if (isset($_GET["nom_parcours"])) {
    $parcours_selectionne = $_GET["nom_parcours"];
}

/**
 * AJOUT D'UN POINT DANS LA BDD
 * Si le formulaire du bas a été envoyé (en POST), on récupère les infos.
 */
if (isset($_POST["nom_parcours"])) {
    $nom_parcours = $_POST["nom_parcours"];
    $ordre = $_POST["ordre"];
    $latitude = $_POST["latitude"];
    $longitude = $_POST["longitude"];

    // Requête SQL pour insérer une nouvelle ligne dans la table points
    $requete = "INSERT INTO points (nom_parcours, ordre, latitude, longitude) VALUES ('$nom_parcours', $ordre, $latitude, $longitude)";
    
    // On exécute la requête
    $resultat = $db->exec($requete);

    // On vérifie si ça a marché
    if ($resultat) {
        $message = "Point ajouté.";
        $parcours_selectionne = $nom_parcours; // On force l'affichage du parcours qu'on vient de modifier
    } else {
        $message = "Erreur lors de l'ajout.";
    }
}

/**
 * LECTURE DES POINTS EXISTANTS
 * On prépare la liste des points à afficher sur la page.
 */
if ($parcours_selectionne != "") {
    // Si un parcours est sélectionné, on ne cherche que ses points à lui
    $points = $db->query("SELECT id, nom_parcours, ordre, latitude, longitude FROM points WHERE nom_parcours = '$parcours_selectionne' ORDER BY ordre");
} else {
    // Sinon, on prend absolument tous les points de la base
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
            // On récupère tous les noms de parcours sans doublons
            $parcours = $db->query("SELECT DISTINCT nom_parcours FROM points ORDER BY nom_parcours");
            while ($ligne = $parcours->fetchArray()) {
                echo "<option value=\"" . $ligne["nom_parcours"] . "\"";
                
                // Si c'est le parcours qu'on est en train de regarder, on le pré-sélectionne
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
    <ul>
        <?php
        // Boucle pour afficher chaque point trouvé sous forme de liste à puces
        while ($point = $points->fetchArray()) {
            echo "<li>";
            echo $point["nom_parcours"] . " - point " . $point["ordre"];
            echo " (" . $point["latitude"] . ", " . $point["longitude"] . ")";
            echo "</li>";
        }
        ?>
    </ul>

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