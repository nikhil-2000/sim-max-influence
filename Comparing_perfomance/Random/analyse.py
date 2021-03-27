import pickle
import networkx as nx
from model_objects.ICM import Independent_Cascade_Model
from model_objects.LTM import Linear_Threshold_Model
from Active_Set_Selection.highest_weights import highest_avg_weight_active_set, highest_total_weight_active_set
import numpy as np

def get_total_weights(G,node,weights):

    in_edges = G.in_edges(node)
    out_edges = G.out_edges(node)

    total_in = 0
    total_out = 0

    for edge in in_edges:
        u,v = edge
        total_in += weights[u][v]

    for edge in out_edges:
        v,w = edge
        total_out += weights[v][w]

    return total_in,total_out

sets_file = open("LTM/tmp\sets.txt", "rb")
weights_file = open("LTM/tmp\weights.txt", "rb")

G = nx.readwrite.read_gpickle('LTM/tmp\graph.txt')
sets = pickle.load(sets_file)
weights = pickle.load(weights_file)

LTM = Linear_Threshold_Model(G, weights)
avg_weight = highest_avg_weight_active_set(LTM, 5)
total_weight = highest_total_weight_active_set(LTM, 5)
sets.append(avg_weight)
sets.append(total_weight)
print(sets[2].intersection(total_weight))

for s in sets:
    in_out_degrees = [(G.in_degree(x), G.out_degree(x)) for x in s]
    in_out_weights = [get_total_weights(G,node,weights) for node in s]

    ins = [n[0] for n in in_out_degrees]
    outs = [n[1] for n in in_out_degrees]
    ins_weights = [t[0] for t in in_out_weights]
    outs_weights = [t[1] for t in in_out_weights]
    print(np.mean(ins), np.mean(outs), np.sum(ins_weights), np.sum(outs_weights) , LTM.run_model(s,mc = 100))


