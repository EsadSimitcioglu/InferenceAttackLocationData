from statistics import mode

import numpy as np
from hidden_markov_model import hmm_model_GRR, hmm_model_GRR_pre_analyze, hmm_model_RAPPOR, hmm_model_OUE
from LDP.protocols import GRR_Client, SIMPLE_RAPPOR_Client, OUE_Client, OLH_Client, OLH_Client2
from metric.path_distance import find_path_distance

states = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20"]


def binary_to_decimal(binary_number):
    decimal_number = 0
    index_counter = len(binary_number) - 1

    for number in binary_number:
        decimal_number += (int(number) * (2 ** index_counter))
        index_counter -= 1
    return decimal_number


def GRR_estimated_guess(user_values_list, k, epsilon, model_type, test_type):
    if model_type == "plain":
        model = hmm_model_GRR(epsilon, k)
    else:
        model = hmm_model_GRR_pre_analyze(epsilon, k, user_values_list)
    epsilon_prob = list()
    error_sum = 0

    for user_true_values in user_values_list:
        grr_reports = [GRR_Client(user_true_value, k, epsilon) for user_true_value in user_true_values]

        obs_sequence_list = []
        for grr_report in grr_reports:
            obs_sequence_list.append(grr_report - 1)
        obs_sequence = np.array([obs_sequence_list]).T

        _, state_sequence = model.decode(obs_sequence)
        prob_sum = 0
        index_counter = 0

        if test_type == 'path':
            guess_values = list()
            for o, s in zip(obs_sequence.T[0], state_sequence):
                guess_values.append(int(states[int(s)]))
            error_sum += find_path_distance(user_true_values, guess_values)
        elif test_type == 'guess':
            for o, s in zip(obs_sequence.T[0], state_sequence):
                true_value = user_true_values[index_counter]
                if int(states[int(s)]) == true_value:
                    prob_sum += 1
                index_counter += 1
            epsilon_prob.append(prob_sum / index_counter)

    if test_type == 'path':
        return error_sum
    elif test_type == 'guess':
        return sum(epsilon_prob) / len(epsilon_prob)


def RAPPOR_estimated_guess(user_values_list, k, epsilon, test_type):
    model = hmm_model_RAPPOR(epsilon, k)
    epsilon_prob = list()
    error_sum = 0
    print("RAPPOR Calculation is started")

    for user_true_values in user_values_list:
        rappor_reports = [SIMPLE_RAPPOR_Client(user_true_value, k, epsilon) for user_true_value in user_true_values]

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
        logprob, state_sequence = model.decode(obs_sequence)

        prob_sum = 0
        index_counter = 0

        if test_type == 'path':
            guess_values = list()
            for o, s in zip(obs_sequence.T[0], state_sequence):
                guess_values.append(int(states[int(s)]))
            error_sum += find_path_distance(user_true_values, guess_values)
        elif test_type == 'guess':
            for o, s in zip(obs_sequence.T[0], state_sequence):
                true_value = user_true_values[index_counter]
                if int(states[int(s)]) == true_value:
                    prob_sum += 1
                index_counter += 1
            epsilon_prob.append(prob_sum / index_counter)

    if test_type == 'path':
        return error_sum
    elif test_type == 'guess':
        return sum(epsilon_prob) / len(epsilon_prob)


def OUE_estimated_guess(user_values_list, k, epsilon, test_type):
    model = hmm_model_OUE(epsilon, k)
    epsilon_prob = list()
    error_sum = 0
    print("RAPPOR Calculation is started")

    for user_true_values in user_values_list:
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
        logprob, state_sequence = model.decode(obs_sequence)

        prob_sum = 0
        index_counter = 0

        if test_type == 'path':
            guess_values = list()
            for o, s in zip(obs_sequence.T[0], state_sequence):
                guess_values.append(int(states[int(s)]))
            error_sum += find_path_distance(user_true_values, guess_values)
        elif test_type == 'guess':
            for o, s in zip(obs_sequence.T[0], state_sequence):
                true_value = user_true_values[index_counter]
                if int(states[int(s)]) == true_value:
                    prob_sum += 1
                index_counter += 1
            epsilon_prob.append(prob_sum / index_counter)

    if test_type == 'path':
        return error_sum
    elif test_type == 'guess':
        return sum(epsilon_prob) / len(epsilon_prob)


def OLH_estimated_guess(user_values_list, k, epsilon):
    olh_report_list = list()
    seed_init = 0
    for user_true_values in user_values_list:
        true_value = user_true_values[0]
        olh_reports = OLH_Client(user_true_values, k, epsilon, seed_init)
        seed_init2 = seed_init
        probability_list = list()
        for report in olh_reports:
            is_add = False
            for grid_number in range(1, k + 1):
                grid_number_power = np.repeat(grid_number, 100)
                olh_guess_reports = OLH_Client2(grid_number_power, k, epsilon, seed_init2)
                olh_guess_mode = mode(olh_guess_reports)
                if report == olh_guess_mode and grid_number == true_value:
                    probability_list.append(1)
                    is_add = True
                    break
            seed_init2 += 1
            if not is_add:
                probability_list.append(0)
        olh_report_list.append(sum(probability_list) / (len(probability_list)))
        seed_init += 20
    return olh_report_list