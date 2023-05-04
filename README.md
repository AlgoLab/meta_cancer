# Supporting repository for "Three Metaheuristic Approaches for Tumor Phylogeny Inference"

## Reproduce the experiments

Run all the tools

```bash
snakemake -s simulate.smk --configfiles exp_m15_n50_pp.yaml -c16 -p
snakemake -s simulate.smk --configfiles exp_m15_n50_k3.yaml -c16 -p

snakemake -s simulate.smk --configfiles exp_m30_n100_pp.yaml -c16 -p
snakemake -s simulate.smk --configfiles exp_m30_n100_k3.yaml -c16 -p

snakemake -s simulate.smk --configfiles exp_m50_n200_pp.yaml -c16 -p
snakemake -s simulate.smk --configfiles exp_m50_n200_k3.yaml -c16 -p
```

Compute the distances

```bash
bash csv.sh
```

Make the plots using `results.ipynb`