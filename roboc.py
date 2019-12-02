#!/usr/bin/python3.6
# -*-coding:Utf-8 -*
"""Code pour jouer au jeu du robot dans le labyrinthe"""

import labyrinthe
import sys

#On importe les cartes, on salue le joueur et on lui propose les cartes
cartes=labyrinthe.Cartes()
print('Bienvenue.\nLe but du jeu est de faire sortir le robot (X) du labyrinthe, les O sont des murs, les . des portes et U est la sortie.\nVous pouvez quitter en entrant la lettre Q.\n')
print(cartes)

#On lit le numero de la carte en verifiant que celle existe et que le joueur nous a bien donne un numero
choisir=True
while choisir:
 numero=input("Choississez un labyrinthe pour commencer à jouer.\n")
 try:
  numero=int(numero)
  assert numero >0 and numero<len(cartes)+1
 except ValueError:
  print('Vous devez saisir le numero de la carte.')
 except AssertionError:
  print('Vous avez choisi une carte qui n existe pas.') 
 else:
  choisir=False
#On sauvegarde cette partie sous un nouveau nom
choisir=True
while choisir:
 nom_sauv=input("Quel nom voulez vous donner a votre partie? Vous pouvez choisir un nom deja existant la partie sera alors ecrasee.\n")
 print(nom_sauv.isalpha())
 try:
  nom_sauv.strip()
  assert nom_sauv.isalpha()
 except AssertionError:
  print('Le nom doit etre uniquement compose de lettres')
 except:
  print('Nom invalide')
 else:
  choisir=False
  if nom_sauv not in cartes:
   cartes.append(nom_sauv)


#On initialise le labyrinthe puis on l affiche
lab=labyrinthe.Labyrinthe(cartes[numero-1])
print('Voici le labyrinthe de depart:\n')
print(lab)
print('\n')

#On propose au joueur les actions du jeu
print(lab.print_actions())

jouer=True

#Boucle sur les mouvements du joueur
while jouer:
 choisir=True
 #On demande au joueur de choisir une action et on verifie la validite de son choix
 while choisir:
  action=input("Choisissez une action.\n")
  try:
   action=action.upper()
   assert action[0] in  {'Q'} or  action[0] in lab.actions.keys()
  except AttributeError:
   print('Vous devez taper la lettre correspondant à l action.')
  except AssertionError:
   print('Ceci n est pas une action valable')
  else:
   if action[0]=='M' or action[0]=='P':
    try: 
     assert action[1] in  {'N','E','O','S'}
    except :
     print('Indiquer dans quel direction est le mur')
    else:
     choisir=False
   else:
    if len(action)>1:
     try:
      repetition=int(action[1:])
      assert repetition>0
     except ValueError:
      print('Apres l action, pour la repeter vous devez indiquer un nombre.')
     except AssertionError:
      print('Ce nombre de repetition n est pas valable.')
     else:
      choisir=False
    else:
     choisir=False
     repetition=1
 #On execute l action choisie
 if action[0]=='Q':
  jouer=False
  lab.save(nom_sauv)
  cartes.save()
 elif action[0]=='M' or action[0]=='P':
  retour=lab.action(action[0],action[1])
  print(retour[0])
  print(lab)
  lab.save(nom_sauv)
  if retour[1]:
   jouer=False
 else:
  retour=lab.move(action[0],repetition)
 #On imprime le resultat de l action et on sauvegarde, si la partie est terminee on sort
  print(retour[0])
  print(lab)
  lab.save(nom_sauv)
  if retour[1]:
   jouer=False
   
sys.exit("A bientot") 
