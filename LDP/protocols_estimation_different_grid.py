import numpy as np
from hidden_markov_model import hmm_model_GRR
from LDP.protocols import GRR_Client, SIMPLE_RAPPOR_Client

states = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20"]
observations = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19",
                "20"]


def grr_estimated_guess(user_values_list, k, epsilon):
    model = hmm_model_GRR(epsilon, k)
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


def rappor_estimated_guess(user_values_list, k, epsilon):
    epsilon = 5
    probability_per_user = list()
    for user_true_values in user_values_list:
        grid_number = user_true_values[0] - 1
        rappor_reports = [SIMPLE_RAPPOR_Client(user_true_value, k, epsilon) for user_true_value in user_true_values]
        perturbed_bit_vectors = np.array(rappor_reports)
        sum_perturbed_bit_by_bit = sum(perturbed_bit_vectors)
        perturbed = np.argmax(sum_perturbed_bit_by_bit)


        if guess_of_grid == grid_number or sum_perturbed_bit_by_bit[guess_of_grid] == sum_perturbed_bit_by_bit[
            grid_number]:
            probability_per_user.append(1)
        else:
            probability_per_user.append(0)
    return sum(probability_per_user) / (len(user_values_list))
