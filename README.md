# Powerfull Background

## Mais keskecé ?

C'est un projet d'un petit programme python me permettant d'avoir un fond d'écran avec ma conso cpu, ram, network
(pour l'instant) sur mon fond d'écran.

C'est codé en python pour mon kali linux xfce, je n'ai pas encore réfléchi à la portabilité sur d'autres distribs.

### Early preview

![preview_1](preview_1.png)

## Ça doit manger des ressources ?

Oui et non, avec un i5 dernière génération, cela consomme entre 1 et 3% de cpu.

## Installation

### Prérequis

- python3
- pip3
- un terminal avec accès root

**ATTENTION, Xfce est le seul environnement supporté pour l'instant**

```bash
git clone https://github.com/Farmeurimmo/PowerfullBackground.git
```

```bash
cd PowerfullBackground
```
**ATTENTION, sudo est obligatoire pour l'installation**
```bash
sudo python3 setup.py
```

## Désinstallation

```bash
cd PowerfullBackground
```
**ATTENTION, sudo est obligatoire pour la désinstallation**
```bash
sudo python3 uninstall.py
```
Tous les processus/services sont arrêtés et supprimés.
Le dossier PowerfullBackground n'est pas supprimé, vous pouvez le supprimer manuellement ou non.

### credits image

https://pixabay.com/fr/photos/fantaisie-la-grotte-mystique-roche-2750995/