import sys
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

import measures, loader
import plotting



def plot_accuracy(ground_trees, tools_trees, tools_names, tot_mutations, tot_simulations, exp, out_folder):

    TOOLS = tools_names

    GROUND_TREES = ground_trees
    TOOLS_TREES = tools_trees

    anc_desc = list()
    
    for idx, tree in enumerate(tools_trees):
        anc_desc.append(
            measures.fast_anc_desc_f1(GROUND_TREES, TOOLS_TREES[idx], tot_mutations)
        )

    # print(anc_desc)
    for idx, name in enumerate(tools_names):
        print("%s -- Anc-Desc: %f" %
            (name, np.mean(anc_desc[idx]))
        )
    print('-'*40)

    # ---------------- Compile Pandas

    anc_desc_np = np.zeros((tot_simulations, len(tools_names)))
    for i in range(tot_simulations):
        for j in range(len(tools_names)):
            anc_desc_np[i][j] = anc_desc[j][i]
    df_anc_dec = pd.DataFrame(anc_desc_np, columns=TOOLS).assign(Measure='Ancestor-Descendant')

    diff_lin = list()
    
    for idx, tree in enumerate(tools_trees):
        diff_lin.append(
            measures.fast_diff_lin_f1(GROUND_TREES, TOOLS_TREES[idx], tot_mutations)
        )

    # print(anc_desc)
    for idx, name in enumerate(tools_names):
        print("%s -- Diff-Lin: %f" %
            (name, np.mean(diff_lin[idx]))
        )
    print('-'*40)

    # ---------------- Compile Pandas

    diff_lin_np = np.zeros((tot_simulations, len(tools_names)))
    for i in range(tot_simulations):
        for j in range(len(tools_names)):
            diff_lin_np[i][j] = diff_lin[j][i]
    df_diff_lin = pd.DataFrame(diff_lin_np, columns=TOOLS).assign(Measure='Different Lineages')

    plotting.plot_ancdesc_and_difflin(df_anc_dec, df_diff_lin, exp, folder=out_folder
        )

    df_anc_dec.to_csv("%s/%s.anc_desc.csv" % (out_folder, exp), index=False)
    df_diff_lin.to_csv("%s/%s.diff_lin.csv" % (out_folder, exp), index=False)    

    

if __name__ == '__main__':
    ACCURACY = True

    EXP = 1
    SIMULATIONS = 50
    MUTATIONS = 30
    EL = True

    # long = '-long'
    long=''

    # bimod = '-bimod'
    bimod=''

    TOOLS = ['SASC', 'SCITE', 'SiFit', 'SPhyR']
    # TOOLS = ['SASC', 'SCITE', 'SiFit']


    GROUND_DIR = 'ground/exp%d%s' % (EXP, bimod)
    if EL:
        # SASC_DIR = 'results/sasc/exp%d-A01' % EXP
        SCITE_DIR = 'results/scite/exp%d-el' % EXP
    else:
        # SASC_DIR = 'results/sasc/exp%d%s' % (EXP, long)
        SCITE_DIR = 'results/scite/exp%d%s' % (EXP, bimod)

    SASC_DIR = 'results/sasc/exp%d%s%s' % (EXP, long, bimod)
    SIFIT_DIR = 'results/sifit/exp%d%s' % (EXP, bimod)
    SPHYR_DIR = 'results/sphyr/exp%d%s' % (EXP, bimod)

    GROUND_TREES = list()
    SASC_TREES = list()
    SCITE_TREES = list()
    SIFIT_TREES = list()
    SPHYR_TREES = list()

    for sim_id in range(1, SIMULATIONS + 1):

        ground_file = '%s/sim_%d_truetree.gv' % (GROUND_DIR, sim_id)
        sasc_file = '%s/sim_%d_scs_mlt.gv' % (SASC_DIR, sim_id)
        scite_file = '%s/sim_%d_scs_ml0.gv' % (SCITE_DIR, sim_id)
        sifit_file = '%s/sim_%d_scs.gv' % (SIFIT_DIR, sim_id)
        sphyr_file = '%s/sim_%d_scs.gv' % (SPHYR_DIR, sim_id)

        GROUND_TREES.append(loader.load_from_ground(ground_file))
        SASC_TREES.append(loader.load_from_sasc(sasc_file))
        SCITE_TREES.append(loader.load_from_scite(scite_file))
        SIFIT_TREES.append(loader.load_from_sifit(sifit_file))
        SPHYR_TREES.append(loader.load_from_sphyr(sphyr_file))



    # ==============
    # 
    # ANCESTOR - DESCENDANT score
    # 
    # ==================================

    anc_desc_sasc = measures.anc_desc_f1(GROUND_TREES, SASC_TREES, MUTATIONS)
    anc_desc_scite = measures.anc_desc_f1(GROUND_TREES, SCITE_TREES, MUTATIONS)
    anc_desc_sifit = measures.anc_desc_f1(GROUND_TREES, SIFIT_TREES, MUTATIONS)
    anc_desc_sphyr = measures.anc_desc_f1(GROUND_TREES, SPHYR_TREES, MUTATIONS)

    print("SASC -- Anc-Desc: %f" % np.mean(anc_desc_sasc))
    print("SCITE -- Anc-Desc: %f" % np.mean(anc_desc_scite))
    print("SiFit -- Anc-Desc: %f" % np.mean(anc_desc_sifit))
    print("SPhyR -- Anc-Desc: %f" % np.mean(anc_desc_sphyr))
    print('-'*40)
    # ---------------- Compile Pandas

    anc_desc_np = np.zeros((SIMULATIONS, 4))
    # anc_desc_np = np.zeros((SIMULATIONS, 3))
    for i in range(SIMULATIONS):
        anc_desc_np[i][0] = anc_desc_sasc[i]
        anc_desc_np[i][1] = anc_desc_scite[i]
        anc_desc_np[i][2] = anc_desc_sifit[i]
        anc_desc_np[i][3] = anc_desc_sphyr[i]

    df_anc_dec = pd.DataFrame(anc_desc_np, columns=TOOLS).assign(Measure='Ancestor-Descendant')

    # ==============
    # 
    # DIFFERENT LINEAGES score
    # 
    # ==================================

    diff_lin_sasc = measures.diff_lineages_f1(GROUND_TREES, SASC_TREES, MUTATIONS)
    diff_lin_scite = measures.diff_lineages_f1(GROUND_TREES, SCITE_TREES, MUTATIONS)
    diff_lin_sifit = measures.diff_lineages_f1(GROUND_TREES, SIFIT_TREES, MUTATIONS)
    diff_lin_sphyr = measures.diff_lineages_f1(GROUND_TREES, SPHYR_TREES, MUTATIONS)

    print("SASC -- Diff Lin: %f" % np.mean(diff_lin_sasc))
    print("SCITE -- Diff Lin: %f" % np.mean(diff_lin_scite))
    print("SiFit -- Diff Lin: %f" % np.mean(diff_lin_sifit))
    print("SPhyR -- Diff Lin: %f" % np.mean(diff_lin_sphyr))

    # ---------------- Compile Pandas

    diff_lin_np = np.zeros((SIMULATIONS, 4))
    # diff_lin_np = np.zeros((SIMULATIONS, 3))
    for i in range(SIMULATIONS):
        diff_lin_np[i][0] = diff_lin_sasc[i]
        diff_lin_np[i][1] = diff_lin_scite[i]
        diff_lin_np[i][2] = diff_lin_sifit[i]
        diff_lin_np[i][3] = diff_lin_sphyr[i]

    df_diff_lin = pd.DataFrame(diff_lin_np, columns=TOOLS).assign(Measure='Different Lineages')


    # ==============
    # 
    # PLOTTING
    # 
    # ==================================
    if EL:
        plotting.plot_ancdesc_and_difflin(df_anc_dec, df_diff_lin, EXP, folder='plots'
                , name_append='_el'
            )
    else:
        plotting.plot_ancdesc_and_difflin(df_anc_dec, df_diff_lin, EXP, folder='plots'
            , name_append='_el' #delete this
        )

    plt.show()