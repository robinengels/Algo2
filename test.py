import random
import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms import bipartite


graph = bipartite.random_graph(5,7,0.2)
left_nodes = list(graph.nodes())
left_nodes = left_nodes[:5]
right_nodes = list(graph.nodes())
right_nodes = right_nodes[5:]
pos = dict()
print(graph.edges())

graphique = [[]for i in range(0,5)]
for j in list(graph.edges()):
	graphique[j[0]].append(j[1])

print(graphique)

print(right_nodes,left_nodes)
cmpt = 0
for i in left_nodes:
	cmpt += 1
	pos.update({i:(1,cmpt)})

cmpt = 0
for i in right_nodes:
	cmpt += 1
	pos.update({i:(2,cmpt)})

nx.draw(graph,pos=pos,with_labels = True)
plt.show()