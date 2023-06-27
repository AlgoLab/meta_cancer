#!/bin/bash

set -xe

python comparison/plotting/make.py  \
--tground simulations/exp_m15_n50_pp_fn20/sim_*_truetree.gv  \
--tloaders sasc pso ea ea \
--ttools results/sasc/exp_m15_n50_pp_fn20/sim_*.sasc.mlt.gv  \
--ttools results/pso/exp_m15_n50_pp_fn20/sim_*.pso.best.gv  \
--ttools results/gp/exp_m15_n50_pp_fn20/sim_*.gp.gv  \
--ttools results/vns/exp_m15_n50_pp_fn20/sim_*.vns.gv  \
--names SASC pso gp vns \
--mutations 15 \
--exp exp_m15_n50_pp_fn20 -o csvs

python comparison/plotting/make.py  \
--tground simulations/exp_m15_n50_k3_fn20/sim_*_truetree.gv  \
--tloaders sasc pso ea ea \
--ttools results/sasc/exp_m15_n50_k3_fn20/sim_*.sasc.mlt.gv  \
--ttools results/pso/exp_m15_n50_k3_fn20/sim_*.pso.best.gv  \
--ttools results/gp/exp_m15_n50_k3_fn20/sim_*.gp.gv  \
--ttools results/vns/exp_m15_n50_k3_fn20/sim_*.vns.gv  \
--names SASC pso gp vns \
--mutations 15 \
--exp exp_m15_n50_k3_fn20 -o csvs


python comparison/plotting/make.py  \
--tground simulations/exp_m30_n100_pp_fn20/sim_*_truetree.gv  \
--tloaders sasc pso ea ea \
--ttools results/sasc/exp_m30_n100_pp_fn20/sim_*.sasc.mlt.gv  \
--ttools results/pso/exp_m30_n100_pp_fn20/sim_*.pso.best.gv  \
--ttools results/gp/exp_m30_n100_pp_fn20/sim_*.gp.gv  \
--ttools results/vns/exp_m30_n100_pp_fn20/sim_*.vns.gv  \
--names SASC pso gp vns \
--mutations 30 \
--exp exp_m30_n100_pp_fn20 -o csvs

python comparison/plotting/make.py  \
--tground simulations/exp_m30_n100_k3_fn20/sim_*_truetree.gv  \
--tloaders sasc pso ea ea \
--ttools results/sasc/exp_m30_n100_k3_fn20/sim_*.sasc.mlt.gv  \
--ttools results/pso/exp_m30_n100_k3_fn20/sim_*.pso.best.gv  \
--ttools results/gp/exp_m30_n100_k3_fn20/sim_*.gp.gv  \
--ttools results/vns/exp_m30_n100_k3_fn20/sim_*.vns.gv  \
--names SASC pso gp vns \
--mutations 30 \
--exp exp_m30_n100_k3_fn20 -o csvs



python comparison/plotting/make.py  \
--tground simulations/exp_m50_n200_pp_fn20/sim_*_truetree.gv  \
--tloaders sasc pso ea ea \
--ttools results/sasc/exp_m50_n200_pp_fn20/sim_*.sasc.mlt.gv  \
--ttools results/pso/exp_m50_n200_pp_fn20/sim_*.pso.best.gv  \
--ttools results/gp/exp_m50_n200_pp_fn20/sim_*.gp.gv  \
--ttools results/vns/exp_m50_n200_pp_fn20/sim_*.vns.gv  \
--names SASC pso gp vns \
--mutations 50 \
--exp exp_m50_n200_pp_fn20 -o csvs

python comparison/plotting/make.py  \
--tground simulations/exp_m50_n200_k3_fn20/sim_*_truetree.gv  \
--tloaders sasc pso ea ea \
--ttools results/sasc/exp_m50_n200_k3_fn20/sim_*.sasc.mlt.gv  \
--ttools results/pso/exp_m50_n200_k3_fn20/sim_*.pso.best.gv  \
--ttools results/gp/exp_m50_n200_k3_fn20/sim_*.gp.gv  \
--ttools results/vns/exp_m50_n200_k3_fn20/sim_*.vns.gv  \
--names SASC pso gp vns \
--mutations 50 \
--exp exp_m50_n200_k3_fn20 -o csvs

for d in "m15_n50_pp_fn20" "m15_n50_k3_fn20" "m30_n100_pp_fn20" "m30_n100_k3_fn20" "m50_n200_pp_fn20" "m50_n200_k3_fn20"
do
    python comparison/csv.times.py exp_$d > csvs/exp_$d.times.csv
done
