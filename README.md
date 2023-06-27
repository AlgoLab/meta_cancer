# Supporting repository for "Three Metaheuristic Approaches for Tumor Phylogeny Inference"

## Reproduce Experiments 1-6

Run all the tools

```bash
bash runall.sh # for alpha=0.15
bash runall.fn20.sh # for alpha=0.20
```

Compute the distances

```bash
bash csv.sh # for alpha=0.15
bash csv.fn20.sh # for alpha=0.20
```

## Reproduce Experiment 7

This requires more time and runs only SASC and PSO

```bash
bash runall.large.sh
bash csv.large.sh
```

## Plotting Experiments 1-7

Make the plots using `results.ipynb`
