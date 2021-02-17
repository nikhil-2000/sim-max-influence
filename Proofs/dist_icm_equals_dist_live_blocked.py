from prettytable import PrettyTable

from model_objects.ICM import Independent_Cascade_Model
from model_objects.LBEM import Live_Blocked_Model
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np




def run_models(n = 100, p = 0.2, p_icm = 0.05,iterations = 20):
    g = nx.erdos_renyi_graph(n,p, directed=True)
    p_matrix = (np.ones((n,n)) - np.identity(n)) * p_icm
    LBEM = Live_Blocked_Model(g,p_matrix)
    ICM = Independent_Cascade_Model(g,p_icm)
    # table = PrettyTable()
    # table.field_names = ["Iteration","ICM","LBEM","diff"]
    errors = []
    percent_errors = []
    for i in range(iterations):
        size = np.random.randint(1,n//2)
        initial_active_set = {np.random.randint(0,n) for x in range(size)}
        LBEM.run_model(initial_active_set,1000)
        ICM.run_model(initial_active_set,1000)
        e = abs( LBEM.influence - ICM.influence)
        percent_error= 100 * e/np.average([LBEM.influence,ICM.influence])
        errors.append(e)
        percent_errors.append(percent_error)
        # row = [i+1,LBEM.influence,ICM.influence,LBEM.influence - ICM.influence]
        # table.add_row(row)

    avg_errors = np.average(errors)
    avg_percent_error = np.average(percent_errors)

    print("Average Error: ", avg_errors)
    large_error = [e for e in errors if e >= 1]
    print("Errors larger than 1: ",len(large_error))
    print()
    print("Average Percent Error: ", avg_percent_error)
    large_error = [e for e in percent_errors if e >= 1]
    print("Percent Errors larger than 1: ", len(large_error))


for i in [0.01,0.05,0.1,0.15,0.2]:
    print("n = 100, p_icm_lbem = 0.05,tests = 20,p_random_graph =",i)
    run_models(p = i)
    print()