import math


def find_coordinate(grid_number):
    if grid_number % 4 == 0:
        i = int(grid_number / 4) - 1
        j = 3
    else:
        i = int(grid_number / 4)
        j = (grid_number % 4) - 1

    return i, j


def find_path_distance(user_values_list, guess_values_list):
    error_sum = 0

    for user_values, guess_values in zip(user_values_list, guess_values_list):
        for element_index in range(len(user_values)):
            userX, userY = find_coordinate(user_values[element_index])
            guessX, guessY = find_coordinate(guess_values[element_index])

            error_sum += math.sqrt(((guessX - userX) ** 2) + (guessY - userY) ** 2)

        error_sum /= len(user_values)

    return error_sum


def ratio_of_guess(true_value_list, guess_value_list):
    prob_sum = 0
    index_counter = 0

    for guess_value, true_value in zip(guess_value_list, true_value_list):
        if guess_value == true_value:
            prob_sum += 1
        index_counter += 1

    return prob_sum / index_counter
