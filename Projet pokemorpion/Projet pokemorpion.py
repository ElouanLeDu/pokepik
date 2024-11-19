import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from random import *
from tkiteasy import *
from math import *
from time import time


class Pokemorpion:
    def __init__(self):
        self.score1 = 0
        self.score2 = 0
        self.score_solo = []
        self.score_duo1 = []
        self.score_duo2 = []
        self.score_etape2 = []
        self.score_etape3 = []

        self.g = ouvrirFenetre(1200, 600)
        self.g.afficherImage(0, 0, "fond_menu.jpg")

    def affichage_menu(self):
        self.g.afficherTexte("Choix du mode de jeu :", 700, 70, "black", 22)
        self.duo = self.g.afficherTexte("Mode duo", 525, 230, "black", 20)
        self.algosimple = self.g.afficherTexte("Mode robot simple", 767, 180, "black", 20)
        self.robot = self.g.afficherTexte("Mode robot expert", 765, 230, "black", 20)
        self.tabscore = self.g.afficherTexte("Tableau des scores", 544, 550, "black", 15)
        self.q = self.g.afficherTexte("Quitter le jeu", 900, 540, "black", 15)

        self.g.actualiser()

    def transition(self, nb):
        if nb == 1:  # écran de bienvenue
            a = self.g.afficherTexte("Bienvenue sur le jeu du Pokemorpion", 700, 150, "black", 30)
            b = self.g.afficherTexte("Jouer", 700, 340, "black", 30)
            self.attente_clic(b)
            self.g.supprimer(a)
            self.g.supprimer(b)

    def attente_clic(self, bouton):
        while True:
            clic = self.g.attendreClic()
            x = self.g.recupererObjet(clic.x, clic.y)
            if x == bouton:
                break

    def menu(self):
        self.transition(1)
        self.affichage_menu()

        while True:
            clic = self.g.attendreClic()
            x = self.g.recupererObjet(clic.x, clic.y)

            if x == self.duo:
                self.mode_duo()
            elif x == self.algosimple:
                self.mode_robot_simple()
            elif x == self.robot:
                self.mode_robot_expert()
            elif x == self.tabscore:
                self.Tableau_des_scores()
            elif x == self.q:
                self.fin()
                break
            self.superclean()
            self.affichage_menu()

    def mode_duo(self):
        rejouer = True
        while rejouer:
            self.superclean()
            self.affichage_jetons()
            self.superclean()
            self.transition(2)
            self.superclean()
            clic = self.g.attendreClic()
            x = self.g.recupererObjet(clic.x, clic.y)
            if x != self.c1:
                rejouer = False


            self.score1 = 0
            self.score2 = 0


    def mode_robot_simple(self):
        self.score_rob = 0
        self.score_exp = 0
        self.superclean()
        self.affichage_jetons()
        self.attente_clic(self.q)

    def mode_robot_expert(self):
        self.score_rob = 0
        self.score_exp = 0
        self.superclean()
        self.affichage_jetons()
        self.attente_clic(self.q)


    def Tableau_des_scores(self):
        self.g.afficherTexte("Tableau des scores", 300, 100, "black", 30)
        self.g.afficherTexte("Mode robot", 100, 200, "black", 20)
        self.g.afficherTexte("Étape 2", 60, 230, "black", 13)
        self.g.afficherTexte("Étape 3", 140, 230, "black", 13)
        self.g.afficherTexte("Mode duo", 300, 200, "black", 20)
        self.g.afficherTexte("Joueur 1", 260, 230, "black", 13)
        self.g.afficherTexte("Joueur 2", 340, 230, "black", 13)
        self.g.afficherTexte("Mode solo", 500, 200, "black", 20)

        self.afficher_scores(self.score_solo, 500, 230)
        self.afficher_scores(self.score_duo1, 260, 250)
        self.afficher_scores(self.score_duo2, 340, 250)
        self.afficher_scores(self.score_etape2, 60, 250)
        self.afficher_scores(self.score_etape3, 140, 250)

        self.g.actualiser()

    def afficher_scores(self, scores, x, y):
        for score in scores:
            self.g.afficherTexte(str(score), x, y, "black", 15)
            y += 25


    def superclean(self):
        self.g.supprimerTout()
        self.g.afficherImage(0, 0, "fond_menu.jpg")
        self.q = self.g.afficherTexte("Quitter le jeu", 500, 540, "white", 15)


    def fin(self):
        self.g.fermerFenetre()


if __name__ == "__main__":
    P = Pokemorpion()
    P.menu()