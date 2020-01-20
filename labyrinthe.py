#!/usr/bin/python3.6
# -*-coding:Utf-8 -*
import pickle
import os
from random import randrange


class Cartes(list):
 """Classe derivée des listes que l on modifie pour la rendre spécifique aux cartes"""
 
 def __init__(self):
  """Inialisation de l objet cartes comme une liste"""
  
  fichier='liste_cartes'
  if os.path.exists(fichier):
   with open(fichier,'rb') as fichier_cartes:
    depickler = pickle.Unpickler(fichier_cartes)
    liste_temp=depickler.load()
    list.__init__(self,liste_temp)
  else:
   list.__init__(self,{'facile.txt','prison.txt'})

 def save(self):
  """Methode pour sauvegarder la liste des cartes"""

  fichier='liste_cartes'
  with open(fichier,'wb') as fichier_cartes:
   pickleur = pickle.Pickler(fichier_cartes)
   pickleur.dump(self) 
 

 def __repr__(self):
  """Methode pour ecrire la liste de cartes disponibles"""
  cartes=str()
  cartes='Les cartes diponibles sont: \n'
  for i,value in enumerate(self):
   cartes+='{}: {}\n'.format(i+1,value)

  return cartes



class Labyrinthe():
 """Classe pour creer manipuler le labyrinthe, aussi bien son etat que les actions autorisees dessus"""
 
 def __init__(self,fichier_carte,nb_joueurs):
  """Chargeons le labyrinthe, trouvons le robot et definissons les actions autorisees"""

  #on charge le labyrinthe
  with open(fichier_carte,'r') as carte:
   self.labyrinthe=carte.read()
  
  #On cherche le robot deja present dans le fichier pour l'enlever
  if self.labyrinthe.find('X')!=-1:
   self.labyrinthe=self.labyrinthe.replace('X',' ')

# On place des robots de facon aleatoire, autant de robots que de joueurs
  self.pos_rob=list()
  i=0
  while i<nb_joueurs:
   self.pos_rob.append(-1)
   rob_a_placer=True
   while rob_a_placer:
    self.pos_rob[i]=randrange(0,len(self.labyrinthe))
    if self.labyrinthe[self.pos_rob[i]]==' ':
     self.labyrinthe=self.labyrinthe[:self.pos_rob[i]]+'x'+self.labyrinthe[self.pos_rob[i]+1:]
     rob_a_placer=False
   i=i+1


  #Quelques variables de travail a definir
  lab_line=self.labyrinthe.splitlines()
  self.n_lig=len(lab_line)
  self.n_col=len(lab_line[0])
  self.der_robot=list()
  i=0
  while i<nb_joueurs:
   self.der_robot.append(' ')
   i=i+1
  
  #Initialisation des mouvements autorises pour le robot
  self.actions=dict(N='Aller vers le nord/haut',S='Aller vers le sud/bas',E='Aller vers l est/gauche',O='Aller vers l ouest/droite',M='Murer une porte',P='Percer une porte')


 def __repr__(self):
  """Afficher le labyrinthe a l utilisateur"""

  return self.labyrinthe+'\n'

 def display(self,joueur):
  """Afficher le labyrinthe a un joueur. Son robot est alors mis en majuscule"""

  lab_joueur=self.labyrinthe[:self.pos_rob[joueur]]+'X'+self.labyrinthe[self.pos_rob[joueur]+1:]
  
  return lab_joueur


 def action(self,act,direction,joueur):
  """Fonction pour faire une action sur le labyrinthe, act est soit M pour murer soit P pour percer, la direction est E,O,N,S"""

  fini=False
  message=str()

  #On regarde ou on doit agir
  if direction=='N':
   pos_act=self.pos_rob[joueur]-self.n_col-1
  elif direction=='S':
   pos_act=self.pos_rob[joueur]+self.n_col+1
  elif direction=='O':
   pos_act=self.pos_rob[joueur]-1
  elif direction=='E':
   pos_act=self.pos_rob[joueur]+1
  else:
   message="L action n est pas valide.\n"
   return (message,fini)   

  #On fait l action si elle est possible
  if act=='M':
   if self.labyrinthe[pos_act]==' ' or  self.labyrinthe[pos_act]=='.':
    message="On a mure"
    self.labyrinthe=self.labyrinthe[:pos_act]+'O'+self.labyrinthe[pos_act+1:]
   else:
    message="On ne peut pas murer ici.\n"
    return (message,fini)
  elif act=='P':
   if self.labyrinthe[pos_act]=='O':
    message="On a perce.\n"
    self.labyrinthe=self.labyrinthe[:pos_act]+' '+self.labyrinthe[pos_act+1:]
   else:
    message="On ne peut pas percer ici.\n"
    return (message,fini)
  else:
   message="L action n est pas valide.\n"
   return (message,fini)

  return (message,fini)

 def move(self,cote,repetition,joueur):
  """Fonction pour faire bouger le robot, cote doit avec la valeur N, S, E, O exclusivement"""

  fini=False
  message=str()

  lab_joueur=self.labyrinthe[:self.pos_rob[joueur]]+'X'+self.labyrinthe[self.pos_rob[joueur]+1:]
  #On regarde ou ira le robot avec le mouvement propose
  i=0
  while(i<repetition):
   if cote=='N':
    nouv_pos=self.pos_rob[joueur]-self.n_col-1
   elif cote=='S':
    nouv_pos=self.pos_rob[joueur]+self.n_col+1
   elif cote=='E':
    nouv_pos=self.pos_rob[joueur]+1
   elif cote=='O':
    nouv_pos=self.pos_rob[joueur]-1
   else :
    message="L action n est pas valide.\n"
    return (message,fini)
 

  #On regarde si le mouvement est permis, si il l est on effectue, si on se trouve a la sortie on decrete la fin de la partie
   if lab_joueur[nouv_pos]==' ' or lab_joueur[nouv_pos]=='.':
    self.pos_rob[joueur]=nouv_pos
    lab_joueur=lab_joueur.replace('X',self.der_robot[joueur])
    self.der_robot[joueur]=lab_joueur[self.pos_rob[joueur]]
    lab_joueur=lab_joueur[:self.pos_rob[joueur]]+"X"+lab_joueur[self.pos_rob[joueur]+1:]
    message+='Mouvement {}{}  effectue.\n'.format(cote,i+1)
   elif self.labyrinthe[nouv_pos]=='U':
    self.pos_rob[joueur]=nouv_pos
    lab_joueur=lab_joueur.replace('X',self.der_robot[joueur])
    self.der_robot[joueur]=lab_joueur[self.pos_rob[joueur]]
    lab_joueur=lab_joueur[:self.pos_rob[joueur]]+"X"+self.labyrinthe[self.pos_rob[joueur]+1:]
    message+='Bravo vous avez gagne.\n'
    fini=True
   else:
    message+='Mouvement {}{} interdit.\n'.format(cote,i+1)
   i+=1

  self.labyrinthe=lab_joueur.replace('X','x')
  #On renvoie le message a donner au joueur et un booleen indiquant si la partie est finie  
  return (message,fini)


 def save(self,fichier_carte):
  """Pour sauvegardr la carte dans un fichier"""

  with open(fichier_carte,'w') as carte:
   carte.write(self.labyrinthe)
 

 def print_actions(self):
  """Pour afficher les mouvements autorises pour le robot"""

  actions=str()
  actions='Les actions disponibles sont:\n'
  for i,value in self.actions.items():
   actions+='{}: {}\n'.format(i,value)
  actions+="Les actions peuvent etre utilisee plusieurs fois en indiquant un nombre apres l action.\n"

  return actions

