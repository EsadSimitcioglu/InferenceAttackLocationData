import csv
import numpy as np
import matplotlib.pyplot as plt
from LDP.estimation_different_grid import GRR_estimated_guess, GRR_advance_estimated_guess

# Parameters for simulation
k = 20  # attribute's domain size (grid size)
epsilon_list = [0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 5]  # number of epsilon for test cases
users_grid_value_list = list()
probability_of_guess_grr_plain = list()
probability_of_guess_grr_advance_1 = list()
probability_of_guess_grr_advance_3 = list()
probability_of_guess_grr_advance_5 = list()
probability_of_guess_grr_advance_10 = list()


with open('../../../../../grid/taxi_test_different_grid.dat') as f:
    reader = csv.reader(f, delimiter="\t")
    for line in reader:
        grid_list = line[0].split(" ")
        grid_list_int = [eval(i) for i in grid_list]
        grid_list_int_nd = np.array(grid_list_int)
        users_grid_value_list.append(grid_list_int_nd)

for epsilon in epsilon_list:
    print("Epsilon Value: " + str(epsilon))
    probability_of_guess_grr_plain.append(GRR_estimated_guess(users_grid_value_list, k, epsilon, 'guess'))
    print("Plain GRR is Ready")
    probability_of_guess_grr_advance_1.append(GRR_advance_estimated_guess(users_grid_value_list, k, epsilon, 1))
    print("Advance GRR is Ready")
    probability_of_guess_grr_advance_3.append(GRR_advance_estimated_guess(users_grid_value_list, k, epsilon, 3))
    print("Advance GRR is Ready")
    probability_of_guess_grr_advance_5.append(GRR_advance_estimated_guess(users_grid_value_list, k, epsilon,5))
    print("Advance GRR is Ready")
    probability_of_guess_grr_advance_10.append(GRR_advance_estimated_guess(users_grid_value_list, k, epsilon, 10))
    print("Advance GRR is Ready")

print(probability_of_guess_grr_plain)
print(probability_of_guess_grr_advance_1)
print(probability_of_guess_grr_advance_3)
print(probability_of_guess_grr_advance_5)
print(probability_of_guess_grr_advance_10)
plt.ylim(0, 1)
plt.xlim(min(epsilon_list), max(epsilon_list))
plt.plot(epsilon_list, probability_of_guess_grr_plain, label='GRR-Plain', color='red')
plt.plot(epsilon_list, probability_of_guess_grr_advance_1, label='GRR-Advance-1-iter', color='blue')
plt.plot(epsilon_list, probability_of_guess_grr_advance_3, label='GRR-Advance-3-iter', color='green')
plt.plot(epsilon_list, probability_of_guess_grr_advance_5, label='GRR-Advance-5-iter', color='yellow')
plt.plot(epsilon_list, probability_of_guess_grr_advance_10, label='GRR-Advance-10-iter', color='purple')
plt.ylabel('Probability of Guess')
plt.xlabel('Epsilon values')
plt.legend(loc='upper right', bbox_to_anchor=(1.015, 1.15))
plt.show()
