import numpy as np
import pandas as pd
import time
import threading
from random import choice
import copy

pk=pd.read_csv(r"pokemon.csv",index_col="Name")
pk_normal=pk.loc[pk["Legendary"]==False]
pk_legend=pk.loc[pk["Legendary"]==True]

#### we choose 1 legend pokemon after choosing 9 normal
#### everyone can have 5 legend and 45 normal

pool_normal=pk_normal.sample(n=90)
pool_legend=pk_legend.sample(n=10)

#### after we creat a way to let 2 players to make choices
#### idea is that 2 players can choose their 5 legend pokes first
#### and then creat their deck with their legend pokes
#### the order of choosing is alternate, player 1 first then player 2
#### 10s to choose

def get_input():
    global user_input
    user_input = int(input())

def choose(pool,pl1,pl2):
    print(pool.shape[0])
    ch = pool.sample(n=2, random_state=42)
    #we choose 2 poke in the pool
    pool = pool.drop(ch.index, inplace=True)
    #after choosing, we delet the 2 poke from the pool
    print(ch)#show ch
    ch_lst=np.array(ch.index)
    user_input=None
    input_thread = threading.Thread(target=get_input)
    input_thread.start()
    input_thread.join(timeout=10)
    #10s to choose
    if user_input not in [0, 1]:
        user_input = choice([0, 1])
    name=ch_lst[user_input]
    pl1[name] = ch.loc[ch.index == name].iloc[0]
    np.delete(ch_lst,user_input)
    pl2[ch_lst[0]] = ch.loc[ch.index == ch_lst[0]].iloc[0]
    print(pl1.keys(),pl2.keys())


def main_draft():
    player_1={}
    player_2={}
    pool1, pool2 = pool_legend.copy(), pool_normal.copy()
    for i in range(5):
        if i%2==0:
            choose(pool1,player_1,player_2)
        else:
            choose(pool1,player_2,player_1)
    for i in range(45):
        if i%2==0:
            choose(pool2,player_1,player_2)
        else:
            choose(pool2,player_2,player_1)
    return player_1,player_2


def random_draft(pool_legend,pool_normal):
    pool1, pool2 = pool_legend.copy(), pool_normal.copy()
    legned_p1=pool1.sample(n=5, random_state=42)
    pool1 = pool1.drop(legned_p1.index, inplace=False)
    legned_p2=pool1.sample(n=5, random_state=42)
    normal_p1=pool2.sample(n=45, random_state=42)
    pool2 = pool2.drop(normal_p1.index, inplace=False)
    normal_p2=pool2.sample(n=45, random_state=42)
    player_1=pd.concat([legned_p1,normal_p1])
    player_2=pd.concat([legned_p2,normal_p2])
    return player_1.index,player_2.index


print(main_draft())




