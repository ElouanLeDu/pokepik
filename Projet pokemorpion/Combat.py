import numpy as np
import pandas as pds
import os
import random
from tkiteasy import *
from PIL import Image, ImageTk
import pygame
import time


class Combat_de_pokemon ():

    def __init__(self, g):
        self.g=g
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
        fond = self.g.afficherImage(-50, 0,"poke_stadium.png" )

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
        poke1_hp_bar = self.g.dessinerRectangle(46, 40,self.df.loc[poke1,'HP']*4, 33, col_poke1)
        poke2_hp_bar = self.g.dessinerRectangle(740, 40,self.df.loc[poke2,'HP']*4, 33, col_poke2)

        #noms nettoyés
        cleaned_name1=self.nettoyer_nom_pokemon(poke1)
        cleaned_name2=self.nettoyer_nom_pokemon(poke2)

        #nom des pokemons sous leur barre de vie
        self.g.afficherTexte(cleaned_name1, 96, 110)
        self.g.afficherTexte(cleaned_name2, 1100, 110)

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
            poke1_hp_bar = self.g.dessinerRectangle(46, 40,self.df.loc[poke1,'HP']*4, 33, col_poke1)
            poke2_hp_bar = self.g.dessinerRectangle(740, 40,self.df.loc[poke2,'HP']*4, 33, col_poke2)

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

        fond2 = self.g.afficherImage(-50, 0, "poke_stadium.png")
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


# poke1='DeoxysNormal Forme'
# poke2='Venusaur'
# g=ouvrirFenetre(1200,600)
# C=Combat_de_pokemon(g)
# C.combat(poke1,poke2)
# C.fin()