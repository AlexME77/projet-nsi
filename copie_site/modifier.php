<?php
/**
 * Fichier : modifier.php
 * Rôle : Permet de modifier les coordonnées ou l'ordre d'un point GPS existant.
 * Le fonctionnement se fait en 3 étapes :
 * 1. On choisit le parcours.
 * 2. On choisit le point précis de ce parcours.
 * 3. On modifie les valeurs de ce point dans un formulaire final.
 */

// On charge la connexion à la base de données
include("db.php");

$message = ""; // Pour afficher si la modif a marché ou planté
$parcours_selectionne = ""; // Mémorise le parcours qu'on est en train de regarder
$point_selectionne = null; // Mémorise les données du point qu'on veut modifier

/**
 * ÉTAPE 1 : CHOIX DU PARCOURS (Filtre)
 * On regarde si le premier formulaire a envoyé un nom de parcours dans l'URL (en GET).
 */
if (isset($_GET["nom_parcours"])) {
    $parcours_selectionne = $_GET["nom_parcours"];
}

/**
 * ÉTAPE 2 : CHOIX DU POINT À MODIFIER
 * Si l'URL contient "?id=...", on va chercher toutes les infos de ce point
 * dans la BDD pour pouvoir pré-remplir le formulaire de modification.
 */
if (isset($_GET["id"])) {
    $id = $_GET["id"];
    // On récupère la ligne complète du point sélectionné
    $resultat = $db->query("SELECT * FROM points WHERE id = $id");
    
    if ($resultat) {
        $point_selectionne = $resultat->fetchArray();
        // On met à jour le parcours sélectionné au cas où
        if ($point_selectionne) {
            $parcours_selectionne = $point_selectionne["nom_parcours"];
        }
    }
}

/**
 * ÉTAPE 3 : SAUVEGARDE DES MODIFICATIONS
 * Si le formulaire final a été envoyé (en POST), on met à jour la base de données.
 */
if (isset($_POST["id"])) {
    // On récupère toutes les nouvelles valeurs tapées par l'utilisateur
    $id = $_POST["id"];
    $nom_parcours = $_POST["nom_parcours"];
    $ordre = $_POST["ordre"];
    $latitude = $_POST["latitude"];
    $longitude = $_POST["longitude"];

    // Requête SQL pour modifier (UPDATE) les valeurs du point précis (WHERE id = ...)
    $requete = "UPDATE points SET nom_parcours = '$nom_parcours', ordre = $ordre, latitude = $latitude, longitude = $longitude WHERE id = $id";
    $resultat = $db->exec($requete);

    // On vérifie si la mise à jour a fonctionné
    if ($resultat) {
        $message = "Point modifié.";
    } else {
        $message = "Erreur lors de la modification.";
    }

    // On recharge les nouvelles données du point pour que le formulaire affiche direct les modifs
    $res2 = $db->query("SELECT * FROM points WHERE id = $id");
    if ($res2) {
        $point_selectionne = $res2->fetchArray();
        if ($point_selectionne) {
            $parcours_selectionne = $point_selectionne["nom_parcours"];
        }
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
            // On récupère tous les noms de parcours sans doublons
            $parcours = $db->query("SELECT DISTINCT nom_parcours FROM points ORDER BY nom_parcours");
            while ($ligne = $parcours->fetchArray()) {
                echo "<option value=\"" . $ligne["nom_parcours"] . "\"";
                // On garde la sélection active si on a déjà choisi un parcours
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
    // Si on a bien choisi un parcours, on affiche le 2ème formulaire
    if ($parcours_selectionne != "") {
    ?>
        <form action="modifier.php" method="get">
            <input type="hidden" name="nom_parcours" value="<?php echo $parcours_selectionne; ?>">

            <label>Choisir un point :</label>
            <select name="id" required>
                <?php
                // On va chercher uniquement les points du parcours sélectionné
                $points = $db->query("SELECT id, ordre FROM points WHERE nom_parcours = '$parcours_selectionne' ORDER BY ordre");

                while ($point = $points->fetchArray()) {
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

    <?php 
    // Si on a bien cliqué sur un point précis, on affiche le formulaire de modification
    if ($point_selectionne) { 
    ?>
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