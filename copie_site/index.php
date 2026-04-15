<?php
/**
 * Fichier : index.php
 * Rôle : C'est la page d'accueil (le menu principal) du site web.
 * Elle permet de choisir un parcours dans la liste, de démarrer ou d'arrêter le robot,
 * et d'afficher les messages de réussite ou d'erreur en haut de la page.
 */

// On charge la connexion à la base de données pour pouvoir lire les parcours existants
include("db.php");
?>
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Robot - Menu principal</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>

<div class="container">
    <h1>Menu principal</h1>

    <?php 
    /**
     * GESTION DES MESSAGES DE SUCCÈS
     * On regarde si l'URL contient une variable "?success=..." (grâce à $_GET)
     * Si oui, on affiche le bon message en fonction du mot-clé reçu.
     */
    if (isset($_GET['success'])): 
    ?>
        <p>
            <?php
            if ($_GET['success'] == 'robot_start') echo 'Commande de démarrage envoyée au robot.';
            elseif ($_GET['success'] == 'robot_stop') echo "Commande d’arrêt envoyée au robot.";
            ?>
        </p>
    <?php endif; ?>

    <?php 
    /**
     * GESTION DES MESSAGES D'ERREUR
     * Même principe, on vérifie si "?error=..." est dans l'URL pour avertir l'utilisateur 
     * si un truc s'est mal passé dans lancer.php ou stop.php.
     */
    if (isset($_GET['error'])): 
    ?>
        <p>
            <?php
            if ($_GET['error'] == 'method_not_allowed') echo 'Méthode non autorisée.';
            elseif ($_GET['error'] == 'nom_parcours_vide') echo 'Aucun parcours sélectionné.';
            elseif ($_GET['error'] == 'verification_parcours') echo 'Erreur lors de la vérification du parcours.';
            elseif ($_GET['error'] == 'parcours_introuvable') echo 'Le parcours sélectionné est introuvable.';
            elseif ($_GET['error'] == 'commande_start') echo "Erreur lors de l’envoi de la commande START.";
            elseif ($_GET['error'] == 'commande_stop') echo "Erreur lors de l’envoi de la commande STOP.";
            else echo 'Une erreur est survenue.';
            ?>
        </p>
    <?php endif; ?>

    <form action="lancer.php" method="post">
        <label for="nom_parcours">Choisir un parcours :</label>
        <select name="nom_parcours" id="nom_parcours" required>
            <?php
            /**
             * RÉCUPÉRATION DES PARCOURS
             * On fait une requête SQL pour trouver tous les noms de parcours.
             * Le mot-clé DISTINCT permet de ne pas afficher le même parcours en boucle 
             * s'il contient plusieurs points.
             */
            $parcours = $db->query("SELECT DISTINCT nom_parcours FROM points ORDER BY nom_parcours");
            
            // Boucle while pour lire chaque ligne trouvée dans la base de données
            // et créer dynamiquement une balise <option> dans le menu HTML.
            while ($ligne = $parcours->fetchArray()) {
                $nom = $ligne['nom_parcours'];
                echo '<option value="' . $nom . '">' . $nom . '</option>';
            }
            ?>
        </select>

        <div class="robot-buttons">
            <input type="submit" value="Lancer le robot" class="start">
        </div>
    </form>

    <form action="stop.php" method="post">
        <div class="robot-buttons">
            <input type="submit" value="Arrêter le robot" class="danger">
        </div>
    </form>

    <div class="menu-buttons">
        <a href="ajouter.php" class="menu-btn">Ajouter un point</a>
        <a href="modifier.php" class="menu-btn">Modifier un point</a>
        <a href="supprimer.php" class="menu-btn">Supprimer un point</a>
    </div>
</div>

</body>
</html>