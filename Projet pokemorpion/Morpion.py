import time
import numpy as np
from tkiteasy import *
import math
from combat import combat_de_pokemon
import pandas as pds
from PIL import Image, ImageTk
import os
import tkinter as tk



class Morpion:
    def __init__(self,g):
        self.g = g
        self.mat = np.array([[np.zeros((3, 3)) for i in range(3)] for i in range(3)]) #la matrice contenant des matrices qui representent les petits morpion
        self.main_mat = np.zeros(((3,3)))                                             #la matrice qui represente le grand morpion
        self.dic_asso = {}
        self.fin = False
        self.dico_surbrillance={}
        self.centre = [
            (600, 300,(1,1)), (600, 150,(1,0)), (600, 450,(1,2)),
            (450, 300,(0,1)), (450, 150,(0,0)), (450, 450,(0,2)),
            (750, 300,(2,1)), (750, 150,(2,0)), (750, 450,(2,2))]

        self.mat_poke = np.array([[np.zeros((3, 3)) for i in range(3)] for i in range(3)])
        self.df = pds.read_csv('pokemon_modified.csv', index_col="Name")
        poke = self.df.sample(n=120)
        self.deck = [poke[60:],poke[:60]]
        self.combat = combat_de_pokemon(self.g,self.df)
        self.asso_poke = {}
        self.co_to_poke = {}
        self.name_to_poke = {}


    def afficher_poke(self):
        for j in range(2) :
            for i in range(60):

                poke = self.g.afficherImage(53.5 + 47*(i%6) + 825 * (j%2),75 + 47 * (i//6),f"pokemon_images/{self.deck[j].index[i]}.png",43,43)
                if j == 0 :
                    joueur = 1
                else:
                    joueur = -1
                self.asso_poke[poke] = {"co_mat":(-1,-1), "co": (53.5 + 47*(i%6) + 825 * (j%2),75 + 47 * (i//6)),"name" : self.deck[j].index[i], "joueur": joueur, "dispo" : True }
                self.name_to_poke[self.deck[j].index[i]] = poke


    def afficher_grille(self):
        for y in [225, 375]:
            self.g.dessinerLigne(375, y, 375 + 450, y, "white")
        for x in [525, 675]:
            self.g.dessinerLigne(x, 75, x, 525, "white")

    def afficher_centres(self):
        for x in self.centre:
            coin_haut_gauche = (x[0]-67.5,x[1]-67.5)
            for l in range(3):
                for h in range(3):
                    rect = self.g.dessinerRectangle(coin_haut_gauche[0]+45*l,coin_haut_gauche[1]+45*h,45,45,"black")
                    self.dic_asso[rect] = (x[2][1],x[2][0],h,l)


            self.g.dessinerLigne(x[0] - 22.5, x[1] + 67.5, x[0] - 22.5, x[1] - 67.5, "white")
            self.g.dessinerLigne(x[0] + 22.5, x[1] + 67.5, x[0] + 22.5, x[1] - 67.5, "white")
            self.g.dessinerLigne(x[0] - 67.5, x[1] + 22.5, x[0] + 67.5, x[1] + 22.5, "white")
            self.g.dessinerLigne(x[0] - 67.5, x[1] - 22.5, x[0] + 67.5, x[1] - 22.5, "white")



    def afficher_morpion(self):  #tout ceci sert juste a afficher le morpion
        for x in range(3):
            for y in range(3):
                self.dico_surbrillance[(y,x)]=self.g.dessinerRectangle(375 + x * 150 + 1, 75 + y * 150 + 1, 149, 149, "black")

        self.afficher_grille()
        self.afficher_centres()
        self.g.actualiser()

    def verif_win(self,mat):   # verifie si un morpion est gagné renvoie -1, 1 ou 0 si personne a gagné
        # ligne et colonne
        for i in range (3):
            if abs(mat[i][0] + mat[i][1] + mat[i][2]) == 3 :
                return mat[i][0]
            if abs(mat[0][i] + mat[1][i] + mat[2][i]) == 3 :
                return mat[0][i]

        #diagonale
        if abs(mat[0][0] + mat[1][1] + mat[2][2]) == 3 :
            return mat[0][0]
        if abs(mat[2][0] + mat[1][1] + mat[0][2]) == 3 :
            return mat[1][1]

        return 0


    #jeu simple avec deux joueurs
    def start(self):
        self.afficher_morpion()
        #le joueur qui commence
        j = 1
        prochain_coup = -1
        while not self.fin:
            clic = self.g.recupererClic()
            touche = self.g.recupererTouche()
            if clic :
                #l'utilisation de try est surtout utile pour voir si le clic ramene bien a un objet
                try :
                    objet = self.g.recupererObjet(clic.x, clic.y)
                    #on verfifie si l'emplacement peut etre jouer
                    if objet in self.dic_asso and self.main_mat[self.dic_asso[objet][0]][self.dic_asso[objet][1]] == 0 and self.mat[self.dic_asso[objet][0]][self.dic_asso[objet][1]][self.dic_asso[objet][2]][self.dic_asso[objet][3]] == 0 :
                        #si le prochain coup = -1 alors on peut jouer ou on veut
                        if prochain_coup ==-1 or prochain_coup == (self.dic_asso[objet][0],self.dic_asso[objet][1]) :
                            if j == 1:
                                self.g.afficherImage(objet.x + 2.5, objet.y + 2.5, "rond.png")
                                self.mat[self.dic_asso[objet][0]][self.dic_asso[objet][1]][self.dic_asso[objet][2]][self.dic_asso[objet][3]] = 1
                                j = -1
                            elif j == -1:
                                self.g.afficherImage(objet.x + 2.5, objet.y + 2.5, "croix.png")
                                self.mat[self.dic_asso[objet][0]][self.dic_asso[objet][1]][self.dic_asso[objet][2]][self.dic_asso[objet][3]] = -1
                                j = 1

                            #juste pour l'effet de surbrillance
                            if prochain_coup != -1:
                                self.g.changerCouleur(self.dico_surbrillance[prochain_coup], "black")
                            else :
                                for i in self.dico_surbrillance:
                                    self.g.changerCouleur(self.dico_surbrillance[i], "black")
                            prochain_coup = (self.dic_asso[objet][2], self.dic_asso[objet][3])

                        #on verifie si le morpion sur lequel on a joué a été gagné ou pas
                        win = self.verif_win(self.mat[self.dic_asso[objet][0]][self.dic_asso[objet][1]])
                        if abs(win) == 1:
                            self.main_mat[self.dic_asso[objet][0]][self.dic_asso[objet][1]] = win
                            self.g.dessinerRectangle(375 + self.dic_asso[objet][1] * 150 +1 ,75 + self.dic_asso[objet][0] * 150 + 1,148,148,"black")
                            if win == -1 :
                                image = "croix2.png"
                            elif win == 1 :
                                image = "rond2.png"
                            self.g.afficherImage( 375 + self.dic_asso[objet][1] * 150 ,75 + self.dic_asso[objet][0] * 150, image )
                            if abs(self.verif_win(self.main_mat)) == 1 :
                                self.fin = True

                        if abs(self.main_mat[prochain_coup[0]][prochain_coup[1]]) == 1 or all(x != 0 for y in self.mat[prochain_coup[0]][prochain_coup[1]] for x in y):
                            prochain_coup = -1
                            for i in self.dico_surbrillance:
                                self.g.changerCouleur(self.dico_surbrillance[i],"cyan")
                        elif self.main_mat[prochain_coup[0]][prochain_coup[1]] == 0:
                            self.g.changerCouleur(self.dico_surbrillance[prochain_coup], "cyan")
                except :
                    continue


    def eval_petit(self,mat):#cette fonction evalue un morpion de base
        #le joueur est représenté par des 1 sur la mat et l'ia par des -1
        evaluation = 0
        score = [[0.2, 0.17, 0.2],
                    [0.17, 0.22, 0.17],
                    [0.2, 0.17, 0.2]] #matrice avec les scores de base pour chaque pos (le centre ++, les coins +, les arretes 0)

        for y in range(3) :
            for x in range(3) :
                evaluation -= mat[x][y] * score[x][y]

        win_comb = [((0,0),(0,1),(0,2)),((1,0),(1,1),(1,2)),((2,0),(2,1),(2,2)),#lignes
                    ((0,0),(1,0),(2,0)),((0,1),(1,1),(2,1)),((0,2),(1,2),(2,2)),#colonnes
                    ((0,0),(1,1),(2,2)),((2,0),(1,1),(0,2))]#diagonales

        for i,j,k in win_comb :
            if mat[i[0]][i[1]] + mat[j[0]][j[1]] + mat[k[0]][k[1]] == 2 :   #l'ia domine elle a deux 1 consecutifs
                evaluation -= 6
            if mat[i[0]][i[1]] + mat[j[0]][j[1]] + mat[k[0]][k[1]] == -2 :  #le joueur domine elle a deux 1 consecutifs
                evaluation += 6
            if mat[i[0]][i[1]] + mat[j[0]][j[1]] + mat[k[0]][k[1]] == 3 :   #l'ia peut gagner pour sur
                evaluation -= 7
            if mat[i[0]][i[1]] + mat[j[0]][j[1]] + mat[k[0]][k[1]] == -3 :  #le joueur peut gagner pour sur
                evaluation += 7


        #tout ce qui suit repertorie juste les cas ou une suite de deux rond a été bloqué par une croix et inversement

        a = -1

        if (((mat[0][0] + mat[0][1] == 2 * a ) and mat[0][2] == -a) or ((mat[0][0] + mat[0][2] == 2 * a ) and mat[0][1] == -a) or ((mat[0][1] + mat[0][2] == 2 * a ) and mat[0][0] == -a)
            or ((mat[1][0] + mat[1][1] == 2 * a ) and mat[1][2] == -a) or ((mat[1][0] + mat[1][2] == 2 * a ) and mat[1][1] == -a) or ((mat[1][1] + mat[1][2] == 2 * a ) and mat[1][0] == -a)
            or ((mat[2][0] + mat[2][1] == 2 * a ) and mat[2][2] == -a) or ((mat[2][0] + mat[2][2] == 2 * a ) and mat[2][1] == -a) or ((mat[2][1] + mat[2][2] == 2 * a ) and mat[2][0] == -a)
            or ((mat[0][0] + mat[1][0] == 2 * a ) and mat[2][0] == -a) or ((mat[2][0] + mat[1][0] == 2 * a ) and mat[0][0] == -a) or ((mat[2][0] + mat[0][0] == 2 * a ) and mat[1][0] == -a)
            or ((mat[0][1] + mat[1][1] == 2 * a ) and mat[2][1] == -a) or ((mat[2][1] + mat[1][1] == 2 * a ) and mat[0][1] == -a) or ((mat[2][1] + mat[0][1] == 2 * a ) and mat[1][1] == -a)
            or ((mat[0][2] + mat[1][2] == 2 * a ) and mat[2][2] == -a) or ((mat[2][2] + mat[1][2] == 2 * a ) and mat[0][2] == -a) or ((mat[2][2] + mat[0][2] == 2 * a ) and mat[1][2] == -a)
            or ((mat[0][0] + mat[1][1] == 2 * a ) and mat[2][2] == -a) or ((mat[0][0] + mat[2][2] == 2 * a ) and mat[1][1] == -a) or ((mat[2][2] + mat[1][1] == 2 * a ) and mat[0][0] == -a)
            or ((mat[2][0] + mat[1][1] == 2 * a ) and mat[0][2] == -a) or ((mat[2][0] + mat[0][2] == 2 * a ) and mat[1][1] == -a) or ((mat[0][2] + mat[1][1] == 2 * a ) and mat[2][0] == -a)):
            evaluation -= 9

        a = 1

        if (((mat[0][0] + mat[0][1] == 2 * a ) and mat[0][2] == -a) or ((mat[0][0] + mat[0][2] == 2 * a ) and mat[0][1] == -a) or ((mat[0][1] + mat[0][2] == 2 * a ) and mat[0][0] == -a)
            or ((mat[1][0] + mat[1][1] == 2 * a ) and mat[1][2] == -a) or ((mat[1][0] + mat[1][2] == 2 * a ) and mat[1][1] == -a) or ((mat[1][1] + mat[1][2] == 2 * a ) and mat[1][0] == -a)
            or ((mat[2][0] + mat[2][1] == 2 * a ) and mat[2][2] == -a) or ((mat[2][0] + mat[2][2] == 2 * a ) and mat[2][1] == -a) or ((mat[2][1] + mat[2][2] == 2 * a ) and mat[2][0] == -a)
            or ((mat[0][0] + mat[1][0] == 2 * a ) and mat[2][0] == -a) or ((mat[2][0] + mat[1][0] == 2 * a ) and mat[0][0] == -a) or ((mat[2][0] + mat[0][0] == 2 * a ) and mat[1][0] == -a)
            or ((mat[0][1] + mat[1][1] == 2 * a ) and mat[2][1] == -a) or ((mat[2][1] + mat[1][1] == 2 * a ) and mat[0][1] == -a) or ((mat[2][1] + mat[0][1] == 2 * a ) and mat[1][1] == -a)
            or ((mat[0][2] + mat[1][2] == 2 * a ) and mat[2][2] == -a) or ((mat[2][2] + mat[1][2] == 2 * a ) and mat[0][2] == -a) or ((mat[2][2] + mat[0][2] == 2 * a ) and mat[1][2] == -a)
            or ((mat[0][0] + mat[1][1] == 2 * a ) and mat[2][2] == -a) or ((mat[0][0] + mat[2][2] == 2 * a ) and mat[1][1] == -a) or ((mat[2][2] + mat[1][1] == 2 * a ) and mat[0][0] == -a)
            or ((mat[2][0] + mat[1][1] == 2 * a ) and mat[0][2] == -a) or ((mat[2][0] + mat[0][2] == 2 * a ) and mat[1][1] == -a) or ((mat[0][2] + mat[1][1] == 2 * a ) and mat[2][0] == -a)):
            evaluation += 9

        evaluation -= self.verif_win(mat) * 12

        return evaluation


    def eval_grand(self,mat,pos_actuelle):#cette fonction permet d'evaluer toute la grille actuelle
        score = [[1.4, 1, 1.4],
                 [1, 1.75, 1],
                [1.4, 1, 1.4]] # matrice avec les scores de base pour chaque pos (le centre ++, les coins +, les arretes 0)
        evaluation = 0
        main_mat = np.zeros((3,3))

        #on parcours tout les petits morpion
        for y in range(3):
            for x in range(3):
                evaluation += self.eval_petit(mat[x][y]) * 1.5 * score[x][y]

                #ajoute un bonus si la grille courante est active
                if (x,y) == pos_actuelle :
                    evaluation += self.eval_petit(mat[x][y]) * score[x][y]

                #on verifie si quelqu'un a gagné sur cette grille et on créer en passsant la grille principale pour verifier si il n'y a pas de win globale
                win = self.verif_win(mat[x][y])
                evaluation -= win * score[x][y]
                main_mat[x][y] += win

        evaluation -= self.verif_win(main_mat) * 5000  #si il y'a une win totale on recompense beaucoup beaucoup
        evaluation += self.eval_petit(main_mat) * 150  #on evalue le gros plateau comme les petits mais avec un plus gros coeff pour que l'ia privilegie le gros plateau au petit

        return evaluation


    def minimax(self,main_mat,grille_active, profondeur, alpha, beta, joueur_max):

        meilleur_coup = -1

        evalfin = self.eval_grand(main_mat,grille_active)

        if profondeur <= 0 or abs(evalfin) > 5000 :
            return {0:evalfin,1:meilleur_coup}

        if grille_active == -1 or self.verif_win(main_mat[grille_active[0]][grille_active[1]])!=0 or all(x != 0 for y in main_mat[grille_active[0]][grille_active[1]] for x in y) :
            grille_active = -1#on peut jouer sur toute les grilles

        #on commence par le joueur maximisant
        if joueur_max:
            max_eval = -math.inf
            #on parcours toutes les cases d'un petit morpion
            for y in range(3):
                for x in range(3):
                    #si on peut jouer sur toutes les grilles il faut parcourir toute les positions possible ca peut donc prendre plus de temp
                    if grille_active == -1 :
                        for h in range(3):
                            for l in range(3):
                                if self.verif_win(main_mat[h][l]) == 0 :
                                    if main_mat[h][l][y][x] == 0:
                                        #on joue le coup
                                        main_mat[h][l][y][x] = -1
                                        eval = self.minimax(main_mat, (y, x), profondeur - 1, alpha, beta, False)
                                        #on annule ensuite le coup
                                        main_mat[h][l][y][x] = 0

                                        monstre = eval[0]
                                        if monstre > max_eval:
                                            max_eval = monstre
                                            #on sauvegarde le coup qui a permis "d'ameliorer le score"
                                            meilleur_coup = (h, l, y, x)
                                        alpha = max(alpha, monstre)

                                        # Coupure alpha-bêta
                                        if beta <= alpha:
                                            break

                                    if beta <= alpha:
                                        break

                    else :
                            if main_mat[grille_active[0]][grille_active[1]][y][x] == 0 :
                                main_mat[grille_active[0]][grille_active[1]][y][x] = -1
                                eval = self.minimax(main_mat,(y,x), profondeur-1, alpha, beta,False)
                                main_mat[grille_active[0]][grille_active[1]][y][x] = 0

                                monstre = eval[0]
                                if monstre > max_eval :
                                    max_eval = monstre
                                    meilleur_coup = (grille_active[0],grille_active[1],y,x)
                                alpha = max(alpha,monstre)
                                if beta <= alpha :
                                    break
                if beta <= alpha:
                    break

            return {0:max_eval,1:meilleur_coup}

        #on refait quasi la meme chose pour le joueur minimisant
        else :
            min_eval = math.inf
            for y in range(3):
                for x in range(3):
                    if grille_active == -1 :
                        for h in range(3):
                            for l in range(3):
                                if self.verif_win(main_mat[h][l]) == 0 :
                                    if main_mat[h][l][y][x] == 0:
                                        main_mat[h][l][y][x] = 1
                                        eval = self.minimax(main_mat, (y, x), profondeur - 1, alpha, beta, True)
                                        main_mat[h][l][y][x] = 0

                                        monstre = eval[0]
                                        if monstre < min_eval:
                                            min_eval = monstre
                                            meilleur_coup = (h, l, y, x)
                                        beta = min(beta, monstre)
                                        if beta <= alpha:
                                            break
                                        # Ajout d'un `break` externe à la boucle `l`
                                    if beta <= alpha:
                                        break

                    else :
                        if main_mat[grille_active[0]][grille_active[1]][y][x] == 0:
                            main_mat[grille_active[0]][grille_active[1]][y][x] = 1
                            eval = self.minimax(main_mat, (y, x), profondeur - 1, alpha, beta, True)
                            main_mat[grille_active[0]][grille_active[1]][y][x] = 0

                            monstre = eval[0]
                            if monstre < min_eval:
                                min_eval = monstre
                                meilleur_coup = (grille_active[0],grille_active[1],y,x)
                            beta = min(beta, monstre)
                            if beta <= alpha:
                                break
                if beta <= alpha :
                    break

            return {0: min_eval, 1: meilleur_coup}


    def start_ia(self):
        self.afficher_morpion()
        j = 1
        prochain_coup = -1
        while not self.fin:
            if j == 1:
                clic = self.g.recupererClic()
                if clic :
                    try :
                        objet = self.g.recupererObjet(clic.x, clic.y)
                        if objet in self.dic_asso and self.main_mat[self.dic_asso[objet][0]][self.dic_asso[objet][1]] == 0 and self.mat[self.dic_asso[objet][0]][self.dic_asso[objet][1]][self.dic_asso[objet][2]][self.dic_asso[objet][3]] == 0 :
                            if prochain_coup ==-1 or prochain_coup == (self.dic_asso[objet][0],self.dic_asso[objet][1]) :
                                self.g.afficherImage(objet.x + 2.5, objet.y + 2.5, "rond.png")
                                self.mat[self.dic_asso[objet][0]][self.dic_asso[objet][1]][self.dic_asso[objet][2]][self.dic_asso[objet][3]] = 1
                                j = -1
                                if prochain_coup != -1:
                                    self.g.changerCouleur(self.dico_surbrillance[prochain_coup], "black")
                                else :
                                    for i in self.dico_surbrillance:
                                        self.g.changerCouleur(self.dico_surbrillance[i], "black")
                                prochain_coup = (self.dic_asso[objet][2], self.dic_asso[objet][3])
                            win = self.verif_win(self.mat[self.dic_asso[objet][0]][self.dic_asso[objet][1]])
                            if abs(win) == 1:
                                self.main_mat[self.dic_asso[objet][0]][self.dic_asso[objet][1]] = win
                                self.g.dessinerRectangle(375 + self.dic_asso[objet][1] * 150 + 1,
                                                         75 + self.dic_asso[objet][0] * 150 + 1, 148, 148, "black")
                                if win == -1:
                                    image = "croix2.png"
                                elif win == 1:
                                    image = "rond2.png"
                                self.g.afficherImage(375 + self.dic_asso[objet][1] * 150,
                                                     75 + self.dic_asso[objet][0] * 150, image)
                                if abs(self.verif_win(self.main_mat)) == 1:
                                    self.fin = True
                            if abs(self.main_mat[prochain_coup[0]][prochain_coup[1]]) == 1:
                                prochain_coup = -1
                                for i in self.dico_surbrillance:
                                    self.g.changerCouleur(self.dico_surbrillance[i], "cyan")
                            elif self.main_mat[prochain_coup[0]][prochain_coup[1]] == 0:
                                self.g.changerCouleur(self.dico_surbrillance[prochain_coup], "cyan")
                            self.g.actualiser()
                    except :
                        continue

            else :
                nb_coup_possible = 0
                for x in range(3):
                    for y in range(3):
                        if self.verif_win(self.mat[x][y]) == 0 :
                            for x1 in range(3):
                                for y1 in range(3):
                                    if self.mat[x][y][x1][y1]==0:
                                        nb_coup_possible += 1
                coup_ia = self.minimax(self.mat,prochain_coup,min(4 ,nb_coup_possible),-math.inf,math.inf,True)
                self.mat[coup_ia[1][0]][coup_ia[1][1]][coup_ia[1][2]][coup_ia[1][3]] = -1

                centre = (450 + coup_ia[1][1] * 150, 150 + coup_ia[1][0] * 150)
                self.g.afficherImage((centre[0] - 67.5) + 45 * coup_ia[1][3] + 2.5, (centre[1] - 67.5) + 45 * coup_ia[1][2] + 2.5, "croix.png")
                j = 1

                if prochain_coup != -1:
                    self.g.changerCouleur(self.dico_surbrillance[prochain_coup], "black")
                else:
                    for i in self.dico_surbrillance:
                        self.g.changerCouleur(self.dico_surbrillance[i], "black")

                prochain_coup = (coup_ia[1][2],coup_ia[1][3])
                win = self.verif_win(self.mat[coup_ia[1][0]][coup_ia[1][1]])
                if abs(win) == 1:
                    self.main_mat[coup_ia[1][0]][coup_ia[1][1]] = win
                    self.g.dessinerRectangle(375 + coup_ia[1][1] * 150 + 1,
                                             75 + coup_ia[1][0] * 150 + 1, 148, 148, "black")
                    if win == -1:
                        image = "croix2.png"
                    elif win == 1:
                        image = "rond2.png"
                    self.g.afficherImage(375 + coup_ia[1][1] * 150,
                                         75 + coup_ia[1][0] * 150, image)
                    if abs(self.verif_win(self.main_mat)) == 1:
                        if win == -1:
                            image = "croix2.png"
                        elif win == 1:
                            image = "rond2.png"
                        self.g.afficherImage(0,0,image)
                        time.sleep(10)
                        self.fin = True
                if abs(self.main_mat[prochain_coup[0]][prochain_coup[1]]) == 1 or all(x != 0 for y in self.mat[prochain_coup[0]][prochain_coup[1]] for x in y):
                    prochain_coup = -1
                    for i in self.dico_surbrillance:
                        self.g.changerCouleur(self.dico_surbrillance[i], "cyan")
                elif self.main_mat[prochain_coup[0]][prochain_coup[1]] == 0:
                    self.g.changerCouleur(self.dico_surbrillance[prochain_coup], "cyan")
                self.g.actualiser()

    def start_poke(self):
        self.afficher_poke()
        self.afficher_morpion()

        #le joueur qui commence
        j = 1
        rectangle = self.g.dessinerRectangle(10000,10000,43,43,"red")
        rectangle1 = self.g.dessinerRectangle(10000,10000,43,43,"blue")
        self.g.placerAuDessous(rectangle1)
        self.g.placerAuDessous(rectangle)

        prochain_coup = -1
        poke_choisi = None
        while not self.fin:
            clic = self.g.recupererClic()
            touche = self.g.recupererTouche()
            if clic :
                try :
                    objet = self.g.recupererObjet(clic.x, clic.y)
                    if objet in self.asso_poke and self.asso_poke[objet]["dispo"] and self.asso_poke[objet]["joueur"] == j:
                        if j == 1 :
                            obj =rectangle
                        else :
                            obj = rectangle1
                        self.g.deplacer(obj,self.asso_poke[objet]["co"][0]-obj.x,self.asso_poke[objet]["co"][1] - obj.y)
                        poke_choisi = objet

                    if (poke_choisi and self.asso_poke[poke_choisi]["dispo"] and objet in self.dic_asso
                            and self.main_mat[self.dic_asso[objet][0]][self.dic_asso[objet][1]] == 0
                            and self.mat_poke[self.dic_asso[objet][0]][self.dic_asso[objet][1]][self.dic_asso[objet][2]][self.dic_asso[objet][3]] == 0
                            and self.mat[self.dic_asso[objet][0]][self.dic_asso[objet][1]][self.dic_asso[objet][2]][self.dic_asso[objet][3]] != j) :

                        if prochain_coup ==-1 or prochain_coup == (self.dic_asso[objet][0],self.dic_asso[objet][1]) :
                            if self.mat[self.dic_asso[objet][0]][self.dic_asso[objet][1]][self.dic_asso[objet][2]][self.dic_asso[objet][3]] == -j :

                                poke_selec = self.co_to_poke[(self.dic_asso[objet][0],self.dic_asso[objet][1],self.dic_asso[objet][2],self.dic_asso[objet][3])]

                                resultat = self.combat.combat(self.asso_poke[poke_choisi]["name"],self.asso_poke[poke_selec]["name"])
                                """choisir un pokemon contre qui il combattra"""
                                """lancez combat et afficher le vainceur"""
                                #faut juste enlever le carré qu'il y'a derriere redessiner un carré noir par dessus parce que flemme

                                winner = self.name_to_poke[resultat[0]]
                                loser = self.name_to_poke[resultat[1]]
                                print(loser)
                                print(winner)

                                self.asso_poke[winner]["dispo"] = False
                                self.asso_poke[loser]["dispo"] = True

                                self.mat_poke[self.dic_asso[objet][0]][self.dic_asso[objet][1]][self.dic_asso[objet][2]][self.dic_asso[objet][3]] = self.asso_poke[winner]["joueur"]
                                self.mat[self.dic_asso[objet][0]][self.dic_asso[objet][1]][self.dic_asso[objet][2]][self.dic_asso[objet][3]] = self.asso_poke[winner]["joueur"]

                                self.g.dessinerRectangle(objet.x,objet.y,44,44,"black")

                                if j == self.asso_poke[winner]["joueur"]:
                                    self.g.afficherImage(objet.x + 2.5, objet.y + 2.5, "rond.png")

                                else:
                                    self.g.afficherImage(objet.x + 2.5, objet.y + 2.5, "croix.png")

                                self.g.supprimer(winner)
                                self.g.deplacer(loser, self.asso_poke[loser]["co"][0] - loser.x,self.asso_poke[loser]["co"][1] - loser.y)

                            else :
                                self.g.deplacer(poke_choisi, objet.x - poke_choisi.x + 1,objet.y - poke_choisi.y + 1)
                                if j == 1 :
                                    col = "red"
                                else :
                                    col = "blue"
                                self.g.dessinerRectangle(poke_choisi.x ,poke_choisi.y , 44,44,col)

                                self.g.placerAuDessus(poke_choisi)
                                self.asso_poke[poke_choisi]["dispo"] = False
                                self.asso_poke[poke_choisi]["co_mat"] = (self.dic_asso[objet][0],self.dic_asso[objet][1],self.dic_asso[objet][2],self.dic_asso[objet][3])
                                self.co_to_poke[(self.dic_asso[objet][0],self.dic_asso[objet][1],self.dic_asso[objet][2],self.dic_asso[objet][3])] = poke_choisi
                                self.dic_asso[poke_choisi] = (self.dic_asso[objet][0],self.dic_asso[objet][1],self.dic_asso[objet][2],self.dic_asso[objet][3])
                                self.mat[self.dic_asso[objet][0]][self.dic_asso[objet][1]][self.dic_asso[objet][2]][self.dic_asso[objet][3]] = j

                            if j == 1:
                                obj = rectangle
                            else:
                                obj = rectangle1
                            self.g.deplacer(obj, 10000, 10000)
                            j = -j

                            #juste pour l'effet de surbrillance
                            if prochain_coup != -1:
                                self.g.changerCouleur(self.dico_surbrillance[prochain_coup], "black")
                            else :
                                for i in self.dico_surbrillance:
                                    self.g.changerCouleur(self.dico_surbrillance[i], "black")
                            prochain_coup = (self.dic_asso[objet][2], self.dic_asso[objet][3])

                        #on verifie si le morpion sur lequel on a joué a été gagné ou pas
                        win = self.verif_win(self.mat[self.dic_asso[objet][0]][self.dic_asso[objet][1]])
                        if abs(win) == 1:
                            self.main_mat[self.dic_asso[objet][0]][self.dic_asso[objet][1]] = win
                            self.g.dessinerRectangle(375 + self.dic_asso[objet][1] * 150 +1 ,75 + self.dic_asso[objet][0] * 150 + 1,148,148,"black")
                            if win == -1 :
                                image = "croix2.png"
                            else :
                                image = "rond2.png"
                            self.g.afficherImage( 375 + self.dic_asso[objet][1] * 150 ,75 + self.dic_asso[objet][0] * 150, image )
                            if abs(self.verif_win(self.main_mat)) == 1 :
                                self.fin = True

                        if abs(self.main_mat[prochain_coup[0]][prochain_coup[1]]) == 1 or all(x != 0 for y in self.mat[prochain_coup[0]][prochain_coup[1]] for x in y):
                            prochain_coup = -1
                            for i in self.dico_surbrillance:
                                self.g.changerCouleur(self.dico_surbrillance[i],"cyan")
                        elif self.main_mat[prochain_coup[0]][prochain_coup[1]] == 0:
                            self.g.changerCouleur(self.dico_surbrillance[prochain_coup], "cyan")

                except Exception as e:
                    print(e)
                    continue



#
# g = ouvrirFenetre(1200,600)
# jeu = Morpion(g)
# # jeu.start_ia()
# # jeu.start()
# jeu.start_poke()
