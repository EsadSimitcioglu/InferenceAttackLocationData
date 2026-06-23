# [Privacy risks of continuous location sharing under local differential privacy: Inference attacks and defenses]

Official implementation for the published paper:

> **[Privacy risks of continuous location sharing under local differential privacy: Inference attacks and defenses]**  
> [Muhammed Esad Simitcioglu], [Emre Gursoy], [Author 3]  
> *[Computer Networks]*, [2026/4/23]

[`Paper link`](https://doi.org/10.1016/j.comnet.2026.112333)

## Abstract

This repository contains the code, datasets, and experiment scripts used in our paper on inference attacks against locally differentially private location trajectories. It includes implementations of several local differential privacy protocols, Hidden Markov Model based reconstruction, and the experiment pipelines used to evaluate attack performance under different privacy budgets and threat settings.

If you use this repository in your research, please cite the paper listed below.

## Repository Contents

```text
.
├── dataset/                 Preprocessed trajectory datasets
│   ├── geolife/
│   ├── taxi/
│   └── brinkhoff/
├── experiment/
│   ├── attack/              Attack implementations and evaluation metrics
│   └── defence/             Defense-oriented experiments
├── hidden_markov_model/     HMM-based reconstruction code
├── LDP/                     LDP protocol implementations
├── run/
│   ├── same_grid/           Stationary-user experiments
│   └── different_grid/      Trajectory inference experiments
├── pyproject.toml           Python project metadata
└── uv.lock                  Locked dependency versions
```

## Implemented Methods

This codebase includes implementations of the following mechanisms and attack components:

- `GRR` - Generalized Randomized Response
- `RAPPOR`
- `OUE` - Optimized Unary Encoding
- `OLH` - Optimized Local Hashing
- `HMM` - Hidden Markov Model based trajectory reconstruction

## Environment

The project is configured for:

- Python `>=3.9,<3.10`
- `numpy`, `scipy`, `scikit-learn`
- `matplotlib`, `pandas`, `pillow`
- `shapely`, `xxhash`, `hmmlearn`, `pybind11`

## Installation

### Option 1: `uv`

```bash
uv sync
```

### Option 2: `pip`

```bash
python3.9 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -e .
```

## Datasets

The repository currently includes preprocessed grid-based trajectory files for:

- `Geolife` at `dataset/geolife/geolife_grid.dat`
- `Taxi` at `dataset/taxi/taxi_grid.dat`
- `Brinkhoff` at `dataset/brinkhoff/brinkhoff_grid.dat`

Each line in these files represents one user trajectory encoded as space-separated grid identifiers.

## Reproducing the Main Experiments

The provided scripts sweep privacy budget values `epsilon = {0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 5.0}` over a grid size of `k = 20`.

### 1. Stationary-user attack experiment

Run from the experiment directory so relative dataset paths resolve correctly:

```bash
cd run/same_grid
python epsilon_value_test.py
```

This script evaluates the stationary-user setting using `GRR`, `RAPPOR`, `OUE`, and `OLH`, and saves a plot such as `geolife.png` in the same directory.

### 2. Trajectory inference experiment

```bash
cd run/different_grid
python epsilon_value_test.py
```

This script evaluates trajectory reconstruction with HMM-based inference and writes a figure such as `plot.png` in the same directory.

## Evaluation Metrics

The attack code supports the following metrics:

- `PA` - Prediction Accuracy
- `NDE` - Normalized Distance Error

See [experiment/attack/metrics.py](/Users/esatsimitcioglu/Desktop/InferenceAttackLocationData/experiment/attack/metrics.py) for the metric definitions used by the implementation.

## Reproducibility Notes

- The repository includes the preprocessed datasets used by the experiments.
- Dependency versions are pinned in [pyproject.toml](/Users/esatsimitcioglu/Desktop/InferenceAttackLocationData/pyproject.toml) and [uv.lock](/Users/esatsimitcioglu/Desktop/InferenceAttackLocationData/uv.lock).
- The experiment scripts currently default to the `Geolife` dataset, but the dataset paths in the scripts can be changed to run the same pipeline on `Taxi` or `Brinkhoff`.

## Citation

```bibtex
@article{SIMITCIOGLU2026112333,
title = {Privacy risks of continuous location sharing under local differential privacy: Inference attacks and defenses},
journal = {Computer Networks},
volume = {284},
pages = {112333},
year = {2026},
issn = {1389-1286},
doi = {https://doi.org/10.1016/j.comnet.2026.112333},
url = {https://www.sciencedirect.com/science/article/pii/S1389128626003452},
author = {Muhammed Esad Simitçioğlu and M. Emre Gürsoy},
keywords = {Local differential privacy, Location privacy, Inference attacks, Location-based services (LBS), Hidden Markov models, Internet of Things},
abstract = {Local differential privacy (LDP) has recently emerged as a widely adopted standard for privacy-preserving data collection in IoT, including location data and location-based services (LBS). However, in many practical applications, users need to share their location continuously, which creates temporal correlations that can be exploited by adversaries although individual locations are protected by LDP. In this paper, we propose novel inference attacks that exploit these correlations to compromise users’ privacy under continuous location sharing. We develop attacks in two categories: statistical attacks based on Bayesian adversary formulation targeting near-stationary users and Hidden Markov Model (HMM) based attacks targeting mobile users. We further propose two extensions for our HMM-based attacks: informed attacks, which leverage aggregate population statistics, and chain attacks, which apply multiple iterations of HMM construction. We adapt and apply our attacks to four popular LDP protocols (GRR, RAPPOR, OUE, OLH), three datasets, and varying privacy levels. Experiments show that our attacks are effective, highlighting the privacy risks of correlations in continuous location sharing under LDP. Furthermore, we observe that statistical attacks are indeed more effective on stationary users, whereas HMM-based attacks are more effective on mobile users. Finally, we propose three defense strategies to mitigate the risks: Memoization, Replay, and Replication, and experimentally show that the defenses successfully reduce attack effectiveness. We critically analyze the success, efficiency, and utility aspects of the three defenses by considering varying IoT conditions and provide recommendations regarding when to use which defense.}
}
```

## Contact

For questions about the paper or implementation, please open an issue in this repository or contact the corresponding author:

- `[Muhammed Esad Simitcioglu]` - `[esadsimitcioglu@gmail.com]`

