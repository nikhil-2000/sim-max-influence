#Linear Threshold Model
from itertools import chain

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from prettytable import PrettyTable
"""
On initialisation:
    -> Take in Graph + Weights for directed edges
    -> Generate thresholds for each node
    -> Get live-blocked model

To Run:
    -> Run generated live-blocked model with initial set
    -> returns influence
"""

class Linear_Threshold_Model():
    def __init__(self,graph: nx.Graph ,weights):
        for edge in graph.edges:
            u,v = edge
            graph[u][v]["b_uv"] = weights[u,v]

        for n in graph.nodes:
            graph.nodes[n]["isActive"] = False
            graph.nodes[n]["theta_v"] = np.random.uniform()


        self.G = graph

    def get_graph(self):
        return self.G

    def run_model(self,active_set_0: set, mc = 100):
        self.active_count = {n:0 for n in self.G.nodes}
        for active in active_set_0: self.active_count[active] = mc
        final_active_dist, influences = {}, []

        for i in range(mc):
            final_active_set = self.single_run(active_set_0)

            if final_active_set not in final_active_dist:
                final_active_dist[final_active_set] = 1
            else:
                final_active_dist[final_active_set] += 1

            influences.append(len(final_active_set))
            self.reset_states()

        self.influence = sum(influences)/len(influences)
        self.active_probabilities = {k:v/mc for k,v in self.active_count.items()}
        self.final_dist = {k:v/mc for k,v in final_active_dist.items()}

        return  self.influence

    def single_run(self, active_set_0):
        self.set_thresholds()
        self.activate_set(active_set_0)
        current_active_set = set.copy(active_set_0)
        new_nodes = set.copy(active_set_0)
        while len(new_nodes) > 0:
            next_active_set = set.copy(current_active_set)
            list_of_neigbours = [set(self.G.neighbors(node)) for node in current_active_set]
            all_neigbours = set(chain.from_iterable(list_of_neigbours))

            inactive_nodes_to_check = all_neigbours - current_active_set
            nodes_is_active = self.get_activated_nodes(inactive_nodes_to_check)

            self.activate_nodes(next_active_set, nodes_is_active)

            new_nodes = next_active_set - current_active_set
            current_active_set = next_active_set

        final_active_set = tuple(sorted(list(current_active_set)))
        return final_active_set

    def get_activated_nodes(self, inactive_nodes_to_check):
        nodes_is_active = []
        for node in inactive_nodes_to_check:
            neighbours = set(nx.all_neighbors(self.G, node))
            incoming_neigbours = [n for n in neighbours if (n, node) in self.G.edges]
            edges = [(i, self.G.get_edge_data(i, node)) for i in incoming_neigbours]
            sum_of_weights = sum([d["b_uv"] for neighbour, d in edges if self.G.nodes[neighbour]["isActive"]])

            if sum_of_weights > self.G.nodes[node]["theta_v"]:
                nodes_is_active.append(node)

        return nodes_is_active

    def activate_nodes(self, next_active_set, nodes_is_active):
        for node in nodes_is_active:
            self.G.nodes[node]["isActive"] = True
            self.active_count[node] += 1
            next_active_set.add(node)

    def reset_states(self):
        g = self.G

        for n in g.nodes:
            g.nodes[n]["isActive"] = False

    def activate_set(self,active_set):
        g = self.G
        for n in active_set:
            g.nodes[n]["isActive"] = True

    def set_thresholds(self):
        graph = self.G
        for n in graph.nodes:
            graph.nodes[n]["theta_v"] = np.random.uniform()

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


def degree_matrix(g: nx.DiGraph, a):
    n = len(g.nodes)
    node_weights = []
    w_matrix = np.zeros((n,n))
    for n,d in g.in_degree():
        if d == 0:  v = 0
        else:       v = a/d
        node_weights.append(v)

    for (u,v) in g.edges():
        w_matrix[u,v] = node_weights[v]

    return w_matrix

def weight_matrix(G: nx.DiGraph, a):

    n = len(G.nodes)
    w_matrix = np.zeros((n,n))
    for node in G.nodes:
        neighbours = set(nx.all_neighbors(G,node))
        incoming_neigbours = [n for n in neighbours if (n, node) in G.edges]

        t = np.random.uniform(0,a)

        for neighbour in incoming_neigbours:
            w = np.random.uniform(0,t)
            t = t - w

            w_matrix[neighbour][node] = w

    return w_matrix




if __name__ == '__main__':

    G = nx.erdos_renyi_graph(n=10, p = 0.1, directed=True)

    nx.draw_spring(G,with_labels=True)
    plt.show()

    p = weight_matrix(G)
    print(p)
    # ltm = Linear_Threshold_Model(G,p)
    # ltm.run_model({0},mc = 10000)
    # ltm.print_tables()

