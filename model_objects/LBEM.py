#Live-Blocked Edge Model
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from prettytable import PrettyTable

"""
On initialising the model, need to take in
 -> Graph
 -> probabilities for edges
OR:
 -> A ICM model defined on the graph
OR:
 -> A LTM model defined on the graph


To Run model:
 -> Take in an initial set
 -> Run X times:
    -> Decide state for each edge
    -> Recursively add to set any neighbours that are connected by a live edge
    -> Keep going till no new nodes are added

"""

class Live_Blocked_Model():
    def __init__(self,graph: nx.Graph ,p):
        for edge in graph.edges:
            u,v = edge
            graph[u][v]["p"] = p[u][v]
            graph[u][v]["isLive"] = False


        for n in graph.nodes:
            graph.nodes[n]["isActive"] = False


        self.graph = graph

    def run_model(self,active_set_0: set, mc = 100):
        g = self.graph
        final_active_dist = {}
        influences = []
        for i in range(mc):
            self.set_edge_states()

            self.activate_set(active_set_0)

            current_active_set = set.copy(active_set_0)
            new_nodes = set.copy(active_set_0)
            while len(new_nodes) > 0:
                next_active_set = set.copy(current_active_set)
                for node in new_nodes:
                    neighbours = list(g.neighbors(node))
                    edges = [(neighbour,g.get_edge_data(node,neighbour)) for neighbour in neighbours]

                    for neighbour, data in edges:
                        if data["isLive"] and not g.nodes[neighbour]["isActive"]:
                            next_active_set.add(neighbour)
                            g.nodes[neighbour]["isActive"] = True

                new_nodes = next_active_set - current_active_set
                current_active_set = next_active_set

            final_active_set = tuple(sorted(list(current_active_set)))
            if final_active_set not in final_active_dist:
                final_active_dist[final_active_set] = 1
            else:
                final_active_dist[final_active_set] += 1

            influences.append(len(final_active_set))
            self.reset_states()

        self.influence = sum(influences)/len(influences)
        table = PrettyTable()
        table.field_names = ["Set","p"]

        for k,v in final_active_dist.items():
            row = k,v/mc
            table.add_row(row)

        self.final_dist = table


    def set_edge_states(self):
        for edge in self.graph.edges:
            u,v = edge
            p_live = self.graph[u][v]["p"]
            self.graph[u][v]["isLive"] = p_live > np.random.uniform()

    def reset_states(self):
        g = self.graph

        for edge in g.edges:
            u, v = edge
            g[u][v]["isLive"] = False

        for n in g.nodes:
            g.nodes[n]["isActive"] = False

    def activate_set(self,active_set):
        g = self.graph
        for n in active_set:
            g.nodes[n]["isActive"] = True

