import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import copy

G = nx.erdos_renyi_graph(5, 0.2, directed=True)
G_copy = copy.deepcopy(G)

nx.draw(G, with_labels=True)
plt.show()
edges = G.edges
for e in edges:
    if np.random.uniform() > 0.5:
        G_copy.remove_edge(e[0],e[1])

nx.draw(G_copy, with_labels=True)
plt.show()

tree = nx.algorithms.tree.mst.minimum_spanning_edges(G_copy)
print(tree.nodes)
