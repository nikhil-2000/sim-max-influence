
def highest_avg_weight_active_set(model ,k):

    G = model.get_graph()
    weights = model.get_weights()
    by_avg_weight = sorted(G.nodes, key= lambda x : avg_weight(G,x,weights) ,reverse=True)

    return set(by_avg_weight[:k])

def avg_weight(G,x,weights):
    if G.out_degree(x) > 0:
        return get_total_weights(G, x, weights)[1] / G.out_degree(x)

    return 0

def highest_total_weight_active_set(model ,k):

    G = model.get_graph()
    weights = model.get_weights()
    by_avg_weight = sorted(G.nodes, key= lambda x : get_total_weights(G,x,weights)[1],reverse=True)

    return set(by_avg_weight[:k])

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