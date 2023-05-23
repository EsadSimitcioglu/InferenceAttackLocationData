import numpy as np
from statistics import mode

from LDP.estimation_different_grid import experiment, perturb
from LDP.protocols import GRR_Client
from hidden_markov_model.hidden_markov_model import hmm_model_GRR, hmm_model_RAPPOR, hmm_model_OUE, hmm_model_OLH

states = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20"]


def create_adjacent_lists(lst):
    result = []
    current_list = []
    previous_element = lst[0]

    for index, element in enumerate(lst):
        if len(current_list) == 0 and element == previous_element:
            current_list.append(index)
        elif element != previous_element:
            current_list.append(index)
            result.append(current_list)
            current_list = [index]

        previous_element = element

    if current_list:
        current_list.append(len(lst) - 1)
        result.append(current_list)

    return result


def grr_estimated_guess_same_grid(user_values_list, k, epsilon):
    guess_value_list = list()
    grid_number = user_values_list[0]
    grr_reports = [GRR_Client(user_true_value, k, epsilon) for user_true_value in user_values_list]
    grr_reports_mode = mode(grr_reports)
    return grr_reports_mode


def grr_estimated_guess_different_grid(user_perturbed_report, model):
    obs_sequence_list = []
    for perturbed_report in user_perturbed_report:
        obs_sequence_list.append(perturbed_report - 1)
    obs_sequence = np.array([obs_sequence_list]).T

    _, state_sequence = model.decode(obs_sequence)

    user_guess_list = list()
    for o, s in zip(obs_sequence.T[0], state_sequence):
        guess_value = (s + 1)
        user_guess_list.append(guess_value)

    return user_guess_list


def grr_estimate_guess(perturbed_reports, model):
    for index, user_perturbed_report in enumerate(perturbed_reports):

        guess_prob_list = list()
        obs_sequence_list = []
        for perturbed_report in user_perturbed_report:
            obs_sequence_list.append(perturbed_report - 1)
        obs_sequence = np.array([obs_sequence_list]).T

        _, state_sequence = model.decode(obs_sequence)
        prob_sum = 0
        index_counter = 0

        for o, s in zip(obs_sequence.T[0], state_sequence):
            true_value = perturbed_reports[index][index_counter]
            guess_value = (s + 1)
            if guess_value == true_value:
                prob_sum += 1
            index_counter += 1
        guess_prob_list.append(prob_sum / index_counter)

        return guess_prob_list


def grr_estimated_guess_hybrid(user_values_list, k, epsilon, threshold):
    model = hmm_model_GRR(epsilon, k, 'plain')
    hmm_guess_list = experiment(epsilon, k, user_values_list, "GRR", 'advance', model)
    user_perturb_list = perturb("GRR", epsilon, k, user_values_list)

    true_guess = 0
    false_guess = 0

    for index, hmm_guess in enumerate(hmm_guess_list):
        user_true_values = user_values_list[index]
        user_perturb_values = user_perturb_list[index]
        same_grid_index = create_adjacent_lists(hmm_guess)

        user_hybrid_guess_list = []

        estimated_guess_list = grr_estimated_guess_different_grid(user_perturb_values, model)

        for [start_index, end_index] in same_grid_index:
            if end_index - start_index > threshold:
                guess_value = grr_estimated_guess_same_grid(user_perturb_values[start_index:end_index], k, epsilon)
                estimated_same_grid_guess_list = [guess_value] * (end_index - (start_index))
            else:
                estimated_same_grid_guess_list = estimated_guess_list[start_index:end_index]
            user_hybrid_guess_list.extend(estimated_same_grid_guess_list)

        for index, user_value in enumerate(user_true_values):

            if index >= len(user_hybrid_guess_list):
                break

            if user_hybrid_guess_list[index] == user_value:
                true_guess += 1
            else:
                false_guess += 1

    return true_guess / (true_guess + false_guess)