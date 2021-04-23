import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

def get_new_df():
    with open("LTM/new_alg_data.csv", "r", encoding='utf-8-sig') as data:
        d = data.read()

    d = d.split("\n")
    d = [l.split(",") for l in d]

    df = pd.DataFrame(data=d[1::], columns=d[0])
    for col in df.columns:
        df[col] = df[col].astype(float)

    main_data = df.loc[df.mc_greedy == 1000]
    return main_data

def plot_random_weights(main_data):
    main_data = main_data.melt(id_vars=["n", "p_e", "alpha", "mc_greedy", "k"],
              var_name="algorithm", value_name="influence")

    # main_data = main_data.drop("p_e", axis="columns").groupby(['alpha', 'algorithm']).mean().reset_index()


    low_p = main_data.loc[main_data.p_e == 0.1].groupby(['alpha','algorithm']).mean().reset_index()
    high_p = main_data.loc[main_data.p_e == 0.2].groupby(['alpha','algorithm']).mean().reset_index()

    sns.set_theme(style="darkgrid")
    sns.lineplot(x="alpha", y="influence", hue="algorithm",
                 data=low_p)
    # sns.lineplot(x="alpha", y = "influence", hue="algorithm", data = main_data, ax = ax)

    # ax.legend(loc=2)


plt.title("Random Weights with new algorithms")
main_data = get_new_df()
plot_random_weights(main_data)
plt.savefig("new_algs_plot.png")