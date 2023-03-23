import math


def find_coordinate(grid_number):
    if grid_number % 4 == 0:
        i = int(grid_number / 4) - 1
        j = 3
    else:
        i = int(grid_number / 4)
        j = (grid_number % 4) - 1

    return i, j


def find_path_distance(user_values, guess_values):
    error_sum = 0

    for element_index in range(len(user_values)):
        userX, userY = find_coordinate(user_values[element_index])
        guessX, guessY = find_coordinate(guess_values[element_index])

        error_sum += math.sqrt(((guessX - userX) ** 2) + (guessY - userY) ** 2)

    return error_sum / len(user_values)
