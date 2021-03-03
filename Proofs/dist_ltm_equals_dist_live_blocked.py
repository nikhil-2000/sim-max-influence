from prettytable import PrettyTable

from model_objects.LTM import Linear_Threshold_Model, degree_matrix
from model_objects.LBEM import Live_Blocked_Model
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import time as t



def run_models(n = 100, p = 0.2,iterations = 10, mc = 1000):
    g = nx.erdos_renyi_graph(n,p, directed=True)
    weight_matrix = degree_matrix(g)
    LBEM = Live_Blocked_Model(g,weight_matrix, from_model="LTM")
    LTM = Linear_Threshold_Model(g,weight_matrix)
    errors , percent_errors= [], []
    print("n =", n, ", tests =", iterations, ",p_random_graph =", round(p_edge, 3), ",mc = ",mc)
    for i in range(iterations):
        size = np.random.randint(1,10)
        initial_active_set = {np.random.randint(0,n) for x in range(size)}
        t0 = t.time()
        LBEM.run_model(initial_active_set,mc)
        t1 = t.time()
        LTM.run_model(initial_active_set,mc)
        t2 = t.time()
        e = abs( LBEM.influence - LTM.influence)
        percent_error= 100 * e/np.average([LBEM.influence,LTM.influence])
        errors.append(e)
        percent_errors.append(percent_error)
        print("LBEM:",t1 - t0, " LTM:",t2 - t1)
        print("LBEM:",LBEM.influence, " LTM:",LTM.influence)
        print()

    avg_errors = np.average(errors)
    avg_percent_error = np.average(percent_errors)

    print("Average Error: ", avg_errors)
    large_error = [e for e in errors if e >= 1]
    print("Errors larger than 1: ",len(large_error))
    print()
    # print("Average Percent Error: ", avg_percent_error)
    # large_error = [e for e in percent_errors if e >= 1]
    # print("Percent Errors larger than 1: ", len(large_error))



for i in range(5):
    p_edge = np.random.uniform(0.01,0.2)
    run_models(n=100, p = p_edge, mc = 500,iterations=10)
    print()