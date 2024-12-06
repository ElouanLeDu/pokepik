import pandas as pds
import random
import os
from time import time
import pygame
import time
from tkiteasy import *

class combat_de_pokemon ():

    def __init__(self, g,df):
        self.g=g
        self.df = df
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
        self.cleaner={}
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
        pygame.mixer.music.load("musiques/combat music.mp3")  # Remplace par le chemin de ton fichier

        # Lancer la musique en boucle
        pygame.mixer.music.play(-1)  # -1 pour jouer en boucle

        #image
        img=self.g.afficherImage(-50, 0, "fonds/poke_stadium.png")

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


        #nom des pokemons sous leur barre de vie
        cleaned_name1=self.cleaned_name(poke1)
        cleaned_name2=self.cleaned_name(poke2)
        self.cleaner[poke1] = cleaned_name1
        self.cleaner[poke2] = cleaned_name2
        name1=self.g.afficherTexte(cleaned_name1, 110, 130)
        name2=self.g.afficherTexte(cleaned_name2, 1090, 130)

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

        #Texte début de combat
        x,y,z=self.g.afficherTexte(cleaned_name1,490,160,col_poke1,25),self.g.afficherTexte('VS',600,180,'white',25),self.g.afficherTexte(cleaned_name2,724,180,col_poke2,25)
        self.g.actualiser()
        self.g.attendreClic()
        self.g.supprimer(x)
        self.g.supprimer(y)
        self.g.supprimer(z)

        while self.df.loc[poke1,'HP']>0 and self.df.loc[poke2,'HP']>0 : #boucle tant que les deux pokemons sont en vie
            #actualisation tour et barres de vie
            t=self.g.afficherTexte(f'\n tour {tour}',600,30,'white',22)


            a=self.g.afficherTexte(f'{self.cleaner[attaquant]} attaque !', 600,195,'white',25)
            self.g.attendreClic()
            self.g.supprimer(a)

            #actualisation dégâts et attaquant
            self.degats(attaquant, defenseur)
            attaquant, defenseur = defenseur, attaquant

            #actualisation tour
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
        self.df.loc[looser,'Niveau']+=tour #plus le combat est long plus le pokemon monte en niveau

        #suppression des objets
        self.g.supprimer(poke1_hp_bar)
        self.g.supprimer(poke2_hp_bar)
        self.g.supprimer(name1)
        self.g.supprimer(name2)
        self.g.delete(self.img[poke1])
        self.g.delete(self.img[poke2])


        #gestion musique
        pygame.mixer.music.stop()  # Arrêter la musique à la fin
        pygame.mixer.init()        # démarrer musique de fin
        pygame.mixer.music.load("musiques/Fin.mp3")
        pygame.mixer.music.play(-1)

        #affichage gagnat
        textwin=self.g.afficherTexte(f"\n{self.cleaner[winner]} remporte\n      le combat !",600,185,'white',25)
        imgwin = self.get_pokemon_image(winner)
        win=self.g.create_image(505, 351, image=imgwin, anchor="nw")

        self.g.actualiser()
        self.g.attendreClic()
        self.g.supprimer(img)
        self.g.delete(win)
        self.g.supprimer(textwin)
        pygame.mixer.music.stop()
        return (winner,looser)

    def degats(self,attaquant,defenseur):

        #évitement ou non probabilité calculé en fonction de la vitesse des pokemons
        dodge_chance=self.df.loc[attaquant,'Speed']/ (self.df.loc[attaquant,'Speed']+self.df.loc[defenseur,'Speed'])

        if random.random() <= (1-dodge_chance)/2:  # L'attaque est esquivée

            esq=self.g.afficherTexte(f"    {defenseur} esquive\n   l'attaque de {attaquant} ",600,176,'white',25)
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

            att=self.g.afficherTexte(f"{attaquant} inflige {damage}\n  dégâts à {defenseur}",600,175,'white',25)
            self.g.actualiser()
            self.g.attendreClic()

            self.g.supprimer(att)

            self.g.actualiser()

    def animation_atk(self,attaquant,defenseur):

        #attaque avec la sphère de l'attaquant
        img_atk = self.redimenssioner_img(self.energie_ball[attaquant], 100, 100)
        attack_sphere = self.g.create_image(self.pos[attaquant], 207, image=img_atk, anchor="nw")

        for _ in range(30): #progression de la sphère jusqu'au défenseur
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

    def cleaned_name(self,mot):
        #faire un retour ligne pour chaque espace dans le noms des pokemons pour un affichage propre

        if ' ' in mot:
            return '\n'.join(mot.split(' '))
        else:
            return mot
    def get_color_for_type(self,type): #dico type couleur,sphère énérgie
        color_map = {
            "Bug": ("green","sphere_atk/atk_bug.png"),
            "Dark": ("black","sphere_atk/atk_dark.png"),
            "Dragon": ("purple","sphere_atk/atk_dragon.png"),
            "Electric": ("yellow","sphere_atk/atk_elec.png"),
            "Fairy": ("pink","sphere_atk/atk_fee.png"),
            "Fighting": ("red","sphere_atk/atk_fighting.png"),
            "Fire": ("red","sphere_atk/atk_fire.png"),
            "Flying": ("lightblue","sphere_atk/atk_fly.png"),
            "Ghost": ("purple","sphere_atk/atk_ghost.png"),
            "Grass": ("green","sphere_atk/atk_plante_.png"),
            "Ground": ("brown","sphere_atk/atk_ground.png"),
            "Ice": ("cyan","sphere_atk/atk_ice.png"),
            "Normal": ("gray","sphere_atk/atk_normal.png"),
            "Poison": ("purple","sphere_atk/atk_poison.png"),
            "Psychic": ("violet","sphere_atk/atk_psy.png"),
            "Rock": ("brown","sphere_atk/atk_rock.png"),
            "Steel": ("silver","sphere_atk/atk_steel.png"),
            "Water": ("blue","sphere_atk/atk_water.png")
        }
        return color_map.get(type, "gray")  # Retourne une couleur par défaut (gris)

    # Fonction pour récupérer l'image d'un Pokémon
    def get_pokemon_image(self,pokemon_name):
        image_path = os.path.join("pokemon_images", f"{pokemon_name}.png")

        return self.redimenssioner_img(image_path,190,190)

    def redimenssioner_img(self,img,dimx,dimy):


        image = Image.open(img)  # Charger l'image avec Pillow
        image_resized = image.resize((dimx, dimy))  # Redimensionner (100x100 pixels)

        # Convertir l'image redimensionnée en format compatible avec Tkinter

        return ( ImageTk.PhotoImage(image_resized))

    def combat_simple(self,poke1, poke2):
        """
        Combat entre deux Pokémon sans affichage ni musique.
        Retourne un tuple (vainqueur, perdant).
        """
        # Sauvegarde des stats originales
        stats_origin = {
            poke1: {"HP": self.df.loc[poke1, "HP"], "Attack": self.df.loc[poke1, "Attack"]},
            poke2: {"HP": self.df.loc[poke2, "HP"], "Attack": self.df.loc[poke2, "Attack"]}
        }

        # Boost des stats pour le Pokémon avantagé
        if self.avantage_type(poke1, poke2) is not None:
            poke_dominant = self.avantage_type(poke1, poke2)
            self.df.loc[poke_dominant, 'Attack'] += int(self.df.loc[poke_dominant, 'Attack'] * 0.2)

        # Détermination du Pokémon qui commence
        if self.df.loc[poke1, 'Speed'] > self.df.loc[poke2, 'Speed']:
            attaquant, defenseur = poke1, poke2
        elif self.df.loc[poke1, 'Speed'] < self.df.loc[poke2, 'Speed']:
            attaquant, defenseur = poke2, poke1
        else:
            # Choix aléatoire si égalité de vitesse
            attaquant, defenseur = random.sample([poke1, poke2], 2)

        tour = 1

        # Boucle principale du combat
        while self.df.loc[poke1, 'HP'] > 0 and self.df.loc[poke2, 'HP'] > 0:
            # Dégâts infligés
            self.degats_simple(attaquant, defenseur, self.df)
            attaquant, defenseur = defenseur, attaquant  # Changer les rôles
            tour += 1

        # Déterminer le vainqueur et le perdant
        if self.df.loc[poke2, 'HP'] <= 0:
            winner, looser = poke1, poke2
        else:
            winner, looser = poke2, poke1

        # Réinitialisation des stats du perdant
        self.df.loc[looser, "HP"] = stats_origin[looser]["HP"]
        self.df.loc[looser, "Attack"] = stats_origin[looser]["Attack"]
        self.df.loc[looser, 'Niveau'] += tour

        return (winner, looser)

    def degats_simple(self,attaquant, defenseur, df):
        """
        Calcule les dégâts infligés par un attaquant à un défenseur
        et met à jour les HP du défenseur.
        """
        # Évitement ou non basé sur la vitesse
        dodge_chance = self.df.loc[attaquant, 'Speed'] / (self.df.loc[attaquant, 'Speed'] + self.df.loc[defenseur, 'Speed'])

        if random.random() > (1 - dodge_chance) / 2:
            # L'attaque touche
            CRIT = random.uniform(0.7, 1.5)
            damage = (((((self.df.loc[attaquant, 'Niveau'] * 0.4 + 2) *
                         ((self.df.loc[attaquant, 'Sp. Atk'] + self.df.loc[attaquant, 'Attack']) / 2) *
                         50) / (self.df.loc[defenseur, 'Defense'] + self.df.loc[defenseur, 'Sp. Def'])) + 2) * CRIT) // 1
            self.df.loc[defenseur, 'HP'] = max(0, self.df.loc[defenseur, 'HP'] - damage)

    def fin(self):
        self.g.attendreClic()
        self.g.fermerFenetre()

#poke1='Charizard'
#poke2='Venusaur'
#g=ouvrirFenetre(1200,600)
#df = pds.read_csv('pokemon_modified.csv',index_col='Name')
#C=combat_de_pokemon(g,df)
#C.combat(poke1,poke2)
#C.fin()
