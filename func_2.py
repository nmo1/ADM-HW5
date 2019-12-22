
with open('USA-road-d.CAL.gr', "r") as file:
    graph = file.readlines()
    
    
# read edges
edges = []
for i in graph[7:]:
    temp = list(map(int, (i.strip("\n").split(" ")[1:])))
    
    edges.append([temp[0], temp[1], temp[2]])
ed_d = edges

########################################################
with open('USA-road-t.CAL.gr', "r") as file:
    graph = file.readlines()
    
    
# read edges
edges = []
for i in graph[7:]:
    temp = list(map(int, (i.strip("\n").split(" ")[1:])))
    
    edges.append([temp[0], temp[1], temp[2]])
ed_t = edges



#########################################################
with open('USA-road-d.CAL.gr', "r") as file:
    graph = file.readlines()
    
    
# read edges
edges = []
for i in graph[7:]:
    temp = list(map(int, (i.strip("\n").split(" ")[1:])))
    
    edges.append([temp[0], temp[1], 1])
ed_1 = edges







def find_smartest(nodes_must_pass= [1,2,3], ed = ed_d):
    

    # Dijkstra
    from collections import defaultdict
    from heapq import *

    def di(edges, f, t):
        g = defaultdict(list)
        for l,r,c in edges:
            g[l].append((c,r))

        q, seen, mins = [(0,f,())], set(), {f: 0}
        while q:
            (cost,v1,path) = heappop(q)
            if v1 not in seen:
                seen.add(v1)
                path = (v1, path)
                if v1 == t: return (cost, path)

                for c, v2 in g.get(v1, ()):
                    if v2 in seen: continue
                    prev = mins.get(v2, None)
                    next = cost + c
                    if prev is None or next < prev:
                        mins[v2] = next
                        heappush(q, (next, v2, path))

        return float("inf")






    ###### Permutating over all posiible combinatins
    nodes_list = nodes_must_pass   # User enters




    from itertools import permutations
    perm = list(permutations(nodes_list))


    def Reverse(tuples): 
        new_tup = tuples[::-1] 
        return new_tup

    for i in perm:
        if Reverse(i) in perm:
            perm.remove(i)

    for i in perm:
        if Reverse(i) in perm:
            perm.remove(i)


    lst = []
    for i in perm:
        temp = []
        counter = 0
        for j in range(len(i) - 1):
            temp.append([i[j], i[j + 1]])
        lst.append(temp)



    def get_path(dijkstra_output):
        res = dijkstra_output
        p = []
        while res[1] != ():
            p.append(res[0])
            res = res[1]
        p.append(res[0])
        return(p[1:])



    distances = {}
    for i in lst:

        temp = 0
        for j in i:

            try:
                temp += distances[str([j[0], j[1]])]

            except:
                result = di(ed,j[0], j[1])      ######### functionality  switch      
                distances[str([j[0], j[1]])] = [result[0], Reverse(get_path(result))]
                distances[str([j[1], j[0]])] = [result[0], get_path(result)]  




    minimum = 10e10
    for i in lst:
        tot_dist = 0
        for j in i:
            tot_dist += distances[str(j)][0]
        if tot_dist < minimum:
            minimum = tot_dist



    path = []
    for j in i:
        path.append(distances[str(j)][1][:-1])

    path.append([distances[str(j)][1][-1]])

    print(minimum, sum(path,[]))


def visualize(G , nodes_list, ed):
    
    # feed with the answers come from the fun_2
    result = find_smartest(nodes_list , ed)
    edges = []
    for k in result:
        for i in list(G.neighbors(k)):
            edges.append((k,i))
    road = []
    i = 0
    while len(result)-1 >i:
        edges.append((result[i],result[i+1]))
        road.append((result[i],result[i+1]))
        i +=1
    fig = plt.gcf()
    fig.set_size_inches(21, 12)


    G1 = nx.Graph()
    G1.add_edges_from(edges)

    v_map = {1: 2.0,}

    values = [v_map.get(node, 0.25) for node in G1.nodes()]


    y_edges = road
    edge_colours = ['blue' if not edge in y_edges else 'y'
                    for edge in G1.edges()]
    b_edges = [edge for edge in G1.edges() if edge not in y_edges]

    pos = nx.spring_layout(G1)
    nx.draw_networkx_nodes(G1, pos, cmap=plt.get_cmap('rainbow'), 
                           node_color = values, node_size = 1)
    nx.draw_networkx_labels(G1, pos)
    nx.draw_networkx_edges(G1, pos, edgelist=y_edges, edge_color='y', arrows=True)
    nx.draw_networkx_edges(G1, pos, edgelist=b_edges, edge_color='blue',arrows=False)
    plt.show()
