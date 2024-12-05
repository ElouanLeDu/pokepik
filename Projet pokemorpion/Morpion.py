import time
import numpy as np
from tkiteasy import *
import math
from combat import combat_de_pokemon
import pandas as pds
import pygame



class Morpion:
    def __init__(self,g,df,deck1,deck2):
        self.g = g
        self.mat = np.array([[np.zeros((3, 3)) for i in range(3)] for i in range(3)]) #la matrice contenant des matrices qui representent les petits morpion
        self.main_mat = np.zeros((3,3))                                             #la matrice qui represente le grand morpion
        self.dic_asso = {}
        self.fin = False
        self.dico_surbrillance={}
        self.centre = [
            (600, 300,(1,1)), (600, 150,(1,0)), (600, 450,(1,2)),
            (450, 300,(0,1)), (450, 150,(0,0)), (450, 450,(0,2)),
            (750, 300,(2,1)), (750, 150,(2,0)), (750, 450,(2,2))]

        self.mat_poke = np.array([[np.zeros((3, 3)) for i in range(3)] for i in range(3)])
        self.df = df

        pokemon_list = self.df.sample(n=120).index.tolist()
        self.deck = [deck1,deck2]

        self.combat = combat_de_pokemon(self.g,self.df)
        self.asso_poke = {}
        self.co_to_poke = {}
        self.name_to_poke = {}


    def afficher_poke(self):
        for j in range(2) :
            for i in range(60):

                poke = self.g.afficherImage(53.5 + 47*(i%6) + 825 * (j%2),75 + 47 * (i//6),f"pokemon_images/{self.deck[j][i]}.png",43,43)
                if j == 0 :
                    joueur = 1
                else:
                    joueur = -1
                self.asso_poke[poke] = {"co_mat":(-1,-1), "co": (53.5 + 47*(i%6) + 825 * (j%2),75 + 47 * (i//6)),"name" : self.deck[j][i], "joueur": joueur, "dispo" : True }
                self.name_to_poke[self.deck[j][i]] = poke


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

        pygame.mixer.init()
        pygame.mixer.music.load("musiques/Morpion_msc.mp3")
        pygame.mixer.music.play(-1)


        self.afficher_morpion()
        #le joueur qui commence
        j = 1
        prochain_coup = -1
        while not self.fin:

            cpt = 0

            for ligne in range(3):
                for colonne in range(3):
                    if self.main_mat[ligne][colonne] !=0 or all(x != 0 for y in self.mat[ligne][colonne] for x in y):
                        cpt += 1
            if cpt == 9:
                return 0
                self.fin=True

            clic = self.g.recupererClic()

            if clic :
                #l'utilisation de try est surtout utile pour voir si le clic ramene bien a un objet
                try :
                    objet = self.g.recupererObjet(clic.x, clic.y)
                    #on verfifie si l'emplacement peut etre jouer
                    if objet in self.dic_asso and self.main_mat[self.dic_asso[objet][0]][self.dic_asso[objet][1]] == 0 and self.mat[self.dic_asso[objet][0]][self.dic_asso[objet][1]][self.dic_asso[objet][2]][self.dic_asso[objet][3]] == 0 :
                        #si le prochain coup = -1 alors on peut jouer ou on veut
                        if prochain_coup ==-1 or prochain_coup == (self.dic_asso[objet][0],self.dic_asso[objet][1]) :
                            if j == 1:
                                self.g.afficherImage(objet.x + 2.5, objet.y + 2.5, "rond_croix/rond.png")
                                self.mat[self.dic_asso[objet][0]][self.dic_asso[objet][1]][self.dic_asso[objet][2]][self.dic_asso[objet][3]] = 1
                                j = -1
                            elif j == -1:
                                self.g.afficherImage(objet.x + 2.5, objet.y + 2.5, "rond_croix/croix.png")
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
                                image = "rond_croix/croix2.png"
                            elif win == 1 :
                                image = "rond_croix/rond2.png"
                            self.g.afficherImage( 375 + self.dic_asso[objet][1] * 150 ,75 + self.dic_asso[objet][0] * 150, image )

                            win_globale = self.verif_win(self.main_mat)
                            if abs(win_globale) == 1 :
                                return win_globale
                                self.fin = True

                        if abs(self.main_mat[prochain_coup[0]][prochain_coup[1]]) == 1 or all(x != 0 for y in self.mat[prochain_coup[0]][prochain_coup[1]] for x in y):
                            prochain_coup = -1
                            for i in self.dico_surbrillance:
                                self.g.changerCouleur(self.dico_surbrillance[i],"green")
                        elif self.main_mat[prochain_coup[0]][prochain_coup[1]] == 0:
                            self.g.changerCouleur(self.dico_surbrillance[prochain_coup], "green")
                except :
                    continue
        pygame.mixer.music.stop()


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
        pygame.mixer.init()
        pygame.mixer.music.load("musiques/PVE.mp3")
        pygame.mixer.music.play(-1)


        self.afficher_morpion()
        j = 1
        prochain_coup = -1
        while not self.fin:
            if j == 1:

                cpt = 0

                for ligne in range(3):
                    for colonne in range(3):
                        if self.main_mat[ligne][colonne] != 0 or all(
                                x != 0 for y in self.mat[ligne][colonne] for x in y):
                            cpt += 1
                if cpt == 9:
                    return 0
                    self.fin = True

                clic = self.g.recupererClic()

                if clic :
                    try :
                        objet = self.g.recupererObjet(clic.x, clic.y)
                        if objet in self.dic_asso and self.main_mat[self.dic_asso[objet][0]][self.dic_asso[objet][1]] == 0 and self.mat[self.dic_asso[objet][0]][self.dic_asso[objet][1]][self.dic_asso[objet][2]][self.dic_asso[objet][3]] == 0 :
                            if prochain_coup ==-1 or prochain_coup == (self.dic_asso[objet][0],self.dic_asso[objet][1]) :
                                self.g.afficherImage(objet.x + 2.5, objet.y + 2.5, "rond_croix/rond.png")
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
                                    image = "rond_croix/croix2.png"
                                elif win == 1:
                                    image = "rond_croix/rond2.png"
                                self.g.afficherImage(375 + self.dic_asso[objet][1] * 150,
                                                     75 + self.dic_asso[objet][0] * 150, image)

                                win_globale = self.verif_win(self.main_mat)
                                if abs(win_globale) == 1:
                                    if win_globale == -1 :
                                        return 2
                                    else :
                                        return win_globale
                                    self.fin = True

                        if abs(self.main_mat[prochain_coup[0]][prochain_coup[1]]) == 1:
                                prochain_coup = -1
                                for i in self.dico_surbrillance:
                                    self.g.changerCouleur(self.dico_surbrillance[i], "green")
                        elif self.main_mat[prochain_coup[0]][prochain_coup[1]] == 0:
                            self.g.changerCouleur(self.dico_surbrillance[prochain_coup], "green")
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
                        image = "rond_croix/croix2.png"
                    elif win == 1:
                        image = "rond_croix/rond2.png"
                    self.g.afficherImage(375 + coup_ia[1][1] * 150,75 + coup_ia[1][0] * 150, image)

                    win_globale = self.verif_win(self.main_mat)
                    if abs(win_globale) == 1:
                        if win == -1:
                            return 2
                        else:
                            return win_globale
                        self.fin = True

                if abs(self.main_mat[prochain_coup[0]][prochain_coup[1]]) == 1 or all(x != 0 for y in self.mat[prochain_coup[0]][prochain_coup[1]] for x in y):
                    prochain_coup = -1
                    for i in self.dico_surbrillance:
                        self.g.changerCouleur(self.dico_surbrillance[i], "green")
                elif self.main_mat[prochain_coup[0]][prochain_coup[1]] == 0:
                    self.g.changerCouleur(self.dico_surbrillance[prochain_coup], "green")
                self.g.actualiser()
        pygame.mixer.music.stop()

    def start_poke(self):
        pygame.mixer.init()
        pygame.mixer.music.load("musiques/Morpion_msc.mp3")
        pygame.mixer.music.play(-1)

        self.afficher_poke()
        self.afficher_morpion()


        #le joueur qui commence
        j = 1
        rectangle = self.g.dessinerRectangle(10000,10000,43,43,"red")
        rectangle1 = self.g.dessinerRectangle(10000,10000,43,43,"blue")
        stat = self.g.afficherTexte("",600,550,"white")
        self.g.placerAuDessous(rectangle1)
        self.g.placerAuDessous(rectangle)

        prochain_coup = -1
        poke_choisi = None
        while not self.fin:

            cpt = 0

            for ligne in range(3):
                for colonne in range(3):
                    if self.main_mat[ligne][colonne] != 0 or all(x != 0 for y in self.mat[ligne][colonne] for x in y):
                        cpt += 1
            if cpt == 9:
                return 0
                self.fin = True

            clic = self.g.recupererClic()

            if clic :
                try:
                    a = self.g.find_overlapping(clic.x, clic.y,clic.x, clic.y)
                    try :
                        objet = self.g.recupererObjet(clic.x, clic.y)
                    except :
                        a = self.g.find_overlapping(clic.x, clic.y, clic.x, clic.y)
                        self.g.delete(a[-1])
                        objet = self.g.recupererObjet(clic.x, clic.y)
                    if objet in self.asso_poke and self.asso_poke[objet]["dispo"] and self.asso_poke[objet]["joueur"] == j:
                        if j == 1 :
                            obj = rectangle
                        else :
                            obj = rectangle1
                        name = self.asso_poke[objet]["name"]
                        texte = "Attaque : " + str(self.df.loc[name,"Attack"]) + ", Defense : " + str(self.df.loc[name, "Defense"]) + ", HP : " + str(self.df.loc[name, "HP"]) + " Speed : " + str(self.df.loc[name,"Speed"])
                        self.g.changerTexte(stat,texte)
                        self.g.deplacer(obj,self.asso_poke[objet]["co"][0]-obj.x,self.asso_poke[objet]["co"][1] - obj.y)
                        poke_choisi = objet

                    if (poke_choisi and self.asso_poke[poke_choisi]["dispo"] and objet in self.dic_asso
                            and self.main_mat[self.dic_asso[objet][0]][self.dic_asso[objet][1]] == 0
                            and self.mat_poke[self.dic_asso[objet][0]][self.dic_asso[objet][1]][self.dic_asso[objet][2]][self.dic_asso[objet][3]] == 0
                            and self.mat[self.dic_asso[objet][0]][self.dic_asso[objet][1]][self.dic_asso[objet][2]][self.dic_asso[objet][3]] != j) :

                        self.g.changerTexte(stat, "")
                        if prochain_coup ==-1 or prochain_coup == (self.dic_asso[objet][0],self.dic_asso[objet][1]) :
                            if self.mat[self.dic_asso[objet][0]][self.dic_asso[objet][1]][self.dic_asso[objet][2]][self.dic_asso[objet][3]] == -j :

                                poke_selec = self.co_to_poke[(self.dic_asso[objet][0],self.dic_asso[objet][1],self.dic_asso[objet][2],self.dic_asso[objet][3])]

                                resultat = self.combat.combat(self.asso_poke[poke_choisi]["name"],self.asso_poke[poke_selec]["name"])
                                pygame.mixer.init()
                                pygame.mixer.music.load("Morpion_msc.mp3")
                                pygame.mixer.music.play(-1)


                                winner = self.name_to_poke[resultat[0]]
                                loser = self.name_to_poke[resultat[1]]

                                self.asso_poke[winner]["dispo"] = False
                                self.asso_poke[loser]["dispo"] = True

                                self.mat_poke[self.dic_asso[objet][0]][self.dic_asso[objet][1]][self.dic_asso[objet][2]][self.dic_asso[objet][3]] = self.asso_poke[winner]["joueur"]
                                self.mat[self.dic_asso[objet][0]][self.dic_asso[objet][1]][self.dic_asso[objet][2]][self.dic_asso[objet][3]] = self.asso_poke[winner]["joueur"]

                                self.g.dessinerRectangle(objet.x,objet.y,44,44,"black")

                                if j == self.asso_poke[winner]["joueur"]:
                                    self.g.afficherImage(objet.x + 2.5, objet.y + 2.5, "rond_croix/rond.png")

                                else:
                                    self.g.afficherImage(objet.x + 2.5, objet.y + 2.5, "rond_croix/croix.png")

                                try:
                                    self.g.supprimer(winner)
                                except:
                                    continue
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
                            self.g.dessinerRectangle(375 + self.dic_asso[objet][1] * 150 + 1,75 + self.dic_asso[objet][0] * 150 + 1,148,148,"black")
                            if win == -1 :
                                image = "rond_croix/rond2.png"
                            else :
                                image = "rond_croix/croix2.png"
                            self.g.afficherImage( 375 + self.dic_asso[objet][1] * 150 ,75 + self.dic_asso[objet][0] * 150, image )

                            win_globale = self.verif_win(self.main_mat)
                            if abs(win_globale) == 1 :
                                if win_globale == -1 :
                                    return  2
                                else :
                                    return win_globale
                                self.fin = True

                        if abs(self.main_mat[prochain_coup[0]][prochain_coup[1]]) == 1 or all(x != 0 for y in self.mat[prochain_coup[0]][prochain_coup[1]] for x in y):
                            prochain_coup = -1
                            for i in self.dico_surbrillance:
                                self.g.changerCouleur(self.dico_surbrillance[i],"green")
                        elif self.main_mat[prochain_coup[0]][prochain_coup[1]] == 0:
                            self.g.changerCouleur(self.dico_surbrillance[prochain_coup], "green")
                except :
                    continue

        pygame.mixer.music.stop()

    def a_un_avantage(self, pokemon, adversaire_types):

        types_pokemon = [self.df.loc[pokemon, "Type 1"], self.df.loc[pokemon, "Type 2"]]
        for type_adv in adversaire_types:
            if not pds.isna(type_adv):  # Vérifie que le type adverse existe
                for type_pokemon in types_pokemon:
                    if not pds.isna(type_pokemon) and type_adv in self.combat.dict_av.get(type_pokemon, []):
                        return True
        return False

    def est_suffisant(self, pokemon, adversaire_stats):

        stats_pokemon = self.df.loc[pokemon]
        attaque_effective = max(
            stats_pokemon["Attack"] - adversaire_stats["Defense"],
            stats_pokemon["Sp. Atk"] - adversaire_stats["Sp. Def"])

        return attaque_effective > 0 and stats_pokemon["Speed"] >= adversaire_stats["Speed"]

    def choisir_pokemon(self, adversaire, ma_liste):

        # Récupérer les stats de l'adversaire
        adversaire_stats = self.df.loc[adversaire]
        adversaire_types = [adversaire_stats["Type 1"], adversaire_stats["Type 2"]]

        # Filtrer les Pokémon ayant un avantage de type
        pokemon_avantage = [poke for poke in ma_liste if self.a_un_avantage(poke, adversaire_types)]

        # Si aucun Pokémon n'a un avantage, utiliser tous les Pokémon disponibles
        pokemon_consideres = pokemon_avantage if pokemon_avantage else ma_liste

        # Filtrer les Pokémon capables de gagner
        pokemon_suffisants = [poke for poke in pokemon_consideres if self.est_suffisant(poke, adversaire_stats)]

        # Si aucun Pokémon ne peut gagner, retourner le meilleur et soit il gagnera soit il montera de niveau tout benef
        if not pokemon_suffisants:
            ma_liste.sort(key=lambda p: (self.df.loc[p, "Attack"] + self.df.loc[p, "Sp. Atk"], self.df.loc[p, "Speed"]))
            return ma_liste[-1]

        # Trier les Pokémon capables de gagner par puissance croissante
        pokemon_suffisants.sort(key=lambda p: (self.df.loc[p, "Attack"] + self.df.loc[p, "Sp. Atk"],self.df.loc[p, "Speed"]))
        return pokemon_suffisants[0]  # Le plus faible capable de gagner

    def coup_bloquant(self,mat,pos,j):
        mat[pos[0]][pos[1]] = -j
        if self.verif_win(mat) == j:
            mat[pos[0]][pos[1]] = 0
            return True
        else :
            mat[pos[0]][pos[1]] = 0
            return False

    def minimax_poke(self, main_mat, grille_active, profondeur, alpha, beta, joueur_max, mat_poke):

        meilleur_coup = -1

        evalfin = self.eval_grand(main_mat, grille_active)

        if profondeur <= 0 or abs(evalfin) > 5000:
            return {0: evalfin, 1: meilleur_coup}

        if grille_active == -1 or self.verif_win(main_mat[grille_active[0]][grille_active[1]]) != 0 or all(x != 0 for y in main_mat[grille_active[0]][grille_active[1]] for x in y):
            grille_active = -1  # on peut jouer sur toute les grilles

        # on commence par le joueur maximisant
        if joueur_max:
            max_eval = -math.inf
            # on parcours toutes les cases d'un petit morpion
            for y in range(3):
                for x in range(3):
                    # si on peut jouer sur toutes les grilles il faut parcourir toute les positions possible ca peut donc prendre plus de temp
                    if grille_active == -1:
                        for h in range(3):
                            for l in range(3):
                                if self.verif_win(main_mat[h][l]) == 0:
                                    if mat_poke[h][l][y][x] == 0 and main_mat[h][l][y][x] != -1:
                                        coup_pre = main_mat[h][l][y][x]
                                        main_mat[h][l][y][x] = -1
                                        mat_poke[h][l][y][x] = -1
                                        eval = self.minimax_poke(main_mat, (y, x), profondeur - 1, alpha, beta, False, mat_poke)
                                        main_mat[h][l][y][x] = coup_pre
                                        mat_poke[h][l][y][x] = 0

                                        monstre = eval[0]
                                        if monstre > max_eval:
                                            max_eval = monstre
                                            # on sauvegarde le coup qui a permis "d'ameliorer le score"
                                            meilleur_coup = (h, l, y, x)
                                        alpha = max(alpha, monstre)

                                        # Coupure alpha-bêta
                                        if beta <= alpha:
                                            break

                                    if beta <= alpha:
                                        break

                    else:
                        if mat_poke[grille_active[0]][grille_active[1]][y][x] == 0 and main_mat[grille_active[0]][grille_active[1]][y][x] != -1:
                            coup_pre = main_mat[grille_active[0]][grille_active[1]][y][x]
                            main_mat[grille_active[0]][grille_active[1]][y][x] = -1
                            eval = self.minimax_poke(main_mat, (y, x), profondeur - 1, alpha, beta, False, mat_poke)
                            main_mat[grille_active[0]][grille_active[1]][y][x] = coup_pre

                            monstre = eval[0]
                            if monstre > max_eval:
                                max_eval = monstre
                                meilleur_coup = (grille_active[0], grille_active[1], y, x)
                            alpha = max(alpha, monstre)
                            if beta <= alpha:
                                break
                if beta <= alpha:
                    break

            return {0: max_eval, 1: meilleur_coup}

        # on refait quasi la meme chose pour le joueur minimisant
        else:
            min_eval = math.inf
            for y in range(3):
                for x in range(3):
                    if grille_active == -1:
                        for h in range(3):
                            for l in range(3):
                                if self.verif_win(main_mat[h][l]) == 0:
                                    if mat_poke[h][l][y][x] == 0 and main_mat[h][l][y][x] != 1:
                                        coup_pre = main_mat[h][l][y][x]
                                        main_mat[h][l][y][x] = 1
                                        mat_poke[h][l][y][x] = 1
                                        eval = self.minimax_poke(main_mat, (y, x), profondeur - 1, alpha, beta, True,mat_poke)
                                        main_mat[h][l][y][x] = coup_pre
                                        mat_poke[h][l][y][x] = 0

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

                    else:
                        if mat_poke[grille_active[0]][grille_active[1]][y][x] == 0 and main_mat[grille_active[0]][grille_active[1]][y][x] != 1:
                            coup_pre = main_mat[grille_active[0]][grille_active[1]][y][x]
                            main_mat[grille_active[0]][grille_active[1]][y][x] = 1
                            eval = self.minimax_poke(main_mat, (y, x), profondeur - 1, alpha, beta, True, mat_poke)
                            main_mat[grille_active[0]][grille_active[1]][y][x] = coup_pre

                            monstre = eval[0]
                            if monstre < min_eval:
                                min_eval = monstre
                                meilleur_coup = (grille_active[0], grille_active[1], y, x)
                            beta = min(beta, monstre)
                            if beta <= alpha:
                                break
                if beta <= alpha:
                    break

            return {0: min_eval, 1: meilleur_coup}

    def start_poke_ia(self):
        pygame.mixer.init()
        pygame.mixer.music.load("musiques/PVE.mp3")
        pygame.mixer.music.play(-1)

        self.afficher_poke()
        self.afficher_morpion()

        #le joueur qui commence
        j = 1
        rectangle = self.g.dessinerRectangle(10000,10000,43,43,"red")
        rectangle1 = self.g.dessinerRectangle(10000,10000,43,43,"blue")
        self.g.placerAuDessous(rectangle1)
        self.g.placerAuDessous(rectangle)
        stat = self.g.afficherTexte("", 600,550, "white")

        prochain_coup = -1
        poke_choisi = None
        while not self.fin:

            cpt = 0

            for ligne in range(3):
                for colonne in range(3):
                    if self.main_mat[ligne][colonne] != 0 or all(
                            x != 0 for y in self.mat[ligne][colonne] for x in y):
                        cpt += 1
            if cpt == 9:
                return 0
                self.fin = True

            if j == 1 :
                try:
                    clic = self.g.recupererClic()
                    if clic :
                        a = self.g.find_overlapping(clic.x, clic.y,clic.x, clic.y)
                        try :
                            objet = self.g.recupererObjet(clic.x, clic.y)
                        except :
                            a = self.g.find_overlapping(clic.x, clic.y, clic.x, clic.y)
                            self.g.delete(a[-1])
                            objet = self.g.recupererObjet(clic.x, clic.y)
                        if objet in self.asso_poke and self.asso_poke[objet]["dispo"] and self.asso_poke[objet]["joueur"] == j:
                            if j == 1 :
                                obj = rectangle
                            else :
                                obj = rectangle1
                            name = self.asso_poke[objet]["name"]
                            texte = "Attaque : " + str(self.df.loc[name, "Attack"]) + ", Defense : " + str(self.df.loc[name, "Defense"]) + ", HP : " + str(self.df.loc[name, "HP"]) + " Speed : " + str(self.df.loc[name, "Speed"])
                            self.g.changerTexte(stat, texte)
                            self.g.deplacer(obj,self.asso_poke[objet]["co"][0]-obj.x,self.asso_poke[objet]["co"][1] - obj.y)
                            poke_choisi = objet

                        if (poke_choisi and self.asso_poke[poke_choisi]["dispo"] and objet in self.dic_asso
                                and self.main_mat[self.dic_asso[objet][0]][self.dic_asso[objet][1]] == 0
                                and self.mat_poke[self.dic_asso[objet][0]][self.dic_asso[objet][1]][self.dic_asso[objet][2]][self.dic_asso[objet][3]] == 0
                                and self.mat[self.dic_asso[objet][0]][self.dic_asso[objet][1]][self.dic_asso[objet][2]][self.dic_asso[objet][3]] != j) :

                            self.g.changerTexte(stat, "")

                            if prochain_coup ==-1 or prochain_coup == (self.dic_asso[objet][0],self.dic_asso[objet][1]) :
                                if self.mat[self.dic_asso[objet][0]][self.dic_asso[objet][1]][self.dic_asso[objet][2]][self.dic_asso[objet][3]] == -j :

                                    poke_selec = self.co_to_poke[(self.dic_asso[objet][0],self.dic_asso[objet][1],self.dic_asso[objet][2],self.dic_asso[objet][3])]

                                    resultat = self.combat.combat(self.asso_poke[poke_choisi]["name"],self.asso_poke[poke_selec]["name"])
                                    pygame.mixer.init()
                                    pygame.mixer.music.load("PVE.mp3")
                                    pygame.mixer.music.play(-1)
                                    winner = self.name_to_poke[resultat[0]]
                                    loser = self.name_to_poke[resultat[1]]

                                    self.asso_poke[winner]["dispo"] = False
                                    self.asso_poke[loser]["dispo"] = True

                                    self.mat_poke[self.dic_asso[objet][0]][self.dic_asso[objet][1]][self.dic_asso[objet][2]][self.dic_asso[objet][3]] = self.asso_poke[winner]["joueur"]
                                    self.mat[self.dic_asso[objet][0]][self.dic_asso[objet][1]][self.dic_asso[objet][2]][self.dic_asso[objet][3]] = self.asso_poke[winner]["joueur"]

                                    self.g.dessinerRectangle(objet.x,objet.y,44,44,"black")

                                    if j == self.asso_poke[winner]["joueur"]:
                                        self.g.afficherImage(objet.x + 2.5, objet.y + 2.5, "rond_croix/croix.png")

                                    else:
                                        self.g.afficherImage(objet.x + 2.5, objet.y + 2.5, "rond_croix/rond.png")

                                    try:
                                        self.g.supprimer(winner)
                                    except:
                                        continue
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
                                image = "rond_croix/rond2.png"
                            else :
                                image = "rond_croix/croix2.png"
                            self.g.afficherImage( 375 + self.dic_asso[objet][1] * 150 ,75 + self.dic_asso[objet][0] * 150, image )

                            win_global = self.verif_win(self.main_mat)
                            if abs(win_global) == 1:
                                if win_global == -1:
                                    return 2
                                else:
                                    return win_global
                                self.fin = True

                        if abs(self.main_mat[prochain_coup[0]][prochain_coup[1]]) == 1 or all(x != 0 for y in self.mat[prochain_coup[0]][prochain_coup[1]] for x in y):
                            prochain_coup = -1
                            for i in self.dico_surbrillance:
                                self.g.changerCouleur(self.dico_surbrillance[i],"green")
                        elif self.main_mat[prochain_coup[0]][prochain_coup[1]] == 0:
                            self.g.changerCouleur(self.dico_surbrillance[prochain_coup], "green")
                except :
                    continue
                self.g.actualiser()

            else :
                nb_coup_possible = 0
                for x in range(3):
                    for y in range(3):
                        if self.verif_win(self.mat[x][y]) == 0:
                            for x1 in range(3):
                                for y1 in range(3):
                                    if self.mat[x][y][x1][y1] == 0:
                                        nb_coup_possible += 1
                coup_ia = self.minimax_poke(self.mat, prochain_coup, min(4, nb_coup_possible), -math.inf, math.inf, True,self.mat_poke)

                if self.mat[coup_ia[1][0]][coup_ia[1][1]][coup_ia[1][2]][coup_ia[1][3]] == 1 :
                    a = self.co_to_poke[(coup_ia[1][0],coup_ia[1][1],coup_ia[1][2],coup_ia[1][3])]
                    adversaire = self.asso_poke[a]["name"]
                    poke_choisi = self.choisir_pokemon(adversaire,self.deck[1])


                    resultat = self.combat.combat(poke_choisi, adversaire)
                    pygame.mixer.init()
                    pygame.mixer.music.load("PVE.mp3")
                    pygame.mixer.music.play(-1)
                    self.g.actualiser()

                    winner = self.name_to_poke[resultat[0]]
                    loser = self.name_to_poke[resultat[1]]

                    self.asso_poke[winner]["dispo"] = False
                    self.asso_poke[loser]["dispo"] = True

                    self.mat_poke[coup_ia[1][0]][coup_ia[1][1]][coup_ia[1][2]][coup_ia[1][3]] = self.asso_poke[winner]["joueur"]
                    self.mat[coup_ia[1][0]][coup_ia[1][1]][coup_ia[1][2]][coup_ia[1][3]] = self.asso_poke[winner]["joueur"]

                    self.g.dessinerRectangle(a.x, a.y, 44, 44, "black")

                    if j == self.asso_poke[winner]["joueur"]:
                        self.g.afficherImage(a.x + 2.5, a.y + 2.5, "rond_croix/rond.png")

                    else:
                        self.g.afficherImage(a.x + 2.5, a.y + 2.5, "rond_croix/croix.png")

                    try:
                        self.g.supprimer(winner)
                    except:
                        continue
                    self.g.deplacer(loser, self.asso_poke[loser]["co"][0] - loser.x,self.asso_poke[loser]["co"][1] - loser.y)

                    if prochain_coup != -1:
                        self.g.changerCouleur(self.dico_surbrillance[prochain_coup], "black")
                    else:
                        for i in self.dico_surbrillance:
                            self.g.changerCouleur(self.dico_surbrillance[i], "black")

                    prochain_coup = (coup_ia[1][2], coup_ia[1][3])

                    win = self.verif_win(self.mat[coup_ia[1][0]][coup_ia[1][1]])
                    if abs(win) == 1:
                        self.main_mat[coup_ia[1][0]][coup_ia[1][1]] = win
                        self.g.dessinerRectangle(375 + coup_ia[1][1] * 150 + 1, 75 + coup_ia[1][0] * 150 + 1, 148, 148,
                                                 "black")
                        if win == -1:
                            image = "rond_croix/rond2.png"
                        else:
                            image = "rond_croix/croix2.png"
                        self.g.afficherImage(375 + coup_ia[1][1] * 150, 75 + coup_ia[1][0] * 150, image)

                        win_globale = self.verif_win(self.main_mat)
                        if abs(win_globale) == 1:
                            if win_globale == -1:
                                return 2
                            else:
                                return win_globale
                            self.fin = True

                    if abs(self.main_mat[prochain_coup[0]][prochain_coup[1]]) == 1 or all(
                            x != 0 for y in self.mat[prochain_coup[0]][prochain_coup[1]] for x in y):
                        prochain_coup = -1
                        for i in self.dico_surbrillance:
                            self.g.changerCouleur(self.dico_surbrillance[i], "green")
                    elif self.main_mat[prochain_coup[0]][prochain_coup[1]] == 0:
                        self.g.changerCouleur(self.dico_surbrillance[prochain_coup], "green")

                else :
                    deck = []
                    for i in self.asso_poke :
                        if self.asso_poke[i]["dispo"] and self.asso_poke[i]["joueur"] == -1 :
                            deck.append(self.asso_poke[i]["name"])
                    filtered_df = self.df.loc[deck]
                    sorted_df = filtered_df.sort_values(by=["Attack", "HP", "Sp. Atk", "Speed"], ascending=False)
                    deck_trie = sorted_df.index.tolist()


                    if self.coup_bloquant( self.mat[coup_ia[1][0]][coup_ia[1][1]],(coup_ia[1][2],coup_ia[1][3]), -1):
                        poke_choisi = deck_trie[-1]
                    else :
                        milieu = len(deck_trie)//2
                        poke_choisi = deck_trie[milieu]

                    poke_choisi = self.name_to_poke[poke_choisi]

                    centre = (450 + coup_ia[1][1] * 150, 150 + coup_ia[1][0] * 150)
                    self.g.deplacer(poke_choisi, (centre[0] - 67.5) + 45 * coup_ia[1][3] - poke_choisi.x + 1, (centre[1] - 67.5) + 45 * coup_ia[1][2] - poke_choisi.y + 1)

                    if j == 1:
                        col = "red"
                    else:
                        col = "blue"


                    self.g.dessinerRectangle(poke_choisi.x, poke_choisi.y, 44, 44, col)
                    self.g.placerAuDessus(poke_choisi)
                    self.asso_poke[poke_choisi]["dispo"] = False
                    self.asso_poke[poke_choisi]["co_mat"] = (coup_ia[1][0],coup_ia[1][1],coup_ia[1][2],coup_ia[1][3])
                    self.co_to_poke[(coup_ia[1][0],coup_ia[1][1],coup_ia[1][2],coup_ia[1][3])] = poke_choisi
                    self.dic_asso[poke_choisi] = (coup_ia[1][0],coup_ia[1][1],coup_ia[1][2],coup_ia[1][3])
                    self.mat[coup_ia[1][0]][coup_ia[1][1]][coup_ia[1][2]][coup_ia[1][3]] = j

                    if prochain_coup != -1:
                        self.g.changerCouleur(self.dico_surbrillance[prochain_coup], "black")
                    else:
                        for i in self.dico_surbrillance:
                            self.g.changerCouleur(self.dico_surbrillance[i], "black")


                    prochain_coup = (coup_ia[1][2],coup_ia[1][3])

                    win = self.verif_win(self.mat[coup_ia[1][0]][coup_ia[1][1]])
                    if abs(win) == 1:
                        self.main_mat[coup_ia[1][0]][coup_ia[1][1]] = win
                        self.g.dessinerRectangle(375 + coup_ia[1][1] * 150 + 1, 75 + coup_ia[1][0] * 150 + 1, 148, 148, "black")
                        if win == -1:
                            image = "rond_croix/rond2.png"
                        else:
                            image = "rond_croix/croix2.png"
                        self.g.afficherImage(375 + coup_ia[1][1] * 150, 75 + coup_ia[1][0] * 150,image)
                        win_global = self.verif_win(self.main_mat)
                        if abs(win_global) == 1:
                            if win_global == -1 :
                                return 2
                            else:
                                return win_global
                            self.fin = True

                    if abs(self.main_mat[prochain_coup[0]][prochain_coup[1]]) == 1 or all(x != 0 for y in self.mat[prochain_coup[0]][prochain_coup[1]] for x in y):
                        prochain_coup = -1
                        for i in self.dico_surbrillance:
                            self.g.changerCouleur(self.dico_surbrillance[i], "green")
                    elif self.main_mat[prochain_coup[0]][prochain_coup[1]] == 0:
                        self.g.changerCouleur(self.dico_surbrillance[prochain_coup], "green")

                j = 1
        pygame.mixer.music.stop()

    def start_poke_ia_vs_ia(self):
        self.afficher_morpion()
        self.afficher_poke()

        # le joueur qui commence
        j = 1

        prochain_coup = -1
        while not self.fin:

            cpt = 0

            for ligne in range(3):
                for colonne in range(3):
                    if self.main_mat[ligne][colonne] != 0 or all(
                            x != 0 for y in self.mat[ligne][colonne] for x in y):
                        cpt += 1
            if cpt == 9:
                return 0
                self.fin = True

            #debut jeu

            nb_coup_possible = 0
            for x in range(3):
                for y in range(3):
                    if self.verif_win(self.mat[x][y]) == 0:
                        for x1 in range(3):
                            for y1 in range(3):
                                if self.mat[x][y][x1][y1] == 0:
                                    nb_coup_possible += 1
            if j == 1 :
                joueur = False
            else:
                joueur = True

            coup_ia = self.minimax_poke(self.mat, prochain_coup, min(4, nb_coup_possible), -math.inf, math.inf,joueur, self.mat_poke)

            if self.mat[coup_ia[1][0]][coup_ia[1][1]][coup_ia[1][2]][coup_ia[1][3]] == -j:
                a = self.co_to_poke[(coup_ia[1][0], coup_ia[1][1], coup_ia[1][2], coup_ia[1][3])]
                adversaire = self.asso_poke[a]["name"]
                if j == 1 :
                    indice = 0
                else :
                    indice = 1
                poke_choisi = self.choisir_pokemon(adversaire, self.deck[indice])

                resultat = self.combat.combat(poke_choisi, adversaire)
                self.g.actualiser()

                winner = self.name_to_poke[resultat[0]]
                loser = self.name_to_poke[resultat[1]]

                self.asso_poke[winner]["dispo"] = False
                self.asso_poke[loser]["dispo"] = True

                self.mat_poke[coup_ia[1][0]][coup_ia[1][1]][coup_ia[1][2]][coup_ia[1][3]] = self.asso_poke[winner][
                    "joueur"]
                self.mat[coup_ia[1][0]][coup_ia[1][1]][coup_ia[1][2]][coup_ia[1][3]] = self.asso_poke[winner][
                    "joueur"]

                self.g.dessinerRectangle(a.x, a.y, 44, 44, "black")

                if j == self.asso_poke[winner]["joueur"]:
                    self.g.afficherImage(a.x + 2.5, a.y + 2.5, "rond.png")

                else:
                    self.g.afficherImage(a.x + 2.5, a.y + 2.5, "croix.png")

                try :
                    self.g.supprimer(winner)
                except :
                    continue
                self.g.deplacer(loser, self.asso_poke[loser]["co"][0] - loser.x,self.asso_poke[loser]["co"][1] - loser.y)

                if prochain_coup != -1:
                    self.g.changerCouleur(self.dico_surbrillance[prochain_coup], "black")
                else:
                    for i in self.dico_surbrillance:
                        self.g.changerCouleur(self.dico_surbrillance[i], "black")

                prochain_coup = (coup_ia[1][2], coup_ia[1][3])

                win = self.verif_win(self.mat[coup_ia[1][0]][coup_ia[1][1]])
                if abs(win) == 1:
                    self.main_mat[coup_ia[1][0]][coup_ia[1][1]] = win
                    self.g.dessinerRectangle(375 + coup_ia[1][1] * 150 + 1, 75 + coup_ia[1][0] * 150 + 1, 148, 148,
                                             "black")
                    if win == -1:
                        image = "rond2.png"
                    else:
                        image = "croix2.png"
                    self.g.afficherImage(375 + coup_ia[1][1] * 150, 75 + coup_ia[1][0] * 150, image)

                    win_globale = self.verif_win(self.main_mat)
                    if abs(win_globale) == 1:
                        return win_globale
                        self.fin = True

                if abs(self.main_mat[prochain_coup[0]][prochain_coup[1]]) == 1 or all(
                        x != 0 for y in self.mat[prochain_coup[0]][prochain_coup[1]] for x in y):
                    prochain_coup = -1
                    for i in self.dico_surbrillance:
                        self.g.changerCouleur(self.dico_surbrillance[i], "cyan")
                elif self.main_mat[prochain_coup[0]][prochain_coup[1]] == 0:
                    self.g.changerCouleur(self.dico_surbrillance[prochain_coup], "cyan")

            else:
                deck = []
                for i in self.asso_poke:
                    if self.asso_poke[i]["dispo"] and self.asso_poke[i]["joueur"] == j:
                        deck.append(self.asso_poke[i]["name"])
                filtered_df = self.df.loc[deck]
                sorted_df = filtered_df.sort_values(by=["Attack", "HP", "Sp. Atk", "Speed"], ascending=False)
                deck_trie = sorted_df.index.tolist()

                if self.coup_bloquant(self.mat[coup_ia[1][0]][coup_ia[1][1]], (coup_ia[1][2], coup_ia[1][3]), -1):
                    poke_choisi = deck_trie[-1]
                else:
                    milieu = len(deck_trie) // 2
                    poke_choisi = deck_trie[milieu]

                poke_choisi = self.name_to_poke[poke_choisi]

                centre = (450 + coup_ia[1][1] * 150, 150 + coup_ia[1][0] * 150)
                self.g.deplacer(poke_choisi, (centre[0] - 67.5) + 45 * coup_ia[1][3] - poke_choisi.x + 1,
                                (centre[1] - 67.5) + 45 * coup_ia[1][2] - poke_choisi.y + 1)

                if j == 1:
                    col = "red"
                else:
                    col = "blue"

                self.g.dessinerRectangle(poke_choisi.x, poke_choisi.y, 44, 44, col)
                self.g.placerAuDessus(poke_choisi)
                self.asso_poke[poke_choisi]["dispo"] = False
                self.asso_poke[poke_choisi]["co_mat"] = (coup_ia[1][0], coup_ia[1][1], coup_ia[1][2], coup_ia[1][3])
                self.co_to_poke[(coup_ia[1][0], coup_ia[1][1], coup_ia[1][2], coup_ia[1][3])] = poke_choisi
                self.dic_asso[poke_choisi] = (coup_ia[1][0], coup_ia[1][1], coup_ia[1][2], coup_ia[1][3])
                self.mat[coup_ia[1][0]][coup_ia[1][1]][coup_ia[1][2]][coup_ia[1][3]] = j

                if prochain_coup != -1:
                    self.g.changerCouleur(self.dico_surbrillance[prochain_coup], "black")
                else:
                    for i in self.dico_surbrillance:
                        self.g.changerCouleur(self.dico_surbrillance[i], "black")

                prochain_coup = (coup_ia[1][2], coup_ia[1][3])

                win = self.verif_win(self.mat[coup_ia[1][0]][coup_ia[1][1]])
                if abs(win) == 1:
                    self.main_mat[coup_ia[1][0]][coup_ia[1][1]] = win
                    self.g.dessinerRectangle(375 + coup_ia[1][1] * 150 + 1, 75 + coup_ia[1][0] * 150 + 1, 148, 148,
                                             "black")
                    if win == -1:
                        image = "rond2.png"
                    else:
                        image = "croix2.png"
                    self.g.afficherImage(375 + coup_ia[1][1] * 150, 75 + coup_ia[1][0] * 150, image)
                    win_global = self.verif_win(self.main_mat)
                    if abs(win_global) == 1:
                        return win_global
                        self.fin = True

                if abs(self.main_mat[prochain_coup[0]][prochain_coup[1]]) == 1 or all(
                        x != 0 for y in self.mat[prochain_coup[0]][prochain_coup[1]] for x in y):
                    prochain_coup = -1
                    for i in self.dico_surbrillance:
                        self.g.changerCouleur(self.dico_surbrillance[i], "cyan")
                elif self.main_mat[prochain_coup[0]][prochain_coup[1]] == 0:
                    self.g.changerCouleur(self.dico_surbrillance[prochain_coup], "cyan")
            self.g.actualiser()
            j = -j

    def start_ia_vs_ia(self):
        self.afficher_morpion()
        j = 1
        prochain_coup = -1
        while not self.fin:

            cpt = 0

            for ligne in range(3):
                for colonne in range(3):
                    if self.main_mat[ligne][colonne] != 0 or all(
                            x != 0 for y in self.mat[ligne][colonne] for x in y):
                        cpt += 1
            if cpt == 9:
                return 0
                self.fin = True

            nb_coup_possible = 0
            for x in range(3):
                for y in range(3):
                    if self.verif_win(self.mat[x][y]) == 0:
                        for x1 in range(3):
                            for y1 in range(3):
                                if self.mat[x][y][x1][y1] == 0:
                                    nb_coup_possible += 1

            if j == 1 :
                joueur = False
            else :
                joueur = True


            coup_ia = self.minimax(self.mat, prochain_coup, min(4, nb_coup_possible), -math.inf, math.inf, joueur)
            self.mat[coup_ia[1][0]][coup_ia[1][1]][coup_ia[1][2]][coup_ia[1][3]] = j

            centre = (450 + coup_ia[1][1] * 150, 150 + coup_ia[1][0] * 150)
            if j == 1 :
                image = "rond.png"
            else :
                image = "croix.png"
            self.g.afficherImage((centre[0] - 67.5) + 45 * coup_ia[1][3] + 2.5,
                                 (centre[1] - 67.5) + 45 * coup_ia[1][2] + 2.5, image)
            j = -j

            if prochain_coup != -1:
                self.g.changerCouleur(self.dico_surbrillance[prochain_coup], "black")
            else:
                for i in self.dico_surbrillance:
                    self.g.changerCouleur(self.dico_surbrillance[i], "black")

            prochain_coup = (coup_ia[1][2], coup_ia[1][3])
            win = self.verif_win(self.mat[coup_ia[1][0]][coup_ia[1][1]])
            if abs(win) == 1:
                self.main_mat[coup_ia[1][0]][coup_ia[1][1]] = win
                self.g.dessinerRectangle(375 + coup_ia[1][1] * 150 + 1,
                                         75 + coup_ia[1][0] * 150 + 1, 148, 148, "black")
                if win == -1:
                    image = "croix2.png"
                elif win == 1:
                    image = "rond2.png"
                self.g.afficherImage(375 + coup_ia[1][1] * 150, 75 + coup_ia[1][0] * 150, image)

                win_globale = self.verif_win(self.main_mat)
                if abs(win_globale) == 1:
                    if win == -1:
                        return 2
                    else:
                        return win_globale
                    self.fin = True

            if abs(self.main_mat[prochain_coup[0]][prochain_coup[1]]) == 1 or all(
                    x != 0 for y in self.mat[prochain_coup[0]][prochain_coup[1]] for x in y):
                prochain_coup = -1
                for i in self.dico_surbrillance:
                    self.g.changerCouleur(self.dico_surbrillance[i], "cyan")
            elif self.main_mat[prochain_coup[0]][prochain_coup[1]] == 0:
                self.g.changerCouleur(self.dico_surbrillance[prochain_coup], "cyan")
            self.g.actualiser()




#g = ouvrirFenetre(1200,600)
#jeu = Morpion(g)
# jeu.start_ia()
# jeu.start()
# jeu.start_poke_ia()
# jeu.start_poke()
# jeu.start_poke_ia_vs_ia()
# jeu.start_ia_vs_ia()
