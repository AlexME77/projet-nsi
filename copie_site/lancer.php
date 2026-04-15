<?php
/**
 * Fichier : lancer.php
 * Rôle : C'est le cerveau du bouton "Lancer le robot".
 * Il vérifie que le parcours choisi existe bien, dit à la base de données de passer en mode "start",
 * et exécute la commande Linux pour allumer le vrai script Python sur le Raspberry Pi.
 */

// Affiche les erreurs PHP à l'écran (hyper pratique pour débugger au lieu d'avoir la fameuse erreur 500)
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);

// On charge la connexion à la base de données
include("db.php");

// On vérifie que le formulaire a bien envoyé la variable 'nom_parcours'
if (isset($_POST['nom_parcours'])) {
    $nomParcours = $_POST['nom_parcours'];

    // Si le nom est vide (bug ou bidouille de l'utilisateur), on renvoie une erreur
    if ($nomParcours == '') {
        header('Location: index.php?error=nom_parcours_vide');
        exit(); // On stoppe l'exécution du script direct
    }

    /**
     * VÉRIFICATION DU PARCOURS
     * On compte combien de points portent ce nom de parcours dans la table.
     */
    $requeteCheck = "SELECT COUNT(*) AS total FROM points WHERE nom_parcours = '$nomParcours'";
    $resultCheck = $db->query($requeteCheck);

    // Si la requête SQL a planté
    if (!$resultCheck) {
        header('Location: index.php?error=verification_parcours');
        exit();
    }

    $row = $resultCheck->fetchArray();

    // Si le total est égal à 0, ça veut dire que le parcours n'existe pas en vrai
    if ($row['total'] == 0) {
        header('Location: index.php?error=parcours_introuvable');
        exit();
    }

    /**
     * MISE À JOUR DE LA COMMANDE
     * On prépare le terrain pour le Python en mettant 'start' et le nom du parcours dans la table 'commande'.
     */
    $requeteUpdate = "UPDATE commande SET action = 'start', nom_parcours = '$nomParcours' WHERE id = 1";
    $resultUpdate = $db->exec($requeteUpdate);

    // Si l'écriture dans la BDD échoue (souvent un problème de droits d'accès au fichier .db)
    if (!$resultUpdate) {
        header('Location: index.php?error=commande_start');
        exit();
    }

    /**
     * LANCEMENT DU ROBOT (PYTHON)
     * "sudo -u pi" : On force le script à tourner sous l'utilisateur 'pi' pour avoir le droit d'utiliser les moteurs.
     * ">> /tmp/robot.log 2>&1" : On enregistre tout ce que dit le python (les print et les erreurs) dans un fichier texte.
     * "&" à la fin : On lance ça en arrière-plan pour que la page web charge tout de suite sans attendre que le robot ait fini.
     */
    exec("sudo -u pi /usr/bin/python3 /home/pi/Desktop/PROJET/main.py >> /tmp/robot.log 2>&1 &");

    // Tout s'est bien passé, on redirige vers l'accueil avec un petit message vert de succès !
    header('Location: index.php?success=robot_start');
    exit();
}
?>