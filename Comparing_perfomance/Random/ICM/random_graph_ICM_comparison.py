import networkx as nx
import numpy as np
from Active_Set_Selection.greedy import greedy_active_set
from Active_Set_Selection.highest_degree import highest_degree_active_set
from Active_Set_Selection.random import random_active_set
import matplotlib.pyplot as plt
from model_objects.ICM import Independent_Cascade_Model
from model_objects.LTM import Linear_Threshold_Model, degree_matrix, weight_matrix


def random_graph_compare_ICM(n = 100, p_edge = 0.1, alpha = 0.5, mc_greedy = 100, k = 5, is_random_weights = True):

    G = nx.erdos_renyi_graph(n, p_edge, directed=True)
    if is_random_weights:
        p_matrix = np.random.uniform(low = 0, high = alpha ,size = (n, n))
    else:
        p_matrix = degree_matrix(G)

    ICM = Independent_Cascade_Model(G, p_matrix)

    random_a0 = random_active_set(ICM, k)
    degree_a0 = highest_degree_active_set(ICM, k)
    greedy_a0 = greedy_active_set(ICM, k, mc = mc_greedy)

    sets =  [random_a0, degree_a0, greedy_a0]
    influences = map(lambda x: ICM.run_model(x,mc = 1000),sets)

    return list(influences)




p_edges = [0.1,0.2]
alpha = [0.1,0.2,0.3,0.4,0.5]
mc_greedy = 1000
k = 5
n = 100
is_random_weights = False
a = 0
# for p_edge in p_edges:
#     print(p_edge)
#     for i in range(10):
#         influences = map(str, random_graph_compare_ICM(n = n,p_edge = p_edge, alpha = a, mc_greedy = mc_greedy, k = 5 ,is_random_weights=is_random_weights))
#
#         str_vars = map(str, [n, p_edge, a, mc_greedy, k])
#         line = ",".join(list(str_vars) + list(influences) + [str(int(is_random_weights))]) + '\n'
#         print(line)
#         with open("data.csv", "a") as myfile:
#             myfile.write(line)

p_edge = 0.3
for i in range(10):
    influences = map(str, random_graph_compare_ICM(n = n,p_edge = p_edge, alpha = a, mc_greedy = mc_greedy, k = 5 ,is_random_weights=is_random_weights))

    str_vars = map(str, [n, p_edge, a, mc_greedy, k])
    line = ",".join(list(str_vars) + list(influences) + [str(int(is_random_weights))]) + '\n'
    print(line)
    with open("data.csv", "a") as myfile:
        myfile.write(line)
