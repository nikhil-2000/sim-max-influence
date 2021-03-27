import random
import time
from Active_Set_Selection.highest_weights import get_total_weights


def greedy_active_set(model,k, mc = 100):

    active_set = set()
    G = model.get_graph()



    for i in range(k):
        inactive_nodes = list(set(G.nodes) - set(active_set))
        inactive_nodes = sorted(inactive_nodes, key= lambda x : get_total_weights(G,x,model.get_weights())[1],reverse=True)
        max_influence = 0
        best_addition = random.choice(inactive_nodes)
        checks = 20
        t0 = time.time()
        for n in inactive_nodes:
            next_set = active_set.copy()
            next_set.add(n)
            model.run_model(next_set, mc = mc)
            checks -= 1
            if model.influence > max_influence:
                best_addition = n
                max_influence = model.influence
                checks = 20

            if checks == -1:
                print("Exited Early")
                break

        print(time.time() - t0)
        active_set.add(best_addition)
        print("Picked ",i+1, "/", k)

    return active_set