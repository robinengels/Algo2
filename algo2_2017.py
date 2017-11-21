import random
import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms import bipartite
print()

class Graph:
	def __init__(self,max_noeuds,max_aretes,proba):
		self.graph = {}
		self.nbr_aretes = random.randint(1,max_aretes)

		self.nbr_noeuds = random.randint(1,max_noeuds)
		for i in range(self.nbr_noeuds):
			self.graph[i+1] = [] #Self.graph est un dico avec en clef le numero du noeud et en element une liste contenant les aretes auxquelles il est connecté

		for i in range(self.nbr_aretes): #Itere pour chaque arete et commence à 0
			for j in self.graph.keys(): #Itere a chaque noeud
					if random.randint(1,proba) == 1: #Plus proba est grand, moins la chance qu'un noeud donnée fasse partie d'une arete donnee est petite.
							self.graph[j].append(i+1) #+1 parce que i commence à 0


	def __str__(self):
		print(self.graph)
		for i in range(len(self.graph)): #Commence a 0
			print("Le noeud "+str(i+1)+" fais partie de l'hyper-arete: ",end='')
			print(self.graph[i])

		return("")


	def affiche_graphe_bipartie(self):
		""" Fonction qui affiche le graphe en mode bipartie"""
		graph_affiche =  nx.Graph()
		left_nodes = self.graph.keys()
		right_nodes = [chr(i+96) for i in range(1,self.nbr_aretes+1)] #Transforme les chiffres en lettre
		graph_affiche.add_nodes_from(left_nodes,bipartite=0)
		graph_affiche.add_nodes_from(right_nodes,bipartite=1)

		edge = []
		for i in self.graph.keys(): #On définit a quelle arrete apartient chaque point
			current_node = i

			if self.graph[i] != []: #Si le point n'appartient a aucune aretes, alors pas besoin de chercher les autres points
				for j in self.graph[i]:
					current_edge = chr(j+96)
					edge.append((current_node,current_edge))#On associe a chaque point son arrete 

		graph_affiche.add_edges_from(edge)

		pos = dict()
		cmpt = 0
		#On positionne les arretes d'un coté et les noeuds de l'autres
		for i in left_nodes:
			cmpt += 1
			pos.update({i:(1,-cmpt)})
		cmpt = 0
		for i in right_nodes:
			cmpt += 1
			pos.update({i:(2,-cmpt)})

		nx.draw(graph_affiche, pos=pos,with_labels = True)#On affiche le graphe
		plt.show()

	def affiche_graphe_primal(self):
		"""Fonction qui affiche le graphe primal"""
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

	def find_clique(self,taille_max = 100000000000):
		"""Fonction qui renvoye les plus grande clique trouvée plus petite que la taille max par défaut assigné a l'infini"""
		clique = [[]]
		voisin = []
		current_clique = []
		
		for i in self.graph:#Test chaque point du graphe

			voisin = self.voisin(i)
			current_clique = []
			correct = True

			for j in voisin:#On regarde dans les voisin du point
				
				to_test = self.voisin(j)

				for k in voisin: #On vérifie que tout les voisin du point I se retrouve dans les voisins de J

					if k not in to_test:
						correct = False

					if correct and j not in current_clique:
						current_clique.append(j)

			if len(current_clique) > len(clique[0]) and len(current_clique)<=taille_max: #On vérifie la taille de la clique trouvée
				clique = [current_clique]
			elif len(current_clique) == len(clique[0]):
				clique.append(current_clique)
		return clique


	def voisin(self,node):
		"""Node est le numéro du noeuds pour le quelle on veut récupérer la liste des voisins"""
		result = [node]
		arc = self.graph[node]
		for i in self.graph:#On regarde tout les points du graphe
			for j in arc:
				if j in self.graph[i] and i not in result:#Si le point est dans un arc commun a Node alors il sont voisin
					result.append(i)


		return result



	def is_chordal(self):
		"""Renvoie True si le graphe est cordal"""
		
		self.clean_graph()#Retire tout les noeuds seuls

		end = False
		ordre = []
		taille_max = 1000000000000000000
		
		while not end:
			
			deleted = False #Serts a savoir si un noeuds a été éffacé
			clique = self.find_clique(taille_max)
			taille_max = len(clique[0])#Définit la taille maximum = la taille de la clique trouvée

			for j in clique:
				for i in j:#On parcourt une des clique trouvée
					if i in self.graph and self.is_simplicial(i):#Si le sommet est simplicial on le supprime

						ordre.append(i)
						del self.graph[i]
						taille_max = 100000000000000000 #On remet la taille max a infini
						deleted = True

			if not deleted:
				"""Si aucun sommet simplicial n'est supprimé
				il est possible qu'un sommet simplcial se trouve dans une clique plus petite"""

				taille_max -= 1
				if taille_max < 2:
					end = True #Si on a testé toute les clique les graphe n'est pas cordal

				chordal = False
			if self.graph == {}: #Si on a supprimé tout il est cordal
				end = True
				chordal = True

		return chordal


	def is_simplicial(self,node):
		"""Renvoie True si le sommet envoyé est simplicial"""

		out = True
		voisin = self.get_voisins(node)[1:]

		if voisin != []:
			for i in voisin:
				for j in voisin:#Vérifie pour chaque voisin qu'il a les même voisin commun
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
			if voisin == []: #Si il n'as aucun voisin on le supprime
				del self.graph[i]

	def get_voisins(self,node):
		"""Node est le numéro du noeuds pour lequel on veut récupérer la liste des voisins"""
		result = [node]
		arc = self.graph[node]
		for i in self.graph:
			for j in arc:
				if j in self.graph[i] and i not in result:
					result.append(i)
		return result


	def berge(self):
		point_de_depart = 1 #Commence a 1 car le graphe commence a 1, et non a 0
		self.points_de_depart_a_eviter = [] #Liste contenant des points deja visites, et dont il n'y aurait pas d'interet a faire l'analyse
		self.points_visites = [] #Stocke les points visites pour eviter les allers retours, et si on tombe deux fois sur le meme point, alors il est cyclique
		self.aretes_a_eviter = [] #Stocke les aretes deja parcourues, pour ne pas passer deux fois sur la meme arete
		self.result = False #Si un cycle est trouve, alors cette valeur vaudra True

		while not self.result and point_de_depart < len(self.graph)+1: #Si un cycle a ete trouve, ou que tout les noeuds ont ete fouilles, alors la boucle s'arrete
			if point_de_depart not in self.points_de_depart_a_eviter:
				self.aretes_a_eviter = [] #Nettoie la liste
				self.points_visites = [point_de_depart] #Nettoie la liste et y place uniquement le point de depart
				self.cherche_aretes(point_de_depart)
			point_de_depart += 1
		return(self.result)

	def cherche_aretes(self,point):
		"""Recherche toutes les aretes qui partent d'un point et les fais passer dans la fonction cherche_points"""
		arete = 0
		while not self.result and arete < len(self.graph[point]):
			if self.graph[point][arete] in self.aretes_a_eviter and self.graph[point][arete] != self.aretes_a_eviter[-1]: #Si une des aretes connectees a ce noeud a deja ete visitee, et que ce n'est pas la derniere arete visitee, alors un cycle a ete trouve
				self.result = True
			if self.graph[point][arete] not in self.aretes_a_eviter:
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
				self.points_de_depart_a_eviter.append(point)
				self.cherche_aretes(point)
				self.points_visites.pop()
			i += 1


def hypercycle(graph):
	if not graph.berge():
		print("Ce graphe est acyclique au sens de Berge")
	elif graph.is_chordal():
		print("Ce graphe est alpha-acyclique")
	else:
		print("Ce graphe est cyclique")

def main():
	graph = Graph(15,10,4)
	graph.affiche_graphe_bipartie()
	hypercycle(graph)

main()
