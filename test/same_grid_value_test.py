# Common libraries
import numpy as np
import matplotlib.pyplot as plt

# Multi-Freq-LDPy functions for L-SUE protocol (a.k.a. Basic RAPPOR[11])
from LDP.protocols import GRR_Client, GRR_Aggregator, SIMPLE_RAPPOR_Client, \
    SIMPLE_RAPPOR_Aggregator, OLH_Client, OLH_Aggregator, OLH_Aggregator2, OLH_Client2, OUE_Client


def grr_estimated_freq_per_epsilon(user_values_list, k, epsilon):
    probability_per_user = list()
    for user_true_values in user_values_list:
        grid_number = user_true_values[0]
        grr_reports = [GRR_Client(user_true_value, k, epsilon) for user_true_value in user_true_values]
        count_of_user_value = grr_reports.count(grid_number)
        percentage_of_guess = ((count_of_user_value / k) * 100) / 100
        probability_per_user.append(percentage_of_guess)
    return sum(probability_per_user) / (len(user_values_list))


def rappor_estimated_freq_per_epsilon(user_values_list, k, epsilon):
    probability_per_user = list()
    for user_true_values in user_values_list:
        grid_number = user_true_values[0]
        rappor_reports = [SIMPLE_RAPPOR_Client(user_true_value, k, epsilon) for user_true_value in user_true_values]
        perturbed_bit_vectors = np.array(rappor_reports)
        sum_perturbed_bit_by_bit = sum(perturbed_bit_vectors)
        sum_perturbed_bits = sum(sum_perturbed_bit_by_bit)
        percentage_of_guess = ((sum_perturbed_bit_by_bit[grid_number] / sum_perturbed_bits) * 100) / 100
        probability_per_user.append(percentage_of_guess)
    return sum(probability_per_user) / (len(user_values_list))


def olh_estimated_freq_per_epsilon(user_values_list, n, k, epsilon):
    probability_per_user = list()
    for user_true_values in user_values_list:
        grid_number = user_true_values[0]
        olh_reports = OLH_Client2(user_true_values, n, k, epsilon)
        olh_est = OLH_Aggregator2(olh_reports, n, k, epsilon)
        probability_per_user.append(olh_est[grid_number])
    return sum(probability_per_user) / (len(user_values_list))


def oue_estimated_guess_per_epsilon(user_values_list, k, epsilon):
    probability_per_user = list()
    for user_true_values in user_values_list:
        grid_number = user_true_values[0]
        oue_reports = [OUE_Client(user_true_value, k, epsilon) for user_true_value in user_true_values]
        perturbed_bit_vectors = np.array(oue_reports)
        sum_perturbed_bit_by_bit = sum(perturbed_bit_vectors)
        sum_perturbed_bits = sum(sum_perturbed_bit_by_bit)
        percentage_of_guess = ((sum_perturbed_bit_by_bit[grid_number] / sum_perturbed_bits) * 100) / 100
        probability_per_user.append(percentage_of_guess)
    return sum(probability_per_user) / (len(user_values_list))


# Parameters for simulation
n = 20  # number of timestamps
k = 20  # attribute's domain size (grid size)
epsilon_list = [0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4]  # number of epsilon for test cases
users_grid_value_list = list()
probability_of_guess_grr = list()
probability_of_guess_rappor = list()
probability_of_guess_oue = list()

data = np.genfromtxt('../grid/taxi_test.dat', delimiter=' ', dtype=int)

for user_values in data:
    users_grid_value_list.append(user_values)

for epsilon in epsilon_list:
    grr_est_freq = grr_estimated_freq_per_epsilon(users_grid_value_list, k, epsilon)
    probability_of_guess_grr.append(grr_est_freq)

    rappor_est_freq = rappor_estimated_freq_per_epsilon(users_grid_value_list, k, epsilon)
    probability_of_guess_rappor.append(rappor_est_freq)

    oue_est_freq = oue_estimated_guess_per_epsilon(users_grid_value_list, k, epsilon)
    probability_of_guess_oue.append(oue_est_freq)

plt.ylim(0, 1)
plt.xlim(min(epsilon_list), max(epsilon_list))
plt.plot(epsilon_list, probability_of_guess_grr, label='GRR', color='red')
plt.plot(epsilon_list, probability_of_guess_rappor, label='RAPPOR', color='blue')
plt.plot(epsilon_list, probability_of_guess_oue, label='OUE', color='yellow')
plt.ylabel('Probability of Guess')
plt.xlabel('Epsilon values')
plt.legend(loc='upper right', bbox_to_anchor=(1.015, 1.15))
plt.show()
