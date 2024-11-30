import time
import numpy as np
from tkiteasy import *
import math
from Combat import Combat_de_pokemon
import pandas as pds
from PIL import Image, ImageTk
import os
import tkinter as tk


def get_pokemon_image( pokemon_name):
    image_path = os.path.join("pokemon_images", f"{pokemon_name}.png")

    return redimenssioner_img(image_path, 43, 43)


def redimenssioner_img(img, dimx, dimy):
    image = Image.open(img)  # Charger l'image avec Pillow
    image_resized = image.resize((dimx, dimy))  # Redimensionner (100x100 pixels)

    # Convertir l'image redimensionnée en format compatible avec Tkinter

    return (ImageTk.PhotoImage(image_resized))

df = pds.read_csv('pokemon_modified.csv')

g = ouvrirFenetre(1200,600)

deck = [df.sample(n=60), df.sample(n=60)]

first_poke = deck[0].iloc[0]
poke = get_pokemon_image(deck[0].iloc[0]["Name"])
img1 = g.create_image(313, 207, image=poke, anchor="nw")
a = g.afficherImage(0,0,f"pokemon_images/{deck[0].iloc[0]["Name"]}.png",60,60)

g.actualiser()

# a = g.dessinerRectangle(0,0,50,50,"white")
# print(a)
clic = g.attendreClic()
objet2 = g.recupererObjet(clic.x,clic.y)
print(objet2)
g.deplacer(objet2,30,30)
g.actualiser
g.attendreClic()
