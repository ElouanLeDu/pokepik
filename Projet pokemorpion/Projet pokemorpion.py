import numpy as np
import pandas as pds

import random
from tkiteasy import *
from math import *
from time import time
import matplotlib.pyplot as pyplt

# Début du programme :
# Aucune fonction n'a de renvoi. C'etait plus simple pour la construction du programme, bien que cela soit un peu inutile

class Pokemorpion():
    def __init__(self):
        self.score1 = 0
        self.score2 = 0
        self.g = ouvrirFenetre(1200, 600)
        self.g.afficherImage(0, 0, "fond_menu.jpg")


    def affichage_menu(self):  # affichage du menu principal
        self.b = self.g.afficherTexte("Choix du mode de jeu :", 700, 70, "black", 22)
        self.duo = self.g.afficherTexte("Mode duo", 525, 230, "black", 20)
        self.algosimple = self.g.afficherTexte("Mode robot simple", 767, 180, "black", 20)
        self.robot = self.g.afficherTexte("Mode robot expert", 765, 230, "black", 20)
        self.tabscore = self.g.afficherTexte("Tableau des scores", 544, 550, "black", 15)
        self.q = self.g.afficherTexte("Quitter le jeu", 900, 540, "black", 15)

        self.g.actualiser()

    def transition(self, nb):  # affichage uniquement transition menu de début de jeu
        # cette fonction est utilisee a 2 moments differents, le parametre permet de les distinguer
        # et d'eviter des doublons
        if nb == 1:  # écran de début du jeu
            a = self.g.afficherTexte("Bienvenue sur le jeu du Pokemorpion", 700, 150, "black", 30)
            b = self.g.afficherTexte("Jouer", 700, 340, "black", 30)
        #à voir si l'on fait d'autres transitions
        clic = self.g.attendreClic()
        x = self.g.recupererObjet(clic.x, clic.y)
        while x != b:  # le joueur doit cliquer sur jouer pour continuer
            clic = self.g.attendreClic()
            x = self.g.recupererObjet(clic.x, clic.y)
        self.g.supprimer(a)
        self.g.supprimer(b)

    def menu(self):  # menu principal, appel des fonctions et gestion des fonctionnalites
        self.transition(1)
        self.affichage_menu()
        stop = False
        while stop == False:  # on boucle tant que le joueur en clique pas sur quitter la partie
            clic = self.g.attendreClic()
            x = self.g.recupererObjet(clic.x, clic.y)

            if x == self.duo:

                rejouer = True

                while rejouer == True:  # même fonctionnement pour le mode duo en dehors du fait que le jeu est adapté pour 2 joueurs
                    self.superclean()
                    #fonction jeu 2 joueurs ici
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

            if x == self.algosimple:  # mode robot resolution simple

                self.superclean()
                self.affichage_jetons()
                #self.mode_auto_simple IA simple
                clic = self.g.attendreClic()
                x = self.g.recupererObjet(clic.x, clic.y)



            if x == self.robot:  # algo etape 3

                self.score_rob = 0
                self.score_exp = 0
                self.superclean()
                self.affichage_jetons()
                #self.mode_auto_opti(1) robot fort
                clic = self.g.attendreClic()
                x = self.g.recupererObjet(clic.x, clic.y)


            if x == self.tabscore:  # affichage du tableau des scores
                self.superclean()
                self.Tableau_des_scores()

                clic = self.g.attendreClic()
                x = self.g.recupererObjet(clic.x, clic.y)


            if x == self.q:  # bouton pour quitter le jeu
                self.fin()

            self.superclean()
            self.affichage_menu()

    def Tableau_des_scores(self):  # affichage du tableau des scores

        self.g.afficherTexte("Tableau des scores", 300, 100, "black", 30)
        self.g.afficherTexte("Mode robot", 100, 200, "black", 20)
        self.g.afficherTexte("étape 2", 60, 230, "black", 13)
        self.g.afficherTexte("étape 3", 140, 230, "black", 13)
        self.g.afficherTexte("Mode duo", 300, 200, "black", 20)
        self.g.afficherTexte("Joueur 1", 260, 230, "black", 13)
        self.g.afficherTexte("Joueur 2", 340, 230, "black", 13)
        self.g.afficherTexte("Mode solo", 500, 200, "black", 20)
        # boucles pour afficher l'ensemble des scores contenus dans des listes prévues à cet effet
        y = 230
        for i in range(len(self.score_solo)):  # affichage des scores dans l'ordre des parties
            self.g.afficherTexte(f"{self.score_solo[i]}", 500, y, "black", 15)

            y += 25
        y = 250
        for i in range(len(self.score_duo1)):
            self.g.afficherTexte(f"{self.score_duo1[i]}", 260, y, "black", 15)
            y += 25

        y = 250
        for i in range(len(self.score_duo2)):
            self.g.afficherTexte(f"{self.score_duo2[i]}", 340, y, "black", 15)
            y += 25

        y = 250
        for i in range(len(self.score_etape2)):
            self.g.afficherTexte(f"{self.score_etape2[i]}", 60, y, "black", 15)
            y += 25

        y = 250
        for i in range(len(self.score_etape3)):
            self.g.afficherTexte(f"{self.score_etape3[i]}", 140, y, "black", 15)
            y += 25

        self.g.actualiser()

    def superclean(self):
        self.g.supprimerTout()  # suppression de tous les éléments graphiques et restauration de certains
        self.q = self.g.afficherTexte("Quitter le jeu", 500, 540, "white", 15)
        self.g.afficherImage(0, 0, "fond_menu.jpg")

    def fin(self):
        self.g.fermerFenetre()  # fin de partie


#P = Pokemorpion()
#P.menu()


df = pds.read_csv('pokemon.csv', index_col='Name')
dict_av={
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


def avantage_type(poke1,poke2):
    for i in range(1, 3):
        for j in range(1, 3):

            type1 = df.loc[poke1, f'Type {i}']
            type2 = df.loc[poke2, f'Type {j}']

            # Ignorer si un des types est NaN
            if pds.isna(type1) or pds.isna(type2):
                continue

            # Vérifier si type2 est dans les avantages de type1
            if type2 in dict_av.get(type1, []):
                return poke1

            # Vérifier si type1 est dans les avantages de type2
            if type1 in dict_av.get(type2, []):
                return poke2

        # Aucun avantage trouvé
    return None


def combat (poke1,poke2):
    #sauvegarde stats

    stats_origin = {
        poke1: {"Total": df.loc[poke1, "Total"], "Attack": df.loc[poke1, "Attack"]},
        poke2: {"Total": df.loc[poke2, "Total"], "Attack": df.loc[poke2, "Attack"]}
    }


    if avantage_type(poke1, poke2) != None:
        poke_dominant = avantage_type(poke1, poke2)
        df.loc[poke_dominant,'Attack'] +=int(df.loc[poke_dominant,'Attack'] * 0.15)
        # paramètre général qui change l'avantage donné (vitesse,defense,..)??
    if df.loc[poke1, 'Speed']>df.loc[poke2, 'Speed']:
        attaquant=poke1
        defenseur=poke2
    elif df.loc[poke1, 'Speed']<df.loc[poke2, 'Speed']:
        attaquant=poke2
        defenseur=poke1
    else:
        i=randint(0,1)
        l=[poke1,poke2]
        attaquant = l[i]
        defenseur = l[(i+1)%2]
    tour=1
    while df.loc[poke1,'Total']>0 and df.loc[poke2,'Total']>0 :

        print(f'\n tour {tour}')
        print(f'{attaquant} attaque !')

        degats(attaquant, defenseur)
        attaquant, defenseur = defenseur, attaquant

        tour +=1
    # Déterminer le vainqueur
    winner = poke1 if df.loc[poke2,'Total'] <= 0 else poke2

    #réinitialisation des stats du gagant
    df.loc[winner, "Total"], df.loc[winner, "Attack"] = stats_origin[winner]["Total"], stats_origin[winner]["Attack"]

    return f"\n{winner} remporte le combat !"

def degats(attaquant,defenseur):
    dodge_chance=df.loc[attaquant,'Speed']/ (df.loc[attaquant,'Speed']+df.loc[defenseur,'Speed'])
    if random.random() <= 1-dodge_chance:  # L'attaque est esquivée
        print(f"{defenseur} esquive l'attaque de {attaquant} !")
    else:
        damage=int(df.loc[attaquant,'Attack']+df.loc[attaquant,'Sp. Atk']/df.loc[defenseur,'Defense']+df.loc[attaquant,'Sp. Def'])
        if df.loc[defenseur,'Total']-damage<0:
            df.loc[defenseur, 'Total']=0
        else :
            df.loc[defenseur, 'Total']-=damage
        print(f"{attaquant} inflige {damage} dégâts à {defenseur}. PV restants de {defenseur} : {df.loc[defenseur,'Total']}")
#print(combat('Charizard','Bulbasaur'))

#print(combat('Grimer','Cobalion'))


#TRAVAUX !!!

# Fonction pour obtenir la couleur en fonction du type

def get_color_for_type(type):
    color_map = {
        "Bug": "green",
        "Dark": "black",
        "Dragon": "purple",
        "Electric": "yellow",
        "Fairy": "pink",
        "Fighting": "red",
        "Fire": "red",
        "Flying": "lightblue",
        "Ghost": "purple",
        "Grass": "green",
        "Ground": "brown",
        "Ice": "cyan",
        "Normal": "gray",
        "Poison": "purple",
        "Psychic": "violet",
        "Rock": "gray",
        "Steel": "silver",
        "Water": "blue"
    }
    return color_map.get(type, "gray")  # Retourne une couleur par défaut (gris)
#print(combat('Charizard','Bulbasaur'))

#print(combat('Grimer','Cobalion'))


# Créer les carrés représentant les Pokémon et leurs barres de vie

#poke1_rect = g.dessinerRectangle(50, 200, 60, 60, get_color_for_type(type1))
#poke2_rect = g.dessinerRectangle(300, 200, 60, 60, get_color_for_type(type2))

#poke1_hp_bar = g.dessinerRectangle(50, 180, 60, 10, "green")
#poke2_hp_bar = g.dessinerRectangle(300, 180, 60, 10, "green")

#poke1_text = g.afficherTexte(poke1, 80, 270)
#poke2_text = g.afficherTexte(poke2, 320, 270)

#attack_line = g.dessinerLigne(80, 230, 320, 230, get_color_for_type(df.loc[attacker, 'Type 1']), 5)

#############################################################################################################################################################################################

#IMAGES

import requests
from PIL import Image, ImageTk
import tkinter as tk
from io import BytesIO


# pokeclean
def nettoyer_nom_pokemon(nom):
    # Vérifie si "Mega" est dans le nom
    if "Mega" in nom:
        # Séparer le nom en deux parties à "Mega" et retourner la première partie
        return nom.split("Mega")[0].strip()
    return nom  # Si "Mega" n'est pas présent, renvoie le nom original


# Fonction pour récupérer l'image d'un Pokémon
def get_pokemon_image(pokemon_name):
    cleaned_name = nettoyer_nom_pokemon(pokemon_name)
    url = f"https://pokeapi.co/api/v2/pokemon/{cleaned_name.lower()}"
    response = requests.get(url)
    data = response.json()
    image_url = data['sprites']['front_default']

    # Télécharger l'image
    img_response = requests.get(image_url)
    img_data = img_response.content
    img = Image.open(BytesIO(img_data))

    return ImageTk.PhotoImage(img)


# Créer une fenêtre Tkinter
root = tk.Tk()

# Charger l'image de Pikachu
pokemon_image = get_pokemon_image('CharizardMega Charizard')

# Afficher l'image dans Tkinter
label = tk.Label(root, image=pokemon_image)
label.pack()

root.mainloop()