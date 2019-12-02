# -*-coding:Utf-8 -*

"""Ce fichier contient le code principal du jeu.

Exécutez-le avec Python pour lancer le jeu.

"""

import os
import sys
from robot import Robot
import labyrinthe

# import carte

#definitions des valeurs de sortie du programme roboc
SORTIE_ERREUR = -1
SORTIE_SUCCES = 0


from carte import Carte

def PlayRoboc(carte):
        """"
        Fonction de gestion du jeu
        :param : carte de jeu
        :return
        - true si c'est gagné
        - false sinon
        """
        # Affichage de l'aide
        carte.labyrinthe.printHelp()

        # Demande d'un choix au joueur
        choice = input("Jouer [A/N/S/E/O/Q] > ").lower()

        # On sépare le choix du joueur en une direction et un nombre de case
        (command, case) = carte.labyrinthe.splitChoice(choice)

        # On sort avec le choix 'q' ou quand la partie est gagnée
        while ((command != 'q') and (carte.labyrinthe.win == False)):
            #print("your choice : {}".format(self.splitChoice(command)))
            #print("You have chosen character \'{}\'".format(command))

            # Affichage de l'aide
            if (command == 'a'):
                carte.labyrinthe.printHelp()
            # Choix de direction
            elif (command == 'n' or command == 's' or command == 'e' or command == 'o'):
                #print("Need to chack position!")
                # On bouge le robot en fonction du choix
                carte.labyrinthe.CheckNextAndMove(command, int(case))
            #test pour savoir si c'est gagné ou non
            if carte.labyrinthe.win == False :
                # on sauvegarde automatiquement
                cartes[choix].save()
                # Next choice
                print(carte.labyrinthe)
                # On rejoue
                choice = input("Jouer [A/N/S/E/O/Q] > ").lower()
                (command, case) = carte.labyrinthe.splitChoice(choice)
        # Test de fin, on vérifie si on a gagné ou non
        if carte.labyrinthe.win == False:
            print("Vous avez demandé à sortir du labyrinthe")
            return False
        else:
            print(carte.labyrinthe)
            print("Félicitations, vous êtes sorti du labyrinthe :-)")
            return True


# On charge les cartes existantes
cartes = []
for nom_fichier in os.listdir("cartes"):
    #print("trouvé {} ".format(str(nom_fichier)))
    if nom_fichier.endswith(".txt"):
        chemin = os.path.join("cartes", nom_fichier)
        nom_carte = nom_fichier[:-4].lower()
        with open(chemin, "r") as fichier:
            contenu = fichier.read()
            # Création d'une carte
            nouvelle_carte = Carte(nom_carte, contenu)
        # Ajout de la carte à la liste des cartes
        cartes.append(nouvelle_carte)

# On vérifie qu'on a bien trouvé au moins une carte
if ( cartes != [] ):
    # On affiche les cartes existantes, dont les parties sauvegardées
    print("Labyrinthes existants :")
    for i, carte in enumerate(cartes):
        if  (carte.nom.endswith("_save") is True):
            print("  {} - {} (partie en cours)".format(i + 1, carte.nom))
        else:
            print("  {} - {}".format(i + 1, carte.nom))

    #print("Il y a \'{}\' cartes à jouer".format(len(cartes)))

    user_input = input("Entrez un numéro de labyrinthe pour commencer à jouer : ")

    # test de la valeur de l'entrée : entier ou non
    try:
       val = int(user_input)
    except ValueError:
       print("Ce n'est pas un entier, on sort")
       sys.exit(SORTIE_ERREUR)

    #on vérifie que le numéro est valide
    if (val <= 0 or val > len(cartes)):
        print("Choix non disponible, on sort.")
        sys.exit(SORTIE_ERREUR)
    else:
        #on sauvegarde le choix
        choix = val-1
        print("Vous avez choisi le labyrinthe {}".format(cartes[choix]))
        # print(type(cartes[choix].labyrinthe))

    #on recherche le robot
    print(cartes[choix].labyrinthe.FindRobot())

    # Début du jeu
    #if (cartes[choix].labyrinthe.Play() == False):
    if (PlayRoboc(cartes[choix]) == False):

        #print("Fin du jeu")
        if (cartes[choix].save() == True):
            print("Votre partie a été sauvegardée avec succès dans le fichier \'{}\'".format(cartes[choix].get_name_for_saving()))
        else:
            print("erreur de sauvegarde")
else:
    print("Aucune carte n'a été trouvée dans le dossier \'cartes\'!")

print("\nFin du programme Roboc")

sys.exit(SORTIE_SUCCES)
