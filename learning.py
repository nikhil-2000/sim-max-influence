import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

def get_col(p):
    is_live = np.random.uniform() < p
    return "r" if is_live else "b"

n = 100
p = 0.5
g = nx.erdos_renyi_graph(n,2/n, directed=True)
d = dict(g.degree)
edges = g.edges()
colors = [get_col(p) for u,v in edges]
pos = nx.circular_layout(g)

nx.draw(g, nodelist=list(d.keys()), node_size=[v*10 for v in d.values()], edge_color=colors)
plt.show()