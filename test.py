# Parameters for simulation
import csv

import numpy as np

from LDP.protocols_estimation_different_grid import grr_estimated_guess

k = 20  # attribute's domain size (grid size)
epsilon_list = [0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 5]  # number of epsilon for test cases
users_grid_value_list = list()
probability_of_guess_grr_plain = list()
probability_of_guess_grr_trained = list()
probability_of_guess_rappor = list()
probability_of_guess_oue = list()
probability_of_guess_olh = list()


with open('grid/taxi.dat') as f:
    reader = csv.reader(f, delimiter="\t")
    for line in reader:
        grid_list = line[0].split(" ")
        grid_list_int = [eval(i) for i in grid_list]
        grid_list_int_nd = np.array(grid_list_int)
        users_grid_value_list.append(grid_list_int_nd)


for epsilon in epsilon_list:
    probability_of_guess_grr_plain.append(grr_estimated_guess(users_grid_value_list, k, epsilon, "plain"))
    probability_of_guess_grr_trained.append(grr_estimated_guess(users_grid_value_list, k, epsilon, "trained"))