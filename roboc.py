#!/usr/bin/python3.6
# -*-coding:Utf-8 -*
"""Code pour jouer au jeu du robot dans le labyrinthe"""

import labyrinthe
import sys
import socket
import select

#On allume la partie serveur
hote=''
port=12800
connexion_principale = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connexion_principale.bind((hote, port))
connexion_principale.listen(5)
print("Le serveur écoute à présent sur le port {}".format(port))
clients_connectes = []
count=0
i=0

while count<20:
 connexions_demandees, wlist, xlist = select.select([connexion_principale],
            [], [], 0.5)
 count=count+1
 for connexion in connexions_demandees:
     i=i+1
     connexion_avec_client, infos_connexion = connexion.accept()
  # On ajoute le socket connecté à la liste des clients
     clients_connectes.append(connexion_avec_client)
     connexion_avec_client.send(b'Bienvenue joueur {}.'.format(i))
if len(clients_connectes)==0:
  print('Personne ne veut jouer')
  exit()

#connexion_avec_client, infos_connexion = connexion_principale.accept()

#On importe les cartes, on salue le joueur et on lui propose les cartes
cartes=labyrinthe.Cartes()
msg_a_envoyer='Bienvenue.\nLe but du jeu est de faire sortir le robot (X) du labyrinthe, les O sont des murs, les . des portes et U est la sortie.\nVous pouvez quitter en entrant la lettre Q.\n'
msg_a_envoyer=msg_a_envoyer+cartes.__repr__()

nb_joueurs=len(clients_connectes)
print('ils sont ',nb_joueurs)
for client in clients_connectes:
    client.send(msg_a_envoyer.encode())

 #On lit le numero de la carte en verifiant que celle existe et que le joueur nous a bien donne un numero
choisir=True
while choisir:
 lire=True
 while lire:
  clients_a_lire = []
  try:
       clients_a_lire, wlist, xlist = select.select(clients_connectes,
              [], [], 0.05)
  except select.error:
      pass
  else:
      #if len(clients_a_lire)>1:
   for client in clients_a_lire:
     msg_recu = client.recv(1024)
     numero=msg_recu.decode()
     print(numero)
     lire=False

 try:
  numero=int(numero)
  assert numero >0 and numero<len(cartes)+1
 except ValueError:
     for client in clients_connectes:
         client.send(b'Vous devez saisir le numero de la carte.')
 except AssertionError:
     for client in clients_connectes:
         client.send(b'Vous avez choisi une carte qui n existe pas.')
 else:
  choisir=False
  lab=labyrinthe.Labyrinthe(cartes[numero-1],nb_joueurs)
  msg_a_envoyer='Voici le labyrinthe de depart:\n'+lab.__repr__()+'\n'+lab.print_actions()
  for client in clients_connectes:
      client.send(msg_a_envoyer.encode())


jouer=True
 #Boucle sur les mouvements du joueur
while jouer:
 i=-1
 for client in clients_connectes:
  if not jouer:
   break
  i=i+1
  client.send(b'A vous')
  choisir=True
  while choisir:
   msg_recu = client.recv(1024)
   action=msg_recu.decode()
   print(action)
   try:
    action=action.upper()
    assert action[0] in  {'Q'} or  action[0] in lab.actions.keys()
   except AttributeError:
    client.send(b'Vous devez taper la lettre correspondant a l action.')
   except AssertionError:
    client.send(b'Ceci n est pas une action valable')
   else:
    if action[0]=='M' or action[0]=='P':
     try:
      assert action[1] in  {'N','E','O','S'}
     except :
      client.send(b'Indiquer dans quel direction est le mur')
     else:
        choisir=False
    else:
     if len(action)>1:
      try:
       repetition=int(action[1:])
       assert repetition>0
      except ValueError:
       client.send(b'Apres l action, pour la repeter vous devez indiquer un nombre.')
      except AssertionError:
       client.send(b'Ce nombre de repetition n est pas valable.')
      else:
          choisir=False
     else:
      choisir=False
      repetition=1
  #On execute l action choisie
  if action[0]=='Q':
   jouer=False
   for client2 in clients_connectes:
       client2.send(b'Fin')
  elif action[0]=='M' or action[0]=='P':
   retour=lab.action(action[0],action[1],i)
   msg_a_envoyer=retour[0]+lab.__repr__()
   if retour[1]:
    jouer=False
    msg_a_envoyer=msg_a_envoyer+'\nFin'
    for client2 in clients_connectes:
        client2.send(msg_a_envoyer.encode())
   else:
       for client2 in clients_connectes:
           client2.send(msg_a_envoyer.encode())
  else:
   retour=lab.move(action[0],repetition,i)
   msg_a_envoyer=retour[0]+lab.__repr__()
  if retour[1]:
    jouer=False
    msg_a_envoyer=msg_a_envoyer+'\nFin'
    for client2 in clients_connectes:
       client2.send(msg_a_envoyer.encode())
  else:
       for client2 in clients_connectes:
           client2.send(msg_a_envoyer.encode())
 
print("Fermeture de la connexion")
connexion_avec_client.close()
connexion_principale.close()

sys.exit("A bientot")

