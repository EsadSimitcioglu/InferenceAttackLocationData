import csv
import numpy as np
import matplotlib.pyplot as plt
from LDP.estimation_different_grid import OUE_estimated_guess, OUE_advance_estimated_guess, OUE_FK_estimated_guess

# Parameters for simulation
k = 20  # attribute's domain size (grid size)
epsilon_list = [0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 5]  # number of epsilon for test cases
users_grid_value_list = list()
probability_of_guess_oue_plain = list()
probability_of_guess_oue_advance = list()
probability_of_guess_oue_fk = list()

with open('../../../../../dataset/taxi/taxi_test_different_grid.dat') as f:
    reader = csv.reader(f, delimiter="\t")
    for line in reader:
        grid_list = line[0].split(" ")
        grid_list_int = [eval(i) for i in grid_list]
        grid_list_int_nd = np.array(grid_list_int)
        users_grid_value_list.append(grid_list_int_nd)

for epsilon in epsilon_list:
    print("Epsilon Value: " + str(epsilon))
    probability_of_guess_oue_plain.append(OUE_estimated_guess(users_grid_value_list, k, epsilon, 'guess'))
    print("Plain OUE is Ready")
    probability_of_guess_oue_advance.append(OUE_advance_estimated_guess(users_grid_value_list, k, epsilon, 1))
    print("Advance OUE is Ready")
    probability_of_guess_oue_fk.append(OUE_FK_estimated_guess(users_grid_value_list, k, epsilon, 'guess'))
    print("FK OUE is Ready")

print(probability_of_guess_oue_plain)
print(probability_of_guess_oue_advance)
print(probability_of_guess_oue_fk)
plt.ylim(0, 1)
plt.xlim(min(epsilon_list), max(epsilon_list))
plt.plot(epsilon_list, probability_of_guess_oue_plain, label='OUE-Plain', color='red')
plt.plot(epsilon_list, probability_of_guess_oue_advance, label='OUE-Advance', color='blue')
plt.plot(epsilon_list, probability_of_guess_oue_fk, label='OUE-FK', color='yellow')
plt.ylabel('Probability of Guess')
plt.xlabel('Epsilon values')
plt.legend(loc='upper right', bbox_to_anchor=(1.015, 1.15))
plt.show()
