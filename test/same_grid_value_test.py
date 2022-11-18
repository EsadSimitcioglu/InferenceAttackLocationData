# Common libraries
import numpy as np
import matplotlib.pyplot as plt

# Multi-Freq-LDPy functions for L-SUE protocol (a.k.a. Basic RAPPOR[11])
from LDP.protocols import GRR_Client, GRR_Aggregator


# Parameters for simulation
n = 1  # number of users
k = 20  # attribute's domain size (grid size)
epsilon_list = [1, 2, 4, 8, 20, 50]  # number of epsilon for test cases
gird_number = 3  # user's grid number (location)

estimated_fre_per_epsilon = list()
grid_list = list()

for location in range(100):
    grid_list.append(gird_number+1)


# Simulation dataset where every user has a number between [0-k) with n users
data = np.random.randint(k, size=n)

for epsilon in epsilon_list:
    # Simulation of client-side
    grr_reports = [GRR_Client(input_data, k, epsilon) for input_data in grid_list]

    # Simulation of server-side aggregation
    grr_est_freq = GRR_Aggregator(grr_reports, k, epsilon)

    estimated_fre_per_epsilon.append(grr_est_freq[gird_number+1])

plt.ylim(0, 1)
plt.xlim(min(epsilon_list), max(epsilon_list))
plt.plot(epsilon_list, estimated_fre_per_epsilon, label='Estimated Frequency', color='red')
plt.ylabel('Estimated Frequency')
plt.xlabel('Epsilon values')
plt.legend(loc='upper right', bbox_to_anchor=(1.015, 1.15))
plt.show()