#Live-Blocked Edge Model

"""
On initialising the model, need to take in
 -> Graph
 -> probabilities for edges
OR:
 -> A ICM model defined on the graph
OR:
 -> A LTM model defined on the graph


To Run model:
 -> Take in an initial set
 -> Run X times:
    -> Decide state for each edge
    -> Recursively add to set any neighbours that are connected by a live edge
    -> Keep going till no new nodes are added

"""