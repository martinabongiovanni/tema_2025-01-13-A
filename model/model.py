import copy
import networkx as nx

from database.DAO import DAO
from operator import itemgetter

class Model:
    def __init__(self):
        # grafo
        self._grafo = nx.Graph()
        self._classifications = []
        self._genes = []
        self._id_map_classifications = {}
        self._id_map_genes = {}
        # ricorsione
        self._best_path = []
        self._best_n_cc = 0

    def get_all_localization(self):
        return DAO.get_all_localizations()

    def get_nodes(self):
        return self._grafo.nodes()

    def get_edges(self):
        return self._grafo.edges()

    def get_info_edges(self):
        lista = []
        for g1, g2, data in self._grafo.edges(data=True):
            lista.append([str(g1), str(g2), data["weight"]])
        # ordino la lista per pesi crescenti
        # lista.sort(key=lambda x: x[2])
        lista.sort(key=itemgetter(2))
        return lista


    def build_graph(self, localization):
        self._grafo.clear()
        # aggiungo i nodi
        self.fill_id_map_classifications(localization)
        self.fill_id_map_edge()
        self._grafo.add_nodes_from(self._classifications)
        # aggiungo gli archi
        all_interactions = DAO.get_all_interactions()
        all_edges = self.define_edges(all_interactions)
        for edge in all_edges:
            self._grafo.add_edge(self._id_map_classifications[edge[0]], self._id_map_classifications[edge[1]], weight=edge[2])
        return self._grafo.number_of_nodes(), self._grafo.number_of_edges()

    def fill_id_map_classifications(self, localization):
        self._classifications = DAO.get_all_classifications(localization)
        for c in self._classifications:
            self._id_map_classifications[c.GeneID] = c

    def fill_id_map_edge(self, ):
        self._genes = DAO.get_all_genes()
        for g in self._genes:
            self._id_map_genes[g.GeneID] = g

    def define_edges(self, all_interactions):
        all_edges = []
        for interaction in all_interactions:
            if (interaction.GeneID1 in self._id_map_classifications and
                interaction.GeneID2 in self._id_map_classifications and
                interaction.GeneID1 in self._id_map_genes and
                interaction.GeneID2 in self._id_map_genes):
                if self._id_map_genes[interaction.GeneID1].Chromosome == self._id_map_genes[interaction.GeneID2].Chromosome :
                    weight = self._id_map_genes[interaction.GeneID1].Chromosome
                else:
                    weight = self._id_map_genes[interaction.GeneID1].Chromosome + self._id_map_genes[interaction.GeneID2].Chromosome
                edge = (interaction.GeneID1, interaction.GeneID2, weight)
                all_edges.append(edge)
        return all_edges

    def get_componente_connessa(self):
        lista_all_componenti =[]
        set_componenti = nx.connected_components(self._grafo) # mi restituisce una lista di set (ogni set è la componente connessa, quindi un set di nodi)
        for element in set_componenti:
            if len(element) > 1:
                lista_ordinata = sorted(element)
                lista_all_componenti.append(lista_ordinata)
        return sorted(lista_all_componenti, key=lambda x:x[0])

    def get_longest_path(self):
        temp_path = []
        for n in self._grafo.nodes():
            temp_path.append(n)
            for vicino in self._grafo.neighbors(n):
                temp_path.append(vicino)
                self.ricorsione(temp_path)
                temp_path.pop()
        return self._best_path

    def ricorsione(self, temp_path):
        if len(temp_path) > len(self._best_path):
            self._best_path = copy.deepcopy(temp_path)
            self._best_n_cc = nx.number_connected_components(self._grafo.subgraph(self._best_path))
        if len(temp_path) == len(self._best_path):
            temp_n_cc = nx.number_connected_components(self._grafo.subgraph(temp_path))
            if temp_n_cc < self._best_n_cc:
                self._best_path = copy.deepcopy(temp_path)
                self._best_n_cc = temp_n_cc
        ultimo = temp_path[-1]
        for vicino in self._grafo.neighbors(ultimo):
            if vicino not in temp_path:
                temp_path.append(vicino)
                self.ricorsione(temp_path)
                temp_path.pop()
