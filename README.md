
# Inference Attack On Location Data


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
| Plain Attack       | :white_check_mark:           | :white_check_mark:  |
| Chain Attack       | :white_check_mark:           | :x:             |
| Inference Attack   | :white_check_mark:           | :x:             |

### Dataset 

| Dataset            | Plain Attack on Stationary Dataset | Statistical Inferences with Mode Attack on Transit Dataset |
| ------------------ | ----------------------------------- | ------------------------------------------------------- |
| Taxi Dataset       | :x:                                 | :x:                                                     |
| Geolife Dataset    | :x:                                 | :x:                                                     |
| Brinkoff Dataset   | :x:                                 | :x:                                                     |
