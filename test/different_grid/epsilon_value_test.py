import numpy as np
import matplotlib.pyplot as plt

from LDP.protocols_estimation_different_grid import grr_estimated_guess, rappor_estimated_guess

# Parameters for simulation
k = 20  # attribute's domain size (grid size)
epsilon_list = [0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 5]  # number of epsilon for test cases
users_grid_value_list = list()
probability_of_guess_grr = list()
probability_of_guess_rappor = list()
probability_of_guess_oue = list()
probability_of_guess_olh = list()

data = np.genfromtxt('../../grid/taxi_test_different_grid.dat', delimiter=' ', dtype=int)

for user_values in data:
    users_grid_value_list.append(user_values)

for epsilon in epsilon_list:
    temp_probability_of_guess_grr = list()
    temp_probability_of_guess_rappor = list()
    temp_probability_of_guess_oue = list()
    temp_probability_of_guess_olh = list()
    for _ in range(20):
        grr_report_guess = grr_estimated_guess(users_grid_value_list, k, epsilon)
        temp_probability_of_guess_grr.append(grr_report_guess)

        #rappor_est_freq = rappor_estimated_guess(users_grid_value_list, k, epsilon)
        #temp_probability_of_guess_rappor.append(rappor_est_freq)

        # oue_est_freq = oue_estimated_guess(users_grid_value_list, k, epsilon)
        # temp_probability_of_guess_oue.append(oue_est_freq)

        # olh_est_freq = olh_estimated_guess(users_grid_value_list, k, epsilon)
        # temp_probability_of_guess_olh.append(olh_est_freq)

    probability_of_guess_grr.append(sum(temp_probability_of_guess_grr) / len(temp_probability_of_guess_grr))
    #probability_of_guess_rappor.append(sum(temp_probability_of_guess_rappor) / len(temp_probability_of_guess_rappor))
    #probability_of_guess_oue.append(sum(temp_probability_of_guess_oue) / len(temp_probability_of_guess_oue))
    #probability_of_guess_olh.append(sum(temp_probability_of_guess_olh) / len(temp_probability_of_guess_olh))

print(probability_of_guess_grr)
plt.ylim(0, 1)
plt.xlim(min(epsilon_list), max(epsilon_list))
plt.plot(epsilon_list, probability_of_guess_grr, label='GRR', color='red')
#plt.plot(epsilon_list, probability_of_guess_rappor, label='RAPPOR', color='blue')
#plt.plot(epsilon_list, probability_of_guess_oue, label='OUE', color='yellow')
plt.ylabel('Probability of Guess')
plt.xlabel('Epsilon values')
plt.legend(loc='upper right', bbox_to_anchor=(1.015, 1.15))
plt.show()
