"""Code pour jouer au jeu du robot dans le labyrinthe, en mode client/serveur, un joueur ou plusieurs joueurs. Ici on a le code client."""
import socket

hote = "localhost"
port = 12800

connexion_avec_serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connexion_avec_serveur.connect((hote, port))
print("Connexion établie avec le serveur sur le port {}".format(port))

#On recoit le message d accueil
msg_recu = connexion_avec_serveur.recv(1024).decode()
print(msg_recu)

#Si on est le joueur un on choisit le labyrinthe sinon on attend le choix du joueur un
if 'Choississez' in msg_recu:
 msg_recu=''
 while not 'Voici' in  msg_recu :
  numero=input('')
  connexion_avec_serveur.send(numero.encode())
  msg_recu = connexion_avec_serveur.recv(1024).decode()
  print(msg_recu)
else:
 msg_recu = connexion_avec_serveur.recv(1024).decode()
 print(msg_recu)

#Quand c est a nous de jouer on choisit une action. Quand le serveur envoie fin en sort de la boucle et on clot la connecion
while not 'Fin'  in  msg_recu :
 if 'A vous' in msg_recu:  
  action= input('Choississez une action\n')
  connexion_avec_serveur.send(action.encode())

 msg_recu = connexion_avec_serveur.recv(1024).decode()
 print(msg_recu)


print("A bientot")
connexion_avec_serveur.close()
