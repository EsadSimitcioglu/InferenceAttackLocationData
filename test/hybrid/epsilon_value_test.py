import csv

import numpy as np
import matplotlib.pyplot as plt

from LDP.estimation_same_grid import grr_estimated_guess, rappor_estimated_guess, oue_estimated_guess, \
    olh_estimated_guess
from LDP.estimation_hybrid_grid import grr_estimated_guess_hybrid
from LDP.estimation_different_grid import GRR_advance_estimated_guess

# Parameters for simulation
n = 20  # number of timestamps
k = 20  # attribute's domain size (grid size)
epsilon_list = [0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 5]  # number of epsilon for test cases
users_grid_value_list = list()
probability_of_guess_grr_hybrid = list()
probability_of_guess_grr_different = list()
probability_of_guess_grr_same = list()
probability_of_guess_rappor = list()
probability_of_guess_oue = list()
probability_of_guess_olh = list()

with open('../../grid/geolife.dat') as f:
    reader = csv.reader(f, delimiter="\t")
    for line in reader:
        grid_list = line[0].split(" ")
        grid_list_int = [eval(i) for i in grid_list]
        grid_list_int_nd = np.array(grid_list_int)
        users_grid_value_list.append(grid_list_int_nd)

for epsilon in epsilon_list:
    print("Epsilon Value Is: " + str(epsilon))
    temp_probability_of_guess_grr = list()
    temp_probability_of_guess_rappor = list()
    temp_probability_of_guess_oue = list()
    temp_probability_of_guess_olh = list()

    grr_est_freq_hybrid = grr_estimated_guess_hybrid(users_grid_value_list, k, epsilon, 5)
    probability_of_guess_grr_hybrid.append(grr_est_freq_hybrid)

    grr_est_freq_different = GRR_advance_estimated_guess(users_grid_value_list, k, epsilon, 3)
    probability_of_guess_grr_different.append(grr_est_freq_different)

    grr_est_freq_same = grr_estimated_guess(users_grid_value_list, k, epsilon)
    probability_of_guess_grr_same.append(grr_est_freq_same)


plt.rcParams.update({'font.size': 12})
plt.figure(figsize=(4 * 1.33, 4 * 1.33))
plt.plot(epsilon_list, probability_of_guess_grr_same, linewidth=2, color='purple', marker='o', markersize=10, mew=1.5,
         fillstyle='none', clip_on=False, label="GRR-Same")
plt.plot(epsilon_list, probability_of_guess_grr_different, linewidth=2, color='grey', marker='o', markersize=10, mew=1.5,
         fillstyle='none', clip_on=False, label="GRR-Different")
plt.plot(epsilon_list, probability_of_guess_grr_hybrid, linewidth=2, color='blue', marker='o', markersize=10, mew=1.5,
         fillstyle='none', clip_on=False, label="GRR-Hybrid")
plt.ylim(0, 1)
plt.xticks(fontsize=15)
plt.ylabel("Ratio Of Guess")
plt.xlabel('Epsilon Values')
plt.grid(linestyle=':')
plt.legend(prop={'size': 12}, ncol=2, columnspacing=0.75)
plt.savefig('expected-sr-vs-U.png', format='png', dpi=300, bbox_inches='tight')
plt.show()
