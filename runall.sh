#!/bin/bash
set -xe

snakemake -s simulate.smk --configfiles exp_m15_n50_pp.yaml -c16 -p
snakemake -s simulate.smk --configfiles exp_m15_n50_k3.yaml -c16 -p

snakemake -s simulate.smk --configfiles exp_m30_n100_pp.yaml -c16 -p
snakemake -s simulate.smk --configfiles exp_m30_n100_k3.yaml -c16 -p

snakemake -s simulate.smk --configfiles exp_m50_n200_pp.yaml -c16 -p
snakemake -s simulate.smk --configfiles exp_m50_n200_k3.yaml -c16 -p

