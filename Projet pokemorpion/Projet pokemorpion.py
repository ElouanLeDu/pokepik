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
import requests
from PIL import Image, ImageTk
import tkinter as tk
from io import BytesIO
import pygame
import time


# Début du programme :
# Aucune fonction n'a de renvoi. C'etait plus simple pour la construction du programme, bien que cela soit un peu inutile


class Pokemorpion():
    def __init__(self):
        self.pk = pds.read_csv(r"pokemon.csv", index_col="Name")
        self.pk_normal = self.pk.loc[self.pk["Legendary"] == False]
        self.pk_legend = self.pk.loc[self.pk["Legendary"] == True]
        self.player1={}
        self.player2={}
        self.g = ouvrirFenetre(1200, 600)
        self.g.afficherImage(0, 0, "fond_entree.png")


    def affichage_menu(self):  # affichage du menu principal
        self.g.afficherImage(0, 0, "fond_menu.jpg")
        self.b = self.g.afficherTexte("Choix du mode de jeu :", 700, 70, "black", 22)
        self.duo = self.g.afficherTexte("Joueur contre joueur", 525, 230, "black", 20)
        self.algosimple = self.g.afficherTexte("Duel contre l'IA", 767, 180, "black", 20)
        self.robot = self.g.afficherTexte("Duel d'IA", 765, 230, "black", 20)
        self.combat= self.g.afficherTexte("combat", 765, 230, "black", 20)
        self.q = self.g.afficherTexte("Quitter le jeu", 900, 540, "black", 15)

        self.distri_random=self.g.afficherTexte('distri_random', 200, 200, 'red')
        self.distri_draft=self.g.afficherTexte('distri_draft', 200, 250, 'blue')

        self.duel_de_pokemon=self.g.afficherTexte("Duel de pokemon", 200, 540, "black", 15)

        self.g.actualiser()

    def transition(self, nb):  # affichage uniquement transition menu de début de jeu
        # cette fonction est utilisee a 2 moments differents, le parametre permet de les distinguer
        # et d'eviter des doublons
        if nb == 1:  # écran de début du jeu

            a = self.g.afficherImage(430,40,"Titre.png")
            b = self.g.afficherImage(400, 270,"bouton_jouer.png")
        pygame.mixer.init()
        pygame.mixer.music.load("Debut.mp3")
        pygame.mixer.music.play(-1)
        #à voir si l'on fait d'autres transitions
        clic = self.g.attendreClic()
        x = self.g.recupererObjet(clic.x, clic.y)
        while x != b:  # le joueur doit cliquer sur jouer pour continuer
            clic = self.g.attendreClic()
            x = self.g.recupererObjet(clic.x, clic.y)
        self.g.supprimer(a)
        self.g.supprimer(b)
        pygame.mixer.music.stop()

    def menu(self):  # menu principal, appel des fonctions et gestion des fonctionnalites

        self.transition(1)
        self.g.supprimerTout()
        self.affichage_menu()
        pygame.mixer.init()
        pygame.mixer.music.load("menu2.mp3")
        pygame.mixer.music.play(-1)
        stop = False
        while stop == False:  # on boucle tant que le joueur en clique pas sur quitter la partie
            clic = self.g.attendreClic()
            x = self.g.recupererObjet(clic.x, clic.y)
            pygame.mixer.music.stop()
            if x == self.duo:

                rejouer = True

                while rejouer == True:  # même fonctionnement pour le mode duo en dehors du fait que le jeu est adapté pour 2 joueurs

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

                self.g.supprimerTout()



                clic = self.g.attendreClic()
                x = self.g.recupererObjet(clic.x, clic.y)

            if x==self.combat:
                self.g.supprimerTout()

                clic = self.g.attendreClic()
                x = self.g.recupererObjet(clic.x, clic.y)

            elif x == self.robot:  # algo etape 3


                self.superclean()


                clic = self.g.attendreClic()
                x = self.g.recupererObjet(clic.x, clic.y)


            if x == self.duel_de_pokemon:

                self.superclean()


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



    def distribute_interface1(self):
        self.g.master.destroy()
        self.random_draft()


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

class combat_de_pokemon ():

    def __init__(self, g):
        self.g=g
        self.g.afficherImage(-50, 0,"poke_stadium.png" )
        self.df = pds.read_csv('pokemon_modified.csv', index_col='Name')
        self.dict_av = {
            "Bug": ["Grass", "Psychic", "Dark"],
            "Dark": ["Psychic", "Ghost"],
            "Dragon": ["Dragon"],
            "Electric": ["Water", "Flying"],
            "Fairy": ["Fighting", "Dragon", "Dark"],
            "Fighting": ["Normal", "Ice", "Rock", "Dark", "Steel"],
            "Fire": ["Grass", "Ice", "Bug", "Steel"],
            "Flying": ["Grass", "Fighting", "Bug"],
            "Ghost": ["Psychic", "Ghost"],
            "Grass": ["Water", "Ground", "Rock"],
            "Ground": ["Fire", "Electric", "Poison", "Rock", "Steel"],
            "Ice": ["Grass", "Ground", "Flying", "Dragon"],
            "Normal": [],
            "Poison": ["Grass", "Fairy"],
            "Psychic": ["Fighting", "Poison"],
            "Rock": ["Fire", "Ice", "Flying", "Bug"],
            "Steel": ["Ice", "Rock", "Fairy"],
            "Water": ["Fire", "Ground", "Rock"]
        }

        self.puissance=10 #puissance modérée peut-être augmentée pour des combats plus rapides
        self.pos={}
        self.img={}
        self.energie_ball={}
    def avantage_type(self,poke1,poke2):
        for i in range(1, 3):
            for j in range(1, 3):

                type1 = self.df.loc[poke1, f'Type {i}']
                type2 = self.df.loc[poke2, f'Type {j}']

                # Ignorer si un des types est NaN
                if pds.isna(type1) or pds.isna(type2):
                    continue

                # Vérifier si type2 est dans les avantages de type1
                if type2 in self.dict_av.get(type1, []):
                    return poke1

                # Vérifier si type1 est dans les avantages de type2
                if type1 in self.dict_av.get(type2, []):
                    return poke2

            # Aucun avantage trouvé
        return None


    def combat (self,poke1,poke2):
        #musique
        # Initialisation de Pygame Mixer
        pygame.mixer.init()

        # Charger la musique
        pygame.mixer.music.load("combat music.mp3")  # Remplace par le chemin de ton fichier

        # Lancer la musique en boucle
        pygame.mixer.music.play(-1)  # -1 pour jouer en boucle


        #sauvegarde stats
        stats_origin = {
            poke1: {"HP": self.df.loc[poke1, "HP"], "Attack": self.df.loc[poke1, "Attack"]},
            poke2: {"HP": self.df.loc[poke2, "HP"], "Attack": self.df.loc[poke2, "Attack"]}
        }
        #couleur associée à chaque pokemon
        col_poke1=self.get_color_for_type(self.df.loc[poke1,'Type 1'])[0]
        col_poke2=self.get_color_for_type(self.df.loc[poke2,'Type 1'])[0]

        #boule d'énergie de chaque pokemon
        self.energie_ball[poke1] = self.get_color_for_type(self.df.loc[poke1, 'Type 1'])[1]
        self.energie_ball[poke2] = self.get_color_for_type(self.df.loc[poke2, 'Type 1'])[1]

        #affichage des pokemons et de leur barre de vie
        poke1_hp_bar = g.dessinerRectangle(46, 40,self.df.loc[poke1,'HP']*4, 33, col_poke1)
        poke2_hp_bar = g.dessinerRectangle(740, 40,self.df.loc[poke2,'HP']*4, 33, col_poke2)

        #noms nettoyés
        cleaned_name1=self.nettoyer_nom_pokemon(poke1)
        cleaned_name2=self.nettoyer_nom_pokemon(poke2)

        #nom des pokemons sous leur barre de vie
        g.afficherTexte(cleaned_name1, 96, 110)
        g.afficherTexte(cleaned_name2, 1100, 110)

        #image de pokemons
        img1=self.get_pokemon_image(poke1)
        img2=self.get_pokemon_image(poke2)

        self.img[poke1]=self.g.create_image(313, 207, image=img1, anchor="nw")
        self.img[poke2]=self.g.create_image(695, 207, image=img2, anchor="nw")

        #position des pokemon
        self.pos[poke1],self.pos[poke2]=313,695
        self.g.actualiser()
        self.g.attendreClic()

        #boost de stat pour le pokemon avantagé
        if self.avantage_type(poke1, poke2) != None:
            poke_dominant = self.avantage_type(poke1, poke2)
            self.df.loc[poke_dominant,'Attack'] +=int(self.df.loc[poke_dominant,'Attack'] * 0.2)
            # paramètre général qui change l'avantage donné (vitesse,defense,..)??

        #determination du pokemon qui commence
        if self.df.loc[poke1, 'Speed']>self.df.loc[poke2, 'Speed']:
            attaquant=poke1
            defenseur=poke2
        elif self.df.loc[poke1, 'Speed']<self.df.loc[poke2, 'Speed']:
            attaquant=poke2
            defenseur=poke1
        else:
            i=random.randint(0,1)
            l=[poke1,poke2]
            attaquant = l[i]
            defenseur = l[(i+1)%2]
        tour=1

        x,y,z=self.g.afficherTexte(f'VS',600,180,'white',25),self.g.afficherTexte(cleaned_name1,500,180,col_poke1,25),self.g.afficherTexte(cleaned_name2 ,700,180,col_poke2,25)
        self.g.actualiser()
        self.g.attendreClic()
        self.g.supprimer(x)
        self.g.supprimer(z)
        self.g.supprimer(y)
        while self.df.loc[poke1,'HP']>0 and self.df.loc[poke2,'HP']>0 :
            #actualisation tour et barres de vie
            t=self.g.afficherTexte(f'\n tour {tour}',600,30,'white',22)


            a=self.g.afficherTexte(f'{attaquant} attaque !', 600,195,'white',25)
            self.g.attendreClic()
            self.g.supprimer(a)
            self.degats(attaquant, defenseur)
            attaquant, defenseur = defenseur, attaquant

            self.g.supprimer(t)
            tour +=1

            #actualisation barres de vie
            self.g.supprimer(poke1_hp_bar)
            self.g.supprimer(poke2_hp_bar)
            poke1_hp_bar = g.dessinerRectangle(46, 40,self.df.loc[poke1,'HP']*4, 33, col_poke1)
            poke2_hp_bar = g.dessinerRectangle(740, 40,self.df.loc[poke2,'HP']*4, 33, col_poke2)

            self.g.actualiser()
        # Déterminer le vainqueur
        if self.df.loc[poke2, 'HP'] <= 0 :
            winner = poke1
            looser = poke2
        else :
            winner = poke2
            looser = poke1

        #réinitialisation des stats du perdant + montée de niveau par rapport à la durée du combat
        self.df.loc[looser, "HP"], self.df.loc[looser, "Attack"] = stats_origin[looser]["HP"], stats_origin[looser]["Attack"]
        self.df.loc[attaquant,'Niveau']+=tour//2
        self.g.supprimerTout()

        #gestion musique
        pygame.mixer.music.stop()  # Arrêter la musique à la fin
        pygame.mixer.init()
        pygame.mixer.music.load("Fin.mp3")
        pygame.mixer.music.play(-1)

        self.g.afficherImage(-50, 0, "poke_stadium.png")
        self.g.afficherTexte(f"\n{winner} remporte\n      le combat !",600,185,'white',25)
        imgwin = self.get_pokemon_image(winner)
        self.g.create_image(505, 351, image=imgwin, anchor="nw")
        self.g.actualiser()
        self.g.attendreClic()
        pygame.mixer.music.stop()
        return (winner,looser,tour)

    def degats(self,attaquant,defenseur):

        #évitement ou non probabilité calculé en fonction de la vitesse des pokemons
        dodge_chance=self.df.loc[attaquant,'Speed']/ (self.df.loc[attaquant,'Speed']+self.df.loc[defenseur,'Speed'])

        if random.random() <= (1-dodge_chance)/2:  # L'attaque est esquivée

            esq=self.g.afficherTexte(f"    {defenseur} esquive\n   l'attaque de {attaquant} ",600,192,'white',25)
            self.g.attendreClic()
            self.g.supprimer(esq)
            self.g.actualiser()
            for _ in range(7):  # 7 cycles de vibrations
                self.g.deplacer_img(self.img[defenseur], 150, 5)
                self.g.actualiser()
                time.sleep(0.03)
                self.g.deplacer_img(self.img[defenseur], -150, -5)
                self.g.actualiser()
                time.sleep(0.03)

        # calcul des dégats et diminution des pv
        else:
            CRIT=random.uniform(0.7,1)
            damage=((((((self.df.loc[attaquant,'Niveau']*0.4+2)*((self.df.loc[attaquant,'Sp. Atk']+self.df.loc[attaquant,'Attack'])/2)*self.puissance)/8000*(self.df.loc[defenseur,'Defense']+self.df.loc[defenseur,'Sp. Def'])))+2)*CRIT)//1
            if self.df.loc[defenseur,'HP']-damage<0:
                self.df.loc[defenseur, 'HP']=0
            else :
                self.df.loc[defenseur, 'HP']-=damage

            #animation attaque et actualisation
            self.animation_atk(attaquant,defenseur)

            att=self.g.afficherTexte(f"{attaquant} inflige {damage}\n  dégâts à {defenseur}",600,195,'white',25)
            self.g.actualiser()
            self.g.attendreClic()

            self.g.supprimer(att)

            self.g.actualiser()

    def animation_atk(self,attaquant,defenseur):
        img_atk = self.redimenssioner_img(self.energie_ball[attaquant], 100, 100)
        attack_sphere = self.g.create_image(self.pos[attaquant], 207, image=img_atk, anchor="nw")
        for _ in range(30):
            self.g.deplacer_img(attack_sphere, (self.pos[defenseur] - self.pos[attaquant]) // 30, 0)
            time.sleep(0.03)
            self.g.actualiser()
        self.g.delete(attack_sphere)
        for _ in range(4):  # 4 cycles de vibrations
            self.g.deplacer_img(self.img[defenseur], 10, 0)
            self.g.actualiser()
            time.sleep(0.03)
            self.g.deplacer_img(self.img[defenseur], -10, 0)
            self.g.actualiser()
            time.sleep(0.03)

    def get_color_for_type(self,type):
        color_map = {
            "Bug": ("green","atk_bug.png"),
            "Dark": ("black","atk_dark.png"),
            "Dragon": ("purple","atk_dragon.png"),
            "Electric": ("yellow","atk_elec.png"),
            "Fairy": ("pink","atk_fee.png"),
            "Fighting": ("red","atk_fighting.png"),
            "Fire": ("red","atk_fire.png"),
            "Flying": ("lightblue","atk_fly.png"),
            "Ghost": ("purple","atk_ghost.png"),
            "Grass": ("green","atk_plante_.png"),
            "Ground": ("brown","atk_ground.png"),
            "Ice": ("cyan","atk_ice.png"),
            "Normal": ("gray","atk_normal.png"),
            "Poison": ("purple","atk_poison.png"),
            "Psychic": ("violet","atk_psy.png"),
            "Rock": ("brown","atk_rock.png"),
            "Steel": ("silver","atk_steel.png"),
            "Water": ("blue","atk_water.png")
        }
        return color_map.get(type, "gray")  # Retourne une couleur par défaut (gris)

    def nettoyer_nom_pokemon(self,nom):
        # Vérifie si "Mega" est dans le nom
        l=['Mega','Black',"White",'Heat', 'Wash', 'Frost', 'Fan', 'Mow','Primal','Plant']
        for prefixe in l:
            if prefixe in nom:
                # Séparer le nom en deux parties à "Mega" et retourner la première partie
                return nom.split(prefixe)[0].strip()
        return nom  # Si "Mega" n'est pas présent, renvoie le nom original

    # Fonction pour récupérer l'image d'un Pokémon
    def get_pokemon_image(self,pokemon_name):
        image_path = os.path.join("pokemon_images", f"{pokemon_name}.png")

        return self.redimenssioner_img(image_path,200,200)
    def redimenssioner_img(self,img,dimx,dimy):


        image = Image.open(img)  # Charger l'image avec Pillow
        image_resized = image.resize((dimx, dimy))  # Redimensionner (100x100 pixels)

        # Convertir l'image redimensionnée en format compatible avec Tkinter

        return ( ImageTk.PhotoImage(image_resized))



    def fin(self):
        self.g.attendreClic()
        self.g.fermerFenetre()
poke1='DeoxysNormal Forme'
poke2='Venusaur'
g=ouvrirFenetre(1200,600)
C=combat_de_pokemon(g)
C.combat(poke1,poke2)
C.fin()

