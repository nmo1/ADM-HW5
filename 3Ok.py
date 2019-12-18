import webbrowser
import networkx as nx
from collections import defaultdict
import folium
from folium import plugins
import heapq as hp

G = nx.Graph()
adj = defaultdict(set)

with open(r'/home/giorgio/ADM/HW5/USA-road-d.CAL.co','r') as file:
    for line in file:
        if line[0] == 'v':
            x,lat,lon = list(map(int, line[2:].split()))
            G.add_node(x,latitude = lon/1000000,longitude = lat/1000000)

with open(r'/home/giorgio/ADM/HW5/USA-road-d.CAL.gr','r') as file1:
    for line in file1:
        if line[0] == 'a':
            x1,x2, d =  list(map(int, line[2:].split()))
            G.add_edge(x1,x2,distance = d,weight = 1)
            adj[x1].add(x2)
            adj[x2].add(x1)

with open(r'/home/giorgio/ADM/HW5/USA-road-t.CAL.gr','r') as file2:
    for line in file2:
        if line[0] == 'a':
            x1,x2, t = list(map(int, line[2:].split()))
            G.add_edge(x1,x2,time = t)

def ordAlg(v,end,p,graph = G,adjacent = adj):
    F = []
    hp.heapify(F)
    actualNode = v
    visited = {v: (None, 0)}
    while actualNode != end:
        adjacentes = adjacent[actualNode]
        weight_to_actualNode = visited[actualNode][1]
        for node in adjacentes:
            weight = graph[actualNode][node][p] + weight_to_actualNode
            if node not in visited:
                visited[node] = (actualNode, weight)
                hp.heappush(F,(weight,node))
            else:
                current_shortest_weight = visited[node][1]
                if current_shortest_weight > weight:
                    visited[node] = (actualNode, weight)
                    hp.heappush(F,(weight,node))
        #also here I check if the border is empty, if it's empty and we haven't left yet while it means that
        #I checked all the nodes without having reached the destination node
        #so I can say that there is no path between the starting node and the one of destination
        if not F:
            return "Route Not Possible"
        actualNode = hp.heappop(F)[1]
    path = []
    while actualNode is not None:
        path.append(actualNode)
        next_node = visited[actualNode][0]
        actualNode = next_node
    path.reverse()
    return path

def route(v,nodes,p):
    path = ordAlg(v,nodes[0],p)
    if type(path) == str:
        return path
    for i in range(1,len(nodes)):
        path1 = ordAlg(nodes[i-1],nodes[i],p)
        if type(path1) == str: #There is a Path?
            return path1
        else:
            path += path1[1:]
    return path


def createMap(nodelst):
    pos = G.nodes[nodelst[0]]
    vismap = folium.Map(location=[pos['latitude'], pos['longitude']])
    folium.LayerControl().add_to(vismap)
    visminimap = plugins.MiniMap(toggle_display=True)
    vismap.add_child(visminimap)
    plugins.ScrollZoomToggler().add_to(vismap)
    folium.Marker(location=[(pos['latitude']), (pos['longitude'])], popup=(nodelst[0])).add_to(vismap)

    for i in range(len(nodelst) - 1):
        pos = (G.nodes[nodelst[i + 1]])
        folium.Marker(location=[(pos['latitude']), (pos['longitude'])], popup=(nodelst[i + 1])).add_to(vismap)

    return vismap


def pathMap(nodelst, map_name):
    coordinateLst = []
    for i in nodelst:
        coordinateLst.append(list(G.nodes[i].values()))
    plugins.AntPath(coordinateLst).add_to(map_name)

    return map_name

def f3():
    h = int(input("Start Node: "))
    d = int(input("Arrive Node: "))
    t = input('Weight, distance, time: ')
    nodelst = ordAlg(h, d, t, graph=G, adjacent=adj)
    fpath = route(h, nodelst, t)
    c = createMap(fpath)
    a=pathMap(fpath, c)
    a.save('map.html')
    webbrowser.open('map.html')
f3()