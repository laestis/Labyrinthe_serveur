import socket

import threading


class Interroger(threading.Thread):
    def __init__(self, message,connexion_avec_serveur):

        threading.Thread.__init__(self)

        self.message = message
        self.connexion_avec_serveur=connexion_avec_serveur
        self._stop_event = threading.Event()

    def run(self):
        msg=input(self.message)
        self.connexion_avec_serveur.send(msg.encode())

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()


class Recevoir(threading.Thread):
    def __init__(self,connexion_avec_serveur):

        threading.Thread.__init__(self)
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
 recelab.join()
 interrolab.stop()
 interrolab.join()
 msg_recu=recelab.msg_recu

while not 'Fin' in  msg_recu :
 while not 'A vous' in  msg_recu :
  recelab=Recevoir(connexion_avec_serveur)
  recelab.start()
  recelab.join()
  msg_recu=recelab.msg_recu

 interroact=Interroger("Choississez une action.\n",connexion_avec_serveur)
 receact=Recevoir(connexion_avec_serveur)
 interroact.start()
 receact.start()
 receact.join()
 interroact.stop()
 interroact.join()
 msg_recu=receact.msg_recu

print("A bientot")
connexion_avec_serveur.close()
