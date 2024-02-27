import csv

import numpy as np
import xxhash
from hmmlearn import hmm



from LDP.protocols.HBV import HBV
from experiment.attack.metrics import experiment_metrics
from hidden_markov_model.HMM import HMM
from hidden_markov_model.helper import ratio_of_guess
from hidden_markov_model.hidden_markov_model import guess, getAdjacent


def binary_to_decimal(binary_number):
    decimal_number = 0
    index_counter = len(binary_number) - 1

    for number in binary_number:
        decimal_number += (int(number) * (2 ** index_counter))
        index_counter -= 1
    return decimal_number

def decimal_to_binary(decimal_num, k):
    if decimal_num == 0:
        return '0' * k
    binary_num = ''
    while decimal_num > 0:
        remainder = decimal_num % 2
        binary_num = str(remainder) + binary_num
        decimal_num = decimal_num // 2
    if len(binary_num) < k:
        padding = '0' * (k - len(binary_num))
        binary_num = padding + binary_num
    return binary_num


def OLH_bit_vector(user_values_list, k, epsilon):
    return experiment(epsilon, k, user_values_list)


def perturb(epsilon, k, user_true_value_list):
    perturbed_reports = list()
    seed_value = 1
    hbv = HBV(k, epsilon)
    for user_true_values in user_true_value_list:
        user_perturbed_report = list()
        bit_vector_list = hbv.client(user_true_values, seed_value)
        for report in bit_vector_list:
            report_string = ""
            for rappor_report in report:
                report_string += str(int(rappor_report))
            user_perturbed_report.append(binary_to_decimal(report_string))
        perturbed_reports.append(user_perturbed_report)
        seed_value += 1

    return perturbed_reports


def experiment(epsilon, k, user_values_list):
    guess_list = list()
    perturbed_reports = perturb(epsilon, k, user_values_list)

    hbv = HBV(k, epsilon)

    """
    for index, user_perturbed_report in enumerate(perturbed_reports):
        seed_counter = index + 1
        model = hmm_model_HBV(epsilon, k, seed_counter)
        guessed_users_value_first_layer = guess(model, user_perturbed_report)
        guess_metric.append(ratio_of_guess(user_values_list[index], guessed_users_value_first_layer))
    """

    for user_index, report in enumerate(perturbed_reports):
        hbv_model = HMM(k, epsilon)
        hbv_model.create_plain_protocol_model(hbv, user_index + 1)
        guess_list.append(hbv_model.guess_user_values(hbv, report))
    return experiment_metrics('PA', user_values_list, guess_list)


def hmm_model_HBV(epsilon, k, seed_counter):
    p = np.exp(epsilon / 2) / (np.exp(epsilon / 2) + 1)
    q = 1 / (np.exp(epsilon / 2) + 1)
    g = int(round(np.exp(epsilon))) + 1
    grid = np.arange(k).reshape(k // 4, k // 5)

    model = hmm.MultinomialHMM(n_components=k, algorithm='viterbi')

    model.startprob_ = np.array([1 / k] * k)

    matrix_list = []
    for i in range(1, k + 1):
        sub_list = []
        adjacent_elements = getAdjacent(grid, i)
        for j in range(1, k + 1):
            if j in adjacent_elements or j == i:
                sub_list.append(1 / (len(adjacent_elements) + 1))
            else:
                sub_list.append(0)
        matrix_list.append(sub_list)
    model.transmat_ = np.array(matrix_list)

    rappor_report_list = list()
    for x in range(2 ** g):
        rappor_report_list.append((bin(x)[2:].zfill(g)))

    emission_prob_list = list()
    for row in range(k):
        hash_value_of_hidden_state = (xxhash.xxh32(str(row), seed=seed_counter).intdigest() % g)
        bit_vector_of_hidden_state = decimal_to_binary(hash_value_of_hidden_state, g)
        row_prob_list = list()
        for column_index in range(len(rappor_report_list)):
            column = rappor_report_list[column_index]
            prob = 1
            for char_index in range(g):
                if bit_vector_of_hidden_state[char_index] == column[char_index]:
                    prob *= p
                else:
                    prob *= q
            row_prob_list.append(prob)
        emission_prob_list.append(row_prob_list)

    model.emissionprob_ = np.array(emission_prob_list)

    return model


users_grid_value_list = list()
epsilon_list = [0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 5]  # number of epsilon for test cases

with open('../../../dataset/taxi/taxi_grid_2.dat') as f:
    reader = csv.reader(f, delimiter="\t")
    for line in reader:
        grid_list = line[0].split(" ")
        grid_list_int = [eval(i) for i in grid_list]
        grid_list_int_nd = np.array(grid_list_int)
        users_grid_value_list.append(grid_list_int_nd)

for epsilon in epsilon_list:
    print("Epsilon Value: " + str(epsilon))
    print(OLH_bit_vector(users_grid_value_list, 20, epsilon))