import numpy as np
from hidden_markov_model import hmm_model_GRR, hmm_model_GRR_pre_analyze, hmm_model_RAPPOR
from LDP.protocols import GRR_Client, SIMPLE_RAPPOR_Client
from metric.path_distance import find_path_distance

states = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20"]


def binary_to_decimal(binary_number):
    decimal_number = 0
    index_counter = len(binary_number) - 1

    for number in binary_number:
        decimal_number += (int(number) * (2 ** index_counter))
        index_counter -= 1
    return decimal_number


def grr_estimated_guess(user_values_list, k, epsilon, model_type):
    if model_type == "plain":
        model = hmm_model_GRR(epsilon, k)
    else:
        model = hmm_model_GRR_pre_analyze(epsilon, k, user_values_list)
    epsilon_prob = list()

    for user_true_values in user_values_list:
        grr_reports = [GRR_Client(user_true_value, k, epsilon) for user_true_value in user_true_values]

        obs_sequence_list = []
        for grr_report in grr_reports:
            obs_sequence_list.append(grr_report - 1)
        obs_sequence = np.array([obs_sequence_list]).T

        _, state_sequence = model.decode(obs_sequence)
        prob_sum = 0
        index_counter = 0

        for o, s in zip(obs_sequence.T[0], state_sequence):
            true_value = user_true_values[index_counter]
            if int(states[int(s)]) == true_value:
                prob_sum += 1
            index_counter += 1
        epsilon_prob.append(prob_sum / index_counter)

    return sum(epsilon_prob) / len(epsilon_prob)


def grr_estimated_guess_path(user_values_list, k, epsilon, model_type):
    if model_type == "plain":
        model = hmm_model_GRR(epsilon, k)
    else:
        model = hmm_model_GRR_pre_analyze(epsilon, k, user_values_list)
    error_list = list()

    for user_true_values in user_values_list:
        grr_reports = [GRR_Client(user_true_value, k, epsilon) for user_true_value in user_true_values]

        obs_sequence_list = []
        for grr_report in grr_reports:
            obs_sequence_list.append(grr_report - 1)
        obs_sequence = np.array([obs_sequence_list]).T

        _, state_sequence = model.decode(obs_sequence)

        guess_values = list()
        for o, s in zip(obs_sequence.T[0], state_sequence):
            guess_values.append(int(states[int(s)]))

        error_list.append(find_path_distance(user_true_values, guess_values))

    return error_list


def rappor_estimated_guess(user_values_list, k, epsilon):
    model = hmm_model_RAPPOR(epsilon, k)
    rappor_reports_decimal_list = list()
    epsilon_prob = list()

    for user_true_values in user_values_list:
        rappor_reports = [SIMPLE_RAPPOR_Client(user_true_value, k, epsilon) for user_true_value in user_true_values]

        for rappor_report in rappor_reports:
            report_string = ""
            for index in rappor_report:
                report_string += str(int(index))
            report_binary = binary_to_decimal(report_string)
            rappor_reports_decimal_list.append(report_binary)

        obs_sequence_list = []
        for grr_report in rappor_reports_decimal_list:
            obs_sequence_list.append(grr_report - 1)
        obs_sequence = np.array([obs_sequence_list]).T
        # Find most likely state sequence corresponding to obs_sequence
        logprob, state_sequence = model.decode(obs_sequence)

        prob_sum = 0
        index_counter = 0

        for o, s in zip(obs_sequence.T[0], state_sequence):
            if index_counter == len(user_true_values):
                break
            true_value = user_true_values[index_counter]
            if int(states[int(s)]) == true_value:
                prob_sum += 1
            index_counter += 1
        epsilon_prob.append(prob_sum / index_counter)

    return sum(epsilon_prob) / len(epsilon_prob)
