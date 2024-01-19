import csv
from statistics import mode
import random
import numpy as np
from collections import Counter

from numpy import exp
from LDP.protocols.GRR import GRR
from LDP.protocols.RAPPOR import RAPPOR
from LDP.protocols.OUE import OUE
from LDP.protocols.OLH import OLH


def choose_item_from_non_normalized_probabilities(probabilities):
    total_prob = sum(probabilities)

    if total_prob == 0:
        raise ValueError("Sum of probabilities cannot be zero.")

    normalized_probabilities = [prob / total_prob for prob in probabilities]

    random_num = random.uniform(0, 1)
    cumulative_prob = 0

    for i, prob in enumerate(normalized_probabilities):
        cumulative_prob += prob
        if random_num <= cumulative_prob:
            return i + 1


def analyze_dataset(user_values_list):
    grid_occur_dict = {}
    grid_prob_dict = {}
    for user_true_values in user_values_list:
        init_grid = user_true_values.item(0)
        grid_occur_dict[init_grid] = grid_occur_dict.get(init_grid, 0) + 1

    grid_occur_dict = dict(sorted(grid_occur_dict.items()))
    sum_grid_counts = sum(grid_occur_dict.values())
    for grid_count in grid_occur_dict:
        grid_prob_dict[grid_count] = grid_occur_dict[grid_count] / sum_grid_counts

    return grid_prob_dict


def find_mode(perturbed_reports, grid_prob_dict=None):
    data = Counter(perturbed_reports)
    get_mode = dict(data)
    mode_list = [k for k, v in get_mode.items() if v == max(list(data.values()))]
    if len(mode_list) > 1:
        if grid_prob_dict is None:
            reports_mode = np.random.choice(mode_list)
        else:
            user_grid_prob_list = list()
            for grid in range(1, 21):
                if grid in mode_list:
                    user_grid_prob_list.append(1 / len(mode_list))
                else:
                    user_grid_prob_list.append(0)
            res_prob_list = [grid_dict_prob * grid_user_prob for grid_dict_prob, grid_user_prob in
                             zip(grid_prob_dict, user_grid_prob_list)]
            norm_res_prob_list = [prob / sum(res_prob_list) for prob in res_prob_list]
            reports_mode = choose_item_from_non_normalized_probabilities(norm_res_prob_list)
    else:
        reports_mode = mode_list[0]

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


def grr_informed_guess(user_values_list, k, epsilon):
    probability_per_user = list()
    grid_prob_dict = analyze_dataset(user_values_list)
    for user_true_values in user_values_list:
        grid_number = user_true_values[0] - 1
        grr = GRR(k, epsilon)
        grr_reports = [grr.client(user_true_value) for user_true_value in user_true_values]
        grr_reports_mode = find_mode(grr_reports, grid_prob_dict)
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


def rappor_informed_guess(user_values_list, k, epsilon):
    probability_per_user = list()
    grid_prob_dict = analyze_dataset(user_values_list)
    for user_true_values in user_values_list:
        grid_number = user_true_values[0]
        rappor = RAPPOR(k, epsilon)
        rappor_reports = [rappor.client(user_true_value) for user_true_value in user_true_values]
        perturbed_bit_vectors = np.array(rappor_reports)
        sum_perturbed_bit_by_bit = sum(perturbed_bit_vectors)
        max_grid = max(sum_perturbed_bit_by_bit)
        max_grid_list = [i+1 for i, val in enumerate(sum_perturbed_bit_by_bit) if val == max_grid]
        user_grid_prob_list = [0] * k
        for grid in range(1, 21):
            if grid in max_grid_list:
                user_grid_prob_list[grid-1] = 1 / len(max_grid_list)
        res_prob_list = [grid_dict_prob * grid_user_prob for grid_dict_prob, grid_user_prob in
                         zip(grid_prob_dict, user_grid_prob_list)]
        norm_res_prob_list = [prob / sum(res_prob_list) for prob in res_prob_list]
        guess_of_grid = choose_item_from_non_normalized_probabilities(norm_res_prob_list)
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


def oue_informed_guess(user_values_list, k, epsilon):
    probability_per_user = list()
    grid_prob_dict = analyze_dataset(user_values_list)
    for user_true_values in user_values_list:
        grid_number = user_true_values[0]
        oue = OUE(k, epsilon)
        oue_reports = [oue.client(user_true_value) for user_true_value in user_true_values]
        perturbed_bit_vectors = np.array(oue_reports)
        sum_perturbed_bit_by_bit = sum(perturbed_bit_vectors)
        max_grid = max(sum_perturbed_bit_by_bit)
        max_grid_list = [i+1 for i, val in enumerate(sum_perturbed_bit_by_bit) if val == max_grid]
        user_grid_prob_list = [0] * k
        for grid_val in range(1, 21):
            if grid_val in max_grid_list:
                user_grid_prob_list[grid_val-1] = 1 / len(max_grid_list)
        res_prob_list = [grid_dict_prob * grid_user_prob for grid_dict_prob, grid_user_prob in
                         zip(grid_prob_dict, user_grid_prob_list)]
        norm_res_prob_list = [prob / sum(res_prob_list) for prob in res_prob_list]
        guess_of_grid = choose_item_from_non_normalized_probabilities(norm_res_prob_list)
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


def olh_informed_guess(user_values_list, k, epsilon):
    probability_per_user = list()
    seed_init = 1
    g = int(round(np.exp(epsilon))) + 1
    olh = OLH(k, epsilon)
    grid_prob_dict = analyze_dataset(user_values_list)


    for user_true_values in user_values_list:
        true_value = user_true_values[0]
        olh_reports = list()

        for user_true_value in user_true_values:
            olh_reports.append(olh.client(user_true_value, seed_init))
            seed_init += 1
        olh_reports_mode = find_mode(olh_reports)

        grid_list = list()
        for grid_number in range(1, k + 1):
            grid_number_power = np.repeat(grid_number, 100)
            olh_guess_reports = [olh.client(user_true_value, seed_init) for user_true_value in grid_number_power]
            olh_guess_mode = find_mode(olh_guess_reports)
            if olh_guess_mode == olh_reports_mode:
                grid_list.append(grid_number)



        if len(grid_list) >= 1:
            user_grid_prob_list = list()
            for grid in range(1, 21):
                if grid in grid_list:
                    user_grid_prob_list.append(1 / len(grid_list))
                else:
                    user_grid_prob_list.append(0)
            res_prob_list = [grid_dict_prob * grid_user_prob for grid_dict_prob, grid_user_prob in
                             zip(grid_prob_dict, user_grid_prob_list)]
            norm_res_prob_list = [prob / sum(res_prob_list) for prob in res_prob_list]
            reports_mode = choose_item_from_non_normalized_probabilities(norm_res_prob_list)
            if reports_mode == true_value:
                probability_per_user.append(1)
            else:
                probability_per_user.append(0)
        else:
            probability_per_user.append(0)

    return sum(probability_per_user) / (len(user_values_list))
