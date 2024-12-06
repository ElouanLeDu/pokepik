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


class Pokemorpion ():
    def __init__(self):
        self.g = ouvrirFenetre(1200, 600)
        self.df=pds.read_csv('pokemon_modified.csv', index_col='Name')
        self.g.afficherImage(0, 0, "fonds/fond_entree.png")
        self.deck1 = []
        self.deck2 = []
        self.jeu=Morpion(self.g,self.df,self.deck1,self.deck2)
        self.fight=combat_de_pokemon(self.g,self.df)
        self.distri=Distri(self.g,self.df)
        self.poke1 = ""
        self.poke2 = ""
        self.choice_var = "Fight with display"




    def affichage_menu(self):  # affichage du menu principal
        self.g.afficherImage(0, 0, "fonds/fond_menu.jpg")
        self.g.afficherImage(410, -130,"titres/game_mode.png")
        self.g.afficherImage(700, 140,"boutons/Classic_mod.png")
        self.g.afficherImage(810, 120, "boutons/pokemode.png")
        self.combat = self.g.afficherImage(940, 340,"boutons/Fight.png")
        self.pvp = self.g.afficherImage(680, 330,"boutons/PVP.png")
        self.pve = self.g.afficherImage(680, 200,"boutons/PVE.png")
        self.eve= self.g.afficherImage(550,200,"boutons/EVE.png")
        self.poke_eve = self.g.afficherImage(930,200,"boutons/blue_eve.png")
        self.q = self.g.afficherImage(1000, 440,"boutons/QUIT.png")
        self.draft=self.g.afficherImage(395, 340,"boutons/Draft.png")
        self.random_deck=self.g.afficherImage(385, 200,"boutons/Random_deck.png")
        self.pve_poke=self.g.afficherImage(810,200,"boutons/PVE_blue.png")
        self.pvp_poke=self.g.afficherImage(810, 330,"boutons/PVP_blue.png")

        # Ajout des boutons pour configurer le mode de combat
        def set_choice(choice):
            self.choice_var = choice  # Mise à jour de la variable
            print(f"Choice set to: {self.choice_var}")

        # Création des boutons Tkinter
        self.fight_with_display_button = tk.Button(
            self.g, text="Fight with display", command=lambda: set_choice("Fight with display")
        )
        self.fight_with_display_button.place(x=250, y=390)  # Positionner le bouton

        self.fight_without_display_button = tk.Button(
            self.g, text="Fight without display", command=lambda: set_choice("Fight without display")
        )
        self.fight_without_display_button.place(x=250, y=260)  # Positionner le bouton

        self.g.actualiser()

    def transition(self, nb):  # affichage uniquement transition menu de début de jeu
        # cette fonction est utilisee a 2 moments differents, le parametre permet de les distinguer
        # et d'eviter des doublons

        if nb == 1:  # écran de début du jeu

            play = self.g.afficherImage(470, 300,"boutons/Bouton_jouer.png")

            self.g.afficherImage(386, 0,"titres/Title.png")
            pygame.mixer.init()
            pygame.mixer.music.load("musiques/Debut.mp3")
            pygame.mixer.music.play(-1)
            clic = self.g.attendreClic()
            x = self.g.recupererObjet(clic.x, clic.y)
            while x != play  :  # le joueur doit cliquer sur jouer pour continuer
                clic = self.g.attendreClic()
                x = self.g.recupererObjet(clic.x, clic.y)

        elif nb == 2 : #transition avant combat

            self.g.afficherImage(0, 0, "fonds/entree_arène.png")
            self.g.afficherImage(740, 160, "titres/P2.png")
            self.g.afficherImage(340, 160, "titres/P1.png")
            self.g.afficherImage(540, 200, "boutons/start.png")
            self.g.actualiser()
            pygame.mixer.init()
            pygame.mixer.music.load("musiques/battle_transition.mp3")
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

    def ecran_win(self,x):
        self.g.afficherImage(0,0,"fonds/win_fond.png")
        pygame.mixer.init()
        pygame.mixer.music.load("musiques/win_msc.mp3")
        pygame.mixer.music.play(-1)

        if x==1:
            self.g.afficherImage(390,190,"titres/win_P1.png")

        elif x==-1:
            self.g.afficherImage(390,190, "titres/win_P2.png")

        elif x==0:
            self.g.afficherImage(390,170, "titres/Draw.png")

        elif x==2:
            pygame.mixer.music.stop()

            pygame.mixer.init()
            pygame.mixer.music.load("musiques/defeat_msc.mp3")
            pygame.mixer.music.play(-1)

            self.g.afficherImage(360, 0, "titres/loose_title.png")



        self.g.attendreClic()
        self.g.supprimerTout()
        pygame.mixer.music.stop()


    def menu(self):  # menu principal, appel des fonctions et gestion des fonctionnalites

        self.transition(1)

        stop = False
        while stop == False:  # on boucle tant que le joueur en clique pas sur quitter la partie
            pygame.mixer.init()
            pygame.mixer.music.load("musiques/menu2.mp3")
            pygame.mixer.music.play(-1)
            self.g.supprimerTout()
            self.affichage_menu()
            clic = self.g.attendreClic()
            x = self.g.recupererObjet(clic.x, clic.y)
            self.fight_with_display_button.destroy()
            self.fight_without_display_button.destroy()


            if x == self.eve: #affichage pour chaque mode de jeu

                pygame.mixer.music.stop()
                self.g.afficherImage(0, 0, "fonds/fond_morpion.jpg")
                x=self.jeu.start_ia_vs_ia()
                self.g.attendreClic()
                self.ecran_win(x)

                self.jeu = Morpion(self.g, self.df, self.deck1, self.deck2)

            if x == self.poke_eve:
                if (self.deck1,self.deck2)==([],[]):
                    continue


                pygame.mixer.music.stop()
                self.g.afficherImage(0, 0, "fonds/fond_morpion.jpg")
                if self.choice_var=="Fight with display" :
                    x=self.jeu.start_poke_ia_vs_ia(1)
                    self.g.attendreClic()
                else:
                    x = self.jeu.start_poke_ia_vs_ia(2)
                    self.g.attendreClic()
                self.ecran_win(x)

                self.jeu = Morpion(self.g, self.df, self.deck1, self.deck2)

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
                self.deck1, self.deck2 =[],[]
                [self.deck1, self.deck2] = self.distri.distribute_draft()
                self.jeu = Morpion(self.g, self.df, self.deck1, self.deck2)
                self.g.attendreClic()


            if x == self.pvp:
                pygame.mixer.music.stop()
                self.g.supprimerTout()
                self.g.afficherImage(0, 0, "fonds/fond_morpion.jpg", 1200,600)
                x=self.jeu.start()
                self.ecran_win(x)

                self.jeu = Morpion(self.g, self.df, self.deck1, self.deck2)

            if x == self.pvp_poke:
                if (self.deck1,self.deck2)==([],[]):
                    continue

                pygame.mixer.music.stop()
                self.g.supprimerTout()
                self.g.afficherImage(0, 0, "fonds/fond_morpion.jpg", 1200,600)
                if self.choice_var=="Fight with display" :
                    x=self.jeu.start_poke(1)
                else:
                    x = self.jeu.start_poke(2)


                self.ecran_win(x)

                self.jeu = Morpion(self.g, self.df, self.deck1, self.deck2)


            if x==self.random_deck:

                pygame.mixer.music.stop()
                self.g.supprimerTout()
                self.deck1, self.deck2 = [], []
                [self.deck1,self.deck2]=self.distri.distribute_random()

                self.jeu = Morpion(self.g, self.df, self.deck1, self.deck2)



            if x == self.pve:
                pygame.mixer.music.stop()
                self.g.supprimerTout()
                self.g.afficherImage(0, 0, "fonds/fond_morpion.jpg")
                x=self.jeu.start_ia()
                self.ecran_win(x)

                self.jeu = Morpion(self.g, self.df, self.deck1, self.deck2)

            if x == self.pve_poke:
                if (self.deck1,self.deck2)==([],[]):
                    continue

                pygame.mixer.music.stop()
                self.g.supprimerTout()
                self.g.afficherImage(0, 0, "fonds/fond_morpion.jpg")
                if self.choice_var=="Fight with display" :
                    x=self.jeu.start_poke_ia(1)
                else:
                    x = self.jeu.start_poke_ia(2)

                self.ecran_win(x)

                self.jeu = Morpion(self.g, self.df, self.deck1, self.deck2)


            if x == self.q:  # bouton pour quitter le jeu
                pygame.mixer.music.stop()
                stop=True
                self.g.fermerFenetre()





P = Pokemorpion()
P.menu()

