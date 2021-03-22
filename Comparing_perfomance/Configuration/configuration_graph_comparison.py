
import networkx as nx
import numpy as np
from Active_Set_Selection.greedy import greedy_active_set
from Active_Set_Selection.highest_degree import highest_degree_active_set
from Active_Set_Selection.random import random_active_set
import matplotlib.pyplot as plt
from model_objects.ICM import Independent_Cascade_Model
from networkx.generators.random_graphs import random_powerlaw_tree_sequence




def config_compare_ICM(n = 100, degree_dist = [], alpha = 0.5, mc_greedy = 100, k = 5):

    G = nx.configuration_model(degree_dist)
    p_matrix = np.random.uniform(low = 0, high = alpha ,size = (n, n))

    ICM = Independent_Cascade_Model(G, p_matrix)

    random_a0 = random_active_set(ICM, k)
    degree_a0 = highest_degree_active_set(ICM, k)
    greedy_a0 = greedy_active_set(ICM, k, mc = mc_greedy)

    sets =  [random_a0, degree_a0, greedy_a0]
    influences = map(lambda x: ICM.run_model(x,mc = 1000),sets)

    return list(influences)

p_edges = [0.1,0.2]
alpha = [0.1,0.2,0.3,0.4,0.5]
mc_greedy = 100
k = 5
# n = 100


# z=random_powerlaw_tree_sequence(5, gamma=3, seed=None, tries=1000)

din = np.random.randint(low = 0, high = 5, size = 7)
dout = np.random.permutation(din)
# We now expect an edge from node 0 to a new node, node 3.
D = nx.directed_configuration_model(din ,dout )

D = nx.DiGraph(D)
print(din)
print([d for n,d in D.in_degree])

print()

print(dout)
print([d for n,d in D.out_degree])

print()
print(list(filter(lambda x: x[0] == x[1], D.edges)))

nx.draw(D, with_labels=True)
plt.show()


