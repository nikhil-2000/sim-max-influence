from model_objects.ICM import *
from model_objects.LBEM import *
from model_objects.LTM import *
from Active_Set_Selection.highest_degree import highest_degree_active_set

import time

p_edge = 0.2
n = 100
G = nx.erdos_renyi_graph(n, p_edge, directed=True)
w_matrix = degree_matrix(G)

icm = Independent_Cascade_Model(G, w_matrix)
lbem_icm = Live_Blocked_Model(G, w_matrix,from_model="ICM")
lbem_ltm = Live_Blocked_Model(G, w_matrix,from_model="LTM")
ltm = Linear_Threshold_Model(G, w_matrix)
models = [icm, lbem_icm, lbem_ltm, ltm]

active_set = highest_degree_active_set(icm, 5)

for m in models:
    t0 = time.time()
    m.run_model(active_set, mc=1000)
    t = time.time() - t0
    print(t, m.influence)
    print()
