import pickle
from collections import defaultdict
import sys



with open(r'/home/giorgio/ADM/HW5/USA-road-d.CAL.co', 'r') as f1:
    content = f1.read()
nodes= dict()
for line in content.splitlines():  
    if line[0] == 'v':  
        nodes[int(line.split()[1])] = (int(line.split()[2]), int(line.split()[3]))  # create the dict

with open('dictGraph.pkl', 'wb') as f2:
    pickle.dump(nodes, f2, pickle.HIGHEST_PROTOCOL) #HIGHEST_PROTOCOL: An integer, the highest protocol version available. This value can be passed as a protocol value to functions dump() and dumps() as well as the Pickler constructor.

def processing(argumentFile):
    weight = defaultdict(list)
    for lenght in argumentFile.splitlines():
        if lenght[0] == 'a':
            weight[int(lenght.split()[1])].append((int(lenght.split()[2]), int(lenght.split()[3]))) #dict
    return weight

with open(r'/home/giorgio/ADM/HW5/USA-road-d.CAL.gr', 'r') as f3: 
    argument = f3.read()
distance = processing(argument) #dict
with open('distances.pkl', 'wb') as f4:
    pickle.dump(distance, f4, pickle.HIGHEST_PROTOCOL)


with open(r'/home/giorgio/ADM/HW5/USA-road-t.CAL.gr', 'r') as f4:
    argument = f4.read()
timeTravel = processing(argument)
with open('time.pkl', 'wb') as f5:
    pickle.dump(timeTravel, f5, pickle.HIGHEST_PROTOCOL)


def distanceGraph():
    with open('dictGraph.pkl', 'rb') as fileNode:
        nodeFile = pickle.load(fileNode)
    with open('distances.pkl', 'rb') as fileDist:
        distFile = pickle.load(fileDist)
    return nodeFile, distFile


def order(firstNode, visitNode, edges): #For John Bercow
    bestPath = [firstNode]
    while visitNode:
        ordNode = bfs(bestPath[-1], visitNode, edges)
        bestPath.append(ordNode)
        visitNode.remove(ordNode)

    del bestPath[0]

    return bestPath  # returning the ordered path


def bfs(first, target, edge):
    # first let's initialise the set that will stores the nodes we visited, we don't want to visit the same node
    # more than once
    visit = set()

    # than creating the queue of the elements to visit
    queue = [first]  # at the beginning we start with our starting node
    visit.add(first)

    while queue:  #if the queue is not empty work
        now = queue.pop() #the node where we are

        if now in target: return now

        for neighbour, weight in edge[now]:
            if neighbour not in visit:
                queue.insert(0, neighbour)  # at the beginning we start with our starting node
                visit.add(neighbour)

def main(firstNode, visit):
    try:
        vertice, edge = distanceGraph()

        orderNodes = order(firstNode, visit, edge)

        shortPath = orderNodes
    except:
        print("There is a problem")
        sys.exit(0)
    print(shortPath)

main()
#main(1, set([8,5,4]))