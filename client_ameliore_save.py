import socket

from threading import Thread

class Interroger(Thread):
    def __init__(self, message,connexion_avec_serveur):

        Thread.__init__(self)

        self.message = message
        self.connexion_avec_serveur=connexion_avec_serveur

    def run(self):
        msg=input(self.message)
        self.connexion_avec_serveur.send(msg.encode())

class Recevoir(Thread):
    def __init__(self,connexion_avec_serveur):

        Thread.__init__(self)
        self.connexion_avec_serveur=connexion_avec_serveur
        

    def run(self):

        msg_recu = self.connexion_avec_serveur.recv(1024)
        self.msg_recu=msg_recu.decode()
        print(self.msg_recu)


hote = "localhost"
port = 12800

connexion_avec_serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connexion_avec_serveur.connect((hote, port))
print("Connexion établie avec le serveur sur le port {}".format(port))

rece=Recevoir(connexion_avec_serveur)
rece.start()
rece.join()


msg_recu=''
while not 'Voici' in  msg_recu :
 interrolab=Interroger("Choississez un labyrinthe pour commencer à jouer.\n",connexion_avec_serveur)
 recelab=Recevoir(connexion_avec_serveur)
 interrolab.start()
 recelab.start()
# interrolab.join()
 recelab.join()
 msg_recu=recelab.msg_recu
 

while not 'Fin' in  msg_recu :
 interroact=Interroger("Choississez une action.\n",connexion_avec_serveur)
 receact=Recevoir(connexion_avec_serveur)
 interroact.start()
 receact.start()
# interroact.join()
 receact.join()
 msg_recu=receact.msg_recu

#msg_fin=b""
#while msg_fin!=b"fin":
# msg_recu = b""
# while msg_recu != b"OK":
#     action=input("Choississez une action.\n")
#     connexion_avec_serveur.send(action.encode())
#     msg_recu = connexion_avec_serveur.recv(1024)
#     if msg_recu != b"OK":
#      print(msg_recu.decode())
#
# msg_recu = connexion_avec_serveur.recv(1024)
# print(msg_recu.decode())
# msg_fin = connexion_avec_serveur.recv(1024)




print("A bientot")
connexion_avec_serveur.close()
