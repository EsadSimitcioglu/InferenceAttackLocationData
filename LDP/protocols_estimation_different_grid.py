import json

import numpy as np

from LDP.protocols import GRR_Client

row_count = 4


def analyze_taken_path(users_value_list):
    path_dict = {}
    for user_value in users_value_list:
        for value_index,value in enumerate(user_value):
            if value_index == 0:
                continue

            prev_grid = user_value[value_index - 1]

            if value == prev_grid:
                continue

            path = str(prev_grid) + "->" + str(value)

            if path in path_dict:
                path_dict[path] += 1
            else:
                path_dict[path] = 1

    return {k: v for k, v in sorted(path_dict.items(), key=lambda item: item[1], reverse= True)}

def analyze_not_taken_path(users_value_list):

    for column in range(1,5):
        for row in range(1,6):

            pass



        print("\n")

def check_possibility(perturb_value_list, row_count):
    possibility_list = list()

    for value_index, value in enumerate(perturb_value_list):
        if value_index == 0:
            possibility_list.append(1)
            continue

        prev_grid_location = perturb_value_list[value_index - 1]

        if (value - 1 <= prev_grid_location <= value + 1) or \
                (value - row_count - 1 <= prev_grid_location <= value - row_count + 1) or \
                (value + row_count - 1 <= prev_grid_location <= value + row_count + 1):
            possibility_list.append(1)
        else:
            possibility_list.append(0)

    return possibility_list


def grr_estimated_guess(user_values_list, k, epsilon):
    average_zero_count = 0

    for user_true_values in user_values_list:
        grr_reports = [GRR_Client(user_true_value, k, epsilon) for user_true_value in user_true_values]
        possibility_list = check_possibility(grr_reports, row_count)
        zero_count = possibility_list.count(0)
        average_zero_count += zero_count
        print("****************************************************")
        print(user_true_values)
        print(grr_reports)
        print(possibility_list)
        print("Number of 0: " + str(zero_count))

    average_zero_count /= len(user_values_list)
    return average_zero_count


# Parameters for simulation
n = 20  # number of timestamps
k = 20  # attribute's domain size (grid size)
epsilon_list = [0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 5]  # number of epsilon for test cases
users_grid_value_list = list()
probability_of_guess_grr = list()

for line in open('../grid/taxi.dat'):
    lst_int = [int(x) for x in line.split()]
    users_grid_value_list.append(lst_int)

analyzed_path_dict = analyze_taken_path(users_grid_value_list)
analyze_not_taken_path(users_grid_value_list)



with open('../grid/taxi_path.dat', 'w') as convert_file:
    for element in analyzed_path_dict.items():
        convert_file.write(json.dumps(element) + "\n")

"""
for epsilon in epsilon_list:
    print("-----------------------------------------------------")
    print("Epsilon: " + str(epsilon))
    average_zero_count = grr_estimated_guess(users_grid_value_list, k, epsilon)
    print("Average of 0: " + str(average_zero_count))
"""