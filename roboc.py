#!/usr/bin/python3.6
# -*-coding:Utf-8 -*
"""Code pour jouer au jeu du robot dans le labyrinthe, en mode client/serveur, un joueur ou plusieurs joueurs. Ici on a le code serveur."""

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

#Connection des joueurs,apres connection du premier joueur on attend 15s pour que d autres nous rejoinent

pas_de_joueurs=True
#On attend le premier joueur
while pas_de_joueurs:
 connexions_demandees, wlist, xlist = select.select([connexion_principale],
            [], [], 0.5)
 for connexion in connexions_demandees:
    connexion_avec_client, infos_connexion = connexion.accept()
  # On ajoute le socket connecté à la liste des clients
    clients_connectes.append(connexion_avec_client)
    pas_de_joueurs=False 

#On laisse un peu de temps aux autres joueurs pour se connecter
while count<30:
 connexions_demandees, wlist, xlist = select.select([connexion_principale],
            [], [], 0.5)
 count=count+1
 for connexion in connexions_demandees:
     connexion_avec_client, infos_connexion = connexion.accept()
  # On ajoute le socket connecté à la liste des clients
     clients_connectes.append(connexion_avec_client)

#nombre de joueurs pour la partie
nb_joueurs=len(clients_connectes)

#On importe les cartes, on salue le/les joueurs et on propose les cartes
cartes=labyrinthe.Cartes()
msg_cartes='Le but du jeu est de faire sortir le robot (X) du labyrinthe, les O sont des murs, les . des portes et U est la sortie.\nVous pouvez quitter en entrant la lettre Q.\n'
msg_cartes=msg_cartes+cartes.__repr__()

#Le joueur 1 est celui qui choisit la carte
i=0
for client in clients_connectes:
 if i!=0:
  msg_a_envoyer='Bienvenue joueur '+str(i+1)+'\n.'+msg_cartes+'On attend que le joueur 1 choississe le labyrinthe.\n'
 else :
  msg_a_envoyer='Bienvenue joueur '+str(i+1)+'\n.'+msg_cartes+'Choississez un labyrinthe pour commencer à jouer.\n'
 client.send(msg_a_envoyer.encode())
 i=i+1

 #On lit le numero de la carte en verifiant que celle ci existe et que le joueur nous a bien donne un numero
choisir=True
while choisir:
 msg_recu = clients_connectes[0].recv(1024)
 numero=msg_recu.decode()
 print(numero)
 lire=False
 try:
  numero=int(numero)
  assert numero >0 and numero<len(cartes)+1
 except ValueError:
  clients_connectes[0].send(b'Vous devez saisir le numero de la carte.')
 except AssertionError:
  clients_connectes[0].send(b'Vous avez choisi une carte qui n existe pas.')
 else:
  choisir=False
  lab=labyrinthe.Labyrinthe(cartes[numero-1],nb_joueurs)
  i=0
# Une fois le choix fait on envoie le labyrinthe a tos les joueurs
  for client in clients_connectes:
   msg_a_envoyer='Voici le labyrinthe de depart:\n'+lab.display(i)+'\n'+lab.print_actions()
   client.send(msg_a_envoyer.encode())
   i=i+1


jouer=True
while jouer:
 i=-1
 #Les joueurs jouent chacun leur tours
 for client in clients_connectes:
#Si le jeu est fini on sort
  if not jouer:
   break
  i=i+1
  client.send(b'A vous')
  choisir=True
  while choisir:
 #on verifie que le joueur a choisi une action conforme
   msg_recu = client.recv(1024)
   action=msg_recu.decode()
   print(action)
   try:
    action=action.upper()
    assert action[0] in  {'Q'} or  action[0] in lab.actions.keys()
   except AttributeError:
    client.send(b'Vous devez taper la lettre correspondant a l action.\n A vous.\n')
   except AssertionError:
    client.send(b'Ceci n est pas une action valable.\n A vous.\n')
   else:
    if action[0]=='M' or action[0]=='P':
     try:
      assert action[1] in  {'N','E','O','S'}
     except :
      client.send(b'Indiquer dans quel direction est le mur.\n A vous.\n')
     else:
        choisir=False
    else:
     if len(action)>1:
      try:
       repetition=int(action[1:])
       assert repetition>0
      except ValueError:
       client.send(b'Apres l action, pour la repeter vous devez indiquer un nombre.\n A vous.\n')
      except AssertionError:
       client.send(b'Ce nombre de repetition n est pas valable.\n A vous.\n')
      else:
          choisir=False
     else:
      choisir=False
      repetition=1
  #On execute l action choisie
  #Si un joueur fait une action non valide il perd son tour
  #Si on envoie fin le client ferme la connection
  if action[0]=='Q':
   jouer=False
   for client2 in clients_connectes:
       client2.send(b'Fin')
  elif action[0]=='M' or action[0]=='P':
   retour=lab.action(action[0],action[1],i)  
   j=0
   for client2 in clients_connectes:
     msg_a_envoyer=retour[0]+lab.display(j)
     if retour[1]:
      jouer=False
      msg_a_envoyer=msg_a_envoyer+'\nFin'
     client2.send(msg_a_envoyer.encode())
     j=j+1
  else:
   retour=lab.move(action[0],repetition,i)
   j=0
   for client2 in clients_connectes:
    msg_a_envoyer=retour[0]+lab.display(j)
    if retour[1]:
     jouer=False
     msg_a_envoyer=msg_a_envoyer+'\nFin'
    client2.send(msg_a_envoyer.encode())
    j=j+1
 
print("Fermeture de la connexion")
connexion_avec_client.close()
connexion_principale.close()

sys.exit("A bientot")

