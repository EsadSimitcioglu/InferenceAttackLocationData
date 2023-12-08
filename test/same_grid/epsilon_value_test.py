import csv

import numpy as np
import matplotlib.pyplot as plt

from experiment.attack.stationary.guess_trajectory import grr_estimated_guess, rappor_estimated_guess, oue_estimated_guess, \
    olh_estimated_guess

# Parameters for simulation
n = 20  # number of timestamps
k = 20  # attribute's domain size (grid size)
epsilon_list = [0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 5]  # number of epsilon for test cases
users_grid_value_list = list()
probability_of_guess_grr = list()
probability_of_guess_rappor = list()
probability_of_guess_oue = list()
probability_of_guess_olh = list()

with open('../../dataset/geolife/geolife_stationary_grid.dat') as f:
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

    grr_est_freq = grr_estimated_guess(users_grid_value_list, k, epsilon)
    temp_probability_of_guess_grr.append(grr_est_freq)

    rappor_est_freq = rappor_estimated_guess(users_grid_value_list, k, epsilon)
    temp_probability_of_guess_rappor.append(rappor_est_freq)

    oue_est_freq = oue_estimated_guess(users_grid_value_list, k, epsilon)
    temp_probability_of_guess_oue.append(oue_est_freq)

    olh_est_freq = olh_estimated_guess(users_grid_value_list, k, epsilon)
    temp_probability_of_guess_olh.append(olh_est_freq)

    probability_of_guess_grr.append(sum(temp_probability_of_guess_grr) / len(temp_probability_of_guess_grr))
    probability_of_guess_rappor.append(sum(temp_probability_of_guess_rappor) / len(temp_probability_of_guess_rappor))
    probability_of_guess_oue.append(sum(temp_probability_of_guess_oue) / len(temp_probability_of_guess_oue))
    probability_of_guess_olh.append(sum(temp_probability_of_guess_olh) / len(temp_probability_of_guess_olh))


print("Probability Of Guess For GRR: " + str(probability_of_guess_grr))
print("Probability Of Guess For RAPPOR: " + str(probability_of_guess_rappor))
print("Probability Of Guess For OUE: " + str(probability_of_guess_oue))
print("Probability Of Guess For OLH: " + str(probability_of_guess_olh))


plt.rcParams.update({'font.size': 12})
plt.figure(figsize=(4 * 1.33, 4 * 1.33))
plt.title("Geolife")
plt.plot(epsilon_list, probability_of_guess_grr, linewidth=2, color='purple', marker='o', markersize=10, mew=1.5, fillstyle='none', clip_on=False, label="GRR")
plt.plot(epsilon_list, probability_of_guess_rappor, linewidth=2, color='grey', marker='s', markersize=10, mew=1.5, fillstyle='none', clip_on=False, label="RAPPOR")
plt.plot(epsilon_list, probability_of_guess_oue, linewidth=2, color='blue', marker='x', markersize=10, mew=1.5, fillstyle='none', clip_on=False, label="OUE")
plt.plot(epsilon_list, probability_of_guess_olh, linewidth=2, color='green', marker='d', markersize=10, mew=1.5, fillstyle='none', clip_on=False, label="OLH")
plt.ylim(0, 1)
plt.xticks(fontsize=15)
plt.ylabel("Ratio Of Guess")
plt.xlabel('Epsilon Values')
plt.grid(linestyle=':')
plt.legend(prop={'size': 12}, ncol=2, columnspacing=0.75)
plt.savefig('geolife.png', format='png', dpi=300, bbox_inches='tight')
plt.show()