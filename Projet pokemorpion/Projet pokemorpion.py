import numpy as np
import pandas as pds

from random import *
from tkiteasy import *
from math import *
from time import time
import matplotlib.pyplot as pyplt

# Début du programme :
# Aucune fonction n'a de renvoi. C'etait plus simple pour la construction du programme, bien que cela soit un peu inutile

class Pokemorpion():
    def __init__(self):
        self.score1 = 0
        self.score2 = 0
        self.g = ouvrirFenetre(1200, 600)
        self.g.afficherImage(0, 0, "fond_menu.jpg")


    def affichage_menu(self):  # affichage du menu principal
        self.b = self.g.afficherTexte("Choix du mode de jeu :", 700, 70, "black", 22)
        self.duo = self.g.afficherTexte("Mode duo", 525, 230, "black", 20)
        self.algosimple = self.g.afficherTexte("Mode robot simple", 767, 180, "black", 20)
        self.robot = self.g.afficherTexte("Mode robot expert", 765, 230, "black", 20)
        self.tabscore = self.g.afficherTexte("Tableau des scores", 544, 550, "black", 15)
        self.q = self.g.afficherTexte("Quitter le jeu", 900, 540, "black", 15)

        self.g.actualiser()

    def transition(self, nb):  # affichage uniquement transition menu de début de jeu
        # cette fonction est utilisee a 2 moments differents, le parametre permet de les distinguer
        # et d'eviter des doublons
        if nb == 1:  # écran de début du jeu
            a = self.g.afficherTexte("Bienvenue sur le jeu du Pokemorpion", 700, 150, "black", 30)
            b = self.g.afficherTexte("Jouer", 700, 340, "black", 30)
        #à voir si l'on fait d'autres transitions
        clic = self.g.attendreClic()
        x = self.g.recupererObjet(clic.x, clic.y)
        while x != b:  # le joueur doit cliquer sur jouer pour continuer
            clic = self.g.attendreClic()
            x = self.g.recupererObjet(clic.x, clic.y)
        self.g.supprimer(a)
        self.g.supprimer(b)

    def menu(self):  # menu principal, appel des fonctions et gestion des fonctionnalites
        self.transition(1)
        self.affichage_menu()
        stop = False
        while stop == False:  # on boucle tant que le joueur en clique pas sur quitter la partie
            clic = self.g.attendreClic()
            x = self.g.recupererObjet(clic.x, clic.y)

            if x == self.duo:

                rejouer = True

                while rejouer == True:  # même fonctionnement pour le mode duo en dehors du fait que le jeu est adapté pour 2 joueurs
                    self.superclean()
                    self.affichage_jetons()
                    #fonction jeu 2 joueurs ici
                    self.superclean()
                    self.transition(2)
                    self.superclean()
                    #self.score(2) enregistrement du score pour pouvoir le voir dans le tableau des scores?
                    clic = self.g.attendreClic()
                    x = self.g.recupererObjet(clic.x, clic.y)

                    if not x == self.c1:
                        rejouer = False
                    self.score1 = 0
                    self.score2 = 0

            if x == self.algosimple:  # mode robot resolution simple

                self.score_rob = 0  # initialisation à chaque fois des scores à 0 pour éviter une accumulation de score
                self.score_exp = 0
                self.superclean()
                self.affichage_jetons()
                #self.mode_auto_simple IA simple
                clic = self.g.attendreClic()
                x = self.g.recupererObjet(clic.x, clic.y)



            if x == self.robot:  # algo etape 3

                self.score_rob = 0
                self.score_exp = 0
                self.superclean()
                self.affichage_jetons()
                #self.mode_auto_opti(1) robot fort
                clic = self.g.attendreClic()
                x = self.g.recupererObjet(clic.x, clic.y)


            if x == self.tabscore:  # affichage du tableau des scores
                self.superclean()
                self.Tableau_des_scores()

                clic = self.g.attendreClic()
                x = self.g.recupererObjet(clic.x, clic.y)


            if x == self.q:  # bouton pour quitter le jeu
                self.fin()

            self.superclean()
            self.affichage_menu()

    def Tableau_des_scores(self):  # affichage du tableau des scores

        self.g.afficherTexte("Tableau des scores", 300, 100, "black", 30)
        self.g.afficherTexte("Mode robot", 100, 200, "black", 20)
        self.g.afficherTexte("étape 2", 60, 230, "black", 13)
        self.g.afficherTexte("étape 3", 140, 230, "black", 13)
        self.g.afficherTexte("Mode duo", 300, 200, "black", 20)
        self.g.afficherTexte("Joueur 1", 260, 230, "black", 13)
        self.g.afficherTexte("Joueur 2", 340, 230, "black", 13)
        self.g.afficherTexte("Mode solo", 500, 200, "black", 20)
        # boucles pour afficher l'ensemble des scores contenus dans des listes prévues à cet effet
        y = 230
        for i in range(len(self.score_solo)):  # affichage des scores dans l'ordre des parties
            self.g.afficherTexte(f"{self.score_solo[i]}", 500, y, "black", 15)

            y += 25
        y = 250
        for i in range(len(self.score_duo1)):
            self.g.afficherTexte(f"{self.score_duo1[i]}", 260, y, "black", 15)
            y += 25

        y = 250
        for i in range(len(self.score_duo2)):
            self.g.afficherTexte(f"{self.score_duo2[i]}", 340, y, "black", 15)
            y += 25

        y = 250
        for i in range(len(self.score_etape2)):
            self.g.afficherTexte(f"{self.score_etape2[i]}", 60, y, "black", 15)
            y += 25

        y = 250
        for i in range(len(self.score_etape3)):
            self.g.afficherTexte(f"{self.score_etape3[i]}", 140, y, "black", 15)
            y += 25

        self.g.actualiser()

    def superclean(self):
        self.g.supprimerTout()  # suppression de tous les éléments graphiques et restauration de certains
        self.q = self.g.afficherTexte("Quitter le jeu", 500, 540, "white", 15)
        self.g.afficherImage(0, 0, "fond_menu.jpg")

    def fin(self):
        self.g.fermerFenetre()  # fin de partie


P = Pokemorpion()
P.menu()


#caca