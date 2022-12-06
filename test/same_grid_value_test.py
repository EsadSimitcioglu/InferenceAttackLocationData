# Common libraries
import numpy as np
import matplotlib.pyplot as plt

# Multi-Freq-LDPy functions for L-SUE protocol (a.k.a. Basic RAPPOR[11])
from LDP.protocols import GRR_Client, GRR_Aggregator, SIMPLE_RAPPOR_Client, \
    SIMPLE_RAPPOR_Aggregator


def grr_estimated_freq_per_epsilon(user_values_list, k, epsilon):
    probability_per_user = list()
    for user_true_values in user_values_list:
        grid_number = user_true_values[0]
        grr_reports = [GRR_Client(user_true_value, k, epsilon) for user_true_value in user_true_values]
        grr_est = GRR_Aggregator(grr_reports, k, epsilon)
        probability_per_user.append(grr_est[grid_number])
    return sum(probability_per_user) / (len(user_values_list))


def rappor_estimated_freq_per_epsilon(user_values_list, k, epsilon):
    probability_per_user = list()
    for user_true_values in user_values_list:
        grid_number = user_true_values[0]
        rappor_reports = [SIMPLE_RAPPOR_Client(user_true_value, k, epsilon) for user_true_value in user_true_values]
        rappor_est = SIMPLE_RAPPOR_Aggregator(rappor_reports, epsilon)
        probability_per_user.append(rappor_est[grid_number])
    return sum(probability_per_user) / (len(user_values_list))


# Parameters for simulation
n = 1  # number of users
k = 20  # attribute's domain size (grid size)
epsilon_list = [0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4]  # number of epsilon for test cases
users_grid_value_list = list()
probability_of_guess_grr = list()
probability_of_guess_rappor = list()


data = np.genfromtxt('../grid/taxi_test.dat', delimiter=' ', dtype=int)

for user_values in data:
    users_grid_value_list.append(user_values)

for epsilon in epsilon_list:
    grr_est_freq = grr_estimated_freq_per_epsilon(users_grid_value_list, k, epsilon)
    probability_of_guess_grr.append(grr_est_freq)

    rappor_est_freq = rappor_estimated_freq_per_epsilon(users_grid_value_list, k, epsilon)
    probability_of_guess_rappor.append(rappor_est_freq)

plt.ylim(0, 1)
plt.xlim(min(epsilon_list), max(epsilon_list))
plt.plot(epsilon_list, probability_of_guess_grr, label='GRR', color='red')
plt.plot(epsilon_list, probability_of_guess_rappor, label='RAPPOR', color='blue')
plt.ylabel('Probability of Guess')
plt.xlabel('Epsilon values')
plt.legend(loc='upper right', bbox_to_anchor=(1.015, 1.15))
plt.show()
