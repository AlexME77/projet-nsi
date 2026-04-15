<?php
/**
 * Fichier : stop.php
 * Rôle : C'est le bouton d'arrêt du robot.
 * Il met à jour la base de données pour dire au script Python d'arrêter les moteurs,
 * puis redirige directement vers le menu principal.
 */

// On charge la connexion à la base de données
include("db.php");

/**
 * MISE À JOUR DE LA COMMANDE
 * On change l'action à 'stop' et on vide le nom du parcours (NULL)
 * pour que le robot sache qu'il ne doit plus rien faire et qu'il stoppe sa boucle.
 */
$requete = "UPDATE commande SET action = 'stop', nom_parcours = NULL WHERE id = 1";

// On exécute la requête dans la base de données
$result = $db->exec($requete);

// Si la modification de la base de données a échoué (souvent un souci de droits sur le fichier)
if (!$result) {
    // On renvoie l'utilisateur vers l'accueil avec un code d'erreur dans l'URL
    header('Location: index.php?error=commande_stop');
    exit(); // On stoppe l'exécution du script PHP ici
}

// Si la requête a bien fonctionné, on renvoie vers l'accueil avec un message de réussite vert
header('Location: index.php?success=robot_stop');
exit();
?>