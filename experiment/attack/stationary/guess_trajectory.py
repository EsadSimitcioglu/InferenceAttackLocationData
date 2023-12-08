from statistics import mode
import random
import numpy as np
from collections import Counter

from numpy import exp
from LDP.protocols.GRR import GRR
from LDP.protocols.RAPPOR import RAPPOR
from LDP.protocols.OUE import OUE
from LDP.protocols.OLH import OLH




def find_mode(perturbed_reports):
    data = Counter(perturbed_reports)
    get_mode = dict(data)
    mode = [k for k, v in get_mode.items() if v == max(list(data.values()))]
    if len(mode) > 1:
        reports_mode = random.choice(mode)
    else:
        reports_mode = mode[0]

    return reports_mode


def grr_estimated_guess(user_values_list, k, epsilon):
    probability_per_user = list()
    for user_true_values in user_values_list:
        grid_number = user_true_values[0] - 1
        grr = GRR(k, epsilon)
        grr_reports = [grr.client(user_true_value) for user_true_value in user_true_values]
        grr_reports_mode = find_mode(grr_reports)
        if grr_reports_mode == grid_number:
            probability_per_user.append(1)
        else:
            probability_per_user.append(0)

    return sum(probability_per_user) / (len(user_values_list))


def rappor_estimated_guess(user_values_list, k, epsilon):
    probability_per_user = list()
    for user_true_values in user_values_list:
        grid_number = user_true_values[0] - 1
        rappor = RAPPOR(k, epsilon)
        rappor_reports = [rappor.client(user_true_value) for user_true_value in user_true_values]
        perturbed_bit_vectors = np.array(rappor_reports)
        sum_perturbed_bit_by_bit = sum(perturbed_bit_vectors)
        guess_of_grid = np.argmax(sum_perturbed_bit_by_bit)
        if guess_of_grid == grid_number:
            probability_per_user.append(1)
        else:
            probability_per_user.append(0)
    return sum(probability_per_user) / (len(user_values_list))


def oue_estimated_guess(user_values_list, k, epsilon):
    probability_per_user = list()
    for user_true_values in user_values_list:
        grid_number = user_true_values[0] - 1
        oue = OUE(k, epsilon)
        oue_reports = [oue.client(user_true_value) for user_true_value in user_true_values]
        perturbed_bit_vectors = np.array(oue_reports)
        sum_perturbed_bit_by_bit = sum(perturbed_bit_vectors)
        guess_of_grid = np.argmax(sum_perturbed_bit_by_bit)
        if guess_of_grid == grid_number:
            probability_per_user.append(1)
        else:
            probability_per_user.append(0)
    return sum(probability_per_user) / (len(user_values_list))


def olh_estimated_guess(user_values_list, k, epsilon):
    probability_per_user = list()
    seed_init = 1
    g = int(round(np.exp(epsilon))) + 1
    olh = OLH(k, epsilon)

    for user_true_values in user_values_list:
        true_value = user_true_values[0]
        olh_reports = [olh.client(user_true_value, seed_init) for user_true_value in user_true_values]
        olh_reports_mode = find_mode(olh_reports)

        grid_list = list()
        for grid_number in range(1, k + 1):
            grid_number_power = np.repeat(grid_number, 100)
            olh_guess_reports = [olh.client(user_true_value, seed_init) for user_true_value in grid_number_power]
            olh_guess_mode = find_mode(olh_guess_reports)
            if olh_guess_mode == olh_reports_mode:
                grid_list.append(grid_number)

        if len(grid_list) >= 1:
            random_grid = random.choice(grid_list)
            if random_grid == true_value:
                probability_per_user.append(1)
            else:
                probability_per_user.append(0)
        else:
            probability_per_user.append(0)
        seed_init += 1

    return sum(probability_per_user) / (len(user_values_list))
