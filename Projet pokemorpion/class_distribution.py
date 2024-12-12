####### Class distribution ######
import traceback

from tkiteasy import *
import time
import pandas as pds
import os
from random import choice

class distribution():

    def __init__(self, window):
        self.pk = pds.read_csv(r"pokemon.csv", index_col="Name")
        self.pk_normal = self.pk.loc[self.pk["Legendary"] == False]
        self.pk_legend = self.pk.loc[self.pk["Legendary"] == True]
        self.player1 = []  # list of pokemon names for player 1
        self.player2 = []  # list of pokemon names for player 2
        self.g = window  # the main window to show the distribution, in class projetmorpion is self.g

    def get_pokemon_image(self, pokemon_name): # get a image of pokemon from the file
        pokemon_name = f'{pokemon_name}.png'  # add png
        files = os.listdir('pokemon_images')  # list of picture's name
        if pokemon_name in files:
            image_path = os.path.join('pokemon_images', pokemon_name)  # charge image
            try:
                # print(f'already found {pokemon_name}')
                return image_path # we return the path of image
                # because afficherImage in tkiteasy can only show the image by searching the path of image
            except Exception as e:
                print(f"impossible charging {pokemon_name}，error：{e}")
                # prevent the error situation
        else:
            print(f"can't find {pokemon_name} in pokemon_images ")

    def distribute_random(self):  # random distribute
        self.g.afficherImage(90, 0, 'distri_page.jpg', 1020, 600)
        submit = self.g.afficherTexte('submit', 600, 300, 'black', 25)
        # a button submit for backing to the main menu, it can be changed by a picture or other stuff
        self.g.actualiser()
        pool_1 = self.pk.loc[(self.pk['Total'] <= 550) & (self.pk['Total'] > 450)] # pool of 450<Total<550
        pool_2 = self.pk.loc[(self.pk['Total'] <= 360) & (self.pk['Total'] > 270)] # pool of 270<Total<360
        pool_3 = self.pk.loc[(self.pk['Total'] <= 450) & (self.pk['Total'] > 360)] # pool of 450<Total<550
        pool_4 = self.pk.loc[(self.pk['Total'] > 550)] # pool of 550<Total
        # divide all pokemons in 4 pool, according to their total value
        # all the number of each pool depends on the ratio of each range of pokemons' number in the whole dataset
        pl1_pool_1 = pool_1.sample(n=25) # 'sample' is random choice in the dataframe
        pool_1 = pool_1.drop(pl1_pool_1.index, inplace=False)
        pl2_pool_1 = pool_1.sample(n=25)
        # pool 1 of each player includes 25 pokemon
        pl1_pool_2 = pool_2.sample(n=15)
        pool_2 = pool_2.drop(pl1_pool_2.index, inplace=False)
        pl2_pool_2 = pool_2.sample(n=15)
        # pool 1 of each player includes 15 pokemon
        pl1_pool_3 = pool_3.sample(n=10)
        pool_3 = pool_3.drop(pl1_pool_3.index, inplace=False)
        pl2_pool_3 = pool_3.sample(n=10)
        # pool 1 of each player includes 10 pokemon
        pl1_pool_4 = pool_4.sample(n=10)
        pool_4 = pool_4.drop(pl1_pool_4.index, inplace=False)
        pl2_pool_4 = pool_4.sample(n=10, random_state=42)
        # pool 1 of each player includes 10 pokemon
        self.player1 = pds.concat([pl1_pool_1, pl1_pool_2, pl1_pool_3, pl1_pool_4])
        self.player2 = pds.concat([pl2_pool_1, pl2_pool_2, pl2_pool_3, pl2_pool_4])
        # we merge the pools that we have chosen
        self.player1 = list(self.player1.index)
        self.player2 = list(self.player2.index)
        # we choose only the index of dataframe as list
        l1 = []
        l2 = []
        for i in range(60):
            l1.append(self.get_pokemon_image(self.player1[i]))
            l2.append(self.get_pokemon_image(self.player2[i]))
            # l1 and l2 are used to conserve paths of images in self.player1 and self.player2
        for n in range(20):
            self.g.afficherImage(0, 30 * n, l1[n], 30, 30)
            self.g.afficherImage(30, 30 * n, l1[n + 20], 30, 30)
            self.g.afficherImage(60, 30 * n, l1[n + 40], 30, 30)
            self.g.afficherImage(1110, 30 * n, l2[n], 30, 30)
            self.g.afficherImage(1140, 30 * n, l2[n + 20], 30, 30)
            self.g.afficherImage(1170, 30 * n, l2[n + 40], 30, 30)
            time.sleep(0.05)
            self.g.actualiser()
        # show images in 2 sides of menu
        clic = self.g.attendreClic()
        x = self.g.recupererObjet(clic.x, clic.y)
        if x == submit:
            self.g.supprimerTout()
            # back to main menu

    def choose(self, pool, pl1, pl2, end_1_x, end_1_y, end_2_x, end_2_y):
        ### fonction of choosing pokemon in draft (clic and move from one side to other side)
        time_start = time.time()
        time_now = time.time()
        print(pool.shape[0])
        ch = pool.sample(n=2, random_state=42)
        # each time we choose random 2 pokemons in the targeted pool
        pool.drop(ch.index, inplace=True)
        # after choosing 2 pokemons, we delete these 2 pokemons from the pool
        ch = list(ch.index)
        # we conserve only the name of pokemons
        image_1_path = self.get_pokemon_image(ch[0])
        image_2_path = self.get_pokemon_image(ch[1])
        image_1 = self.g.afficherImage(200, 300, image_1_path, 200, 200)
        image_2 = self.g.afficherImage(750, 300, image_2_path, 200, 200)
        # show the image of 2 pokemons
        total_1 = self.g.afficherTexte(f'Total: {self.pk.loc[ch[0],'Total']}', 300, 250, 'black')
        total_2 = self.g.afficherTexte(f'Total: {self.pk.loc[ch[1], 'Total']}', 900, 250, 'black')
        # show the Total of 2 pokemons
        while time_now <= time_start + 10: # 10 seconds to choose
            time_now = time.time()
            t = self.g.afficherTexte(f"time:{int(time_start + 10 - time_now)}", 600, 150, 'red', 20)
            # show the time
            clic = self.g.recupererClic()
            self.g.supprimer(t)
            try:
                if clic != None: # if clic realised
                    o = self.g.recupererObjet(clic.x, clic.y) # we find the object of clic found
                    if o == image_1: # if we clic on the first image of pokemon
                        pl1.append(ch[0])
                        pl2.append(ch[1])
                        # add
                        self.g.supprimer(total_1)
                        self.g.supprimer(total_2)
                        # we delete text of Total
                        ch = None
                        # clear the list of 2 pokemons' names
                        for i in range(11):
                            self.g.supprimer(image_1)
                            self.g.supprimer(image_2)
                            image_1 = self.g.afficherImage(200 - ((200 - end_1_x) * i / 10),
                                                           300 - ((300 - end_1_y) * i / 10), image_1_path, 200 - i * 17,
                                                           200 - i * 17)
                            image_2 = self.g.afficherImage(750 - ((750 - end_2_x) * i / 10),
                                                           300 - ((300 - end_2_y) * i / 10), image_2_path, 200 - i * 17,
                                                           200 - i * 17)
                            # the movement of 2 image
                            time.sleep(0.1)
                            # time between 2 movements
                            self.g.actualiser()
                        break
                    elif o == image_2: # same methode as choose the first image, but we choose the second
                        self.g.supprimer(total_1)
                        self.g.supprimer(total_2)
                        pl1.append(ch[0])
                        pl2.append(ch[1])
                        ch = None
                        for i in range(11):
                            self.g.supprimer(image_1)
                            self.g.supprimer(image_2)
                            image_1 = self.g.afficherImage(200 - ((200 - end_2_x) * i / 10),
                                                           300 - ((300 - end_2_y) * i / 10), image_1_path, 200 - i * 17,
                                                           200 - i * 17)
                            image_2 = self.g.afficherImage(750 - ((750 - end_1_x) * i / 10),
                                                           300 - ((300 - end_1_y) * i / 10), image_2_path, 200 - i * 17,
                                                           200 - i * 17)
                            time.sleep(0.1)
                            self.g.actualiser()
                        break
            except KeyError as e:
                if type(e)==int:
                    print(e)

        if ch != None: # if we don't choose during 10 seconds:
            auto = choice([1, 2])
            # the computer choose random in the first and the second pokemon
            if auto == 1: # if computer choose the 1st image, we do the same movement as previous
                pl1.append(ch[0])
                pl2.append(ch[1])
                self.g.supprimer(total_1)
                self.g.supprimer(total_2)
                for i in range(10):
                    self.g.supprimer(image_1)
                    self.g.supprimer(image_2)
                    image_1 = self.g.afficherImage(200 - ((200 - end_1_x) * i / 10), 300 - ((300 - end_1_y) * i / 10),
                                                   image_1_path, 200 - i * 17, 200 - i * 17)
                    image_2 = self.g.afficherImage(750 - ((750 - end_2_x) * i / 10), 300 - ((300 - end_2_y) * i / 10),
                                                   image_2_path, 200 - i * 17, 200 - i * 17)
                    time.sleep(0.1)
                    self.g.actualiser()
            else: # if computer choose the 2nd image, we do the same movement as previous
                pl1.append(ch[1])
                pl2.append(ch[0])
                self.g.supprimer(total_1)
                self.g.supprimer(total_2)
                for i in range(10):
                    self.g.supprimer(image_1)
                    self.g.supprimer(image_2)
                    image_1 = self.g.afficherImage(250 - ((250 - end_2_x) * i / 10), 300 - ((300 - end_2_y) * i / 10),
                                                   image_1_path, 200 - i * 17, 200 - i * 17)
                    image_2 = self.g.afficherImage(800 - ((800 - end_1_x) * i / 10), 300 - ((300 - end_1_y) * i / 10),
                                                   image_2_path, 200 - i * 17, 200 - i * 17)
                    time.sleep(0.1)
                    self.g.actualiser()

    def distribute_draft(self):  # draft
        self.g.afficherImage(90, 0, 'distri_page.jpg', 1020, 600)
        pool1 = self.pk_legend.sample(n=20) # the first pool is legend pokemon
        pool2 = self.pk_normal.sample(n=100) # the second pool is normal pokemon
        for i in range(10): # choose from the legend pool
            if i % 2 == 0: # player 1 to choose
                t = self.g.afficherTexte('Round player 1', 600, 250, 'black', 40)
                if i>=9:
                    self.choose(pool1, self.player1, self.player2, 0, 90, 1170,90)
                else:
                    if i % 3 == 0:
                        self.choose(pool1, self.player1, self.player2, 0, 30*(i//3) , 1170,30*(i//3))
                    elif i % 3 == 1:
                        self.choose(pool1, self.player1, self.player2, 30, 30*(i//3), 1140,30*(i//3))
                    else:
                        self.choose(pool1, self.player1, self.player2, 60, 30*(i//3), 1110,30*(i//3))
                self.g.supprimer(t)
            else:# player 2 to choose
                t = self.g.afficherTexte('Round player 2', 600, 250, 'black', 40)
                if i >= 9:
                    self.choose(pool1, self.player2, self.player1, 0, 90, 1170, 90)
                else:
                    if i % 3 == 0:
                        self.choose(pool1, self.player2, self.player1, 1170, 30 * (i // 3), 0, 30 * (i // 3))
                    elif i % 3 == 1:
                        self.choose(pool1, self.player2, self.player1, 1140, 30 * (i // 3), 30, 30 * (i // 3))
                    else:
                        self.choose(pool1, self.player2, self.player1, 1110, 30 * (i // 3), 60, 30 * (i // 3))
                self.g.supprimer(t)
        for i in range(10,60):
            if i % 2 == 0: # player 1 to choose
                # too many image of normal so we show images in 2 colones
                t = self.g.afficherTexte('Round player 1', 600, 250, 'black', 40)
                if i == 10:
                    self.choose(pool2, self.player1, self.player2, 30, 90, 1140, 90)
                else:
                    if i % 3 == 0:
                        self.choose(pool2, self.player1, self.player2, 0, 30 * (i // 3), 1170, 30 * (i // 3))
                    elif i % 3 == 1:
                        self.choose(pool2, self.player1, self.player2, 30, 30 * (i // 3), 1140, 30 * (i // 3))
                    else:
                        self.choose(pool2, self.player1, self.player2, 60, 30 * (i // 3), 1110, 30 * (i // 3))
                self.g.supprimer(t)
            else: # player 1 to choose
                t = self.g.afficherTexte('Round player 2', 600, 250, 'black', 40)
                if i == 11:
                    self.choose(pool2, self.player2, self.player1, 1110, 90, 60, 90)
                else:
                    if i % 3 == 0:
                        self.choose(pool2, self.player2, self.player1, 1170, 30 * (i // 3), 0, 30 * (i // 3))
                    elif i % 3 == 1:
                        self.choose(pool2, self.player2, self.player1, 1140, 30 * (i // 3), 30, 30 * (i // 3))
                    else:
                        self.choose(pool2, self.player2, self.player1, 1110, 30 * (i // 3), 60, 30 * (i // 3))
                self.g.supprimer(t)
        self.g.supprimerTout() # back to the menu

g=ouvrirFenetre(1200,600)
d=distribution(g)
#d.distribute_draft()
d.distribute_random()