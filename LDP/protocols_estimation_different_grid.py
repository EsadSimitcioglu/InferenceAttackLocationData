from statistics import mode

import numpy as np
import xxhash

from hidden_markov_model import hmm_model_GRR, hmm_model_GRR_pre_analyze, hmm_model_RAPPOR, hmm_model_OUE, hmm_model_OLH
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


def OLH_estimated_guess(user_values_list, k, epsilon, test_type):
    guess_prob_list = list()
    error_sum = 0
    seed_init = 0
    g = int(round(np.exp(epsilon))) + 1
    for user_true_values in user_values_list:
        olh_reports = OLH_Client(user_true_values, k, epsilon, seed_init)
        seed_init2 = seed_init
        for index, report in enumerate(olh_reports):
            true_value = user_true_values[index]
            model = hmm_model_OLH(epsilon, k, seed_init2)
            obs_sequence_list = [report]
            obs_sequence = np.array([obs_sequence_list]).T
            _, state_sequence = model.decode(obs_sequence)

            if test_type == 'path':
                guess_values = list()
                for o, s in zip(obs_sequence.T[0], state_sequence):
                    guess_values.append(int(states[int(s)]))
                error_sum += find_path_distance(user_true_values[index], report)
            elif test_type == 'guess':
                true_value = (xxhash.xxh32(str(true_value), seed=seed_init2).intdigest() % g)
                guess_value = obs_sequence[0][0]
                if guess_value == true_value:
                    guess_prob_list.append(1)
                else:
                    guess_prob_list.append(0)
            seed_init2 += 1
        seed_init += 20
    return np.average(guess_prob_list)