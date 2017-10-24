import random
import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms import bipartite

def generate_graph():
	nbre_arrete = random.randint(1,8)
	nbre_noeuds = random.randint(1,10)
	graph = [[]for i in range(nbre_noeuds)]
	for i in range(1,nbre_arrete):
		for j in graph:
			chance = random.randint(1,2)
			if chance == 1:
				j.append(i)


	return graph

def print_graph(graph):
	for i in range(1,8):
		print("Noeuds dans l'hyper-arrête "+str(i)+" : ",end="")
		for j in graph:
			if i in j:
				print(str(graph.index(j)+1),end=", ")

		print()

def affiche_graph(graph):



	X, Y = bipartite.sets(graph)
	print(X,Y)

	pos = dict()
	cmpt = 0
	for i in X:
		cmpt += 1
		pos.update({i:(1,cmpt)})

	cmpt = 0
	for i in Y:
		cmpt += 1
		pos.update({i:(2,cmpt)})

	nx.draw(B, pos=pos,with_labels = True)
	plt.show()



