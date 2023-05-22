import csv
import numpy as np
import matplotlib.pyplot as plt
from LDP.estimation_different_grid import GRR_estimated_guess, RAPPOR_estimated_guess, OUE_estimated_guess, \
    OLH_estimated_guess, GRR_advance_estimated_guess, RAPPOR_advance_estimated_guess, OUE_advance_estimated_guess, \
    OLH_advance_estimated_guess

# Parameters for simulation
k = 20  # attribute's domain size (grid size)
epsilon_list = [0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 5]  # number of epsilon for test cases
users_grid_value_list = list()
probability_of_guess_grr_plain = list()
probability_of_guess_grr_trained = list()
probability_of_guess_rappor = list()
probability_of_guess_oue = list()
probability_of_guess_olh = list()


with open('../../grid/taxi_test_different_grid.dat') as f:
    reader = csv.reader(f, delimiter="\t")
    for line in reader:
        grid_list = line[0].split(" ")
        grid_list_int = [eval(i) for i in grid_list]
        grid_list_int_nd = np.array(grid_list_int)
        users_grid_value_list.append(grid_list_int_nd)


for epsilon in epsilon_list:

    print("Epsilon Value: " + str(epsilon))
    probability_of_guess_grr_plain.append(GRR_advance_estimated_guess(users_grid_value_list, k, epsilon, 3))
    print("GRR is Ready")
    probability_of_guess_rappor.append(RAPPOR_advance_estimated_guess(users_grid_value_list, k, epsilon, 3))
    print("RAPPOR is Ready")
    probability_of_guess_oue.append(OUE_advance_estimated_guess(users_grid_value_list, k, epsilon, 3))
    print("OUE is Ready")
    probability_of_guess_olh.append(OLH_advance_estimated_guess(users_grid_value_list, k, epsilon))
    print("OLH is Ready")

print(probability_of_guess_olh)

plt.rcParams.update({'font.size': 12})
plt.figure(figsize=(4 * 1.33, 4 * 1.33))
plt.plot(epsilon_list, probability_of_guess_grr_plain, linewidth=2, color='purple', marker='o', markersize=10, mew=1.5, fillstyle='none', clip_on=False, label="GRR")
plt.plot(epsilon_list, probability_of_guess_rappor, linewidth=2, color='grey', marker='s', markersize=10, mew=1.5, fillstyle='none', clip_on=False, label="RAPPOR")
plt.plot(epsilon_list, probability_of_guess_oue, linewidth=2, color='blue', marker='x', markersize=10, mew=1.5, fillstyle='none', clip_on=False, label="OUE")
plt.plot(epsilon_list, probability_of_guess_olh, linewidth=2, color='green', marker='d', markersize=10, mew=1.5, fillstyle='none', clip_on=False, label="OLH")
plt.ylim(0, 1)
plt.xticks(fontsize=15)
plt.ylabel("Ratio Of Guess")
plt.xlabel('Epsilon Values')
plt.grid(linestyle=':')
plt.legend(prop={'size': 12}, ncol=2, columnspacing=0.75)
plt.savefig('expected-sr-vs-U.png', format='png', dpi=300, bbox_inches='tight')
plt.show()