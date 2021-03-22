import random

def greedy_active_set(model,k, mc = 100):

    active_set = set()
    G = model.get_graph()


    for i in range(k):
        inactive_nodes = set(G.nodes) - set(active_set)
        max_influence = 0
        best_addition = random.choice(list(inactive_nodes))
        for n in inactive_nodes:
            next_set = active_set.copy()
            next_set.add(n)
            model.run_model(next_set, mc = mc)

            if model.influence > max_influence:
                best_addition = n
                max_influence = model.influence

        active_set.add(best_addition)

    return active_set