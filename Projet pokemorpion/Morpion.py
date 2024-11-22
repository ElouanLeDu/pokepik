import time
import numpy as np
from tkiteasy import *


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
        prochain_coup = None
        while not self.fin:
            clic = self.g.recupererClic()
            touche = self.g.recupererTouche()
            if touche == "Return":
                self.fin = True
            if clic :
                try :
                    objet = self.g.recupererObjet(clic.x, clic.y)
                    if objet in self.dic_asso and self.main_mat[self.dic_asso[objet][0]][self.dic_asso[objet][1]] == 0 and self.mat[self.dic_asso[objet][0]][self.dic_asso[objet][1]][self.dic_asso[objet][2]][self.dic_asso[objet][3]] == 0 :
                        if not prochain_coup or prochain_coup == (self.dic_asso[objet][0],self.dic_asso[objet][1]) :
                            if j == 1:
                                self.g.afficherImage(objet.x + 2.5, objet.y + 2.5, "rond.png")
                                self.mat[self.dic_asso[objet][0]][self.dic_asso[objet][1]][self.dic_asso[objet][2]][self.dic_asso[objet][3]] = 1
                                j = -1
                            elif j == -1:
                                self.g.afficherImage(objet.x + 2.5, objet.y + 2.5, "croix.png")
                                self.mat[self.dic_asso[objet][0]][self.dic_asso[objet][1]][self.dic_asso[objet][2]][self.dic_asso[objet][3]] = -1
                                j = 1

                            if prochain_coup :
                                self.g.changerCouleur(self.dico_surbrillance[prochain_coup], "black")
                            elif not prochain_coup :
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
                        if abs(self.main_mat[prochain_coup[0]][prochain_coup[1]]) == 1 :
                            prochain_coup = None
                            for i in self.dico_surbrillance:
                                self.g.changerCouleur(self.dico_surbrillance[i],"cyan")
                        elif self.main_mat[prochain_coup[0]][prochain_coup[1]] == 0:
                            self.g.changerCouleur(self.dico_surbrillance[prochain_coup], "cyan")
                except :
                    continue



g = ouvrirFenetre(1200,600)
jeu = Morpion(g)
# jeu.afficher_morpion()
jeu.start()