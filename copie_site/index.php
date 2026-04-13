<?php
include("db.php");

function e(string $value): string {
    return htmlspecialchars($value, ENT_QUOTES, 'UTF-8');
}
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

    <?php if (isset($_GET['success'])): ?>
        <p>
            <?php
            if ($_GET['success'] === 'robot_start') echo 'Commande de démarrage envoyée au robot.';
            elseif ($_GET['success'] === 'robot_stop') echo "Commande d’arrêt envoyée au robot.";
            ?>
        </p>
    <?php endif; ?>

    <?php if (isset($_GET['error'])): ?>
        <p>
            <?php
            if ($_GET['error'] === 'method_not_allowed') echo 'Méthode non autorisée.';
            elseif ($_GET['error'] === 'nom_parcours_vide') echo 'Aucun parcours sélectionné.';
            elseif ($_GET['error'] === 'verification_parcours') echo 'Erreur lors de la vérification du parcours.';
            elseif ($_GET['error'] === 'parcours_introuvable') echo 'Le parcours sélectionné est introuvable.';
            elseif ($_GET['error'] === 'commande_start') echo "Erreur lors de l’envoi de la commande START.";
            elseif ($_GET['error'] === 'commande_stop') echo "Erreur lors de l’envoi de la commande STOP.";
            else echo 'Une erreur est survenue.';
            ?>
        </p>
    <?php endif; ?>

    <form action="lancer.php" method="post">
        <label for="nom_parcours">Choisir un parcours :</label>
        <select name="nom_parcours" id="nom_parcours" required>
            <?php
            $parcours = $db->query("SELECT DISTINCT nom_parcours FROM points ORDER BY nom_parcours");
            while ($ligne = $parcours->fetchArray(SQLITE3_ASSOC)) {
                $nom = $ligne['nom_parcours'];
                echo '<option value="' . e($nom) . '">' . e($nom) . '</option>';
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