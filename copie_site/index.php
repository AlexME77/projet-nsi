<?php
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

    <form action="lancer.php" method="post">
        <label>Choisir un parcours :</label>
        <select name="nom_parcours" required>
            <?php
            $parcours = $db->query("SELECT DISTINCT nom_parcours FROM points ORDER BY nom_parcours");
            while ($ligne = $parcours->fetchArray(SQLITE3_ASSOC)) {
                echo "<option value=\"" . $ligne["nom_parcours"] . "\">";
                echo $ligne["nom_parcours"];
                echo "</option>";
            }
            ?>
        </select>

        <div class="robot-buttons">
            <input type="submit" value="Lancer le robot" class="start">
    </form>

    <form action="stop.php" method="post">
            <input type="submit" value="Arrêter le robot" class="danger">
    </form>
        </div>

    <div class="menu-buttons">
        <a href="ajouter.php" class="menu-btn">Ajouter un point</a>
        <a href="modifier.php" class="menu-btn">Modifier un point</a>
        <a href="supprimer.php" class="menu-btn">Supprimer un point</a>
    </div>

</div>

</body>
</html>