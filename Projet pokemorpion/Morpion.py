import time
import numpy as np
from tkiteasy import *


class Morpion:
    def __init__(self):
        self.g = ouvrirFenetre(1200, 600)
        self.mat = np.array([[np.zeros((3, 3)) for _ in range(3)] for _ in range(3)])
        self.dic_poke = {}
        self.dic_asso = {}
        self.fin = False
        self.CELL_CENTERS = [
            (600, 300,(1,1)), (600, 150,(1,0)), (600, 450,(1,2)),
            (450, 300,(0,1)), (450, 150,(0,0)), (450, 450,(0,2)),
            (750, 300,(2,1)), (750, 150,(2,0)), (750, 450,(2,2))]
        self.afficher_morpion()

    def afficher_grille(self):
        for y in [225, 375]:
            self.g.dessinerLigne(375, y, 375 + 450, y, "white")
        for x in [525, 675]:
            self.g.dessinerLigne(x, 75, x, 525, "white")

    def afficher_centres(self):
        for x in self.CELL_CENTERS:
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
        self.afficher_grille()
        self.afficher_centres()
        self.g.actualiser()


    def start(self):
        self.afficher_morpion()
        j = "red"
        while not self.fin:
            clic = self.g.recupererClic()
            if clic :
                try :
                    objet = self.g.recupererObjet(clic.x, clic.y)
                    if objet in self.dic_asso and self.mat[self.dic_asso[objet][0]][self.dic_asso[objet][1]][self.dic_asso[objet][2]][self.dic_asso[objet][3]] == 0 :
                        self.g.changerCouleur(objet, j)
                        if j == "red" :
                            self.mat[self.dic_asso[objet][0]][self.dic_asso[objet][1]][self.dic_asso[objet][2]][self.dic_asso[objet][3]] = 1
                        elif j == "blue" :
                            self.mat[self.dic_asso[objet][0]][self.dic_asso[objet][1]][self.dic_asso[objet][2]][self.dic_asso[objet][3]] = 2
                except :
                    continue


    #
    # def select_obj(self):
    #     clic = self.g.attendreClic()
    #     if clic :
    #         objet = self.g.recupererObjet(clic.x,clic.y)
    #         self.g.changerCouleur(objet,"red")








jeu = Morpion()
# jeu.afficher_morpion()
jeu.start()