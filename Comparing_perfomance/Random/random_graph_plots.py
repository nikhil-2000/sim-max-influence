import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as tkr



with open("ICM/data.csv", "r", encoding='utf-8-sig') as data:
    d = data.read()

d = d.split("\n")
d = [l.split(",") for l in d]

df = pd.DataFrame(data=d[1::], columns=d[0])
for col in df.columns:
    df[col] = df[col].astype(float)

main_data = df.loc[df.mc_greedy == 1000]

def plot_random_weights(main_data):
    main_data = main_data.loc[df.random_weights == True]

    low_p = main_data.loc[df.p_e == 0.1] \
        .melt(id_vars=["n", "p_e", "alpha", "mc_greedy", "k"],
              var_name="algorithm", value_name="influence")

    high_p = main_data.loc[df.p_e == 0.2] \
        .melt(id_vars=["n", "p_e", "alpha", "mc_greedy", "k"],
              var_name="algorithm", value_name="influence")

    sns.set_theme(style="darkgrid")
    sns.lineplot(x="alpha", y="influence", hue="algorithm",
                 data=low_p)
    sns.lineplot(x="alpha", y="influence", hue="algorithm",
                 style='algorithm', dashes=[(2, 2), (2, 2), (2, 2)],
                 data=high_p)
    plt.savefig("random_comparison_plot")

def plot_degree_weights(main_data):
    main_data = main_data.loc[df.random_weights == False]

    dfs = []
    p_e = [0.1,.2,.3]

    for p in p_e:
        df_p = main_data.loc[df.p_e == p] \
            .melt(id_vars=["n", "p_e", "alpha", "mc_greedy", "k", "random_weights"],
                  var_name="algorithm", value_name="influence")

        df_p = df_p.groupby("algorithm").mean()
        df_p.reset_index(level=0, inplace=True)

        dfs.append(df_p)

    all_data = pd.concat(dfs)

    # fig, ax1 = plt.subplots(figsize=(10, 4))
    plt.rcParams["xtick.labelsize"] = 3

    sns.set_theme(style="darkgrid")
    sns.catplot(x="p_e", y="influence", hue="algorithm",
                 data=all_data,kind="bar" ,legend=False)
    plt.legend(loc='upper right')
    plt.xticks(
        rotation=0,
        fontweight='light',
        ticks=[0,1],
        labels=["0.1","0.2"]
    )
    print(all_data)
    plt.show()


plot_degree_weights(main_data)
