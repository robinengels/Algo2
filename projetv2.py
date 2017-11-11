import random
import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms import bipartite

class Graph:
	def __init__(self,max_aretes,max_noeuds,proba):
		self.graph = {}
		self.nbr_aretes = random.randint(1,max_aretes)
		#self.nbr_aretes = 3
		print("nbr aretes " + str(self.nbr_aretes))
		self.nbr_noeuds = random.randint(1,max_noeuds)
		#self.nbr_noeuds = 7
		print("nbr noeuds " + str(self.nbr_noeuds))
		for i in range(self.nbr_noeuds):
			self.graph[i+1] = [] #Self.graph est un dico avec en clef le umero du noeud et en element une liste contenant les aretes auxquelles il est connecté
		

		for i in range(self.nbr_aretes): #Itere pour chaque arete et commence à 0
			for j in self.graph.keys(): #Itere a chaque noeud
				if random.randint(1,proba) == 1: #Une chance sur trois que le noeud fasse partie de l'arrete i, comme ca c'est moins frequent
					self.graph[j].append(i+1) #+1 parce que i commence à 0

		#Exemple d'un graphe qui est Cordal e=[(1,2),(1,3),(2,3),(2,4),(3,4),(3,5),(3,6),(4,5),(4,6),(5,6)]
		#self.graph = {1:[1,2],2:[1,3],3:[2,3],4:[2,4],5:[3,4],6:[3,5],7:[3,6],8:[4,5],9:[4,6],10:[5,6]}
		
		#self.graph = {1:[1],2:[1,2],3:[1,2,3],4:[4],5:[3],6:[3],7:[]} #temporaire, pour faire des testes sur la cyclicite
		#self.graph = [[2, 4, 5, 6, 7], [1, 7, 8], [2, 5, 6, 7], [2, 5, 6], [1, 3, 5, 6, 7, 8], [1, 2, 3, 4, 5], [3, 4, 7], [1, 2, 5, 7], [4], [1, 3, 4, 5]]
		#self.graph = [[], [1, 2], [2], [2, 3], [2], [2, 3], [2, 3]]
		print("Test:",self.graph)

	def __str__(self):
		print(self.graph)
		for i in range(len(self.graph)): #Commence a 0
			print("Le noeud "+str(i+1)+" fais partie de l'hyper-arete: ",end='')
			print(self.graph[i])
	
		return("")


	def affiche_graphe_bipartie(self):
		graph_affiche =  nx.Graph()
		left_nodes = self.graph.keys()
		right_nodes = [chr(i+96) for i in range(1,self.nbr_aretes+1)]
		graph_affiche.add_nodes_from(left_nodes,bipartite=0)
		graph_affiche.add_nodes_from(right_nodes,bipartite=1)

		edge = []
		for i in self.graph.keys():
			current_node = i

			if self.graph[i] != []: #Si le point n'appartient a aucune aretes, alors pas besoin de chercher les autres points
				for j in self.graph[i]:
					current_edge = chr(j+96)
					edge.append((current_node,current_edge))

		graph_affiche.add_edges_from(edge)
		
		pos = dict()
		cmpt = 0
		for i in left_nodes:
			cmpt += 1
			pos.update({i:(1,-cmpt)})
		cmpt = 0
		for i in right_nodes:
			cmpt += 1
			pos.update({i:(2,-cmpt)})
		print(graph_affiche.nodes())
		nx.draw(graph_affiche, pos=pos,with_labels = True)
		plt.show()

	def affiche_graphe_primal(self):
		pos = {}
		graph_affiche = nx.Graph()
		graph_affiche.add_nodes_from(self.graph.keys())

		for noeud in self.graph.keys():
			for arete_apartient in self.graph[noeud]:
				for autre_noeud in self.graph.keys():
					if noeud != autre_noeud: #Si on ne verifie pas deux fois le meme noeud
						if arete_apartient in self.graph[autre_noeud]:
							graph_affiche.add_edge(noeud,autre_noeud)
				

		nx.draw_circular(graph_affiche, with_labels = True)
		plt.show()

	def find_clique(self):
		clique = []
		voisin = []
		current_clique = []
		for i in self.graph:
			voisin = self.voisin(i)
			print(i,voisin)
			current_clique = []
			correct = True
			for j in voisin:
				for k in voisin:
					if k not in self.voisin(j):
						correct = False
				print(current_clique)
				if correct and j not in current_clique:
					current_clique.append(j)





			if len(current_clique) >= len(clique):
				clique = current_clique

		return clique

	def voisin(self,node):
		"""Node est le numéro du noeuds pour le quelle on veut récupérer la liste des voisins"""
		result = [node]
		arc = self.graph[node]
		for i in self.graph:
			for j in arc:
				if j in self.graph[i] and i not in result:
					result.append(i)


		return result



	def is_chordal(self):



		pass


	def is_simplicial(self,node):
		"""Renvoie True si le sommet envoyé est simplicial"""

		out = True
		voisin = self.get_voisin(node)[1:]
		if voisin != []:
			to_compare = self.get_voisin(voisin[0])
			for i in voisin:
				if self.get_voisin(i).sort() != to_compare.sort():
					out = False
					break
		return out	















	def berge(self):
		point_de_depart = 1 #Commence a 1 car le graphe commence a 1, et non a 0
		self.derniere_arete_visitee,self.dernier_pont_visite = None, None #Stocke la derniere arete visitee et le dernier point visite pour eviter les allers retours
		self.points_visites = [] #Stocke les points visites pour eviter les allers retours, et si on tombe deux fois sur le meme point, alors il est cyclique
		self.aretes_a_ne_pas_aller = []
		self.result = False
		
		while not self.result and point_de_depart < len(self.graph)+1:
			self.aretes_a_ne_pas_aller = [] #Nettoie la liste
			self.points_visites = [point_de_depart] #Iinitialise la liste des points visites avec uniquement le point de depart dedans
			self.dernier_point_visite = point_de_depart
			self.derniere_arete_visitee = None
			self.cherche_aretes(point_de_depart)
			point_de_depart += 1
		return(self.result)
	
	def cherche_aretes(self,point):
		"""Recherche toutes les aretes qui partent d'un point et fais passer la fonction cherche_points dessus"""
		arete = 0
		while not self.result and arete < len(self.graph[point]) and self.graph[point][arete] not in self.aretes_a_ne_pas_aller:
			self.derniere_arete_visitee = self.graph[point][arete]
			self.aretes_a_ne_pas_aller.append(self.graph[point][arete])
			self.cherche_points(self.graph[point][arete])
			self.aretes_a_ne_pas_aller.pop()
			arete += 1

	def cherche_points(self,arete):
		"""Recherche toutes les aretes qui partent d'un point et fais passer la fonction cherche_arete dessus jusqu'a ce qu'on retombe sur le point de depart ou qu'on ai visite tout les points"""
		points_connecte = []
		for i in range(len(self.graph)):
			if arete in self.graph[i+1] and i+1 != self.dernier_point_visite:  #Si l'arete en question est liee a un point (dans la liste du point), alors le point est connecte a cette arete.
				points_connecte.append(i+1)


		i = 0
		while not self.result and i < len(points_connecte):
			point = points_connecte[i]
			temp = self.dernier_point_visite #Temp sauvegarde le dernier point visite au travers de la recursivite
			self.dernier_point_visite = point
			if point in self.points_visites:
				self.result = True
			else:
				self.points_visites.append(point)
				self.cherche_aretes(point)
				self.points_visites.pop()
			self.dernier_point_visite = temp
			i += 1


	"""def find_clique(self):
		clique = []
		voisin = []
		current_clique = []
		for i in self.graph:
			voisin = self.get_voisins(i)
			print("Voisins: ",i,voisin)
			current_clique = []
			correct = True
			for j in voisin:
				for k in voisin:
					if k not in self.get_voisins(j):
						correct = False
				if correct and j not in current_clique:
					current_clique.append(j)

			if ((clique == [] and len(current_clique)>=3) or (clique != [] and len(current_clique) >= len(clique))):
				clique = current_clique

		return clique"""

	def get_voisins(self,node):
		"""Node est le numéro du noeuds pour lequel on veut récupérer la liste des voisins"""
		result = [node]
		arc = self.graph[node]
		for i in self.graph:
			for j in arc:
				if j in self.graph[i] and i not in result:
					result.append(i)
		return result

		

a = Graph(4,6,3)
print("clique" + str(a.find_clique()))
a.affiche_graphe_primal()
