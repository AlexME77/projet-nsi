<?php
require 'db.php';

$stmt = $pdo->prepare("UPDATE commande SET action = 'stop' HERE id =1");
$stmt->execute();

header("Location: index.php");
exit();
?>