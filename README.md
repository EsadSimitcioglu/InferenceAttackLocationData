
# Inference Attack On Location Data

## Environment

This repository now includes a `uv` project definition in [pyproject.toml](/Users/esatsimitcioglu/Desktop/InferenceAttackLocationData/pyproject.toml).

Typical setup:

```bash
uv sync
uv run python results_with_plots.py
```


## Experiments

### Stationary Experiment

| Stationary Experiment                   | Estimation Percentage Metric |
| --------------------------------------- | ---------------------------- |
| Statistical Inferences with Mode Attack | :white_check_mark:           |

### Transit Experiment

| Iteration Experiment       | Estimation Percentage Metric |
| ---------------------      | ---------------------------- |
| Optimal $\alpha$           | :white_check_mark:           |

| Transit Experiment | Estimation Percentage Metric | Path Metric   |
| ------------------ | ---------------------------- | ------------- |
| Plain Attack       | :white_check_mark:           | :white_check_mark:            |
| Chain Attack       | :white_check_mark:           | :white_check_mark:           |
| Inference Attack   | :white_check_mark:           | :white_check_mark:            |

### Dataset 

| Dataset            | Plain Attack on Stationary Dataset | Statistical Inferences with Mode Attack on Transit Dataset |
| ------------------ | ----------------------------------- | ------------------------------------------------------- |
| Taxi Dataset       | :white_check_mark:                                 | :white_check_mark:                                                     |
| Geolife Dataset    | :white_check_mark:                                 | :white_check_mark:                                                     |
| Brinkoff Dataset   | :white_check_mark:                                 | :white_check_mark:                                                     |
