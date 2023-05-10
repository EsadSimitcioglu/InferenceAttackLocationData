from statistics import mode

import numpy as np
from collections import Counter

from LDP.protocols import OUE_Client, SIMPLE_RAPPOR_Client, GRR_Client, OLH_Client2


def count_most_repeated_list(lst):
    flattened = [tuple(sublst) for sublst in lst]  # Convert inner lists to tuples for hashability
    counts = Counter(flattened)
    most_common_list, count = counts.most_common(1)[0]
    return list(most_common_list), count


def grr_estimated_guess(user_values_list, k, epsilon):
    probability_per_user = list()
    guess_mode_list = list()
    for grid_number in range(1, k + 1):
        grid_number_power = np.repeat(grid_number, 100)
        grr_guess = [GRR_Client(value, k, epsilon) for value in grid_number_power]
        grr_guess_mode = mode(grr_guess)
        guess_mode_list.append(grr_guess_mode)

    for user_true_values in user_values_list:
        true_value = user_true_values[0]
        grr_reports = [GRR_Client(user_true_value, k, epsilon) for user_true_value in user_true_values]
        for report in grr_reports:
            if report in guess_mode_list:
                index_of_report = guess_mode_list.index(report)
                if index_of_report == true_value - 1:
                    probability_per_user.append(1)
                    continue
            probability_per_user.append(0)
    return sum(probability_per_user) / (len(user_values_list) * len(user_values_list[0]))


def rappor_estimated_guess(user_values_list, k, epsilon):
    probability_per_user = list()
    for user_true_values in user_values_list:
        grid_number = user_true_values[0] - 1
        rappor_reports = [SIMPLE_RAPPOR_Client(user_true_value, k, epsilon) for user_true_value in user_true_values]
        perturbed_bit_vectors = np.array(rappor_reports)
        sum_perturbed_bit_by_bit = sum(perturbed_bit_vectors)
        guess_of_grid = np.argmax(sum_perturbed_bit_by_bit)
        if guess_of_grid == grid_number:
            probability_per_user.append(1)
        else:
            probability_per_user.append(0)
    return sum(probability_per_user) / (len(user_values_list))


def rappor_estimated_guess_advance(user_values_list, k, epsilon):
    probability_per_user = list()
    guess_mode_list = list()
    for grid_number in range(1, k + 1):
        grid_number_power = np.repeat(grid_number, 100)
        rappor_reports = [SIMPLE_RAPPOR_Client(user_true_value, k, epsilon) for user_true_value in grid_number_power]
        guess_of_grid = count_most_repeated_list(rappor_reports)
        guess_mode_list.append(guess_of_grid[0])

    for user_true_values in user_values_list:
        true_value = user_true_values[0]
        rappor_reports = [SIMPLE_RAPPOR_Client(user_true_value, k, epsilon) for user_true_value in user_true_values]
        for report in rappor_reports:
            if report in guess_mode_list:
                index_of_report = guess_mode_list.index(report)
                if index_of_report == true_value - 1:
                    probability_per_user.append(1)
                    continue
            probability_per_user.append(0)
    return sum(probability_per_user) / (len(user_values_list) * len(user_values_list[0]))


def oue_estimated_guess(user_values_list, k, epsilon):
    probability_per_user = list()
    for user_true_values in user_values_list:
        grid_number = user_true_values[0] - 1
        oue_reports = [OUE_Client(user_true_value, k, epsilon) for user_true_value in user_true_values]
        perturbed_bit_vectors = np.array(oue_reports)
        sum_perturbed_bit_by_bit = sum(perturbed_bit_vectors)
        guess_of_grid = np.argmax(sum_perturbed_bit_by_bit)
        if guess_of_grid == grid_number:
            probability_per_user.append(1)
        else:
            probability_per_user.append(0)
    return sum(probability_per_user) / (len(user_values_list))


def oue_estimated_guess_advance(user_values_list, k, epsilon):
    probability_per_user = list()
    guess_mode_list = list()
    for grid_number in range(1, k + 1):
        grid_number_power = np.repeat(grid_number, 100)
        oue_reports = [OUE_Client(user_true_value, k, epsilon) for user_true_value in grid_number_power]
        guess_of_grid = count_most_repeated_list(oue_reports)
        guess_mode_list.append(guess_of_grid[0])

    for user_true_values in user_values_list:
        true_value = user_true_values[0]
        oue_reports = [OUE_Client(user_true_value, k, epsilon) for user_true_value in user_true_values]
        for report in oue_reports:
            report = report.tolist()
            if report in guess_mode_list:
                index_of_report = guess_mode_list.index(report)
                if index_of_report == true_value - 1:
                    probability_per_user.append(1)
                    continue
            probability_per_user.append(0)
    return sum(probability_per_user) / (len(user_values_list) * len(user_values_list[0]))


def olh_estimated_guess(user_values_list, k, epsilon):
    probability_per_user = list()
    seed_init = 0
    for user_true_values in user_values_list:
        true_value = user_true_values[0]
        olh_reports = OLH_Client2(user_true_values, k, epsilon, seed_init)

        seed_init2 = seed_init
        olh_mode_list = list()
        for report in olh_reports:
            for grid_number in range(1, k + 1):
                grid_number_power = np.repeat(grid_number, 100)
                olh_guess_reports = OLH_Client2(grid_number_power, k, epsilon, seed_init2)
                olh_guess_mode = mode(olh_guess_reports)
                olh_mode_list.append(olh_guess_mode)
            if report in olh_mode_list:
                index_of_report = olh_mode_list.index(report)
                if index_of_report == true_value - 1:
                    probability_per_user.append(1)
                    continue
            probability_per_user.append(0)
        seed_init += 1

    return sum(probability_per_user) / (len(user_values_list) * len(user_values_list[0]))
