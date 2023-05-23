from LDP.estimation_same_grid import grr_estimated_guess_per_user
from LDP.estimation_different_grid import perturb
from hidden_markov_model.hidden_markov_model import hmm_model_GRR, guess


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
        current_list.append(len(lst))
        result.append(current_list)

    return result


def grr_estimated_guess_hybrid(user_values_list, k, epsilon, threshold):
    model = hmm_model_GRR(epsilon, k, 'plain')
    hmm_guess_list = list()
    user_perturb_list = perturb(protocol_type='GRR', epsilon=epsilon, k=k, user_true_value_list=user_values_list)

    for perturbed_value in user_perturb_list:
        hmm_guess_list.append(guess(model, perturbed_value))

    true_guess = 0
    false_guess = 0

    for hmm_guess_index, hmm_guess in enumerate(hmm_guess_list):
        user_true_values = user_values_list[hmm_guess_index]
        user_perturb_values = user_perturb_list[hmm_guess_index]
        same_grid_index = create_adjacent_lists(hmm_guess)

        user_hybrid_guess_list = []

        for [start_index, end_index] in same_grid_index:
            if end_index - start_index > threshold:
                guess_value = grr_estimated_guess_per_user(user_perturb_values[start_index: end_index], k, epsilon) + 2
                estimated_same_grid_guess_list = [guess_value] * (end_index - start_index)
            elif end_index - start_index == 1:
                estimated_same_grid_guess_list = [hmm_guess[start_index]]
            else:
                estimated_same_grid_guess_list = hmm_guess[start_index:end_index]
            user_hybrid_guess_list.extend(estimated_same_grid_guess_list)

        for user_value_index, user_value in enumerate(user_true_values):
            estimate = user_hybrid_guess_list[user_value_index]

            if user_value_index >= len(user_hybrid_guess_list):
                break

            if estimate == user_value:
                true_guess += 1
            else:
                false_guess += 1

    return true_guess / (true_guess + false_guess)
