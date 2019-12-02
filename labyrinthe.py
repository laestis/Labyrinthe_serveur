# -*-coding:Utf-8 -*
import re
from robot import  Robot

"""Ce module contient la classe Labyrinthe."""

class Labyrinthe:

    """Classe représentant un labyrinthe."""

    def __init__(self):
        """
        Fonction d'initialisation
        parametres :
        :param robot: contient l'objet robot
        :param grille: grille de jeu
        :param dimension: dimension du labyinthe (abscisses, ordonnées)
        :param win: booléean pour sauvergarder le labyrhinthe gagné/perdu
        """
        #print("init")
        self.robot = Robot()
        self.grille = {}
        self.dimension = {"abs": 0, "ord": 0 }
        # ...creer_labyrinthe_depuis_chaine
        self.win = False

    def creer_labyrinthe_depuis_chaine(self, chaine):
        """"
        Fonction de création du labyrinthe
        :param: chaine de caractère
        """
        #print("creer_labyrinthe_depuis_chaine\n{}".format(chaine))
        # recherche des dimensions
        nb_lignes = 0
        nb_colonnes = 0
        for ligne in chaine.splitlines():
            #print("Ligne {} len {}".format(nb_lignes, len(ligne)))
            # need to check if the line is empty or not
            if len(ligne) > 0 :
                nb_lignes +=1
            if (nb_colonnes == 0):
                #print("updating nb_colonnes from {} to {}".format(nb_colonnes, len(ligne)))
                nb_colonnes = len(ligne)
            #elif (nb_colonnes != len(ligne)):
            #    print("warning nb_colonnes is {} and found {} in line".format(nb_colonnes, len(ligne)))

        #print("On a trouvé \'{}\' lignes and \'{}\' colonnes".format(nb_lignes, nb_colonnes))

        # mise à jour du parametre dimension
        self.dimension["abs"] = nb_colonnes
        self.dimension["ord"] = nb_lignes
        nb_x_grille = nb_colonnes
        nb_y_grille = nb_lignes

        #creation de la grille vide
        new_grille = [[]] * self.dimension["abs"]
        for abs_x in range(self.dimension["abs"]):
            #print("filling abs {}".format(abs_x))
            new_grille[abs_x] = ['-'] * self.dimension["ord"]

        #print(new_grille)
        #print("{}-{} char {}".format(0, 10, new_grille[0][10]))

        # remplissage de la grille avec les paramètres de la chaine de caractères
        index_ligne = 0
        for ligne in chaine.splitlines():
            if len(ligne) > 0:
                # print("ligne N° {} : len {} -> \'{}\'".format(index_ligne, len(ligne), ligne))
                index_colonne = 0
                while index_colonne < nb_colonnes :
                    onechar = ligne[index_colonne]
                    #print("{}-{} char \'{}\'".format(index_colonne, nb_lignes-index_ligne-1, onechar))
                    new_grille[index_colonne][nb_lignes-index_ligne-1] = onechar
                    #looking for cursor
                    if (onechar.lower() == 'x'):
                        #print("setting robot in {}-{}".format(index_colonne, nb_lignes-index_ligne-1))
                        self.robot = Robot(index_colonne, nb_lignes-index_ligne-1)
                    index_colonne +=1
                index_ligne +=1
        #print("fin de creer labyrinthe")

        # Mise à jour de la grille avec l'import de chaine de caractères
        self.grille = new_grille

    def __repr__(self):
        """
        Représentation de la classe labyrinthe
        :return: chaine de caractères
        """
        text = "\n"
        #nb_x_grille = len(self.grille)
        #nb_y_grille = len(self.grille[0])
        #print("Grille nb_x_grille {} nb_y_grille {}".format(nb_x_grille, nb_y_grille))

        index_x = 0
        index_y = self.dimension["ord"] - 1

        while index_y >= 0 :
            ligne_str = ""
            index_x = 0

            while index_x < self.dimension["abs"] :
                ligne_str = ligne_str + self.grille[index_x][index_y]
                index_x +=1

            text = text + ligne_str + "\n"
            index_y -= 1
        # renvoi du text
        return text

    def CheckNextAndMove(self, direction, case):
        """
        Fonction de gestion du jeu
        :param direction: direction du robot (n/s/e/o)
        :param case: nombre de cases
        :return:
        """
        #print("checking position")
        #print("robot in position {}-{} value is \'{}\'".format(self.robot.pos_x , self.robot.pos_y ,self.grille[self.robot.pos_x][self.robot.pos_y]))
        next_case = {"pos_x":self.robot.pos_x, "pos_y":self.robot.pos_y}
        i = 0
        intowall = False
        while (i < case and intowall == False ):
            if direction == 'n':
                #print("N -> target case is {}-{}, value is \'{}\'".format(self.robot.pos_x, self.robot.pos_y+1, self.grille[self.robot.pos_x][self.robot.pos_y-1]))
                next_case["pos_y"] = next_case["pos_y"]+1
            elif direction == 's':
                #print("S -> target case is {}-{}, value is \'{}\'".format(self.robot.pos_x, self.robot.pos_y-1, self.grille[self.robot.pos_x][self.robot.pos_y+1]))
                next_case["pos_y"] = next_case["pos_y"]-1
            elif direction == 'e':
                #print("E -> target case is {}-{}, value is \'{}\'".format(self.robot.pos_x+1, self.robot.pos_y, self.grille[self.robot.pos_x+1][self.robot.pos_y]))
                next_case["pos_x"] = next_case["pos_x"]+1
            elif direction == 'o':
                #print("O -> target case is {}-{}, value is \'{}\'".format(self.robot.pos_x-1, self.robot.pos_y, self.grille[self.robot.pos_x-1][self.robot.pos_y]))
                next_case["pos_x"] = next_case["pos_x"]-1

            # On teste la valeur de la prochaine case (vide/mur/porte/sortie)
            if (self.grille[next_case["pos_x"]][next_case["pos_y"]] == 'O') :
                print("Vous avez foncé dans le mur, vous devez changer de direction!")
                intowall = True
            elif (self.grille[next_case["pos_x"]][next_case["pos_y"]] == 'U') :
                print("Très bon choix !")
                # on met à jour la parametre de statut de la partie
                self.win = True
                if self.robot.ThroughDoor == True:
                    self.grille[self.robot.pos_x][self.robot.pos_y] = '.'
                    # Updating door parameter
                    self.robot.ThroughDoor = False
                else:
                    self.grille[self.robot.pos_x][self.robot.pos_y] = ' '
                    # Updating door parameter
                    self.robot.ThroughDoor = False

                #setting the robot to the new position
                self.robot.pos_x = next_case["pos_x"]
                self.robot.pos_y = next_case["pos_y"]
                self.grille[self.robot.pos_x][self.robot.pos_y] = 'X'

            # gestion des portes
            elif (self.grille[next_case["pos_x"]][next_case["pos_y"]] == '.') :
                #print("Moving from {}-{} to {}-{}".format(self.robot.pos_x, self.robot.pos_y, next_case["pos_x"], next_case["pos_y"]))

                if self.robot.ThroughDoor == True:
                    self.grille[self.robot.pos_x][self.robot.pos_y] = '.'
                    # Updating door parameter
                    self.robot.ThroughDoor = True
                else:
                    self.grille[self.robot.pos_x][self.robot.pos_y] = ' '
                    # Updating door parameter
                    self.robot.ThroughDoor = True

                #setting the robot to the new position
                self.robot.pos_x = next_case["pos_x"]
                self.robot.pos_y = next_case["pos_y"]
                self.grille[self.robot.pos_x][self.robot.pos_y] = 'X'
            # la case est vide
            else:
                #print("Moving from {}-{} to {}-{}".format(self.robot.pos_x, self.robot.pos_y, next_case["pos_x"], next_case["pos_y"]))
                # making the case a free case

                if self.robot.ThroughDoor == True:
                    self.grille[self.robot.pos_x][self.robot.pos_y] = '.'
                    # Updating door parameter
                    self.robot.ThroughDoor = False
                else:
                    self.grille[self.robot.pos_x][self.robot.pos_y] = ' '
                    # Updating door parameter
                    self.robot.ThroughDoor = False

                #setting the robot to the new position
                self.robot.pos_x = next_case["pos_x"]
                self.robot.pos_y = next_case["pos_y"]
                self.grille[self.robot.pos_x][self.robot.pos_y] = 'X'

            i+=1

    def FindRobot(self):
        """
        Fontion de recherche de robot, on cherche un X dans la grille
        :return: mise à jour de self
        """

        nb_x_grille = self.dimension["abs"]
        #Robot (self.grille)
        nb_y_grille = self.dimension["ord"]
        # len(self.grille[0])

        index_x = 0
        index_y = nb_y_grille - 1

        while index_y >= 0 :
            ligne_str = "|"
            index_x = 0

            while index_x < nb_x_grille :
                if self.grille[index_x][index_y].lower() == 'x':
                    self.robot.pos_x = index_x
                    self.robot.pos_y = index_y
                    #print("found the robot in position {}".format(self.robot))
                    return self
                index_x +=1
            index_y -= 1

        print("Error, Robot not found")

    def Play(self):
        """"
        Fonction de gestion du jeu
        :return
        - true si c'est gagné
        - false sinon
        """
        # Affichage de l'aide
        self.printHelp()

        # Demande d'un choix au joueur
        choice = input("Jouer [A/N/S/E/O/Q] > ").lower()

        # On sépare le choix du joueur en une direction et un nombre de case
        (command, case) = self.splitChoice(choice)

        # On sort avec le choix 'q' ou quand la partie est gagnée
        while ((command != 'q') and (self.win == False)):
            #print("your choice : {}".format(self.splitChoice(command)))
            #print("You have chosen character \'{}\'".format(command))

            # Affichage de l'aide
            if (command == 'a'):
                self.printHelp()
            # Choix de direction
            elif (command == 'n' or command == 's' or command == 'e' or command == 'o'):
                #print("Need to chack position!")
                # On bouge le robot en fonction du choix
                self.CheckNextAndMove(command, int(case))
            #test pour savoir si c'est gagné ou non
            if self.win == False :
                # Next choice
                print(self)
                # On rejoue
                choice = input("Jouer [A/N/S/E/O/Q] > ").lower()
                (command, case) = self.splitChoice(choice)
        # Test de fin, on vérifie si on a gagné ou non
        if self.win == False:
            print("Vous avez demandé à sortir du labyrinthe")
            return False
        else:
            print(self)
            print("Félicitations, vous êtes sorti du labyrinthe :-)")
            return True

    def splitChoice(choice):
        """
         Fonction de separation d'une chaine de caractère en une lettre et un nombre
         :param choice: choix du joueur, chaine de caractère
         :return
          - tuple avec lettre et chiffre"""
        # On autorise un seul caractère suivi de chiffres
        m = re.match(r"([a-z])([0-9]*)", choice)
        # on teste l'entrée
        try:
            x, y = m.groups()
            # initialisation de la variable x
            if x == '': x = None

            # default number of case is one
            if y == '': y = 1
        except:
            # entrée incorrecte, on affiche l'aide
            print("Entrée incorrecte !")
            x = 'a'
            y = 1

        # renvoi du résultat
        return ((x, y))

    """ static method to display help"""
    def printHelp():
        print("Options de jeu disponibles:")
        print("A : pour Aide")
        print("N : pour Nord (vers le haut")
        print("S : pour Sud (vers le bas)")
        print("O : pour Ouest (vers la gauche)")
        print("E : pour Est (vers la droite)")
        print("Q : pour Quitter et Sauvegarder")
        print("Chacune des directions ci-dessus suivies d'un nombre permet d'avancer de plusieurs cases : ")
        print(" - exemple \'E3\' permet de se déplacer de trois cases vers l'Est (si possible)")
        print(" - exemple \'N2\' permet de se déplacer de deux cases vers le Nord (si possible)")

    def grilletodata(self):
        """
        Fonction d'une conversion d'une grille en chaine de caractères
        :return: chaine de caractères prête à écrire
        """
        text = ""
        index_y = self.dimension["ord"] - 1
        while index_y >= 0:
            ligne_str = ""
            index_x = 0
            while index_x < self.dimension["abs"]:
                ligne_str = ligne_str + self.grille[index_x][index_y]
                index_x += 1

            text = text + ligne_str + "\n"
            index_y -= 1
        return text

    # Methodes statiques
    printHelp = staticmethod(printHelp)
    splitChoice = staticmethod(splitChoice)
