import argparse, os, sys, errno
import numpy as np

import measures, loader

# import plotting
import plot_accuracy
import plot_alpha_learn
import plot_mlted
import plot_alpha_mse
import plot_pscore

parser = argparse.ArgumentParser(description='plot figures', add_help=True)
parser.add_argument('--ground', action='store', type=str, required=True,
                    help='path of the ground folder')
parser.add_argument('--tools', action='store', nargs='+', required=True,
                    help='path of the tools\' folders')
parser.add_argument('--names', action='store', nargs='+', required=True,
                    help='names of the tools')
parser.add_argument('--exp', action='store', type=int, required=True,
                    help='experiment number')
parser.add_argument('--mutations', action='store', type=int, required=True,
                    help='number of mutations')
parser.add_argument('-o', '--outdir', action='store', type=str, required=True,
                    help='output directory.')

parser.add_argument('--simulations', action='store', type=int, default=50,
                    help='number of simulation')

args = parser.parse_args()

file_loaders = [
    loader.load_from_sasc,
    loader.load_from_scite,
    loader.load_from_sifit,
    loader.load_from_sphyr,
]

t_file_formats = [
    '%s/sim_%d_scs_mlt.gv', #SASC
    '%s/sim_%d_scs_ml0.gv', #SCITE
    '%s/sim_%d_scs.gv', #SiFit
    '%s/sim_%d_scs.gv', #Sphyr
]

m_file_formats = [
    '%s/sim_%d_scs_out.txt', #SASC
    '%s/sim_%d_scs_out.txt', #SCITE
    '%s/sim_%d_scs_out.txt', #SIFIT
    '%s/sim_%d_scs_out.txt', #SPHYR
]

def get_filepaths(args):
    ground_dir = args.ground
    tools_dirs = args.tools

    ground_trees = list()
    tools_trees = list()
    for t in tools_dirs:
        tools_trees.append([])

    for sim_id in range(1, args.simulations + 1):
        ground_file = '%s/sim_%d_truetree.gv' % (ground_dir, sim_id)
        ground_trees.append(ground_file)

        for idx, tool_dir in enumerate(tools_dirs):
            tool_file = t_file_formats[idx] % (tool_dir, sim_id)
            tools_trees[idx].append(tool_file)

    return [ground_trees, tools_trees]

def load_trees(args):
    ground_dir = args.ground
    tools_dirs = args.tools

    ground_trees = list()
    tools_trees = list()
    for t in tools_dirs:
        tools_trees.append([])

    for sim_id in range(1, args.simulations + 1):
        ground_file = '%s/sim_%d_truetree.gv' % (ground_dir, sim_id)
        ground_trees.append(loader.load_from_ground(ground_file))

        for idx, tool_dir in enumerate(tools_dirs):
            tool_file = t_file_formats[idx] % (tool_dir, sim_id)
            tools_trees[idx].append(file_loaders[idx](tool_file))

    return [ground_trees, tools_trees]


def load_matrices(args):
    ground_dir = args.ground
    tools_dirs = args.tools

    ground_mat = list()
    noisy_mat = list()
    tools_mat = list()
    for t in tools_dirs:
        tools_mat.append([])

    for sim_id in range(1, args.simulations + 1):
        ground_file = '%s/sim_%d_truescs.txt' % (ground_dir, sim_id)
        ground_mat.append(np.genfromtxt(ground_file, delimiter=' ', dtype=int))

        noisy_file = '%s/sim_%d_scs.txt' % (ground_dir, sim_id)
        noisy_mat.append(np.genfromtxt(noisy_file, delimiter=' ', dtype=int))

        for idx, tool_dir in enumerate(tools_dirs):
            tool_file = m_file_formats[idx] % (tool_dir, sim_id)
            tools_mat[idx].append(np.genfromtxt(tool_file, delimiter=' ', dtype=int))

    return [ground_mat, noisy_mat, tools_mat]

if __name__ == '__main__':
    try:
        os.makedirs(args.outdir)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(args.outdir):
            pass
        else:
            raise

    print('='*50)
    print('Loading files')
    ground_trees, tools_trees = load_trees(args)
    ground_mat, noisy_mat, tools_mat = load_matrices(args)
    ground_tfiles, tools_tfiles = get_filepaths(args)
    

    print('='*50)
    print('Computing tree accuracies')
    # plot_accuracy.plot_accuracy(ground_trees, tools_trees, args.names, 
    #     args.mutations, args.simulations, args.exp, args.outdir)

    # print('='*50)
    # print('Computing FN learn accuracy')
    # plot_alpha_learn.plot_alpha_learn(ground_mat, noisy_mat, tools_mat, args.names,
    #     args.mutations, args.simulations, args.exp, args.outdir)

    # print('='*50)
    # print('Computing MLTED')
    # plot_mlted.plot_mlted(ground_trees, tools_trees, args.names, 
    #     args.mutations, args.simulations, args.exp, args.outdir)
    
    # print('='*50)
    # print('Computing MSE')
    # plot_alpha_mse.plot_alpha_mse(ground_mat, noisy_mat, tools_mat, args.names,
    #     args.mutations, args.simulations, args.exp, args.outdir)

    # print('='*50)
    # print('Computing pscores')
    # plot_pscore.plot_pscore(ground_mat, noisy_mat, tools_mat, args.names,
    #     args.mutations, args.simulations, args.exp, args.outdir, 
    #     drop=['SiFit'])

    print('cacca')
    print(ground_tfiles, tools_tfiles)