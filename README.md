# Projet Robot GPS – Interface Web et Navigation Autonome

## Présentation

Ce projet a été réalisé dans le cadre de la spécialité **Numérique et Sciences Informatiques (NSI)** en Terminale.

Il consiste à programmer un robot mobile capable de suivre un parcours défini par l'utilisateur via une interface web dynamique, en utilisant des coordonnées GPS.

Le robot est accessible en Wi-Fi et peut être contrôlé à distance via http://{ip du robot}

---

## Objectifs du projet

* Permettre à un utilisateur de définir un parcours géolocalisé
* Transmettre ce parcours au robot via un serveur web
* Faire déplacer le robot de manière autonome
* Utiliser les données GPS pour calculer l'orientation et la distance
* Détecter et éviter les obstacles

---

## Répartitions des tâches

Le projet repose sur quatres parties principales :

### 1. Pilotage du robot (Élève 1 : MAI--EMERY Alexandre)

* Contrôle des moteurs (avant, arrière, rotation)
* Gestion des déplacements
* Détection d'obstacles avec capteur ultrason

### 2. Navigation GPS (Élève 2 : MAI--EMERY Mickaël)

* Récupération de la position GPS du robot
* Calcul de la direction à suivre
* Ajustement de l’orientation pour atteindre une destination

### 3. Autonomie du robot et comportement (Élève 1 et 2)

* Mise en commun entre robot et GPS

### 3. Interface Web (Élève 3 : ONNO Aymeric)

* Création d’un site web accessible en Wi-Fi
* Saisie d’un parcours par l’utilisateur
* Stockage des données dans une base de données

---

## Technologies utilisées

* Python
* HTML / CSS / PHP
* Communication réseau (Wi-Fi)
* Base de données (SQL)
* Capteurs et robot (ultrason, GPS, moteurs robot)

---

## Compétences mises en œuvre

Ce projet nous a permis de travailler sur :

* l’algorithmique
* la programmation
* les systèmes embarqués
* la communication réseau
* travail en équipe et utilisation d’outils de versionnement (Git)

---

## Problèmes encore présents

* Lancement du fichier main.py impossible à partir du site (utilisation de ssh pour se connecter au robot puis utiliser sudo python3 ~/Desktop/PROJET/main.py)
* Comportement du robot aléatoire (raison : précision du gps trop faible : à chaque déplacement le robot ne voit pas le déplacement et va donc dans tous les sens)
* Évitement d'obstacle qui s'active de façon spontané alors qu'il n'y a pas d'obstacle parfois (imprécisions du capteur ultrason)


---

## Améliorations possibles

* Trouver des solutions pour que le site soit 100% fonctionnel avec le bouton "Lancer"
* Améliorer le site en lui apportant d'autres fonctionnalités (lecture de la console directement sur le site, meilleur esthétique...)
* Selon nous, avec le matériel mis à notre disposition, le projet est impossible à fonctionner selon les critère données:
  * Le GPS est imprécis et ne permet pas de diriger un robot sur des petits déplacements
  * Le capteur ultrason reste quelque chose de peu fiable et qui s'active sans notre demande

---

## Accès au projet

Le code source et les fichiers du projet sont disponibles dans ce dépôt https://github.com/AlexME77:projet-nsi ainsi que dans le dossier du projet dans le dépose travail.

---

## Auteurs

Projet réalisé en Terminale dans le cadre de la spécialité NSI :
* MAI--EMERY Alexandre : intervient sur :
  * capteur_ultrason.py
  * robot.py
  * navigation_robot.py
  * main.py
* Ressources utilisé par MAI--EMERY Alexandre :
  * Motor_Driver.py
  * PiSoftPwm.py
* MAI--EMERY Mickaël : intervient sur :
  * database.py
  * gps.py
  * main.py
* ONNO Aymeric : intervient sur :
  * Tous les fichiers php du site
  * La base de donnée parcours.db
