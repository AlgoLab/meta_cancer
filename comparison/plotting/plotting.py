import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

def plot_ancdesc_and_difflin(df_ad, df_dl, exp, folder=None, title=False, name_append=''):
    sns.set(style="whitegrid")

    f, ax = plt.subplots(1, 2, figsize=(6,4))
    ax[0] = sns.boxplot(data=df_ad, ax=ax[0], palette="Set2", linewidth=1.5)
    ax[0] = sns.swarmplot(data=df_ad, ax=ax[0], palette="Set2", alpha=.6, size=4, edgecolor="gray", linewidth=.5)
    ax[0].set(title="Ancestor-Descendant")

    ax[1] = sns.boxplot(data=df_dl, ax=ax[1], palette="Set2", linewidth=1.5)
    ax[1] = sns.swarmplot(data=df_dl, ax=ax[1], palette="Set2", alpha=.6, size=4, edgecolor="gray", linewidth=.5)
    ax[1].set(title="Different Lineages")

    # f.set_title('Exp {0}: Accuracy on tree distance measures'.format(exp), fontsize=12)
    # f.set(ylabel="Accuracy", xlabel="")
    if title:
        f.suptitle('Exp {0}: Accuracy on tree distance measures'.format(exp), fontsize=12)


    plt.tight_layout()

    if folder:
        f.savefig("%s/plot_%s_acc_measures%s.png" % (folder, exp, name_append))
    else:
        f.savefig("plot_%s_acc_measures%s.png" % (exp, name_append))


def plot_pscore(df_pscore, exp, folder=None, title=None, drop=None, name_append=''):
    '''

        example: drop=['SiFit'] or drop=['SCITE', 'Sifit']
    '''
    sns.set(style="whitegrid")

    if drop:
        custom_palette = sns.color_palette("Set2")
        f, ax = plt.subplots(2, 1, figsize=(6,4))

        df_reduced = df_pscore
        for d in drop:
            drop_index = df_reduced.columns.get_loc(d)
            custom_palette.pop(drop_index)
            df_reduced = df_reduced.drop(d, axis=1)
        
        ax[0] = sns.violinplot(data=df_pscore, palette="Set2", linewidth=1.5, cut=1, bw=.2, ax=ax[0])
        
        ax[1] = sns.violinplot(data=df_reduced, palette=custom_palette, linewidth=1.5, cut=1, bw=.2, ax=ax[1])

        if title:
            ax[0].set_title(title, fontsize=12)

    else:
        plt.figure(figsize=(6,4))

        ax = sns.violinplot(data=df_pscore, palette="Set2", linewidth=1.5, cut=1, bw=.2)

        if title:
            ax.set_title(title, fontsize=12)

        f=plt
    
    plt.tight_layout()
    # f.suptitle('Exp {0}: Number of flips '.format(exp_title), fontsize=12)
    if folder:
        f.savefig("%s/plot_exp%d_pscore%s.png" % (folder, exp, name_append))
    else:
        f.savefig("plot_exp%d_pscore%s.png" % (exp, name_append))

def plot_singles_fn_learning(xs, noisy, exp, df_alphas, alpha_text, folder=None, name_append='', title=None):
    '''

        example: alpha_text -> [x_pos, y_pos, label] > [-2, 162, r'$\alpha$']
    '''
    sns.set(style="whitegrid")

    plt.figure(figsize=(6,4))

    ax = sns.lineplot(x=xs, y=noisy, linewidth=2.5, color='red')
    ax.text(*alpha_text, horizontalalignment='left', size='medium', color='red', weight='bold')

    ax = sns.scatterplot(x='index', y='value', hue='tool', data=df_alphas, palette="Set2")

    if title:
        ax.set_title(title, fontsize=12)

    ax.set_xlabel("Simulation", fontsize=10)
    ax.set_ylabel("Number of FNs", fontsize=10)

    handles, labels = ax.get_legend_handles_labels()

    ax.legend(loc='upper left', ncol=2, fontsize=8, handles=handles[1:], labels=labels[1:])


    plt.tight_layout()

    if folder:
        plt.savefig("%s/plot_exp%d_fnlearn%s.png" % (folder, exp, name_append))
    else:
        plt.savefig("plot_exp%d_fnlearn%s.png" % (exp, name_append))

def plot_cenk_dist(df_dist, exp, folder=None, title=None, name_append=''):
    sns.set(style="whitegrid")

    f, ax = plt.subplots(figsize=(6,4))

    sns.boxplot(x="value", y="tool", data=df_dist, palette="Set2", linewidth=1.5)
    # sns.swarmplot(x="value", y="tool", data=df_dist, palette="Set2", alpha=.6, size=4, edgecolor="gray", linewidth=.5)

    # ax.set_title('Exp {0}: Accuracy on tree distance measures'.format(exp), fontsize=12)
    ax.set(ylabel="", xlabel="")
    if title:
        f.suptitle(title, fontsize=12)


    plt.tight_layout()

    if folder:
        f.savefig("%s/plot_exp%d_mlted%s.png" % (folder, exp, name_append))
    else:
        f.savefig("plot_exp%d_mlted%s.png" % (exp, name_append))