from storage import *
from agents import *

import random
import math
import networkx as nx

def generate_random_graph(stop_list, lim):
    G = nx.Graph()
    nodes_color = []
    stops = [eval(s.id) for s in stop_list]

    for x in range(lim[0]):
        for y in range(lim[1]):
            if x-1 < lim[0] and x-1 >= 0:
                G.add_edge((x,y), (x-1,y), weight=random.randint(50,200))
            if y-1 < lim[1] and y-1 >= 0:
                G.add_edge((x,y), (x,y-1), weight=random.randint(50,200))
    list_nodes_color = [abs(int(random.gauss(0,1.5))) for i in range(lim[0]*lim[1])]

    for i, n in enumerate(G.nodes().keys()):
        print(n)
        r = list_nodes_color[i] 
        if n in stops:
            s=stops.index(n)
            G.nodes()[n].update({'value':stop_list[s]})
            nodes_color.append('red')
        else:
            if r == 3 :
                if len(list(G.neighbors(n))) >=3:
                    G.nodes()[n].update({'value': MapNode(str(n), 0,  semaphore= Semaphore(str(n)))})
                    nodes_color.append('yellow')
                else:
                  r = 0
            if r == 2 :
                if len(list(G.neighbors(n))) >=3:
                    G.nodes()[n].update({'value': MapNode(str(n), 0,  semaphore= Semaphore(str(n)), authority = Authority(str(n)))})
                    nodes_color.append('green')
                else:
                  r = 0
            if r == 0 or r == 1:
                G.nodes()[n].update({'value': MapNode(str(n), 0)})
                nodes_color.append('black')        
            if r >= 4 :
                G.nodes()[n].update({'value': MapNode(str(n), 0,  authority = Authority(str(n)))})
                nodes_color.append('blue')
    print(G)
    print(nodes_color)
    print(len(nodes_color))
    return G
        
def write_map(graph,name):

    heigth = list(graph.nodes())[len(list(graph.nodes()))-1][0] + 1
    width = list(graph.nodes())[len(list(graph.nodes()))-1][1] + 1


    for i in range(heigth):
        line = []
        for j in range(width):
            if G.nodes()[(i,j)]['value'].authority != None and G.nodes()[(i,j)]['value'].semaphore != None:
                line.append(3)
            elif G.nodes()[(i,j)]['value'].authority != None:
                line.append(2)
            elif G.nodes()[(i,j)]['value'].semaphore != None:
                line.append(1)
            else:
                line.append(0)

        with open(name + '.txt','a') as f:
            f.write(str(line) + '\n')

    with open(name + '.txt','a') as f:
            f.write('Cost' + '\n')

    
    for e in graph.edges():
        edge1=e[0]
        edge2=e[1]
        weight = graph[edge1][edge2]['weight']

        with open(name + '.txt','a') as f:
            f.write('['+ str(edge1) + ';' + str(edge2) + ']' + ':' + str(weight) + '\n')


G = generate_random_graph([],(10,10))
print(G)
write_map(G,'map1')