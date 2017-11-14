import random
import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms import bipartite
print()

class Graph:
	def __init__(self,max_aretes,max_noeuds,proba):
		self.graph = {}
		self.nbr_aretes = random.randint(1,max_aretes)
<<<<<<< HEAD
		self.nbr_aretes = 4
		print("nbr aretes " + str(self.nbr_aretes))
=======
		#self.nbr_aretes = 3
		#print("nbr aretes " + str(self.nbr_aretes))
>>>>>>> 00bbe174b387dc1524ed93ab6db18cb0b253a9b4
		self.nbr_noeuds = random.randint(1,max_noeuds)
		#self.nbr_noeuds = 7
		#print("nbr noeuds " + str(self.nbr_noeuds))
		for i in range(self.nbr_noeuds):
			self.graph[i+1] = [] #Self.graph est un dico avec en clef le umero du noeud et en element une liste contenant les aretes auxquelles il est connecté
		

		for i in range(self.nbr_aretes): #Itere pour chaque arete et commence à 0
			for j in self.graph.keys(): #Itere a chaque noeud
				if random.randint(1,proba) == 1: #Une chance sur trois que le noeud fasse partie de l'arrete i, comme ca c'est moins frequent
					self.graph[j].append(i+1) #+1 parce que i commence à 0

		#Exemple d'un graphe qui est Cordal e=[(1,2),(1,3),(2,3),(2,4),(3,4),(3,5),(3,6),(4,5),(4,6),(5,6)]
		#self.graph = {1:[1,2],2:[1,3],3:[2,3],4:[2,4],5:[3,4],6:[3,5],7:[3,6],8:[4,5],9:[4,6],10:[5,6]}
<<<<<<< HEAD
		
		self.graph = {1:[1],2:[1,2],3:[1,2,3],4:[4],5:[3],6:[3],7:[]} #temporaire, pour faire des testes sur la cyclicite de Berge
=======
		self.graph  = {3: [3], 4: [4], 5: [1, 4], 7: [2, 5], 8: [4, 5], 9: [1, 2, 3], 10: [1, 4]} # Graqhe non cordal pour test
		#self.graph = {1:[1],2:[1,2],3:[1,2,3],4:[4],5:[3],6:[3],7:[]} #temporaire, pour faire des testes sur la cyclicite
>>>>>>> 00bbe174b387dc1524ed93ab6db18cb0b253a9b4
		#self.graph = [[2, 4, 5, 6, 7], [1, 7, 8], [2, 5, 6, 7], [2, 5, 6], [1, 3, 5, 6, 7, 8], [1, 2, 3, 4, 5], [3, 4, 7], [1, 2, 5, 7], [4], [1, 3, 4, 5]]
		#self.graph = [[], [1, 2], [2], [2, 3], [2], [2, 3], [2, 3]]
		#print("Test:",self.graph)

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
			
			current_clique = []
			correct = True
			for j in voisin:
				for k in voisin:
					if k not in self.voisin(j):
						correct = False
				
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
		self.clean_graph()
		print("Itération de chordal: ",self.graph)
		end = False
		ordre = []
		while not end:
			deleted = False
			clique = self.find_clique()
			print(clique)
			for i in clique:

				print("test",i, self.is_simplicial(i))		
				if self.is_simplicial(i):
					print("Supprime ",i)
					ordre.append(i)
					del self.graph[i]
					deleted = True
			if not deleted:
				end = True
				chordal = False
			if self.graph == {}:
				end = True
				chordal = True
		print(ordre)
		return end


	def is_simplicial(self,node):
		"""Renvoie True si le sommet envoyé est simplicial"""

		out = True
		voisin = self.get_voisins(node)[1:]
		print(voisin)
		if voisin != []:
			for i in voisin:

				for j in voisin:
					if j not in self.get_voisins(i):

						out = False
						break
		return out	

	def clean_graph(self):
		"""Efface tout les noeuds qui n'ont aucun voisin"""
		cle = list(self.graph)
		for i in cle:
			voisin = self.get_voisins(i)
			voisin.pop()
			if voisin == []:
				del self.graph[i]

	def berge(self):
		point_de_depart = 1 #Commence a 1 car le graphe commence a 1, et non a 0
		self.points_visites = [] #Stocke les points visites pour eviter les allers retours, et si on tombe deux fois sur le meme point, alors il est cyclique
		self.aretes_a_eviter = [] #Stocke les aretes deja parcourues, pour ne pas passer deux fois sur la meme arete
		self.result = False #Si un cycle est trouve, alors cette valeur vaudra True
		
		while not self.result and point_de_depart < len(self.graph)+1: #Si un cycle a ete trouve, ou que tout les noeuds ont ete fouilles, alors la boucle s'arrete
			self.aretes_a_eviter = [] #Nettoie la liste
			self.points_visites = [point_de_depart] #Nettoie la liste et y place uniquement le point de depart
			self.cherche_aretes(point_de_depart)
			point_de_depart += 1
		return(self.result)
	
	def cherche_aretes(self,point):
		"""Recherche toutes les aretes qui partent d'un point et les fais passer dans la fonction cherche_points"""
		arete = 0
		while not self.result and arete < len(self.graph[point]) and self.graph[point][arete] not in self.aretes_a_eviter:
			self.aretes_a_eviter.append(self.graph[point][arete])
			self.cherche_points(self.graph[point][arete])
			self.aretes_a_eviter.pop()
			arete += 1

	def cherche_points(self,arete):
		"""Recherche toutes les points lies a une arete et fais passer la fonction cherche_arete dessus jusqu'a ce qu'on retombe sur le point de depart ou qu'on ai visite tout les points disponibles"""
		points_connecte = []
		for i in range(len(self.graph)):
			if arete in self.graph[i+1] and i+1 != self.points_visites[-1]:
				points_connecte.append(i+1)

		i = 0
		while not self.result and i < len(points_connecte):
			point = points_connecte[i]
			if point in self.points_visites:
				self.result = True
			else:
				self.points_visites.append(point)
				self.cherche_aretes(point)
				self.points_visites.pop()
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

<<<<<<< HEAD
		
a = Graph(1,5,4)
#print("clique" + str(a.find_clique()))
print(a.berge())
#a.affiche_graphe_bipartie()
=======
	def test(self):
		pos = {}
		graph_affiche = nx.Graph()
		graph_affiche.add_nodes_from(self.graph.keys())

		for noeud in self.graph.keys():
			for arete_apartient in self.graph[noeud]:
				for autre_noeud in self.graph.keys():
					if noeud != autre_noeud: #Si on ne verifie pas deux fois le meme noeud
						if arete_apartient in self.graph[autre_noeud]:
							graph_affiche.add_edge(noeud,autre_noeud)
		a = nx.is_chordal(graph_affiche)
		b = self.is_chordal()	
		if a != b:
			print(a,b)



			nx.draw_circular(graph_affiche, with_labels = True)
			plt.show()


a = Graph(1,1,1)
print(a.is_simplicial(7))
a.affiche_graphe_primal()

"""while True:
	a = Graph(5,10,3)
	a.test()"""
>>>>>>> 00bbe174b387dc1524ed93ab6db18cb0b253a9b4
