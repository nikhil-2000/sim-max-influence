import random


def random_active_set(model,k):

    G = model.get_graph()
    n = max(G.nodes)
    return {random.randint(0,n) for i in range(k)}