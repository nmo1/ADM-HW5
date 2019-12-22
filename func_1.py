import pandas as pd
import numpy as np
from collections import defaultdict
import networkx as nx
import matplotlib.pyplot as plt

df = pd.read_csv('C:\\Users\\Daniele\\Desktop\\Homework 5\\USA-road-d.CAL.gr.gz', compression='gzip', header=0, sep=',', quotechar='"')

df = df[6:]

df.rename(columns = {'c 9th DIMACS Implementation Challenge: Shortest Paths':'arc'},inplace = True)

list_df = df.values.tolist()

lis_df = []
for i in list_df:
    lis_df.append(list(map(int,(i[0].split())[1:])))
    
tree = defaultdict(list)
weight = defaultdict(list)

graph = lis_df

for i in range(len(lis_df)):
    id_node1 = graph[i][0]
    id_node2 = graph[i][1]
    w =graph[i][2] 
    
    tree[id_node1].append(id_node2)
    
    w_k = str(id_node1) +',' +(str(id_node2))
    weight[w_k].append(w)
    
def bfs(graph,v,weight,k):
    distance = {}
    for item in tree.keys():
        distance[item] = np.inf
    distance[v] = 0
    queue, output = [],[]
    queue.append(v)
    output.append(v)
    connection = []

    while queue:
        v = queue[0]
        queue.pop(0)
        for u in tree[v]:
            w_k = str(v)+','+str(u)
            if len(weight[w_k])>0:
                if distance[u] > distance[v] + weight[w_k][0]:
                    distance[u] = distance[v] + weight[w_k][0]
                    if distance[u] != np.inf and distance[u] <= k:
                        queue.append(u)
                        output.append(u)
                        connection.append(w_k)
                    
    return output,connection

def main():
    result = bfs(tree,5,weight,10000)
    
    conn = result[1]
    
    G = nx.Graph()
    
    for i in conn:
        j = list(map(int,(i.split(','))))
        G.add_node(j[0])
        G.add_node(j[1])
        G.add_edge(j[0], j[1], weight = weight[i][0])
        
    elarge = [(u, v) for (u, v, d) in G.edges(data=True) if d['weight'] > 0.5]
    esmall = [(u, v) for (u, v, d) in G.edges(data=True) if d['weight'] <= 0.5]
    
    pos = nx.spring_layout(G)  # positions for all nodes
    
    # nodes
    nx.draw_networkx_nodes(G, pos, node_size=700)
    
    # edges
    nx.draw_networkx_edges(G, pos, edgelist=elarge,
                           width=6)
    nx.draw_networkx_edges(G, pos, edgelist=esmall,
                           width=6, alpha=0.5, edge_color='b', style='dashed')
    
    # labels
    nx.draw_networkx_labels(G, pos, font_size=20, font_family='sans-serif')
    
    plt.axis('off')
    plt.show()