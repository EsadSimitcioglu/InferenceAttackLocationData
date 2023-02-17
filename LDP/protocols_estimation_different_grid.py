import numpy as np
from LDP.HiddenMarkovModel import hmm_model_GRR
from LDP.protocols import GRR_Client
import matplotlib.pyplot as plt

def grr_estimated_guess(user_values_list, k, n, epsilon):
    grr_reports_list = list()
    for user_true_values in user_values_list:
        grr_reports = [GRR_Client(user_true_value, k, epsilon) for user_true_value in user_true_values]
        grr_reports_list.append(grr_reports)

    epsilon_prob = list()
    for index in range(len(users_grid_value_list)):
        user_values = users_grid_value_list[index]
        grr_reports = grr_reports_list[index]
        obs_sequence_list = []

        for grr_report in grr_reports:
            obs_sequence_list.append(grr_report - 1)
        obs_sequence = np.array([obs_sequence_list]).T

        _, state_sequence = model.decode(obs_sequence)
        prob_sum = 0
        index_counter = 0

        for o, s in zip(obs_sequence.T[0], state_sequence):
            true_value = user_values[index_counter]
            if int(states[int(s)]) == true_value:
                prob_sum += 1
            index_counter += 1
        epsilon_prob.append(prob_sum)
    return sum(epsilon_prob) / (n*len(epsilon_prob))

# Parameters for simulation
n = 19  # number of timestamps
k = 20  # attribute's domain size (grid size)
epsilon_list = [0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 5]  # number of epsilon for test cases
users_grid_value_list = list()
probability_of_guess_grr = list()

for line in open('../grid/taxi_test_different_grid.dat'):
    lst_int = [int(x) for x in line.split()]
    users_grid_value_list.append(lst_int)

states = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20"]
observations = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20"]
probability_of_guess = list()

for epsilon in epsilon_list:
    model = hmm_model_GRR(epsilon, k)
    grr_report_guess = grr_estimated_guess(users_grid_value_list, k, n, epsilon)
    probability_of_guess_grr.append(grr_report_guess)

plt.ylim(0, 1)
plt.xlim(min(epsilon_list), max(epsilon_list))
plt.plot(epsilon_list, probability_of_guess_grr, label='GRR', color='red')
plt.ylabel('Probability of Guess')
plt.xlabel('Epsilon values')
plt.legend(loc='upper right', bbox_to_anchor=(1.015, 1.15))
plt.show()