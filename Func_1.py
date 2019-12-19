import networkx as nx
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict
import pickle
import math

f = open( 'C:\\Users\\asa\\nevada\\USA-road-t.CAL.gr' , 'r+')
t = pd.read_csv(f  , sep= ' ' ,skiprows= list(range(7)) , names= ["a", "U", "V", "W"]) 

fd = open( 'C:\\Users\\asa\\nevada\\USA-road-d.CAL.gr' , 'r+')
td = pd.read_csv(fd  , sep= ' ' ,skiprows= list(range(7)) , names= ["a", "U", "V", "W"])

t.rename(columns={'distance':'time'},inplace=True)
td.rename(columns={'time':'distance'},inplace=True)
t['distance'] = td['distance']


all_nodes = t['U'].unique().tolist()


# Functionality 1 - Find the Neighbours!

def fun_1(node , dis_func ,d):
    # dis_func gets three different values: t , d or 1 which is the disnctance function
    if (dis_func != 'd' and dis_func != 't' and dis_func != 1):
        print('Please choose the right disdtance function, "d" , "t" or 1')

    elif dis_func == 1:
        neighbours = t[t['U']==node]['V'].tolist()
        a =0
        for i in range(d-1):
            temp= []
            for j in neighbours[a:] :
                temp += t[t['U']==j]['V'].tolist()

            a = len(neighbours)-1   
            neighbours += temp
            neighbours = sorted(set(neighbours) , key =lambda x: neighbours.index(x))
        return neighbours   

    elif dis_func == 't':

        neighbours = {}
        temp = {x:y for x,y in zip(t[t['U']==node]["V"].tolist() , t[t['U']==node]["time"].tolist()) if y<=d}
        while temp:
            for j in temp:
                for key in temp:
                    if key in neighbours:
                        neighbours[key] = min(neighbours[key], temp[key])
                    else:
                        neighbours[key] = temp[key]
                temp = {x:y+int(neighbours.get(j) or 0) for x,y in zip(t[t['U']==j]["V"].tolist() , t[t['U']==j]["time"].tolist()) if y+int(neighbours.get(j) or 0)<=d and x!=node}       
        try:        
            del neighbours[node]
        except:
            pass
        return neighbours 

    elif dis_func == 'd':
        neighbours = {}
        temp = {x:y for x,y in zip(t[t['U']==node]["V"].tolist() , t[t['U']==node]["distance"].tolist()) if y<=d}
        while temp:
            lenght = len(neighbours)
            for j in temp:
                for key in temp:
                    if key in neighbours:
                        neighbours[key] = min(neighbours[key], temp[key]) 
                    else:
                        neighbours[key] = temp[key]

                temp = {x:y+int(neighbours.get(j) or 0) for x,y in zip(t[t['U']==j]["V"].tolist() ,t[t['U']==j]["distance"].tolist()) if y+int(neighbours.get(j) or 0)<=d and x!=node}       

            if len(neighbours)==lenght:
                break
            lenght = len(neighbours)    


        return neighbours

   fun_1(10 , 'd' , 7000) 
