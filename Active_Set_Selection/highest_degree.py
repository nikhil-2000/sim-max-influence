import networkx as nx

def highest_degree_active_set(model ,k):

    G = model.get_graph()
    by_degree = sorted(G.nodes, key= lambda x : G.out_degree(x),reverse=True)

    return set(by_degree[:k])
