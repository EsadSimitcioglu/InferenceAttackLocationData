import numpy as np
import xxhash
from hmmlearn import hmm
import csv

from matplotlib import pyplot as plt

from LDP.protocols import HBV_Client
from hidden_markov_model.hidden_markov_model import guess, getAdjacent
from metric.path_distance import ratio_of_guess

from LDP.protocols import GRR_Client, GRR_Aggregator, HBV_Client, HBV_Aggregator


def binary_to_decimal(binary_number):
    decimal_number = 0
    index_counter = len(binary_number) - 1

    for number in binary_number:
        decimal_number += (int(number) * (2 ** index_counter))
        index_counter -= 1
    return decimal_number


def OLH_bit_vector(user_values_list, k, epsilon):
    return experiment(epsilon, k, user_values_list)


def perturb(epsilon, k, user_true_value_list):
    perturbed_reports = list()
    seed_value = 1
    for user_true_values in user_true_value_list:
        bit_vector = HBV_Client(user_true_values, epsilon, seed_value)
        report_string = ""
        for rappor_report in bit_vector:
            report_string += str(int(rappor_report))
        perturbed_reports.append(binary_to_decimal(report_string))
        seed_value += 1

    return perturbed_reports


def experiment(epsilon, k, user_values_list):
    guess_metric = list()

    perturbed_reports = perturb(epsilon, k, user_values_list)

    for index, user_perturbed_report in enumerate(perturbed_reports):
        seed_counter = index + 1
        model = hmm_model_HBV(epsilon, k, seed_counter, 'plain')
        guessed_users_value_first_layer = guess(model, user_perturbed_report)
        guess_metric.append(ratio_of_guess(user_values_list[index], guessed_users_value_first_layer))

    return np.average(guess_metric)


def hmm_model_HBV(epsilon, k, seed_counter, train_type, user_value_list=None):
    p = np.exp(epsilon / 2) / (np.exp(epsilon / 2) + 1)
    q = 1 / (np.exp(epsilon / 2) + 1)
    g = int(round(np.exp(epsilon))) + 1

    model = hmm.MultinomialHMM(n_components=k, algorithm='viterbi')

    if train_type == 'plain':

        model.startprob_ = np.array([1 / k] * k)

        transmat_prob_list = []
        for i in range(1, k + 1):
            sub_list = []
            for j in range(1, k + 1):
                sub_list.append(1 / k)
            transmat_prob_list.append(sub_list)

        model.transmat_ = np.array(transmat_prob_list)

    rappor_report_list = list()
    for x in range(2 ** g):
        rappor_report_list.append((bin(x)[2:].zfill(g)))

    emission_prob_list = list()
    p_counter = 0
    q_counter = 0
    for state in range(k):
        hash_value_of_state = (xxhash.xxh32(str(state), seed=seed_counter).intdigest() % g)
        binary_value_of_state = (bin(hash_value_of_state)[2:].zfill(g))
        row_prob_list = list()
        for column_index in range(len(rappor_report_list)):
            column = rappor_report_list[column_index]
            prob = 1
            for char_index in range(len(binary_value_of_state)):
                if binary_value_of_state[char_index] == column[char_index]:
                    p_counter += 1
                    prob *= p
                else:
                    q_counter += 1
                    prob *= q
            row_prob_list.append(prob)
        emission_prob_list.append(row_prob_list)

    model.emissionprob_ = np.array(emission_prob_list)

    return model