import time
import numpy as np
from tkiteasy import *
import math


class Morpion:
    def __init__(self,g):
        self.g = g
        self.mat = np.array([[np.zeros((3, 3)) for _ in range(3)] for _ in range(3)])
        self.main_mat = np.zeros(((3,3)))
        # self.dic_poke = {}
        self.dic_asso = {}
        self.fin = False
        self.dico_surbrillance={}
        self.centre = [
            (600, 300,(1,1)), (600, 150,(1,0)), (600, 450,(1,2)),
            (450, 300,(0,1)), (450, 150,(0,0)), (450, 450,(0,2)),
            (750, 300,(2,1)), (750, 150,(2,0)), (750, 450,(2,2))]

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



    def afficher_morpion(self):
        for x in range(3):
            for y in range(3):
                self.dico_surbrillance[(y,x)]=self.g.dessinerRectangle(375 + x * 150 + 1, 75 + y * 150 + 1, 149, 149, "black")

        self.afficher_grille()
        self.afficher_centres()
        self.g.actualiser()

    def verif_win(self,mat):
        for i in range (3):
            if abs(mat[i][0] + mat[i][1] + mat[i][2]) == 3 :
                return mat[i][0]
            if abs(mat[0][i] + mat[1][i] + mat[2][i]) == 3 :
                return mat[0][i]

        if abs(mat[0][0] + mat[1][1] + mat[2][2]) == 3 :
            return mat[0][0]
        if abs(mat[2][0] + mat[1][1] + mat[0][2]) == 3 :
            return mat[1][1]

        return 0

    def start(self):
        self.afficher_morpion()
        j = 1
        prochain_coup = -1
        while not self.fin:
            clic = self.g.recupererClic()
            touche = self.g.recupererTouche()
            if touche == "Return":
                self.fin = True
            if clic :
                try :
                    objet = self.g.recupererObjet(clic.x, clic.y)
                    if objet in self.dic_asso and self.main_mat[self.dic_asso[objet][0]][self.dic_asso[objet][1]] == 0 and self.mat[self.dic_asso[objet][0]][self.dic_asso[objet][1]][self.dic_asso[objet][2]][self.dic_asso[objet][3]] == 0 :
                        if prochain_coup ==-1 or prochain_coup == (self.dic_asso[objet][0],self.dic_asso[objet][1]) :
                            if j == 1:
                                self.g.afficherImage(objet.x + 2.5, objet.y + 2.5, "rond.png")
                                self.mat[self.dic_asso[objet][0]][self.dic_asso[objet][1]][self.dic_asso[objet][2]][self.dic_asso[objet][3]] = 1
                                j = -1
                            elif j == -1:
                                self.g.afficherImage(objet.x + 2.5, objet.y + 2.5, "croix.png")
                                self.mat[self.dic_asso[objet][0]][self.dic_asso[objet][1]][self.dic_asso[objet][2]][self.dic_asso[objet][3]] = -1
                                j = 1

                            if prochain_coup != -1:
                                self.g.changerCouleur(self.dico_surbrillance[prochain_coup], "black")
                            else :
                                for i in self.dico_surbrillance:
                                    self.g.changerCouleur(self.dico_surbrillance[i], "black")
                            prochain_coup = (self.dic_asso[objet][2], self.dic_asso[objet][3])

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





    def eval_petit(self,mat):
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


    def eval_grand(self,mat,pos_actuelle):
        score = [[1.4, 1, 1.4],
                 [1, 1.75, 1],
                [1.4, 1, 1.4]] # matrice avec les scores de base pour chaque pos (le centre ++, les coins +, les arretes 0)
        evaluation = 0
        main_mat = np.zeros((3,3))
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

        evaluation -= self.verif_win(main_mat) * 5000
        evaluation += self.eval_petit(main_mat) * 150

        return evaluation


    def minimax(self,main_mat,grille_active, profondeur, alpha, beta, joueur_max):

        meilleur_coup = -1

        evalfin = self.eval_grand(main_mat,grille_active)

        if profondeur <= 0 or abs(evalfin) > 5000 :
            return {0:evalfin,1:meilleur_coup}

        if grille_active == -1 or self.verif_win(main_mat[grille_active[0]][grille_active[1]])!=0 or all(x != 0 for y in main_mat[grille_active[0]][grille_active[1]] for x in y) :
            grille_active = -1
            print("caca")

        if joueur_max:
            max_eval = -math.inf
            for y in range(3):
                for x in range(3):
                    if grille_active == -1 :
                        for h in range(3):
                            for l in range(3):
                                if self.verif_win(main_mat[h][l]) == 0 :
                                    if main_mat[h][l][y][x] == 0:
                                        main_mat[h][l][y][x] = -1
                                        eval = self.minimax(main_mat, (y, x), profondeur - 1, alpha, beta, False)
                                        main_mat[h][l][y][x] = 0

                                        monstre = eval[0]
                                        if monstre > max_eval:
                                            max_eval = monstre
                                            meilleur_coup = (h, l, y, x)
                                        alpha = max(alpha, monstre)

                                        # Coupure alpha-bêta
                                        if beta <= alpha:
                                            break
                                        # Ajout d'un `break` externe à la boucle `l`
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
                time.sleep(1)
                coup_ia = self.minimax(self.mat,prochain_coup,4,-math.inf,math.inf,True)
                self.mat[coup_ia[1][0]][coup_ia[1][1]][coup_ia[1][2]][coup_ia[1][3]] = -1
                print(self.mat)

                centre = (450 + coup_ia[1][1] * 150, 150 + coup_ia[1][0] * 150)
                print(centre)
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
                        self.fin = True
                if abs(self.main_mat[prochain_coup[0]][prochain_coup[1]]) == 1 or all(x != 0 for y in self.mat[prochain_coup[0]][prochain_coup[1]] for x in y):
                    prochain_coup = -1
                    for i in self.dico_surbrillance:
                        self.g.changerCouleur(self.dico_surbrillance[i], "cyan")
                elif self.main_mat[prochain_coup[0]][prochain_coup[1]] == 0:
                    self.g.changerCouleur(self.dico_surbrillance[prochain_coup], "cyan")
                self.g.actualiser()


g = ouvrirFenetre(1200,600)
jeu = Morpion(g)
jeu.start_ia()
# jeu.test_minimax()
# jeu.start()