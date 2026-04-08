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

## Améliorations possibles

* A COMPLÉTER APRÈS AVOIR FINI

---

## Accès au projet

Le code source et les fichiers du projet sont disponibles dans ce dépôt.

---

## Auteurs

Projet réalisé en Terminale dans le cadre de la spécialité NSI :
* MAI--EMERY Alexandre : intervient sur :
  * tout le dossier capteurs
  * tout le dossier controle
  * tout le dossier motor
  * robot.py
  * main.py
* MAI--EMERY Mickaël : intervient sur :
  * tout le dossier gps
  * tout le dossier controle
  * main.py
* ONNO Aymeric : intervient sur :
  * tout le dossier du site
