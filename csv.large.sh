#!/bin/bash

set -xe

python comparison/plotting/make.py  \
--tground simulations/exp_m100_n200_k3/sim_*_truetree.gv  \
--tloaders sasc pso \
--ttools results/sasc/exp_m100_n200_k3/sim_*.sasc.mlt.gv  \
--ttools results/pso/exp_m100_n200_k3/sim_*.pso.best.gv  \
--names SASC pso  \
--mutations 100 \
--exp exp_m100_n200_k3 -o csvs

python comparison/plotting/make.py  \
--tground simulations/exp_m200_n200_k3/sim_*_truetree.gv  \
--tloaders sasc pso \
--ttools results/sasc/exp_m200_n200_k3/sim_*.sasc.mlt.gv  \
--ttools results/pso/exp_m200_n200_k3/sim_*.pso.best.gv  \
--names SASC pso \
--mutations 200 \
--exp exp_m200_n200_k3 -o csvs

for d in "m100_n200_k3" "m200_n200_k3"
do
    python comparison/csv.times.py exp_$d > csvs/exp_$d.times.csv
done
