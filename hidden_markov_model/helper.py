from collections import defaultdict

import numpy as np


def isValidPos(i, j, n, m):
    if i < 0 or j < 0 or i > n - 1 or j > m - 1:
        return 0
    return 1


def getAdjacent(arr, number):
    if number % 4 == 0:
        i = int(number / 4) - 1
        j = 3
    else:
        i = int(number / 4)
        j = (number % 4) - 1

    # Size of given 2d array
    n = len(arr)
    m = len(arr[0])

    # Initialising a vector array
    # where adjacent element will be stored
    v = []

    # Checking for all the possible adjacent positions
    if isValidPos(i - 1, j - 1, n, m):
        v.append(arr[i - 1][j - 1])
    if isValidPos(i - 1, j, n, m):
        v.append(arr[i - 1][j])
    if isValidPos(i - 1, j + 1, n, m):
        v.append(arr[i - 1][j + 1])
    if isValidPos(i, j - 1, n, m):
        v.append(arr[i][j - 1])
    if isValidPos(i, j + 1, n, m):
        v.append(arr[i][j + 1])
    if isValidPos(i + 1, j - 1, n, m):
        v.append(arr[i + 1][j - 1])
    if isValidPos(i + 1, j, n, m):
        v.append(arr[i + 1][j])
    if isValidPos(i + 1, j + 1, n, m):
        v.append(arr[i + 1][j + 1])

    # Returning the vector
    return [x + 1 for x in v]


def analyze_taken_path(users_grid_value_list):
    path_dict = {}
    for user_value in users_grid_value_list:
        for value_index, value in enumerate(user_value):
            if value_index == 0:
                continue

            prev_grid = user_value[value_index - 1]

            if prev_grid in path_dict:
                value_dict = path_dict.get(prev_grid)

                if value in value_dict:
                    value_dict[value] += 1
                else:
                    value_dict[value] = 1

            else:
                value_dict = {value: 1}
                path_dict[prev_grid] = value_dict

    return path_dict


def create_emission_matrix_rows(k):
    row_list = list()
    for x in range(2 ** k):
        row_list.append((bin(x)[2:].zfill(k)))
    return row_list


def create_emission_matrix_column(k):
    column_list = list()
    for i in range(k):
        bit_vector = ''
        for j in range(k):
            if i == j:
                bit_vector += '1'
            else:
                bit_vector += '0'
        column_list.append(bit_vector)
    return column_list


def ratio_of_guess(true_value_list, guess_value_list):
    prob_sum = 0
    index_counter = 0

    for guess_value, true_value in zip(guess_value_list, true_value_list):
        if guess_value == true_value:
            prob_sum += 1
        index_counter += 1

    return prob_sum / index_counter


def decimal_to_binary(decimal_num, k):
    if decimal_num == 0:
        return '0' * k
    binary_num = ''
    while decimal_num > 0:
        remainder = decimal_num % 2
        binary_num = str(remainder) + binary_num
        decimal_num = decimal_num // 2
    if len(binary_num) < k:
        padding = '0' * (k - len(binary_num))
        binary_num = padding + binary_num
    return binary_num


def create_rappor_emission_matrix(self, rappor, seed):
    row_value_list = create_emission_matrix_rows(self.k)

    column_value_list = create_emission_matrix_column(self.k)

    keep_bit_prob = ((rappor.p ** 2) + (rappor.q ** 2)) if rappor.is_memoized else rappor.p
    flip_bit_prob = (2 * rappor.p * rappor.q) if rappor.is_memoized else rappor.q

    order = 0
    emission_prob_list = list()
    for row_index in range(len(column_value_list)):
        row = column_value_list[row_index]
        row_prob_list = list()
        for column_index in range(len(row_value_list)):
            column = row_value_list[column_index]
            p_counter = 0
            q_counter = 0
            for char_index in range(len(row)):
                if row[char_index] == column[char_index]:
                    p_counter += 1
                else:
                    q_counter += 1

            row_prob_list.append((order, p_counter, q_counter))
            order += 1
        emission_prob_list.append(row_prob_list)

    order = -1
    order_prime = 0
    revised_column_dict_order = defaultdict(lambda: -1)
    q_counter_to_value_dict = defaultdict(lambda: -1)

    for column_index in range(len(emission_prob_list[0])):
        q_counter = 0
        for row_index in range(len(emission_prob_list)):
            element = emission_prob_list[row_index][column_index]
            q_counter += element[2]

        if q_counter <= (self.k // 4) * self.k:
            order += 1
            revised_column_dict_order[row_value_list[column_index]] = order
            q_counter_to_value_dict[row_value_list[column_index]] = order
        else:
            if order_prime == 0:
                order_prime = order + 1
                order += 1
                revised_column_dict_order[order_prime] = []
            revised_column_dict_order[order_prime].append(row_value_list[column_index])
            q_counter_to_value_dict[row_value_list[column_index]] = order_prime

    emission_prob_list = list()
    for row_index in range(len(column_value_list)):
        row = column_value_list[row_index]
        row_prob_list = list()

        prob_list = list()
        for column in revised_column_dict_order:
            prob = 1

            if column == order_prime:
                final_prob = 0
                for column_index in range(len(revised_column_dict_order[column])):
                    prob = 1
                    for char_index in range(len(row)):
                        if row[char_index] == revised_column_dict_order[column][column_index][char_index]:
                            prob *= keep_bit_prob
                        else:
                            prob *= flip_bit_prob
                    final_prob += prob
                row_prob_list.append(final_prob)
            else:
                for char_index in range(len(row)):
                    if row[char_index] == column[char_index]:
                        prob *= keep_bit_prob
                    else:
                        prob *= flip_bit_prob
                row_prob_list.append(prob)
        emission_prob_list.append(row_prob_list)

    self.dict_order = q_counter_to_value_dict
    self.model.emissionprob_ = np.array(emission_prob_list)
