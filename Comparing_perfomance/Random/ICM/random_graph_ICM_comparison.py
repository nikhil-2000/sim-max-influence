import pickle

import networkx as nx
import numpy as np
from Active_Set_Selection.greedy import greedy_active_set
from Active_Set_Selection.highest_degree import highest_degree_active_set
from Active_Set_Selection.random import random_active_set
import matplotlib.pyplot as plt
from model_objects.ICM import Independent_Cascade_Model
from model_objects.LTM import degree_matrix


def random_graph_compare_ICM(n = 100, p_edge = 0.1, alpha = 0.5, mc_greedy = 100, k = 5, is_random_weights = True):

    G = nx.erdos_renyi_graph(n, p_edge, directed=True)
    if is_random_weights:
        p_matrix = np.random.uniform(low = 0, high = alpha ,size = (n, n))
    else:
        p_matrix = degree_matrix(G, alpha)

    ICM = Independent_Cascade_Model(G, p_matrix)

    random_a0 = random_active_set(ICM, k)
    degree_a0 = highest_degree_active_set(ICM, k)
    greedy_a0 = greedy_active_set(ICM, k, mc = mc_greedy)

    sets =  [random_a0, degree_a0, greedy_a0]
    influences = map(lambda x: ICM.run_model(x,mc = 1000),sets)

    print(sets)

    return list(influences)


def random_graph_compare_ICM_analyse(n=100, p_edge=0.1, alpha=0.5, mc_greedy=100, k=5, is_random_weights=True):
    G = nx.erdos_renyi_graph(n, p_edge, directed=True)
    if is_random_weights:
        p_matrix = np.random.uniform(low=0, high=alpha, size=(n, n))
    else:
        p_matrix = degree_matrix(G, alpha)

    ICM = Independent_Cascade_Model(G, p_matrix)

    random_a0 = random_active_set(ICM, k)
    degree_a0 = highest_degree_active_set(ICM, k)
    greedy_a0 = greedy_active_set(ICM, k, mc=mc_greedy)

    sets = [random_a0, degree_a0, greedy_a0]
    influences = list(map(lambda x: ICM.run_model(x, mc=1000), sets))

    print(sets)
    print(influences)

    return sets, G , p_matrix




def check_all_params():
    p_edges = [0.1,0.2]
    alpha = [0.2,0.4,0.6,0.8,1.0]
    isRandom = [False]
    mc_greedy = 1000
    k = 5
    n = 100

    for p_edge in p_edges:
        for a in alpha:
            for r in isRandom:
                influences = \
                    map(str, random_graph_compare_ICM(n = n,p_edge = p_edge, alpha = a, mc_greedy = mc_greedy, k = 5 ,is_random_weights=r))

                str_vars = map(str, [n, p_edge, a, mc_greedy, k])
                line = ",".join(list(str_vars) + list(influences) + [str(int(r))]) + '\n'
                print(line)
                with open("data.csv", "a") as myfile:
                    myfile.write(line)

def check_specific_params(runs = 1):
    p_edge = 0.1
    a = 0.2
    mc_greedy = 100
    k = 5
    r = True
    n = 100
    for i in range(runs):
        sets, G , weights = random_graph_compare_ICM_analyse(n=n, p_edge=p_edge, alpha=a, mc_greedy=mc_greedy, k=k, is_random_weights=r)
        nx.readwrite.write_gpickle(G, 'tmp/graph.txt')
        pickle.dump(sets, open('tmp/sets.txt', 'wb'))
        pickle.dump(weights, open('tmp/weights.txt', 'wb'))

        # line = ",".join(list(str_vars) + list(influences) + [str(int(r))]) + '\n'
        # print(line)
        # with open("data.csv", "a") as myfile:
        #     myfile.write(line)

check_specific_params()