import pickle

import networkx as nx

from Active_Set_Selection.greedy import greedy_active_set
from Active_Set_Selection.highest_degree import highest_degree_active_set
from Active_Set_Selection.random import random_active_set
from Active_Set_Selection.highest_weights import highest_total_weight_active_set, highest_avg_weight_active_set

from model_objects.LBEM import Live_Blocked_Model
from model_objects.LTM import degree_matrix, weight_matrix


def random_graph_compare_LTM(n = 100, p_edge = 0.1, alpha = 0.0, mc_greedy = 100, k = 5, is_random_weights = True):
    G = nx.erdos_renyi_graph(n, p_edge, directed=True)
    if is_random_weights:
        w_matrix = weight_matrix(G, alpha)
    else:
        w_matrix = degree_matrix(G, alpha)

    LTM = Live_Blocked_Model(G, w_matrix, from_model="LTM")

    random_a0 = random_active_set(LTM, k)
    degree_a0 = highest_degree_active_set(LTM, k)
    greedy_a0 = greedy_active_set(LTM, k, mc=mc_greedy)

    sets = [random_a0, degree_a0, greedy_a0]
    influences = map(lambda x: LTM.run_model(x, mc=1000), sets)

    print(random_a0,degree_a0,greedy_a0)

    return list(influences)

def compare_new_algorithms(n = 100, p_edge = 0.1, alpha = 0.0, mc_greedy = 1000, k = 5):
    G = nx.erdos_renyi_graph(n, p_edge, directed=True)
    w_matrix = weight_matrix(G, alpha)


    LTM = Live_Blocked_Model(G, w_matrix, from_model="LTM")

    random_a0 = random_active_set(LTM, k)
    degree_a0 = highest_degree_active_set(LTM, k)
    greedy_a0 = greedy_active_set(LTM, k, mc=mc_greedy)
    avg_weight_a0 = highest_avg_weight_active_set(LTM, k)
    tot_weight_a0 = highest_total_weight_active_set(LTM, k)

    sets = [random_a0, degree_a0, greedy_a0, avg_weight_a0, tot_weight_a0]
    influences = map(lambda x: LTM.run_model(x, mc=1000), sets)

    return list(influences)

def random_graph_compare_LTM_analyse(n=100, p_edge=0.1, alpha=0.5, mc_greedy=100, k=5, is_random_weights=True):
    G = nx.erdos_renyi_graph(n, p_edge, directed=True)
    if is_random_weights:
        w_matrix = weight_matrix(G, alpha)
    else:
        w_matrix = degree_matrix(G, alpha)

    LTM = Live_Blocked_Model(G, w_matrix, from_model="LTM")

    random_a0 = random_active_set(LTM, k)
    degree_a0 = highest_degree_active_set(LTM, k)
    greedy_a0 = greedy_active_set(LTM, k, mc=mc_greedy)

    sets = [random_a0, degree_a0, greedy_a0]
    influences = list(map(lambda x: LTM.run_model(x, mc=1000), sets))

    print(sets)
    print(influences)

    return sets, G , w_matrix

def check_all_params():
    p_edges = [0.1,0.2]
    alpha = [0.2,0.4,0.6,0.8,1.0]
    isRandom = [True]
    mc_greedy = 1000
    k = 5
    n = 100

    for p_edge in p_edges:
        for a in alpha:
            for r in isRandom:
                influences = \
                    map(str, random_graph_compare_LTM(n = n,p_edge = p_edge, alpha = a, mc_greedy = mc_greedy, k = 5 ,is_random_weights=r))

                str_vars = map(str, [n, p_edge, a, mc_greedy, k])
                line = ",".join(list(str_vars) + list(influences) + [str(int(r))]) + '\n'
                print(line)
                with open("data.csv", "a") as myfile:
                    myfile.write(line)

def check_new_params():
    p_edge = 0.1
    alpha = [0.2, 0.4,0.6,0.8,1.0]
    mc_greedy = 1000
    k = 5
    n = 100

    for a in alpha:
        influences = \
            map(str, compare_new_algorithms(n=n, p_edge=p_edge, alpha=a, mc_greedy=mc_greedy, k=5))

        str_vars = map(str, [n, p_edge, a, mc_greedy, k])
        line = ",".join(list(str_vars) + list(influences)) + '\n'
        print(line)
        with open("new_alg_data.csv", "a") as myfile:
            myfile.write(line)


def check_specific_params(runs = 1):
    p_edge = 0.2
    a = 0.8
    mc_greedy = 100
    k = 5
    r = True
    n = 100
    for i in range(runs):

        sets, G , weights = random_graph_compare_LTM_analyse(n=n, p_edge=p_edge, alpha=a, mc_greedy=mc_greedy, k=k, is_random_weights=r)
        nx.readwrite.write_gpickle(G, 'tmp/graph.txt')
        pickle.dump(sets, open('tmp/sets.txt', 'wb'))
        pickle.dump(weights, open('tmp/weights.txt', 'wb'))

for i in range(2):
    print("Run" , i)
    check_new_params()
