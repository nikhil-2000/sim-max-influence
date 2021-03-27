import networkx as nx
from model_objects.LTM import degree_matrix, weight_matrix
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import  seaborn as sns

def gen_graph_and_weights(n = 100, p = 0.2, a = 1.0):

    G = nx.erdos_renyi_graph(n, p, directed=True)

    return G, degree_matrix(G, a), weight_matrix(G,a)

def get_measures(w_matrix):
    w_matrix = w_matrix.flatten()
    above_zero_idxs = np.where(w_matrix > 0)
    above_zero = w_matrix[above_zero_idxs]
    min_w = np.amin(above_zero)
    max_w = np.amax(above_zero)
    average = np.mean(above_zero)
    # variance = np.var(above_zero)
    measures = list(map(str, [min_w, max_w, average]))
    return measures

def build_data():
    n = 100
    p = 0.2
    for alpha in range(1,11):
        alpha = alpha/10
        G, d_weights, r_weights = gen_graph_and_weights(n,p,alpha)
        d_measures = get_measures(d_weights)
        r_measures = get_measures(r_weights)


        str_vars = list(map(str, [n, p, alpha]))
        degree_line = ",".join(str_vars + ["degree"] + d_measures) + '\n'
        random_line = ",".join(str_vars + ["random"] + r_measures) + '\n'
        with open("weight_data.csv", "a") as myfile:
            myfile.write(degree_line)
            myfile.write(random_line)

def melt(df):
    df = df.melt(id_vars=["n", "p", "alpha"],
              var_name="measure", value_name="value")

    return df

def plot_graphs():
    with open("weight_data.csv", "r", encoding='utf-8-sig') as data:
        d = data.read()

    d = d.split("\n")
    d = [l.split(",") for l in d]

    df = pd.DataFrame(data=d[1::], columns=d[0])
    for col in df.columns:
        if col != "w_type":
            df[col] = df[col].astype(float)

    degree_data = df.loc[df.w_type == "degree"].drop("w_type", axis = "columns")
    random_data = df.loc[df.w_type == "random"].drop("w_type", axis = "columns")

    degree_data = melt(degree_data).groupby(['alpha', 'measure']).mean().reset_index()
    random_data = melt(random_data).groupby(['alpha', 'measure']).mean().reset_index()
    print(degree_data)
    fig, axs = plt.subplots(1, 2)
    fig.set_size_inches(12, 5)
    axs[0].set_title("Degree Weights")
    axs[1].set_title("Random Weights")

    sns.lineplot(x="alpha", y="value", hue="measure",
                 data=degree_data, ax=axs[0])
    sns.lineplot(x="alpha", y="value", hue="measure",
                 data=random_data, ax=axs[1])

    fig.savefig("weight_comparison.png")


# for i in range(100): build_data()
plot_graphs()