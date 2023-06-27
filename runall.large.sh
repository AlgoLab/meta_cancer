#!/bin/bash
set -xe

snakemake -s simulate_large.smk --configfiles exp_m100_n200_k3.yaml -c16 -p
snakemake -s simulate_large.smk --configfiles exp_m200_n200_k3.yaml -c16 -p