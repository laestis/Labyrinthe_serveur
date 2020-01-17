import socket

hote = "localhost"
port = 12800

connexion_avec_serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connexion_avec_serveur.connect((hote, port))
print("Connexion établie avec le serveur sur le port {}".format(port))

msg_a_envoyer = b""
msg_recu = b""
msg_recu = connexion_avec_serveur.recv(1024)
print(msg_recu.decode()) 
msg_recu = connexion_avec_serveur.recv(1024)
print(msg_recu.decode()) 
while msg_recu != b"OK":
    numero=input("Choississez un labyrinthe pour commencer à jouer.\n")
    connexion_avec_serveur.send(numero.encode())
    msg_recu = connexion_avec_serveur.recv(1024)
    print(msg_recu.decode()) 

msg_recu = connexion_avec_serveur.recv(1024)
print(msg_recu.decode())

msg_fin=b""
while msg_fin!=b"fin":
 msg_recu = b""
 while msg_recu != b"OK":
     action=input("Choississez une action.\n")
     connexion_avec_serveur.send(action.encode())
     msg_recu = connexion_avec_serveur.recv(1024)
     if msg_recu != b"OK":
      print(msg_recu.decode())

 msg_recu = connexion_avec_serveur.recv(1024)
 print(msg_recu.decode())
 msg_fin = connexion_avec_serveur.recv(1024)




print("A bientot")
connexion_avec_serveur.close()
