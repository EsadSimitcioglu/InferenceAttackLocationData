# Common libraries
import numpy as np
import matplotlib.pyplot as plt

# Multi-Freq-LDPy functions for L-SUE protocol (a.k.a. Basic RAPPOR[11])
from LDP.protocols import GRR_Client, GRR_Aggregator, RAPPOR_Client, RAPPOR_Aggregator


def grr_estimated_freq_per_epsilon(grid_list, k, epsilon):
    grr_reports = [GRR_Client(user_val, k, epsilon) for user_val in grid_list]
    grr_est_freq = GRR_Aggregator(grr_reports, k, epsilon)
    return grr_est_freq[gird_number + 1]


def rappor_estimated_freq_per_epsilon(grid_list, k, epsilon, epsilon_l):
    rappor_reports = RAPPOR_Client(grid_list, k, epsilon, epsilon_l)
    rappor_est_freq = RAPPOR_Aggregator(rappor_reports[0], epsilon, epsilon_l)
    return rappor_est_freq[gird_number + 1]


# Parameters for simulation
n = 1  # number of users
k = 20  # attribute's domain size (grid size)
epsilon_list = [1, 2, 4, 8, 20, 50]  # number of epsilon for test cases
gird_number = 3  # user's grid number (location)

grr_estimated_fre_per_epsilon = list()
rappor_estimated_fre_per_epsilon = list()
grid_list = list()

for location in range(100):
    grid_list.append(gird_number + 1)

# Simulation dataset where every user has a number between [0-k) with n users
data = np.random.randint(k, size=n)

for epsilon in epsilon_list:
    epsilon_l = 0.5 * epsilon  # single report privacy guarantee, i.e., lower bound

    grr_est_freq = grr_estimated_freq_per_epsilon(grid_list, k, epsilon)
    grr_estimated_fre_per_epsilon.append(grr_est_freq)

    rappor_est_freq = rappor_estimated_freq_per_epsilon(grid_list, k, epsilon, epsilon_l)
    rappor_estimated_fre_per_epsilon.append(rappor_est_freq)


plt.ylim(0, 1)
plt.xlim(min(epsilon_list), max(epsilon_list))
plt.plot(epsilon_list, grr_estimated_fre_per_epsilon, label='GRR Estimated Frequency', color='red')
plt.plot(epsilon_list, rappor_estimated_fre_per_epsilon, label='RAPPOR Estimated Frequency', color='blue')
plt.ylabel('Estimated Frequency')
plt.xlabel('Epsilon values')
plt.legend(loc='upper right', bbox_to_anchor=(1.015, 1.15))
plt.show()
