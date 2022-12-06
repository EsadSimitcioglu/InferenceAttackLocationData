# Common libraries
import numpy as np
from numpy import log as ln
import matplotlib.pyplot as plt

# Multi-Freq-LDPy functions for L-SUE protocol (a.k.a. Basic RAPPOR[11])
from LDP.protocols import GRR_Client, GRR_Aggregator, RAPPOR_Client, RAPPOR_Aggregator

# Parameters for simulation
n = 1  # number of users
k = 20  # attribute's domain size (grid size)
epsilon_list = [0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4]  # number of epsilon for test cases

def grr_estimated_freq_per_epsilon(user_values_list, k, epsilon):
    probability_per_user = list()
    for user_values in user_values_list:
        grid_number = user_values[0]
        grr_reports = [GRR_Client(user_value, k, epsilon) for user_value in user_values]
        grr_est_freq = GRR_Aggregator(grr_reports, k, epsilon)
        probability_per_user.append(grr_est_freq[grid_number])
    return sum(probability_per_user) / (len(user_values_list))


def rappor_estimated_freq_per_epsilon(gird_number, grid_list, k, epsilon, epsilon_l):
    rappor_reports = RAPPOR_Client(grid_list, k, epsilon, epsilon_l)
    rappor_est_freq = RAPPOR_Aggregator(rappor_reports[0], epsilon, epsilon_l)
    probability = rappor_est_freq[gird_number + 1] / sum(rappor_est_freq)
    return probability




users_grid_value_list = list()
probability_of_guess_grr = list()
rappor_estimated_fre_per_epsilon = list()
grid_list = list()

data = np.genfromtxt('../grid/taxi_test.dat', delimiter=' ', dtype=int)

for user_values in data:
    users_grid_value_list.append(user_values)

for epsilon in epsilon_list:
    epsilon_l = 0.5 * epsilon  # single report privacy guarantee, i.e., lower bound

    grr_est_freq = grr_estimated_freq_per_epsilon(user_grid_value_list, k, epsilon)
    probability_of_guess_grr.append(grr_est_freq)

    #rappor_est_freq = rappor_estimated_freq_per_epsilon(user_grid_value_list, grid_list, k, epsilon, epsilon_l)
    #rappor_estimated_fre_per_epsilon.append(rappor_est_freq)

print(probability_of_guess_grr)
plt.ylim(0, 1)
plt.xlim(min(epsilon_list), max(epsilon_list))
plt.plot(epsilon_list, probability_of_guess_grr, label='GRR', color='red')
#plt.plot(epsilon_list, rappor_estimated_fre_per_epsilon, label='RAPPOR', color='blue')
plt.ylabel('Probability of Guess')
plt.xlabel('Epsilon values')
plt.legend(loc='upper right', bbox_to_anchor=(1.015, 1.15))
plt.show()
