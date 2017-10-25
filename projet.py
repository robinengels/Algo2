import random
import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms import bipartite

class Graph:
	def __init__(self,max_aretes,max_noeuds,proba):
		self.nbr_aretes = random.randint(1,max_aretes)
		print("nbr aretes " + str(self.nbr_aretes))
		self.nbr_noeuds = random.randint(1,max_noeuds)
		print("nbr noeuds " + str(self.nbr_noeuds))
		self.graph = [[]for i in range(self.nbr_noeuds)] #Graph contenant une liste des noeuds, et chaque sous liste contien les aretes du noeud
		

		for i in range(self.nbr_aretes): #Itere pour chaque arete et commence à 0
			for j in self.graph: #Itere a chaque noeud
				if random.randint(1,proba) == 1: #Une chance sur trois que le noeud fasse partie de l'arrete i, comme ca c'est moins frequent
					j.append(i+1) #+1 parce que i commence à 0
        

		#self.graph = [[0],[0,1],[0,1,2],[3],[2],[2],[]] #temporaire, pour faire des testes sur la cyclicite
		#self.graph = [[], [1, 2], [2], [2, 3], [2], [2, 3], [2, 3]]
		print(self.graph)

	def __str__(self):
		print(self.graph)
		for i in range(len(self.graph)): #Commence a 0
			print("Le noeud "+str(i+1)+" fais partie de l'hyper-arete: ",end='')
			
			print(self.graph[i])
	
		return("")


	def berge(self):
		point_de_depart = 0
		self.derniere_arete_visitee = None #Stocke la derniere arete visitee pour eviter les allers retours
		self.dernier_point_visite = None #Stocke le dernier point visite poour eviter les allers retours
		self.points_visites = [] #Stocke les points visites pour eviter les allers retours, et si on tombe deux fois sur le meme point, alors il est cyclique
		self.arete_a_ne_pas_aller = []
		self.result = False
		
		while not self.result and point_de_depart < len(self.graph):
			self.arete_a_ne_pas_aller = [] #Nettoie la liste
			self.points_visites = [point_de_depart] #Iinitialise la liste des points visites avec uniquement le point de depart dedans
			self.dernier_point_visite = point_de_depart
			self.derniere_arete_visitee = None
			print("\n\npoint de depart: ",str(point_de_depart))
			self.cherche_aretes(point_de_depart)
			point_de_depart += 1
		return(self.result)
	
	def cherche_aretes(self,point):
		"""Recherche toutes les aretes qui partent d'un point et fais passer la fonction cherche_points dessus"""
		arete = 0
		if self.derniere_arete_visitee != None:
			self.arete_a_ne_pas_aller.append(self.derniere_arete_visitee)
		print(self.arete_a_ne_pas_aller)
		while not self.result and arete < len(self.graph[point]) and self.graph[point][arete] not in self.arete_a_ne_pas_aller:
			print("arete connectees:"+str(self.graph[point][arete]))
			self.derniere_arete_visitee = self.graph[point][arete]
			print("derniere arete visitee" + str(self.derniere_arete_visitee))
			self.cherche_points(self.graph[point][arete])
			arete += 1

	def cherche_points(self,arete):
		"""Recherche toutes les aretes qui partent d'un point et fais passer la fonction cherche_arete dessus jusqu'a ce qu'on retombe sur le point de depart ou qu'on ai visite tout les points"""
		points_connecte = []
		for i in range(len(self.graph)):
			if arete in self.graph[i] and i != self.dernier_point_visite:  #Si l'arete en question est liee a un point (dans la liste du point), alors le point est connecte a cette arete.
				points_connecte.append(i)


		i = 0
		while not self.result and i < len(points_connecte):
			point = points_connecte[i]
			print("point visite: "+str(point))
			self.dernier_point_visite = point
			if point in self.points_visites:
				self.result = True
			else:
				self.cherche_aretes(point)
			i += 1

	def affiche_graph(self):


		graph_affiche =  nx.Graph()
		left_nodes = [a for a in range(1,self.nbr_noeuds+1)]

		right_nodes = [chr(i+96) for i in range(1,self.nbr_aretes+1)]
		print(right_nodes,left_nodes)
		graph_affiche.add_nodes_from(left_nodes,bipartite=0)
		graph_affiche.add_nodes_from(right_nodes,bipartite=1)

		
		edge = []
		for i in self.graph:
			current_node = self.graph.index(i)+1
			if i != []:
				for j in i:
					current_edge = chr(j+96)
					edge.append((current_node,current_edge))
		graph_affiche.add_edges_from(edge)		

		pos = dict()
		cmpt = 0
		for i in left_nodes:
			cmpt += 1
			pos.update({i:(1,cmpt)})

		cmpt = 0
		for i in right_nodes:
			cmpt += 1
			pos.update({i:(2,cmpt)})



		#print(pos)
		print(graph_affiche.nodes())
		nx.draw(graph_affiche, pos=pos,with_labels = True)
		plt.show()


a = Graph(5,10,2)
a.affiche_graph()