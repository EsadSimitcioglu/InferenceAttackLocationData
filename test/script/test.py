import csv
import numpy as np
import sys
from LDP.estimation_different_grid import GRR_FK_estimated_guess, RAPPOR_FK_estimated_guess, OUE_FK_estimated_guess, OLH_FK_estimated_guess


method_name_list = ['GRR', 'RAPPOR', 'OUE', 'OLH']
method_func_list = [GRR_FK_estimated_guess, RAPPOR_FK_estimated_guess, OUE_FK_estimated_guess, OLH_FK_estimated_guess]

dataset_file = "taxi.dat"
method_name = "GRR"
method = method_name_list.index(method_name)


user_grid_value_list = []
probability_of_guess = []

with open(dataset_file) as f:
    reader = csv.reader(f, delimiter='\t')
    for line in reader:
        grid_list = line[0].split(" ")
        grid_list_int = [int(i) for i in grid_list]
        grid_list_int_nd = np.array(grid_list_int)
        user_grid_value_list.append(grid_list_int_nd)

for epsilon in [0.1, 0.5, 1, 2, 5]:
    probability_of_guess = method_func_list[method](user_grid_value_list, 20, epsilon, 'guess')

    with open(dataset_file.replace("_",".").split(".")[0] + "-" + method_name + "-" + str(epsilon) + "_FK_guess.csv", "w+") as f:
        f.write(dataset_file.replace("_",".").split(".")[0] + "_FK_guess" + "\n")
        f.write(str(probability_of_guess) + "\n")
        f.flush()

