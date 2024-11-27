import numpy as np
import pandas as pds
import os
from random import *
from tkiteasy import *
from PIL import Image, ImageTk
from io import BytesIO
import tkinter as tk
from math import *
import time
import matplotlib.pyplot as pyplt

# Début du programme :
# Aucune fonction n'a de renvoi. C'etait plus simple pour la construction du programme, bien que cela soit un peu inutile

class Pokemorpion():
    def __init__(self):
        self.score1 = 0
        self.score2 = 0
        self.pk = pds.read_csv(r"pokemon.csv", index_col="Name")
        self.pk_normal = self.pk.loc[self.pk["Legendary"] == False]
        self.pk_legend = self.pk.loc[self.pk["Legendary"] == True]
        self.player1={}
        self.player2={}


    def affichage_menu(self):  # affichage du menu principal
        self.b = self.g.afficherTexte("Choix du mode de jeu :", 700, 70, "black", 22)
        self.duo = self.g.afficherTexte("Mode duo", 525, 230, "black", 20)
        self.algosimple = self.g.afficherTexte("Mode robot simple", 767, 180, "black", 20)
        self.robot = self.g.afficherTexte("Mode robot expert", 765, 230, "black", 20)
        self.tabscore = self.g.afficherTexte("Tableau des scores", 544, 550, "black", 15)
        self.q = self.g.afficherTexte("Quitter le jeu", 900, 540, "black", 15)
        self.distri_random=self.g.afficherTexte('distri_random', 200, 200, 'red')
        self.distri_draft=self.g.afficherTexte('distri_draft', 200, 250, 'blue')
        self.g.actualiser()

    def transition(self, nb):  # affichage uniquement transition menu de début de jeu
        # cette fonction est utilisee a 2 moments differents, le parametre permet de les distinguer
        # et d'eviter des doublons
        self.g = ouvrirFenetre(1200, 600)
        self.g.afficherImage(0, 0, "fond_menu.jpg")
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

            elif x == self.algosimple:  # mode robot resolution simple

                self.score_rob = 0  # initialisation à chaque fois des scores à 0 pour éviter une accumulation de score
                self.score_exp = 0
                self.superclean()
                self.affichage_jetons()
                #self.mode_auto_simple IA simple
                clic = self.g.attendreClic()
                x = self.g.recupererObjet(clic.x, clic.y)



            elif x == self.robot:  # algo etape 3

                self.score_rob = 0
                self.score_exp = 0
                self.superclean()
                self.affichage_jetons()
                #self.mode_auto_opti(1) robot fort
                clic = self.g.attendreClic()
                x = self.g.recupererObjet(clic.x, clic.y)


            elif x == self.tabscore:  # affichage du tableau des scores
                self.superclean()
                self.Tableau_des_scores()

                clic = self.g.attendreClic()
                x = self.g.recupererObjet(clic.x, clic.y)

            elif x==self.distri_random:
                self.superclean()
                self.random_draft()

            elif x==self.distri_draft:
                self.superclean()
                self.distri_draft()


            elif x == self.q:  # bouton pour quitter le jeu
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


    # Fonction pour récupérer l'image d'un Pokémon
    def get_pokemon_image(self,pokemon_name):
        pokemon_name=f'{pokemon_name}.png'#add png
        files = os.listdir('pokemon_images') #list of picture's name
        if pokemon_name in files:
            image_path = os.path.join('pokemon_images', pokemon_name) #charge image
            try:
                print(f'already found {pokemon_name}')
                return image_path
            except Exception as e:
                print(f"impossible charging {pokemon_name}，error：{e}")
        else:
            print(f"can't find {pokemon_name} in pokemon_images ")

    def random_draft(self):
        self.g.afficherImage(0,0,'distri_page.jpg')
        self.g.afficherTexte('player 1',300,100,'black',30)
        submit=self.g.afficherTexte('submit',512,512,'black')
        self.g.actualiser()
        pool_normal = self.pk_normal.sample(n=90)
        pool_legend = self.pk_legend.sample(n=10)
        pool1, pool2 = pool_legend.copy(), pool_normal.copy()
        legned_p1 = pool1.sample(n=5, random_state=42)
        pool1 = pool1.drop(legned_p1.index, inplace=False)
        legned_p2 = pool1.sample(n=5, random_state=42)
        normal_p1 = pool2.sample(n=45, random_state=42)
        pool2 = pool2.drop(normal_p1.index, inplace=False)
        normal_p2 = pool2.sample(n=45, random_state=42)
        self.player_1 = pds.concat([legned_p1, normal_p1])
        self.player_2 = pds.concat([legned_p2, normal_p2])
        self.player_1 = list(self.player_1.index)
        self.player_2 = list(self.player_2.index)
        #print(self.player_1)
        l1=[]
        l2=[]
        for i in range(50):
            l1.append(self.get_pokemon_image(self.player_1[i]))
            l2.append(self.get_pokemon_image(self.player_2[i]))
            #print(i)
            #print(l1,l2)
        for n in range(25):
            print(l1[n])
            self.g.afficherImage(10, 40*n, l1[n],40,40)
            print(l1[n + 25])
            self.g.afficherImage(110, 40*n, l1[n+25],40,40)
            print(l2[n])
            self.g.afficherImage(890, 40*n, l2[n],40,40)
            print(l2[n + 25])
            self.g.afficherImage(790, 40*n, l2[n+25],40,40)
            time.sleep(0.05)
            self.g.actualiser()
        clic = self.g.attendreClic()
        x = self.g.recupererObjet(clic.x, clic.y)
        if x == submit:
            self.superclean()
    def distribute_draft(self):


        return None


    def superclean(self):
        self.g.supprimerTout()  # suppression de tous les éléments graphiques et restauration de certains
        self.q = self.g.afficherTexte("Quitter le jeu", 500, 540, "white", 15)
        self.g.afficherImage(0, 0, "fond_menu.jpg")

    def fin(self):
        self.g.fermerFenetre()  # fin de partie


P = Pokemorpion()
P.menu()
