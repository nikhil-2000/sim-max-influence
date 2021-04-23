import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as tkr


def get_icm_df():
    with open("ICM/data.csv", "r", encoding='utf-8-sig') as data:
        d = data.read()

    d = d.split("\n")
    d = [l.split(",") for l in d]

    df = pd.DataFrame(data=d[1::], columns=d[0])
    for col in df.columns:
        df[col] = df[col].astype(float)

    main_data = df.loc[df.mc_greedy == 1000]
    return main_data

def get_ltm_df():
    with open("LTM/data.csv", "r", encoding='utf-8-sig') as data:
        d = data.read()

    d = d.split("\n")
    d = [l.split(",") for l in d]

    df = pd.DataFrame(data=d[1::], columns=d[0])
    for col in df.columns:
        df[col] = df[col].astype(float)

    main_data = df.loc[df.mc_greedy == 1000]
    return main_data


def plot_random_weights(main_data, ax):
    ax.set_title("Random Weights")
    main_data = main_data.loc[main_data.random_weights == 1].melt(id_vars=["n", "p_e", "alpha", "mc_greedy", "k", "random_weights"],
              var_name="algorithm", value_name="influence")

    # main_data = main_data.drop("p_e", axis="columns").groupby(['alpha', 'algorithm']).mean().reset_index()


    data = main_data.loc[main_data.p_e == 0.2].groupby(['alpha','algorithm']).mean().reset_index()

    sns.set_theme(style="darkgrid")
    sns.lineplot(x="alpha", y="influence", hue="algorithm",
                 data=data, ax = ax)
    # sns.lineplot(x="alpha", y="influence", hue="algorithm",
    #              style='algorithm', dashes=[(2, 2), (2, 2), (2,2)],
    #              data=high_p, ax = ax)
    # sns.lineplot(x="alpha", y = "influence", hue="algorithm", data = main_data, ax = ax)

    # ax.legend(loc=2)

def plot_degree_weights(main_data, ax):
    ax.set_title("Degree Weights")
    main_data = main_data.loc[main_data.random_weights == 0].melt(
        id_vars=["n", "p_e", "alpha", "mc_greedy", "k", "random_weights"],
        var_name="algorithm", value_name="influence")
    data = main_data.loc[main_data.p_e == 0.2].groupby(['alpha', 'algorithm']).mean().reset_index()
    # high_p = main_data.loc[main_data.p_e == 0.2].groupby(['alpha', 'algorithm']).mean().reset_index()

    sns.set_theme(style="darkgrid")
    sns.lineplot(x="alpha", y="influence", hue="algorithm",
                 data=data, ax = ax)



model = "LTM"

fig,axs = plt.subplots(1,2)
fig.set_size_inches(12, 5)
file_name = ""
if model == "ICM":
    main_data = get_icm_df()
    file_name = "ICM/icm_graph.png"
elif model == "LTM":
    main_data = get_ltm_df()
    file_name = "LTM/ltm_graph.png"

plot_degree_weights(main_data, axs[0])
plot_random_weights(main_data,axs[1])


plt.show()
fig.savefig(file_name)
