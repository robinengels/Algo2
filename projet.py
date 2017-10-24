import random

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


graph  = generate_graph()
print_graph(graph)
