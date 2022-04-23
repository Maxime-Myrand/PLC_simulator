# PLC_simulator
Simulation d'un PLC utilisant le protocole OPC-UA.

Je tâcherai d'être le plus précis prossible en expliquant comment mettre en marche ce petit logiciel pour que les personnes non familiarisées avec Python (krumkrumsteven...) puisse l'utiliser sans problème.

## Setup
#### Python
Python 3.9

Télécharger cette version à l'adresse suivante:

https://www.python.org/downloads/

Il est fort probable qu'il soit possible d'utiliser la version 3.10 de python. Nous ne l'avons pas testé, mais si quelqu'un juge nécessaire de tester si cette version fonctionne, nous pourrons tester sans problème.

#### Virtual environnement
Normalement, il est préférable d'utiliser un environnement virtuel python pour chaque projet. Nous pouvons faire un tel environnement ainsi:

###### Installation du logiciel permettant de créer des environnements virtuels
python -m pip install virtualenv
ou
python3 -m pip install virtualenv

###### Création de l'environnement
Il est suggérer d'effectuer ces commandes dans le dossier de ce projet. L'environnement sera créer à l'intérieur de ce dernier.
python -m venv simulator_env
ou
python3 -m venv simulator_env

###### Activation de l'environnement
Linux
cd simulator_env/bin
source activate

Windows
cd simulator_env/Script
activate

###### Installation des dépendances
Un fichier nommé requirements.txt est offert dans ce repo. Afin d'installer les dépendances, il suffit d'effectuer la commande suivante:
python -m pip install -r PATH/TO/requirements.txt
ou
python3 -m pip install -r PATH/TO/requirements.txt

## Utilisation
Il subsiste deux scripts dans ce repo: 1) le serveur et 2) le client. Ils sont dans deux dossiers différents et se nomment main.py tout les deux parce qu'il y a une convention en python voulant que le "coeur" d'un programme se nomme "main.py". Dans notre cas, nous avons deux "coeurs", donc deux main.py.

Nous suggérons d'ouvrir deux terminaux ou command prompt en tant qu'administrateur (utiliser sudo su sous Linux). Si vous n'êtes pas administrateur, vous ne pourrai utiliser la librairy "keyboard". Faites moi confiance ... Tout va bien aller........

Dans le terminier terminal ou dans la première invite de commande, naviguer dans le dossier Server_UPC-UA et utiliser la commande suivante:
python main.py
ou
python3 main.py

Dans le deuxième terminal ou dans la deuxième invite de commande, naviguer dans le dossier client_OPC-UA et utiliser la commande suivante:
python main.py
ou
python3 main.py

Ce faisant, nous devrions avoir des terminaux ressemblant à ceci (serveur à gauche et et client à droit:
![image](https://user-images.githubusercontent.com/81525565/164910114-e3ffd0ca-6ba3-4000-92c4-762eb9cb3fe0.png)

Le serveur dit qu'une raison expliquant l'arrêt de la machine doit être donné. Il s'agit uniquement de l'état de départ du serveur. L'idée est qu'il ne fait rien tant que la machine n'a pas été arrêtée. À droite, le client (la machine) attend que le boutton "marche" soit appuyé. Dans cette simulation, ce boutton est représenté par la touche "m". Lorsque cette touche est appuyée, nous obtenons ce résultat:

![image](https://user-images.githubusercontent.com/81525565/164910276-c54d32c9-070f-4913-8b84-6418e0a15bbe.png)

Maintenant, nous simulons que la machine fabrique des patates. Nous pouvons désromais simuler un arrêt. Pour se faire, nous devons appuyer longuement sur la touche "Alt". Ce faisant, nous obtenons ceci:

![image](https://user-images.githubusercontent.com/81525565/164910362-2e1a9c31-7869-4d19-9cce-3929d8416d79.png)

Désormais, la machine est sur pause pour ainsi dire. Elle attend une réponse du serveur qui va changer son état interne afin qu'elle redevienne "ativable". Pour ce faire dans le cadre de notre simulation, il faut donner une raison dans le serveur lui-même. La raison donner doit simplement être de cinq caractères ou plus. Aucune autre validation n'est effectuée.

![image](https://user-images.githubusercontent.com/81525565/164910474-4f49df16-0a36-4135-8ede-7dfb52aeeecd.png)

Après avoir appuyer sur "Enter", nous obtenons:

![image](https://user-images.githubusercontent.com/81525565/164910509-d8de62b6-4eb4-4f44-9c58-fddd8692f09b.png)

Nous voyons désormais qu'il est de nouveau possible d'activer la machine. En apuyyantsur "m" du côté client, nous obtenons ceci:

![image](https://user-images.githubusercontent.com/81525565/164910578-39c2e321-1fd7-4ef5-9451-ae17d751d441.png)

La machine est désormais de nouveau en fonction.


## Optimisation
Afin d'améliorer la simulation, il pourrait être intéressant d'ajouter un boutton virtuel à l'application plutôt que d'utiliser les touches du clavier. En effet, en ce moment, la machine ne peut être réactivée parce qu'elle se met en état d'attente d'une réponse du serveur. La manière dont la machine est programmée ne permetterait pas de la relancer même si nous pouvions appuyer sur "m". Cependant, présentement, cette touche ne peut être appuyer présentement lorsque la machine est en mode "attente du serveur". Ainsi, afin de simuler le mieux possible, il serait intéressant d'ajouter un boutton cliquable à tout instant et de voir qu'il ne fonctionne pas lorsque le serveur n'a pas spécifié que la machine peut être relancé.

Désolé pour les coquilles, je corrige tout ça lundi. J'ai tout écris d'un seul jet et c'est la fin de semaine tsais!





