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
        self.main_mat = np.zeros((3,3))   #la matrice qui represente le grand morpion
        self.dic_asso = {}
        self.fin = False
        self.dico_surbrillance={}   #vas contenir les objets pour gerer la surbrillance
        self.centre = [
            (600, 300,(1,1)), (600, 150,(1,0)), (600, 450,(1,2)),
            (450, 300,(0,1)), (450, 150,(0,0)), (450, 450,(0,2)),
            (750, 300,(2,1)), (750, 150,(2,0)), (750, 450,(2,2))]  #le centre de chaque grand morpion

        self.mat_poke = np.array([[np.zeros((3, 3)) for i in range(3)] for i in range(3)])  #il y'a des 1 ou - 1 si la case a été gagné par un pokemon c'est a dire si on ne peut plus jouer dessus
        self.df = df

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
                #ce dico est la base du jeu poke on peut retrouver toutes les info neccessaires a partir de l'objet graphique
                self.asso_poke[poke] = {"co_mat":(-1,-1), "co": (53.5 + 47*(i%6) + 825 * (j%2),75 + 47 * (i//6)),"name" : self.deck[j][i], "joueur": joueur, "dispo" : True }
                #associe le nom a l'objet graphique
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

            #on verifie si il y'a egalité ou non
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
                            #on actualise la matrice principale avec les win
                            self.main_mat[self.dic_asso[objet][0]][self.dic_asso[objet][1]] = win
                            self.g.dessinerRectangle(375 + self.dic_asso[objet][1] * 150 +1 ,75 + self.dic_asso[objet][0] * 150 + 1,148,148,"black")
                            if win == -1 :
                                image = "rond_croix/croix2.png"
                            elif win == 1 :
                                image = "rond_croix/rond2.png"
                            self.g.afficherImage( 375 + self.dic_asso[objet][1] * 150 ,75 + self.dic_asso[objet][0] * 150, image )
                            #on verifie si il y'a un gagnant
                            win_globale = self.verif_win(self.main_mat)
                            if abs(win_globale) == 1 :
                                return win_globale
                                self.fin = True

                        #on verifie si le prochain coup n'est pas une grille gagné ou complete
                        if abs(self.main_mat[prochain_coup[0]][prochain_coup[1]]) == 1 or all(x != 0 for y in self.mat[prochain_coup[0]][prochain_coup[1]] for x in y):
                            prochain_coup = -1
                            for i in self.dico_surbrillance:
                                self.g.changerCouleur(self.dico_surbrillance[i],"green")
                        elif self.main_mat[prochain_coup[0]][prochain_coup[1]] == 0:
                            self.g.changerCouleur(self.dico_surbrillance[prochain_coup], "green")
                except :
                    #le try permet juste d'eviter l'erreur ou on clic dans le vide
                    continue
        pygame.mixer.music.stop()


    def eval_petit(self,mat):#cette fonction evalue un morpion de base
        #le joueur est représenté par des 1 sur la mat et l'ia par des -1
        evaluation = 0
        score = [[0.2, 0.17, 0.2],
                 [0.17, 0.22, 0.17],
                 [0.2, 0.17, 0.2]] #matrice avec les scores de base pour chaque pos (le centre ++, les coins +, les arretes -)

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
                 [1.4, 1, 1.4]] # matrice avec les scores de base pour chaque pos (le centre ++, les coins +, les arretes -)
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
                                #on verfie si le coup est possible
                                if self.verif_win(main_mat[h][l]) == 0 :
                                    if main_mat[h][l][y][x] == 0:
                                        #on joue le coup
                                        main_mat[h][l][y][x] = -1
                                        #on retourne dans notre fonction en changeant de joueur pour tester en profondeur quelle coup sera le mieux
                                        eval = self.minimax(main_mat, (y, x), profondeur - 1, alpha, beta, False)
                                        #on annule ensuite le coup
                                        main_mat[h][l][y][x] = 0

                                        eval_act = eval[0]
                                        if eval_act > max_eval:
                                            max_eval = eval_act
                                            #on sauvegarde le coup qui a permis "d'ameliorer le score"
                                            meilleur_coup = (h, l, y, x)
                                        alpha = max(alpha, eval_act)

                                        # Coupure alpha-bêta
                                        if beta <= alpha:
                                            break

                                    if beta <= alpha:
                                        break

                    else :
                        #c'est la meme chose juste on ne parcours pas toute les grilles
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

        #on refait quasi la meme chose pour le joueur minimisant, en changeant certaine valeur car on est au joueur minimisant maintenant
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
        pygame.mixer.init()
        pygame.mixer.music.load("musiques/PVE.mp3")
        pygame.mixer.music.play(-1)

        j = 1 #c'est le joueur qui commence 1 pour le joueur et -1 pour l'ia
        prochain_coup = -1
        while not self.fin:
            #quasi la meme chose que sans ia comme c'est le joueur qui joue
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
                #tour de l'ia
                #on calcule le nombre de coup possible pour prendre la bonne profondeur car sinon quand il y'a egalité ca fera une erreur comme il ne pourra plus jouer aucun coup
                nb_coup_possible = 0
                for x in range(3):
                    for y in range(3):
                        if self.verif_win(self.mat[x][y]) == 0 :
                            for x1 in range(3):
                                for y1 in range(3):
                                    if self.mat[x][y][x1][y1]==0:
                                        nb_coup_possible += 1
                #on calcule le meilleur coup avec minimax
                coup_ia = self.minimax(self.mat,prochain_coup,min(4 ,nb_coup_possible),-math.inf,math.inf,True)
                self.mat[coup_ia[1][0]][coup_ia[1][1]][coup_ia[1][2]][coup_ia[1][3]] = -1

                centre = (450 + coup_ia[1][1] * 150, 150 + coup_ia[1][0] * 150)
                self.g.afficherImage((centre[0] - 67.5) + 45 * coup_ia[1][3] + 2.5, (centre[1] - 67.5) + 45 * coup_ia[1][2] + 2.5, "rond_croix/croix.png")

                #la suite ressemble beaucoup au cas avec un joueur normal
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

                j = 1 #on repasse au joueur 1

        pygame.mixer.music.stop()

    def start_poke(self,aff):
        self.afficher_morpion()
        pygame.mixer.init()
        pygame.mixer.music.load("musiques/Morpion_msc.mp3")
        pygame.mixer.music.play(-1)




        #le joueur qui commence
        j = 1
        #tout ca nous permet de gerer la surbrillance du pokemon choisi
        rectangle = self.g.dessinerRectangle(10000,10000,43,43,"red")
        rectangle1 = self.g.dessinerRectangle(10000,10000,43,43,"blue")
        stat = self.g.afficherTexte("",600,550,"black")

        self.afficher_poke()


        prochain_coup = -1
        poke_choisi = None
        while not self.fin:

            cpt = 0

            for ligne in range(3):
                for colonne in range(3):
                    if self.main_mat[ligne][colonne] != 0 or all(x != 0 for y in self.mat[ligne][colonne] for x in y):
                        cpt += 1
            if cpt == 9:
                self.fin = True
                return 0


            clic = self.g.recupererClic()

            if clic :
                try:
                    #ce "a" permet de resoudre un bug qui arrivait apres un combat car un objet graphique ce supprimer mal
                    #il y'avais un objet tkinter mais pas tkiteasy donc j'essaie de recuperer l'objet tkiteasy et si ca ne marche pas je supprime l'objet tkinter en trop
                    a = self.g.find_overlapping(clic.x, clic.y,clic.x, clic.y)
                    try :
                        objet = self.g.recupererObjet(clic.x, clic.y)
                    except :
                        a = self.g.find_overlapping(clic.x, clic.y, clic.x, clic.y)
                        self.g.delete(a[-1])
                        objet = self.g.recupererObjet(clic.x, clic.y)
                    #je regarde si le pokemon cliqué est jouable ou non
                    if objet in self.asso_poke and self.asso_poke[objet]["dispo"] and self.asso_poke[objet]["joueur"] == j:
                        #la je m'occupe de l'affichage quand je selectionne un pokemon
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

                        #le jeu commence si j'ai bien selectionné un pokemon valide et si j'ai cliqué sur un carré libre

                        self.g.changerTexte(stat, "")
                        if prochain_coup ==-1 or prochain_coup == (self.dic_asso[objet][0],self.dic_asso[objet][1]) :
                            #je verifie si je joue simplement sur une case vide ou si j'engage un combat
                            if self.mat[self.dic_asso[objet][0]][self.dic_asso[objet][1]][self.dic_asso[objet][2]][self.dic_asso[objet][3]] == -j :
                                #je retrouve le pokemon sur lequel j'ai cliqué avce ces co dans la matrice
                                poke_selec = self.co_to_poke[(self.dic_asso[objet][0],self.dic_asso[objet][1],self.dic_asso[objet][2],self.dic_asso[objet][3])]
                                #gere l'affichage des combats ou non
                                if aff==1:

                                    resultat = self.combat.combat(self.asso_poke[poke_choisi]["name"],self.asso_poke[poke_selec]["name"])
                                    pygame.mixer.init()
                                    pygame.mixer.music.load("Morpion_msc.mp3")
                                    pygame.mixer.music.play(-1)
                                else :
                                    resultat = self.combat.combat_simple(self.asso_poke[poke_choisi]["name"],
                                                                  self.asso_poke[poke_selec]["name"])


                                winner = self.name_to_poke[resultat[0]]
                                loser = self.name_to_poke[resultat[1]]

                                self.asso_poke[winner]["dispo"] = False
                                self.asso_poke[loser]["dispo"] = True
                                #je met a jour toutes les matrices
                                self.mat_poke[self.dic_asso[objet][0]][self.dic_asso[objet][1]][self.dic_asso[objet][2]][self.dic_asso[objet][3]] = self.asso_poke[winner]["joueur"]
                                self.mat[self.dic_asso[objet][0]][self.dic_asso[objet][1]][self.dic_asso[objet][2]][self.dic_asso[objet][3]] = self.asso_poke[winner]["joueur"]

                                #j'affiche un rond ou une croix

                                self.g.dessinerRectangle(objet.x,objet.y,44,44,"black")

                                if j == self.asso_poke[winner]["joueur"]:
                                    self.g.afficherImage(objet.x + 2.5, objet.y + 2.5, "rond_croix/rond.png")

                                else:
                                    self.g.afficherImage(objet.x + 2.5, objet.y + 2.5, "rond_croix/croix.png")

                                self.g.supprimer(winner)

                                #un bug est survenu a la derniere minute dans certain cas tres rare je n'ai pas peu trouver la cause par manque de
                                #temp donc j'ai eviter le probleme avec un try except, ce qui fonctionne parfaitement

                                try:
                                    self.g.supprimer(winner)
                                except:
                                    continue
                                #je remet le perdant dans son deck
                                self.g.deplacer(loser, self.asso_poke[loser]["co"][0] - loser.x,self.asso_poke[loser]["co"][1] - loser.y)

                            else :
                                #maintenant le cas ou on clique sur une case vide
                                self.g.deplacer(poke_choisi, objet.x - poke_choisi.x + 1,objet.y - poke_choisi.y + 1)
                                if j == 1 :
                                    col = "red"
                                else :
                                    col = "blue"
                                #j'affiche un rectangle de la couleur du joueur pour bien distinguer les pokemon joué par chaque joueur
                                self.g.dessinerRectangle(poke_choisi.x ,poke_choisi.y , 44,44,col)

                                self.g.placerAuDessus(poke_choisi)
                                #je met a jour les dico et les matrices
                                self.asso_poke[poke_choisi]["dispo"] = False
                                self.asso_poke[poke_choisi]["co_mat"] = (self.dic_asso[objet][0],self.dic_asso[objet][1],self.dic_asso[objet][2],self.dic_asso[objet][3])
                                self.co_to_poke[(self.dic_asso[objet][0],self.dic_asso[objet][1],self.dic_asso[objet][2],self.dic_asso[objet][3])] = poke_choisi
                                #le dic_asso me permet de revenir au co de la mat c'est le meme que pour les carré vides
                                self.dic_asso[poke_choisi] = (self.dic_asso[objet][0],self.dic_asso[objet][1],self.dic_asso[objet][2],self.dic_asso[objet][3])
                                self.mat[self.dic_asso[objet][0]][self.dic_asso[objet][1]][self.dic_asso[objet][2]][self.dic_asso[objet][3]] = j

                            if j == 1:
                                obj = rectangle
                            else:
                                obj = rectangle1
                            self.g.deplacer(obj, 10000, 10000)
                            j = -j

                            #la suite est la meme que en jeu normal

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

#la suite est utile pour le choix du pokemon que l'ia vas jouer

    def a_un_avantage(self, pokemon, adversaire_types):

        types_pokemon = [self.df.loc[pokemon, "Type 1"], self.df.loc[pokemon, "Type 2"]]
        for type_adv in adversaire_types:
            if not pds.isna(type_adv):  # Vérifie que le type adverse existe
                for type_pokemon in types_pokemon:
                    if not pds.isna(type_pokemon) and type_adv in self.combat.dict_av.get(type_pokemon, []):
                        return True
        return False

    def est_suffisant(self, pokemon, adversaire_stats):
        #cette fonction permet de voir si un pokemon est suffisant pour battre son adversaire
        stats_pokemon = self.df.loc[pokemon]
        #pour cela on regarde la diference entre les stats de l'adversaire et les notres
        attaque_effective = max(
            stats_pokemon["Attack"] - adversaire_stats["Defense"],
            stats_pokemon["Sp. Atk"] - adversaire_stats["Sp. Def"])
        #cette maniere de return renvoie un booleen si les conditions sont verifiés
        return attaque_effective > 0 and stats_pokemon["Speed"] >= adversaire_stats["Speed"]

    def choisir_pokemon(self, adversaire, ma_liste):#principale fonction

        # Récupérer les stats de l'adversaire
        adversaire_stats = self.df.loc[adversaire]
        adversaire_types = [adversaire_stats["Type 1"], adversaire_stats["Type 2"]]

        # Filtrer les Pokémon ayant un avantage de type
        pokemon_avantage = [poke for poke in ma_liste if self.a_un_avantage(poke, adversaire_types)]

        # Si aucun Pokémon n'a un avantage, utiliser tous les Pokémon disponibles
        pokemon_consideres = pokemon_avantage if pokemon_avantage else ma_liste

        # Filtrer les Pokémon capables de gagner
        pokemon_suffisants = [poke for poke in pokemon_consideres if self.est_suffisant(poke, adversaire_stats)]

        # Si aucun Pokémon ne peut gagner, retourner le meilleur et soit il gagnera soit il montera de niveau
        if not pokemon_suffisants:
            ma_liste.sort(key=lambda p: (self.df.loc[p, "Attack"] + self.df.loc[p, "Sp. Atk"], self.df.loc[p, "Speed"]))
            return ma_liste[-1]

        # Trier les Pokémon capables de gagner par puissance croissante
        pokemon_suffisants.sort(key=lambda p: (self.df.loc[p, "Attack"] + self.df.loc[p, "Sp. Atk"],self.df.loc[p, "Speed"]))
        return pokemon_suffisants[0]  # Le plus faible capable de gagner

    #permet de voir si un coup bloque l'adversaire
    def coup_bloquant(self,mat,pos,j):
        mat[pos[0]][pos[1]] = -j
        if self.verif_win(mat) == j:
            mat[pos[0]][pos[1]] = 0
            return True
        else :
            mat[pos[0]][pos[1]] = 0
            return False

    def minimax_poke(self, main_mat, grille_active, profondeur, alpha, beta, joueur_max, mat_poke):
        #quasiment pareil que le minimax normal, mais l'ia peut jouer egalement sur les pos adverses si elles sont dispo

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
                                    #on verifie les case joueables
                                    if mat_poke[h][l][y][x] == 0 and main_mat[h][l][y][x] != -1:
                                        coup_pre = main_mat[h][l][y][x]
                                        #on part du principe que l'ia gagnera toujours ces combats si elle choisi bien ces pokemons
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

    def start_poke_ia(self,aff):
        self.afficher_morpion()
        pygame.mixer.init()
        pygame.mixer.music.load("musiques/PVE.mp3")
        pygame.mixer.music.play(-1)



        #le joueur qui commence
        j = 1
        rectangle = self.g.dessinerRectangle(10000,10000,43,43,"red")
        rectangle1 = self.g.dessinerRectangle(10000,10000,43,43,"blue")
        self.afficher_poke()

        stat = self.g.afficherTexte("", 600,550, "black")

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

            #La partie du joueur est la meme que sans ia
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
                                    if aff==1 :
                                        resultat = self.combat.combat(self.asso_poke[poke_choisi]["name"],self.asso_poke[poke_selec]["name"])
                                        pygame.mixer.init()
                                        pygame.mixer.music.load("PVE.mp3")
                                        pygame.mixer.music.play(-1)
                                    else:
                                        resultat = self.combat.combat_simple(self.asso_poke[poke_choisi]["name"],
                                                                      self.asso_poke[poke_selec]["name"])
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
                #maintenant au tour de l'ia qui reprend des aspect de l'ia sans pokemon
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
                    #si l'ia joue sur un poke adversaire c'est la meme chose que quand un joueur lance un combat

                    a = self.co_to_poke[(coup_ia[1][0],coup_ia[1][1],coup_ia[1][2],coup_ia[1][3])]
                    adversaire = self.asso_poke[a]["name"]
                    #l'ia choisi son pokemon ici
                    poke_choisi = self.choisir_pokemon(adversaire,self.deck[1])

                    if aff==1:
                        resultat = self.combat.combat(poke_choisi, adversaire)
                        pygame.mixer.init()
                        pygame.mixer.music.load("PVE.mp3")
                        pygame.mixer.music.play(-1)
                        self.g.actualiser()
                    else:
                        resultat = self.combat.combat_simple(poke_choisi, adversaire)

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
                    #si l'ia joue un carré vide alors elle vas prendre un pokemon moyen par defaut et son meilleur pokemon si elle empeche le joueur de gagner
                    deck = []
                    #on trie les pokemon jouable
                    for i in self.asso_poke :
                        if self.asso_poke[i]["dispo"] and self.asso_poke[i]["joueur"] == -1 :
                            deck.append(self.asso_poke[i]["name"])
                    filtered_df = self.df.loc[deck]
                    sorted_df = filtered_df.sort_values(by=["Attack", "HP", "Sp. Atk", "Speed"], ascending=False)
                    deck_trie = sorted_df.index.tolist()

                    #choix du pokemon
                    if self.coup_bloquant( self.mat[coup_ia[1][0]][coup_ia[1][1]],(coup_ia[1][2],coup_ia[1][3]), -1):
                        poke_choisi = deck_trie[-1]
                    else :
                        milieu = len(deck_trie)//2
                        poke_choisi = deck_trie[milieu]

                    poke_choisi = self.name_to_poke[poke_choisi]

                    #le reste est la meme chose que pour le joueur

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


    #Cette fonction ne marche pas a tout les coups il lui arrive de buger cependant je n'ai pas su trouver exactement le moment qui bloquait par manque de temp
    #Elle fonctionne quand meme la plus part du temp
    def start_poke_ia_vs_ia(self,aff):
        self.afficher_morpion()
        self.afficher_poke()
        pygame.mixer.init()
        pygame.mixer.music.load("musiques/IA_vs_IA.mp3")
        pygame.mixer.music.play(-1)

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
                self.fin = True
                return 0


            #debut jeu

            nb_coup_possible = 0
            for x in range(3):
                for y in range(3):
                    if self.verif_win(self.mat[x][y]) == 0:
                        for x1 in range(3):
                            for y1 in range(3):
                                if self.mat[x][y][x1][y1] == 0:
                                    nb_coup_possible += 1

            #joueur maximisant ou minimisant
            if j == 1 :
                joueur = False
            else:
                joueur = True

            #Le bug est ici le minimax renvoie des fois meilleur coup = -1 ,cela veut dire que dans le minimax elle n'actualise jamais le meilleur coup cependant je n'ai pas sur trouver pourquoi

            coup_ia = self.minimax_poke(self.mat, prochain_coup, min(3, nb_coup_possible), -math.inf, math.inf,joueur, self.mat_poke)
            
            if coup_ia[1] == -1 :
                if prochain_coup != -1 :
                    for p in range(3):
                        for o in range (3):
                            if self.mat[prochain_coup[0]][prochain_coup[1]][p][o] == 0 :
                                coup_ia[1] = (prochain_coup[0],prochain_coup[1],p,o)
                else :
                    for m in range(3):
                        for l in range(3):
                            for p in range(3):
                                for o in range(3):
                                    if self.mat[m][l][p][o] == 0 :
                                        coup_ia[1] = (m,l,p,o)
            
            #le reste reviens au meme que les autres fonction

            if self.mat[coup_ia[1][0]][coup_ia[1][1]][coup_ia[1][2]][coup_ia[1][3]] == -j:
                a = self.co_to_poke[(coup_ia[1][0], coup_ia[1][1], coup_ia[1][2], coup_ia[1][3])]
                adversaire = self.asso_poke[a]["name"]
                if j == 1 :
                    indice = 0
                else :
                    indice = 1
                poke_choisi = self.choisir_pokemon(adversaire, self.deck[indice])
                if aff==1:
                    resultat = self.combat.combat(poke_choisi, adversaire)
                    pygame.mixer.init()
                    pygame.mixer.music.load("musiques/IA_vs_IA.mp3")
                    pygame.mixer.music.play(-1)
                    self.g.actualiser()
                else:
                    resultat = self.combat.combat_simple(poke_choisi, adversaire)


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
                    self.g.afficherImage(a.x + 2.5, a.y + 2.5, "rond_croix/rond.png")

                else:
                    self.g.afficherImage(a.x + 2.5, a.y + 2.5, "rond_croix/croix.png")

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
                    self.g.dessinerRectangle(375 + coup_ia[1][1] * 150 + 1, 75 + coup_ia[1][0] * 150 + 1, 148, 148,"black")
                    if win == -1:
                        image = "rond_croix/rond2.png"
                    else:
                        image = "rond_croix/croix2.png"
                    self.g.afficherImage(375 + coup_ia[1][1] * 150, 75 + coup_ia[1][0] * 150, image)

                    win_globale = self.verif_win(self.main_mat)
                    if abs(win_globale) == 1:
                        self.fin = True
                        return win_globale


                if abs(self.main_mat[prochain_coup[0]][prochain_coup[1]]) == 1 or all(
                        x != 0 for y in self.mat[prochain_coup[0]][prochain_coup[1]] for x in y):
                    prochain_coup = -1
                    for i in self.dico_surbrillance:
                        self.g.changerCouleur(self.dico_surbrillance[i], "green")
                elif self.main_mat[prochain_coup[0]][prochain_coup[1]] == 0:
                    self.g.changerCouleur(self.dico_surbrillance[prochain_coup], "green")

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
                    self.g.dessinerRectangle(375 + coup_ia[1][1] * 150 + 1, 75 + coup_ia[1][0] * 150 + 1, 148, 148,"black")
                    if win == -1:
                        image = "rond_croix/rond2.png"
                    else:
                        image = "rond_croix/croix2.png"
                    self.g.afficherImage(375 + coup_ia[1][1] * 150, 75 + coup_ia[1][0] * 150, image)
                    win_global = self.verif_win(self.main_mat)
                    if abs(win_global) == 1:
                        self.fin = True
                        return win_global


                if abs(self.main_mat[prochain_coup[0]][prochain_coup[1]]) == 1 or all(
                        x != 0 for y in self.mat[prochain_coup[0]][prochain_coup[1]] for x in y):
                    prochain_coup = -1
                    for i in self.dico_surbrillance:
                        self.g.changerCouleur(self.dico_surbrillance[i], "green")
                elif self.main_mat[prochain_coup[0]][prochain_coup[1]] == 0:
                    self.g.changerCouleur(self.dico_surbrillance[prochain_coup], "green")
            self.g.actualiser()
            j = -j


    #cette fonction renverra toujours le meme resultat ce qui est normal car les deux ia ont toujours le meme raisonement, il est possible de leur faire faire d'autre strategie
    #par exemple de ne prendre encompte que les petits morpion mais ce n'est pas tres interressant car elles sont beaucoup moins efficace.
    def start_ia_vs_ia(self):
        #cela marche exactement comme les autres fonctions
        self.afficher_morpion()
        pygame.mixer.init()
        pygame.mixer.music.load("musiques/IA_vs_IA.mp3")
        pygame.mixer.music.play(-1)
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
                self.fin = True
                return 0


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

            #ici il n'y a aucun probleme
            coup_ia = self.minimax(self.mat, prochain_coup, min(4, nb_coup_possible), -math.inf, math.inf, joueur)
            self.mat[coup_ia[1][0]][coup_ia[1][1]][coup_ia[1][2]][coup_ia[1][3]] = j

            centre = (450 + coup_ia[1][1] * 150, 150 + coup_ia[1][0] * 150)
            if j == 1 :
                image = "rond_croix/rond.png"
            else :
                image = "rond_croix/croix.png"
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
                    image = "rond_croix/croix2.png"
                elif win == 1:
                    image = "rond_croix/rond2.png"
                self.g.afficherImage(375 + coup_ia[1][1] * 150, 75 + coup_ia[1][0] * 150, image)

                win_globale = self.verif_win(self.main_mat)
                if abs(win_globale) == 1:
                    if win == -1:
                        return win_globale
                    self.fin = True

            if abs(self.main_mat[prochain_coup[0]][prochain_coup[1]]) == 1 or all(
                    x != 0 for y in self.mat[prochain_coup[0]][prochain_coup[1]] for x in y):
                prochain_coup = -1
                for i in self.dico_surbrillance:
                    self.g.changerCouleur(self.dico_surbrillance[i], "green")
            elif self.main_mat[prochain_coup[0]][prochain_coup[1]] == 0:
                self.g.changerCouleur(self.dico_surbrillance[prochain_coup], "green")
            self.g.actualiser()
        self.g.attendreClic()