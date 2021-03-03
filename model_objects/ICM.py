#Independent Cascade Model
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from prettytable import PrettyTable
"""
On initialisation:
    -> Take in Graph + probability of successful activation
    -> Get live-blocked model

To Run:
    -> Run generated live-blocked model with initial set
    -> returns influence
"""

class Independent_Cascade_Model():
    def __init__(self,graph: nx.Graph ,p_matrix):
        for edge in graph.edges:
            u,v = edge
            graph[u][v]["p"] = p_matrix[u][v]


        for n in graph.nodes:
            graph.nodes[n]["isActive"] = False


        self.G = graph

    def run_model(self,active_set_0: set,mc = 100):
        self.active_count = {n:0 for n in self.G.nodes}
        for active in active_set_0: self.active_count[active] = mc
        final_active_dist, influences = {}, []

        for i in range(mc):
            final_active_set = self.single_run(active_set_0)

            influences.append(len(final_active_set))

            if final_active_set not in final_active_dist:
                final_active_dist[final_active_set] = 1
            else:
                final_active_dist[final_active_set] += 1

        self.influence = sum(influences) / len(influences)
        self.active_probabilities = {k:v/mc for k,v in self.active_count.items()}
        self.final_dist = {k:v/mc for k,v in final_active_dist.items()}


    def reset_states(self):

        for n in self.G.nodes:
            self.G.nodes[n]["isActive"] = False

    def activate_set(self, active_set):
        for n in active_set:
            self.G.nodes[n]["isActive"] = True

    def single_run(self,active_set_0):
        self.activate_set(active_set_0)

        current_active_set = set.copy(active_set_0)
        new_nodes = set.copy(active_set_0)
        while len(new_nodes) > 0:
            next_active_set = set.copy(current_active_set)
            for node in new_nodes:
                neighbours = list(self.G.neighbors(node))
                edges = [(neighbour, self.G.get_edge_data(node, neighbour)) for neighbour in neighbours]

                self.activate_neighbours(edges, next_active_set)

            new_nodes = next_active_set - current_active_set
            current_active_set = next_active_set

        final_active_set = tuple(sorted(list(current_active_set)))
        self.reset_states()

        return final_active_set

    def activate_neighbours(self, edges, next_active_set):
        for neighbour, data in edges:
            if data["p"] > np.random.uniform() and not self.G.nodes[neighbour]["isActive"]:
                next_active_set.add(neighbour)
                self.G.nodes[neighbour]["isActive"] = True
                self.active_count[neighbour] += 1

    def print_tables(self):
        node_prob_table = PrettyTable()
        node_prob_table.field_names = ["Node", "p"]
        for k, v in self.active_probabilities.items():
            row = k, v
            node_prob_table.add_row(row)

        print(node_prob_table)

        set_prob_table = PrettyTable()
        set_prob_table.field_names = ["Set", "p"]
        for k, v in self.final_dist.items():
            row = k, v
            set_prob_table.add_row(row)

        print(set_prob_table)


if __name__ == '__main__':

    G = nx.DiGraph()
    edges = [(0,1,0.4),(0,2,0.4),(2,1,0.4)]
    G.add_nodes_from([0,1,2])
    G.add_weighted_edges_from(edges)

    nx.draw_spring(G,with_labels=True)
    plt.show()

    p = np.array([[0,0.1,0.3],
         [0,0,0],
         [0,0.2,0]])
    icm = Independent_Cascade_Model(G,p)
    icm.run_model({0},mc = 100000)
    icm.print_tables()