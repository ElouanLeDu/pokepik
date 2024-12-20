####### Class distribution ######

import time
import os
import pandas as pds
from random import choice
import pygame

class distribution () :

    def __init__(self, window,df):
        self.pk = df
        self.pk_normal = self.pk.loc[self.pk["Legendary"] == False]
        self.pk_legend = self.pk.loc[self.pk["Legendary"] == True]
        self.player1 = []  # list of pokémon names for player 1
        self.player2 = []  # list of pokémon names for player 2
        self.g = window  # the main window to show the distribution, in class projetmorpion is self.g

    def get_pokemon_image(self, pokemon_name):
        pokemon_name = f'{pokemon_name}.png'  # add png
        files = os.listdir('pokemon_images')  # list of picture's name
        if pokemon_name in files:
            image_path = os.path.join('pokemon_images', pokemon_name)  # charge image
            return image_path


    def distribute_random(self):  # random distribute
        pygame.mixer.init()
        pygame.mixer.music.load("musiques/music_distri.mp3")
        pygame.mixer.music.play(-1)
        self.g.afficherImage(0, 0, "fonds/fond_distri.jpg", 1200, 600)
        submit = self.g.afficherImage(525, 240, "boutons/bouton_submit.png")
        self.g.actualiser()
        pool_1 = self.pk.loc[(self.pk['Total'] <= 550) & (self.pk['Total'] > 450)]
        pool_2 = self.pk.loc[(self.pk['Total'] <= 360) & (self.pk['Total'] > 270)]
        pool_3 = self.pk.loc[(self.pk['Total'] <= 450) & (self.pk['Total'] > 360)]
        pool_4 = self.pk.loc[(self.pk['Total'] > 550)]
        pl1_pool_1 = pool_1.sample(n=25)
        pool_1 = pool_1.drop(pl1_pool_1.index, inplace=False)
        pl2_pool_1 = pool_1.sample(n=25)
        pl1_pool_2 = pool_2.sample(n=15)
        pool_2 = pool_2.drop(pl1_pool_2.index, inplace=False)
        pl2_pool_2 = pool_2.sample(n=15)
        pl1_pool_3 = pool_3.sample(n=10)
        pool_3 = pool_3.drop(pl1_pool_3.index, inplace=False)
        pl2_pool_3 = pool_3.sample(n=10)
        pl1_pool_4 = pool_4.sample(n=10)
        pool_4 = pool_4.drop(pl1_pool_4.index, inplace=False)
        pl2_pool_4 = pool_4.sample(n=10)
        self.player1 = pds.concat([pl1_pool_1, pl1_pool_2, pl1_pool_3, pl1_pool_4])
        self.player2 = pds.concat([pl2_pool_1, pl2_pool_2, pl2_pool_3, pl2_pool_4])
        self.player1 = list(self.player1.index)
        self.player2 = list(self.player2.index)

        l1 = []
        l2 = []
        for i in range(60):
            l1.append(self.get_pokemon_image(self.player1[i]))
            l2.append(self.get_pokemon_image(self.player2[i]))

        for n in range(30):

            self.g.afficherImage(10, 40 * n, l1[n], 40, 40)

            self.g.afficherImage(110, 40 * n, l1[n + 30], 40, 40)

            self.g.afficherImage(1100, 40 * n, l2[n], 40, 40)

            self.g.afficherImage(1000, 40 * n, l2[n + 30], 40, 40)
            time.sleep(0.05)
            self.g.actualiser()
        clic = self.g.attendreClic()
        x = self.g.recupererObjet(clic.x, clic.y)
        while x != submit:
            clic = self.g.attendreClic()
            x = self.g.recupererObjet(clic.x, clic.y)
        pygame.mixer.music.stop()

        return [self.player1,self.player2]


    def choose(self, pool, pl1, pl2, end_1_x, end_1_y, end_2_x, end_2_y):
        time_start = time.time()
        time_now = time.time()

        ch = pool.sample(n=2, random_state=42)

        pool.drop(ch.index, inplace=True)
        ch = list(ch.index)

        image_1_path = self.get_pokemon_image(ch[0])
        image_2_path = self.get_pokemon_image(ch[1])
        image_1 = self.g.afficherImage(200, 300, image_1_path, 200, 200)
        image_2 = self.g.afficherImage(750, 300, image_2_path, 200, 200)
        total_1 = self.g.afficherTexte(f'Total: {self.pk.loc[ch[0], 'Total']}', 300, 250, 'black')
        total_2 = self.g.afficherTexte(f'Total: {self.pk.loc[ch[1], 'Total']}', 900, 250, 'black')
        while time_now <= time_start + 7:
            time_now = time.time()
            t = self.g.afficherTexte(f"time:{int(time_start + 10 - time_now)}", 600, 150, 'red', 20)
            clic = self.g.recupererClic()
            self.g.supprimer(t)
            if clic != None:
                o = self.g.recupererObjet(clic.x, clic.y)
                if o == image_1:
                    pl1.append(ch[0])
                    pl2.append(ch[1])
                    self.g.supprimer(total_1)
                    self.g.supprimer(total_2)
                    ch = None
                    for i in range(11):
                        self.g.supprimer(image_1)
                        self.g.supprimer(image_2)
                        image_1 = self.g.afficherImage(200 - ((200 - end_1_x) * i / 10),
                                                       300 - ((300 - end_1_y) * i / 10), image_1_path, 200 - i * 15,
                                                       200 - i * 15)
                        image_2 = self.g.afficherImage(750 - ((750 - end_2_x) * i / 10),
                                                       300 - ((300 - end_2_y) * i / 10), image_2_path, 200 - i * 15,
                                                       200 - i * 15)
                        time.sleep(0.0001)
                        self.g.actualiser()
                    break
                elif o == image_2:
                    self.g.supprimer(total_1)
                    self.g.supprimer(total_2)
                    pl1.append(ch[0])
                    pl2.append(ch[1])
                    ch = None
                    for i in range(11):
                        self.g.supprimer(image_1)
                        self.g.supprimer(image_2)
                        image_1 = self.g.afficherImage(200 - ((200 - end_2_x) * i / 10),
                                                       300 - ((300 - end_2_y) * i / 10), image_1_path, 200 - i * 15,
                                                       200 - i * 15)
                        image_2 = self.g.afficherImage(750 - ((750 - end_1_x) * i / 10),
                                                       300 - ((300 - end_1_y) * i / 10), image_2_path, 200 - i * 15,
                                                       200 - i * 15)
                        time.sleep(0.0001)
                        self.g.actualiser()
                    break
        if ch != None:

            auto = choice([1, 2])
            if auto == 1:
                pl1.append(ch[0])
                pl2.append(ch[1])
                self.g.supprimer(total_1)
                self.g.supprimer(total_2)
                for i in range(11):
                    self.g.supprimer(image_1)
                    self.g.supprimer(image_2)
                    image_1 = self.g.afficherImage(200 - ((200 - end_1_x) * i / 10), 300 - ((300 - end_1_y) * i / 10),
                                                   image_1_path, 200 - i * 15, 200 - i * 15)
                    image_2 = self.g.afficherImage(750 - ((750 - end_2_x) * i / 10), 300 - ((300 - end_2_y) * i / 10),
                                                   image_2_path, 200 - i * 15, 200 - i * 15)
                    time.sleep(0.0001)
                    self.g.actualiser()
            else:
                pl1.append(ch[1])
                pl2.append(ch[0])
                self.g.supprimer(total_1)
                self.g.supprimer(total_2)
                for i in range(11):
                    self.g.supprimer(image_1)
                    self.g.supprimer(image_2)
                    image_1 = self.g.afficherImage(250 - ((250 - end_2_x) * i / 10), 300 - ((300 - end_2_y) * i / 10),
                                                   image_1_path, 200 - i * 15, 200 - i * 15)
                    image_2 = self.g.afficherImage(800 - ((800 - end_1_x) * i / 10), 300 - ((300 - end_1_y) * i / 10),
                                                   image_2_path, 200 - i * 15, 200 - i * 15)
                    time.sleep(0.0001)
                    self.g.actualiser()


    def distribute_draft(self):  # draft
        pygame.mixer.init()
        pygame.mixer.music.load("musiques/music_distri.mp3")
        pygame.mixer.music.play(-1)
        self.g.afficherImage(0, 0, "fonds/fond_distri.jpg", 1200, 600)
        pool1 = self.pk_legend.sample(n=20)
        pool2 = self.pk_normal.sample(n=100)
        for i in range(10):
            if i % 2 == 0:
                t = self.g.afficherTexte('Round player 1', 600, 250, 'black', 40)
                self.choose(pool1, self.player1, self.player2, 100 + i * 20, 10, 1100 - i * 20, 10)
                self.g.supprimer(t)
            else:
                t = self.g.afficherTexte('Round player 2', 600, 250, 'black', 40)
                self.choose(pool1, self.player2, self.player1, 1100 - i * 20, 10, 100 + i * 20, 10)
                self.g.supprimer(t)
        for i in range(50):
            if i % 2 == 0:
                if i < 25:
                    t = self.g.afficherTexte('Round player 1', 600, 250, 'black', 40)
                    self.choose(pool2, self.player1, self.player2, 100, 40 + i * 20, 1100, 40 + i * 20)
                    self.g.supprimer(t)
                else:
                    t = self.g.afficherTexte('Round player 1', 600, 250, 'black', 40)
                    self.choose(pool2, self.player1, self.player2, 50, 40 + i * 20, 1150, 40 + (i - 25) * 20)
                    self.g.supprimer(t)
            else:
                if i < 25:
                    t = self.g.afficherTexte('Round player 2', 600, 250, 'black', 40)
                    self.choose(pool2, self.player2, self.player1, 1100, 40 + i * 20, 100, 40 + i * 20)
                    self.g.supprimer(t)
                else:
                    t = self.g.afficherTexte('Round player 2', 600, 250, 'black', 40)
                    self.choose(pool2, self.player2, self.player1, 1150, 40 + i * 20, 50, 40 + (i - 24) * 20)
                    self.g.supprimer(t)
        pygame.mixer.music.stop()
        return [self.player1, self.player2]


