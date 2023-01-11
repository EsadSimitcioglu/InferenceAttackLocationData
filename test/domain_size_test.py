import numpy as np
import matplotlib.pyplot as plt

from LDP.protocols_estimation_same_grid import grr_estimated_guess, rappor_estimated_guess, oue_estimated_guess

# Parameters for simulation
n = 20  # number of timestamps
epsilon = 2
domain_list = [10, 15, 20, 25, 30, 35, 40, 45, 50]  # number of epsilon for test cases
users_grid_value_list = list()
probability_of_guess_grr = list()
probability_of_guess_rappor = list()
probability_of_guess_oue = list()
probability_of_guess_olh = list()


data = np.genfromtxt('../grid/taxi_test_same_grid.dat', delimiter=' ', dtype=int)

for user_values in data:
    users_grid_value_list.append(user_values)

for domain in domain_list:
    temp_probability_of_guess_grr = list()
    temp_probability_of_guess_rappor = list()
    temp_probability_of_guess_oue = list()
    temp_probability_of_guess_olh = list()
    for _ in range(20):
        grr_est_freq = grr_estimated_guess(users_grid_value_list, domain, epsilon)
        temp_probability_of_guess_grr.append(grr_est_freq)

        rappor_est_freq = rappor_estimated_guess(users_grid_value_list, domain, epsilon)
        temp_probability_of_guess_rappor.append(rappor_est_freq)

        oue_est_freq = oue_estimated_guess(users_grid_value_list, domain, epsilon)
        temp_probability_of_guess_oue.append(oue_est_freq)

        #olh_est_freq = olh_estimated_freq_per_epsilon(users_grid_value_list, k, epsilon)
        #temp_probability_of_guess_olh.append(olh_est_freq)

    probability_of_guess_grr.append(sum(temp_probability_of_guess_grr) / len(temp_probability_of_guess_grr))
    probability_of_guess_rappor.append(sum(temp_probability_of_guess_rappor) / len(temp_probability_of_guess_rappor))
    probability_of_guess_oue.append(sum(temp_probability_of_guess_oue) / len(temp_probability_of_guess_oue))
    #probability_of_guess_olh.append(sum(temp_probability_of_guess_olh) / len(temp_probability_of_guess_olh))



plt.ylim(0, 1)
plt.xlim(min(domain_list), max(domain_list))
plt.plot(domain_list, probability_of_guess_grr, label='GRR', color='red')
plt.plot(domain_list, probability_of_guess_rappor, label='RAPPOR', color='blue')
plt.plot(domain_list, probability_of_guess_oue, label='OUE', color='yellow')
plt.title("Epsilon Value is " + str(epsilon))
plt.ylabel('Probability of Guess')
plt.xlabel('Domain')
plt.legend(loc='upper right', bbox_to_anchor=(1.015, 1.15))
plt.show()
