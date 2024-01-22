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
