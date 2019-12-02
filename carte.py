# -*-coding:Utf-8 -*

from labyrinthe import Labyrinthe

"""Ce module contient la classe Carte."""

class Carte:

    """Objet de transition entre un fichier et un labyrinthe."""

    def __init__(self, nom, chaine):
        """"
        Fonction d'initialisation
          - nom : nom de la carte
          - labyrinthe : labyrinthe de jeu
        """
        self.nom = nom
        self.labyrinthe = Labyrinthe()
        self.labyrinthe.creer_labyrinthe_depuis_chaine(chaine)

    def __repr__(self):
        """"
        Fonction de representation de carte pour son affichage
        """
        return "<Carte {}>".format(self.nom)

    def get_name_for_saving(self):
        """"
        Récupération du nom de la carte pour sauvegarde
        Retourne le nom du fichier en chaine de caractères
        """
        # Checking if the game has already been saved
        if (self.nom.endswith("_save") is True):
            filename = self.nom + ".txt"
        else:
            filename = self.nom + "_save.txt"
        return filename

    def save(self):
        """"
        Fonction de sauvegarde de carte dans un fichier texte
        Retourne :
        - True si succes
        - False si erreur
        """
        path = "cartes/" + self.get_name_for_saving()

        # ouverture sans test préalable
        fh = open(path, "w")
        try:
            fh.write(self.labyrinthe.grilletodata())
            # caractère de fin optionnel
            fh.write("\n")
        finally:
            fh.close()
            #fichier créé
            return True

        return False

