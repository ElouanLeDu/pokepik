from importlib.metadata import Distribution

import pandas as pds
from tkiteasy import *
import tkinter as tk
from tkinter import messagebox
import pygame
from Morpion import Morpion
from combat import combat_de_pokemon
from distribute import Distri



# Début du programme :
# Aucune fonction n'a de renvoi. C'etait plus simple pour la construction du programme, bien que cela soit un peu inutile


class Pokemorpion():
    def __init__(self):
        self.g = ouvrirFenetre(1200, 600)
        self.df=pds.read_csv('pokemon_modified.csv', index_col='Name')
        self.g.afficherImage(0, 0, "fond_entree.png")
        self.jeu=Morpion(self.g)
        self.fight=combat_de_pokemon(self.g,self.df)
        self.distri=Distri(self.g,self.df)
        self.poke1 = ""
        self.poke2 = ""
        self.deck1=[]
        self.deck2=[]



    def affichage_menu(self):  # affichage du menu principal
        self.g.afficherImage(0, 0, "fond_menu.jpg")
        self.g.afficherImage(410, -110,"game_mode.png")
        self.combat = self.g.afficherImage(740, 330,"Fight.png")
        self.pvp = self.g.afficherImage(560, 330,"PVP.png")
        self.pve = self.g.afficherImage(560,200,"PVE.png")
        self.eve= self.g.afficherImage(740, 200,"EVE.png")
        self.q = self.g.afficherImage(1000, 440,"QUIT.png")
        self.draft=self.g.afficherImage(395, 340,"Draft.png")
        self.random_deck=self.g.afficherImage(385, 200,"Random_deck.png")
        self.g.actualiser()

    def transition(self, nb):  # affichage uniquement transition menu de début de jeu
        # cette fonction est utilisee a 2 moments differents, le parametre permet de les distinguer
        # et d'eviter des doublons

        if nb == 1:  # écran de début du jeu

            play = self.g.afficherImage(470, 300,"Bouton_jouer.png")

            self.g.afficherImage(386, 0,"Title.png")
            pygame.mixer.init()
            pygame.mixer.music.load("Debut.mp3")
            pygame.mixer.music.play(-1)
            clic = self.g.attendreClic()
            x = self.g.recupererObjet(clic.x, clic.y)
            while x != play  :  # le joueur doit cliquer sur jouer pour continuer
                clic = self.g.attendreClic()
                x = self.g.recupererObjet(clic.x, clic.y)

        elif nb == 2 : #transition avant combat

            self.g.afficherImage(0, 0, "entree_arène.png")
            self.g.afficherImage(740, 160, "P2.png")
            self.g.afficherImage(340, 160, "P1.png")
            self.g.afficherImage(540, 200, "start.png")
            self.g.actualiser()
            pygame.mixer.init()
            pygame.mixer.music.load("battle_transition.mp3")
            pygame.mixer.music.play(-1)

            # Champs d'entrée pour les noms des Pokémon
            self.entree_joueur1 = tk.Entry(self.g, width=30)
            self.entree_joueur1.place(x=310, y=270)  # Position de l'entrée pour joueur 1
            self.poke1 = self.entree_joueur1.get()

            self.entree_joueur2 = tk.Entry(self.g, width=30)
            self.entree_joueur2.place(x=720, y=270)  # Position de l'entrée pour joueur 2
            self.poke2 = self.entree_joueur2.get()

            # Bouton "START" pour valider les entrées
            self.bouton_start = tk.Button(self.g, text="START",command=self.valider_joueurs)
            self.bouton_start.place(x=592, y=282)  # Position du bouton

            # Laisser la page de transition active jusqu'à validation
            self.g.mainloop()  # Démarrer la boucle Tkinter pour garder la page active


    def valider_joueurs(self):
        #Valider les noms des Pokémon et lancer le combat si les noms sont valides.
        # Récupérer les noms des Pokémon saisis
        self.poke1 = self.entree_joueur1.get()
        self.poke2 = self.entree_joueur2.get()

        # Vérifier si les champs sont remplis
        if not self.poke1 or not self.poke2:
            messagebox.showerror("Erreur", "Veuillez entrer les noms des deux Pokémon.")
            return
            # Vérification si les noms entrés par les joueurs sont valides.
        try:
            # Cela soulève une erreur si les noms n'existent pas
            test1 = self.df.loc[self.poke1]
            test2 = self.df.loc[self.poke2]

        except KeyError:
            messagebox.showerror("Erreur", "Noms invalides.")
            return


        # Si tout est valide, arrêter la musique et passer au combat
        pygame.mixer.music.stop()
        self.g.supprimerTout()  # Supprimer tout le contenu graphique précédent
        self.bouton_start.destroy()
        self.entree_joueur2.destroy()
        self.entree_joueur1.destroy()
        self.g.actualiser()

        self.g.quit()  # Fermer la boucle Tkinter pour continuer le programme

    def menu(self):  # menu principal, appel des fonctions et gestion des fonctionnalites

        self.transition(1)

        stop = False
        while stop == False:  # on boucle tant que le joueur en clique pas sur quitter la partie
            pygame.mixer.init()
            pygame.mixer.music.load("menu2.mp3")
            pygame.mixer.music.play(-1)
            self.g.supprimerTout()
            self.affichage_menu()
            clic = self.g.attendreClic()
            x = self.g.recupererObjet(clic.x, clic.y)

            if x == self.eve: #affichage pour chaque mode de jeu
                self.g.afficherImage(0, 0, "fond_morpion.jpg")
                self.jeu.start_ia()
                self.g.attendreClic()


            if x == self.combat:
                self.poke1=""
                self.poke2=""
                pygame.mixer.music.stop()
                self.g.supprimerTout()
                self.transition(2)
                self.fight.combat(self.poke1, self.poke2)


            if x==self.draft:

                pygame.mixer.music.stop()
                self.g.supprimerTout()

                self.distri.distribute_draft()

                self.g.attendreClic()


            if x == self.pvp:
                pygame.mixer.music.stop()
                self.g.supprimerTout()
                self.g.afficherImage(0, 0, "fond_morpion.jpg", 1200,600)
                self.jeu.start()
                self.g.attendreClic()


            if x==self.random_deck:

                pygame.mixer.music.stop()
                self.g.supprimerTout()

                self.distri.distribute_random()


            if x == self.pve:
                pygame.mixer.music.stop()
                self.g.supprimerTout()
                self.g.afficherImage(0, 0, "fond_morpion.jpg")
                self.jeu.start_ia()
                self.g.attendreClic()

            if x == self.q:  # bouton pour quitter le jeu
                pygame.mixer.music.stop()
                stop=True
                self.g.fermerFenetre()





P = Pokemorpion()
P.menu()

