from statistics import mode

import numpy as np

from LDP.protocols import OUE_Client, OLH_Client, SIMPLE_RAPPOR_Client, GRR_Client, OLH_Client2


def grr_estimated_guess(user_values_list, k, epsilon):
    probability_per_user = list()
    for user_true_values in user_values_list:
        grid_number = user_true_values[0]
        grr_reports = [GRR_Client(user_true_value, k, epsilon) for user_true_value in user_true_values]
        grr_reports_mode = mode(grr_reports)
        count_of_mode = grr_reports.count(grr_reports_mode)
        count_of_user_value = grr_reports.count(grid_number)
        if count_of_mode == count_of_user_value or grr_reports_mode == grid_number:
            probability_per_user.append(1)
        else:
            probability_per_user.append(0)

    return sum(probability_per_user) / (len(user_values_list))


def rappor_estimated_guess(user_values_list, k, epsilon):
    probability_per_user = list()
    for user_true_values in user_values_list:
        grid_number = user_true_values[0] - 1
        rappor_reports = [SIMPLE_RAPPOR_Client(user_true_value, k, epsilon) for user_true_value in user_true_values]
        perturbed_bit_vectors = np.array(rappor_reports)
        sum_perturbed_bit_by_bit = sum(perturbed_bit_vectors)
        guess_of_grid = np.argmax(sum_perturbed_bit_by_bit)
        if guess_of_grid == grid_number or sum_perturbed_bit_by_bit[guess_of_grid] == sum_perturbed_bit_by_bit[
            grid_number]:
            probability_per_user.append(1)
        else:
            probability_per_user.append(0)
    return sum(probability_per_user) / (len(user_values_list))

def oue_estimated_guess(user_values_list, k, epsilon):
    probability_per_user = list()
    for user_true_values in user_values_list:
        grid_number = user_true_values[0] - 1
        oue_reports = [OUE_Client(user_true_value, k, epsilon) for user_true_value in user_true_values]
        perturbed_bit_vectors = np.array(oue_reports)
        sum_perturbed_bit_by_bit = sum(perturbed_bit_vectors)
        guess_of_grid = np.argmax(sum_perturbed_bit_by_bit)
        if guess_of_grid == grid_number or sum_perturbed_bit_by_bit[guess_of_grid] == sum_perturbed_bit_by_bit[
            grid_number]:
            probability_per_user.append(1)
        else:
            probability_per_user.append(0)
    return sum(probability_per_user) / (len(user_values_list))


def olh_estimated_guess(user_values_list, k, epsilon):
    olh_report_list = list()
    seed_init = 0
    for user_true_values in user_values_list:
        true_value = user_true_values[0]
        olh_reports = OLH_Client2(user_true_values, k, epsilon, seed_init)

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
            if not is_add:
                probability_list.append(0)
        olh_report_list.append(sum(probability_list) / (len(probability_list)))
        seed_init += 1

    return olh_report_list