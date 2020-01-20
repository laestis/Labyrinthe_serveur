import unittest
import labyrinthe

class TestCartes(unittest.TestCase):
 """Classe de tests unitaires sur les cartes"""

 def setUp(self):
  self.cartes=labyrinthe.Cartes()

 def test_Init(self):
  """labyrinthe.Cartes() doit etre une liste, non vide avec des elements de type str()"""
  self.assertIsInstance(self.cartes,list)
  self.assertNotEqual(len(self.cartes),0)
  for elt in self.cartes:
   self.assertIsInstance(elt,str)

class TestLab(unittest.TestCase):
 """Classe de tests unitaires sur la classe du labyrinthe"""


 def test_Init(self):
  """Tests de l initialisation d un labyrinthe"""
  cartes=labyrinthe.Cartes()
  nb_joueur=3
  
  for elt in cartes:
   self.lab=labyrinthe.Labyrinthe(elt,nb_joueur)

#Tests sur le labyrinthe
   self.assertIsInstance(self.lab.labyrinthe,str)
   self.assertGreater(len(self.lab.labyrinthe),0)
   for elt in self.lab.labyrinthe:
    self.assertIn(elt,{'\n','O','x',' ','.','U'})
   
#Tests sur les robots
   self.assertIsInstance(self.lab.pos_rob,list)
   self.assertEqual(len(self.lab.pos_rob),nb_joueur)
   for elt in self.lab.pos_rob:
    self.assertIsInstance(elt,int)
    self.assertGreater(elt,0)
    self.assertEqual(self.lab.labyrinthe[elt],'x')

   self.assertIsInstance(self.lab.der_robot,list)
   self.assertEqual(len(self.lab.der_robot),3)
  for elt in self.lab.der_robot:
    self.assertIsInstance(elt,str)
    self.assertIn(elt,{' ','.'})


 def test_action(self):
  """Tests du labyrinthe apres une action"""
  
  nb_joueur=3
  cartes=labyrinthe.Cartes()
  
  for elt in cartes:
   self.lab=labyrinthe.Labyrinthe(elt,nb_joueur)
   for elt in {'N','S','E','O'}:
    for elt2 in {'M','P'}:
     j=0
     while j<nb_joueur:  
      self.lab.action(elt2,elt,j)
      j=j+1
#Tests sur le labyrinthe
      self.assertIsInstance(self.lab.labyrinthe,str)
      self.assertGreater(len(self.lab.labyrinthe),0)
      for elt in self.lab.labyrinthe:
       self.assertIn(elt,{'\n','O','x',' ','.','U'})

#Tests sur les robots
      self.assertIsInstance(self.lab.pos_rob,list)
      self.assertEqual(len(self.lab.pos_rob),nb_joueur)
      for elt in self.lab.pos_rob:
       self.assertIsInstance(elt,int)
       self.assertGreater(elt,0)
       self.assertEqual(self.lab.labyrinthe[elt],'x')

      self.assertIsInstance(self.lab.der_robot,list)
      self.assertEqual(len(self.lab.der_robot),3)
      for elt in self.lab.der_robot:
       self.assertIsInstance(elt,str)
       self.assertIn(elt,{' ','.'})

 def test_move(self):
  """Tests du labyrinthe apres une action"""

  nb_joueur=3
  cartes=labyrinthe.Cartes()
  nb_actions=5

  for elt in cartes:
   self.lab=labyrinthe.Labyrinthe(elt,nb_joueur)
   for elt in {'N','S','E','O'}:
    i=0
    while i<nb_actions:
     i=i+1
     j=0
     while j<nb_joueur:
      self.lab.move(elt,i,j)
      j=j+1
#Tests sur le labyrinthe
      self.assertIsInstance(self.lab.labyrinthe,str)
      self.assertGreater(len(self.lab.labyrinthe),0)
      for elt in self.lab.labyrinthe:
       self.assertIn(elt,{'\n','O','x',' ','.','U'})

#Tests sur les robots
      self.assertIsInstance(self.lab.pos_rob,list)
      self.assertEqual(len(self.lab.pos_rob),nb_joueur)
      for elt in self.lab.pos_rob:
       self.assertIsInstance(elt,int)
       self.assertGreater(elt,0)
       self.assertEqual(self.lab.labyrinthe[elt],'x')

      self.assertIsInstance(self.lab.der_robot,list)
      self.assertEqual(len(self.lab.der_robot),3)
      for elt in self.lab.der_robot:
       self.assertIsInstance(elt,str)
       self.assertIn(elt,{' ','.'})

