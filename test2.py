import csv

import numpy as np

from LDP.protocols import SIMPLE_RAPPOR_Client, OLH_Client, OUE_Client
from LDP.protocols_estimation_different_grid import binary_to_decimal
from hidden_markov_model import hmm_model_RAPPOR

k = 20
states = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20"]


users_grid_value_list = list()
with open('grid/taxi_test_different_grid.dat') as f:
    reader = csv.reader(f, delimiter="\t")
    for line in reader:
        grid_list = line[0].split(" ")
        grid_list_int = [eval(i) for i in grid_list]
        grid_list_int_nd = np.array(grid_list_int)
        users_grid_value_list.append(grid_list_int_nd)


print("RAPPOR Calculation is started")

epsilon_list = [0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 5]  # number of epsilon for test cases
probability_of_guess_rappor = list()


for epsilon in epsilon_list:
    print("Epsilon Value: " + str(epsilon))
    epsilon_prob = list()
    model = hmm_model_RAPPOR(epsilon, k)

    for user_true_values in users_grid_value_list:
        rappor_reports = [OUE_Client(user_true_value, k, epsilon) for user_true_value in user_true_values]

        rappor_reports_decimal_list = list()
        for rappor_report in rappor_reports:
            report_string = ""
            for index in rappor_report:
                report_string += str(int(index))
            report_binary = binary_to_decimal(report_string)
            rappor_reports_decimal_list.append(report_binary)

        obs_sequence_list = []
        for grr_report in rappor_reports_decimal_list:
            obs_sequence_list.append(grr_report)
        obs_sequence = np.array([obs_sequence_list]).T
        # Find most likely state sequence corresponding to obs_sequence
        logprob, state_sequence = model.decode(obs_sequence)

        prob_sum = 0
        index_counter = 0

        for o, s in zip(obs_sequence.T[0], state_sequence):
            true_value = user_true_values[index_counter]
            if int(states[int(s)]) == true_value:
                prob_sum += 1
            index_counter += 1
            #print("{} -> {}".format(states[int(s)], true_value))
        #print("***********")
        epsilon_prob.append(prob_sum / len(user_true_values))
    print(sum(epsilon_prob)/len(epsilon_prob))
    probability_of_guess_rappor.append(sum(epsilon_prob)/len(epsilon_prob))