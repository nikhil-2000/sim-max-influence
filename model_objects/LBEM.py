# Live-Blocked Edge Model
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

    def __init__(self, graph: nx.Graph, p, from_model="Unchosen"):
        if from_model == "Unchosen":
            print("Pick a model out of LTM or ICM")
            raise ValueError()
        if from_model == "ICM":
            for edge in graph.edges:
                u, v = edge
                graph[u][v]["p"] = p[u][v]
                graph[u][v]["isLive"] = False

        else:
            for edge in graph.edges:
                u, v = edge
                graph[u][v]["influence"] = p[u][v]
                graph[u][v]["isLive"] = False

        for n in graph.nodes:
            graph.nodes[n]["isActive"] = False

        self.G = graph
        self.parent_model = from_model


    def get_graph(self):
        return self.G


    def run_model(self, active_set_0: set, mc=100):
        self.active_count = {n: 0 for n in self.G.nodes}
        for active in active_set_0: self.active_count[active] = mc
        final_active_dist, influences = {}, []

        for i in range(mc):

            final_active_set = self.single_run(active_set_0)

            if final_active_set not in final_active_dist:
                final_active_dist[final_active_set] = 1
            else:
                final_active_dist[final_active_set] += 1

            influences.append(len(final_active_set))

        self.influence = sum(influences) / len(influences)
        self.active_probabilities = {k: v / mc for k, v in self.active_count.items()}
        self.final_dist = {k: v / mc for k, v in final_active_dist.items()}

    def single_run(self, active_set_0):

        if self.parent_model == "ICM":
            self.set_edge_states_ICM()
        elif self.parent_model == "LTM":
            self.set_edge_states_LTM()

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

        self.reset_states()
        final_active_set = tuple(sorted(list(current_active_set)))
        return final_active_set

    def activate_neighbours(self, edges, next_active_set):
        for neighbour, data in edges:
            if data["isLive"] and not self.G.nodes[neighbour]["isActive"]:
                next_active_set.add(neighbour)
                self.G.nodes[neighbour]["isActive"] = True
                self.active_count[neighbour] += 1

    def set_edge_states_ICM(self):
        for edge in self.G.edges:
            u, v = edge
            p_live = self.G[u][v]["p"]
            self.G[u][v]["isLive"] = p_live > np.random.uniform()

    def set_edge_states_LTM(self):
        for node in self.G.nodes:
            # Get Incoming Edges
            neighbours = set(nx.all_neighbors(self.G, node))
            incoming_edges = [(n, node) for n in neighbours if (n, node) in self.G.edges]
            if len(incoming_edges) > 0:
                idxs = [i for i in range(len(incoming_edges))]
                p = [self.G.get_edge_data(u, v)["influence"] for u, v in incoming_edges]
                p_no_edge = 0 if 1 - sum(p) < 0 else 1 - sum(p)
                idxs.append(len(incoming_edges))
                incoming_edges.append("No Edge")
                p.append(p_no_edge)

                idx = np.random.choice(idxs, p=p)
                chosen_edge = incoming_edges[idx]
                if not (chosen_edge == "No Edge"):
                    u, v = chosen_edge
                    self.G[u][v]["isLive"] = True

    def reset_states(self):
        for edge in self.G.edges:
            u, v = edge
            self.G[u][v]["isLive"] = False

        for n in self.G.nodes:
            self.G.nodes[n]["isActive"] = False

    def activate_set(self, active_set):
        for n in active_set:
            self.G.nodes[n]["isActive"] = True

    def draw_graph(self):
        pos = nx.circular_layout(g)

        edges = self.G.edges()
        colors = []
        for u, v in edges:
            if self.G[u][v]["isLive"]:
                colors.append("r")
            else:
                colors.append("g")

        nx.draw(g, pos, edge_color=colors, with_labels=True)
        plt.show()

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
    edges = [(0, 1, 0.4), (0, 2, 0.4), (2, 1, 0.4)]
    G.add_nodes_from([0, 1, 2])
    G.add_weighted_edges_from(edges)

    nx.draw_spring(G, with_labels=True)
    plt.show()

    p = np.array([[0, 0.1, 0.3],
                  [0, 0, 0],
                  [0, 0.2, 0]])
    lbem = Live_Blocked_Model(G, p, from_model="ICM")
    lbem.run_model({0}, mc=100000)
    lbem.print_tables()
