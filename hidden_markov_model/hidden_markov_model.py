import xxhash
from hmmlearn import hmm
import numpy as np

from dataset.analysis.dataset_analysis import analyze_taken_path

states = [
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "10",
    "11",
    "12",
    "13",
    "14",
    "15",
    "16",
    "17",
    "18",
    "19",
    "20",
]
observations = [
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "10",
    "11",
    "12",
    "13",
    "14",
    "15",
    "16",
    "17",
    "18",
    "19",
    "20",
]


def isValidPos(i, j, n, m):
    if i < 0 or j < 0 or i > n - 1 or j > m - 1:
        return 0
    return 1


# Function that returns all adjacent elements
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


def guess(model, user_perturbed_report):
    obs_sequence_list = []
    for perturbed_report in user_perturbed_report:
        obs_sequence_list.append(perturbed_report)
    obs_sequence = np.array([obs_sequence_list]).T

    _, state_sequence = model.decode(obs_sequence)

    for i in range(len(state_sequence)):
        state_sequence[i] = state_sequence[i] + 1

    return state_sequence


def hmm_model_GRR(epsilon, k, train_type, user_value_list=None):
    p = np.exp(epsilon) / (np.exp(epsilon) + k - 1)
    q = (1 - p) / (k - 1)

    discrete_model = hmm.MultinomialHMM(
        n_components=k,
        algorithm="viterbi",  # decoder algorithm.
    )

    if train_type == "plain":
        discrete_model.startprob_ = np.array([1 / k] * k)
        adjacent_matrix = np.arange(20).reshape(5, 4)
        matrix_list = []
        for i in range(1, k + 1):
            sub_list = []
            adjacent_elements = getAdjacent(adjacent_matrix, i)
            for j in range(1, k + 1):
                if j in adjacent_elements or j == i:
                    sub_list.append(1 / (len(adjacent_elements) + 1))
                else:
                    sub_list.append(0)
            matrix_list.append(sub_list)
        discrete_model.transmat_ = np.array(matrix_list)
    elif train_type == "advance":
        dict_of_path = analyze_taken_path(user_value_list)

        start_grid_dict = {}
        for user_true_values in user_value_list:
            init_grid = user_true_values.item(0)
            start_grid_dict[init_grid] = start_grid_dict.get(init_grid, 0) + 1

        start_grid_dict = dict(sorted(start_grid_dict.items()))
        sum_grid_counts = sum(start_grid_dict.values())
        start_prob_list = list()
        for grid_count in start_grid_dict.values():
            start_prob_list.append(grid_count / sum_grid_counts)

        for _ in range(k - len(start_prob_list)):
            start_prob_list.append(0)

        discrete_model.startprob_ = np.array(start_prob_list)

        adjacent_matrix = np.arange(20).reshape(5, 4)
        matrix_list = []
        for i in range(1, k + 1):
            sub_list = []
            adjacent_elements = getAdjacent(adjacent_matrix, i)
            sum_of_path = 0
            if i in dict_of_path and i in dict_of_path[i]:
                sum_of_path = dict_of_path[i][i]
            else:
                dict_of_path[i] = {}
                dict_of_path[i][i] = 1
                sum_of_path += 1
            for element in adjacent_elements:
                if element in dict_of_path[i]:
                    sum_of_path += dict_of_path[i][element]
                else:
                    dict_of_path[i][element] = 1
                    sum_of_path += 1
            for j in range(1, k + 1):
                if (j in adjacent_elements or j == i) and (j in dict_of_path[i]):
                    taken_path = dict_of_path[i][j]
                    sub_list.append(taken_path / sum_of_path)
                else:
                    sub_list.append(0)
            matrix_list.append(sub_list)

        discrete_model.transmat_ = np.array(matrix_list)

    matrix_list = []
    for i in range(k):
        row_list = []
        for j in range(k):
            if i == j:
                row_list.append(p)
            else:
                row_list.append(q)
        matrix_list.append(row_list)

    discrete_model.emissionprob_ = np.array(matrix_list)

    return discrete_model


def hmm_model_RAPPOR(epsilon, k, train_type, user_value_list=None):
    p = np.exp(epsilon / 2) / (np.exp(epsilon / 2) + 1)
    q = 1 / (np.exp(epsilon / 2) + 1)

    model = hmm.MultinomialHMM(n_components=k, algorithm="viterbi")

    if train_type == "plain":
        model.startprob_ = np.array([1 / k] * k)

        adjacent_matrix = np.arange(k).reshape(5, 4)
        transmat_prob_list = []
        for i in range(1, k + 1):
            sub_list = []
            adjacent_elements = getAdjacent(adjacent_matrix, i)
            for j in range(1, k + 1):
                if j in adjacent_elements or j == i:
                    sub_list.append(1 / (len(adjacent_elements) + 1))
                else:
                    sub_list.append(0)
            transmat_prob_list.append(sub_list)

        model.transmat_ = np.array(transmat_prob_list)

    elif train_type == "advance":
        dict_of_path = analyze_taken_path(user_value_list)

        start_grid_dict = {}
        for user_true_values in user_value_list:
            init_grid = user_true_values.item(0)
            start_grid_dict[init_grid] = start_grid_dict.get(init_grid, 0) + 1

        start_grid_dict = dict(sorted(start_grid_dict.items()))
        sum_grid_counts = sum(start_grid_dict.values())
        start_prob_list = list()
        for grid_count in start_grid_dict.values():
            start_prob_list.append(grid_count / sum_grid_counts)

        for _ in range(k - len(start_prob_list)):
            start_prob_list.append(0)

        model.startprob_ = np.array(start_prob_list)

        adjacent_matrix = np.arange(20).reshape(5, 4)
        matrix_list = []
        for i in range(1, k + 1):
            sub_list = []
            adjacent_elements = getAdjacent(adjacent_matrix, i)
            sum_of_path = 0
            if i in dict_of_path and i in dict_of_path[i]:
                sum_of_path = dict_of_path[i][i]
            else:
                if i in dict_of_path:
                    dict_of_path[i][i] = 1
                else:
                    dict_of_path[i] = {}
                    dict_of_path[i][i] = 1
                sum_of_path += 1
            for element in adjacent_elements:
                if element in dict_of_path[i]:
                    sum_of_path += dict_of_path[i][element]
                else:
                    dict_of_path[i][element] = 1
                    sum_of_path += 1
            for j in range(1, k + 1):
                if (j in adjacent_elements or j == i) and (j in dict_of_path[i]):
                    taken_path = dict_of_path[i][j]
                    sub_list.append(taken_path / sum_of_path)
                else:
                    sub_list.append(0)
            matrix_list.append(sub_list)

        model.transmat_ = np.array(matrix_list)

    rappor_report_list = list()
    for x in range(2**k):
        rappor_report_list.append((bin(x)[2:].zfill(k)))

    user_value_list = list()
    for i in range(k):
        bit_vector = ""
        for j in range(k):
            if i == j:
                bit_vector += "1"
            else:
                bit_vector += "0"
        user_value_list.append(bit_vector)

    emission_prob_list = list()
    for row_index in range(len(user_value_list)):
        row = user_value_list[row_index]
        row_prob_list = list()
        for column_index in range(len(rappor_report_list)):
            column = rappor_report_list[column_index]
            prob = 1
            for char_index in range(len(row)):
                if row[char_index] == column[char_index]:
                    prob *= p
                else:
                    prob *= q
            row_prob_list.append(prob)
        emission_prob_list.append(row_prob_list)

    model.emissionprob_ = np.array(emission_prob_list)

    return model


def hmm_model_OUE(epsilon, k, train_type, user_value_list=None):
    p = 1 / 2
    q = 1 / (np.exp(epsilon) + 1)

    model = hmm.MultinomialHMM(n_components=k, algorithm="viterbi")

    if train_type == "plain":
        model.startprob_ = np.array([1 / k] * k)

        adjacent_matrix = np.arange(k).reshape(5, 4)
        transmat_prob_list = []
        for i in range(1, k + 1):
            sub_list = []
            adjacent_elements = getAdjacent(adjacent_matrix, i)
            for j in range(1, k + 1):
                if j in adjacent_elements or j == i:
                    sub_list.append(1 / (len(adjacent_elements) + 1))
                else:
                    sub_list.append(0)
            transmat_prob_list.append(sub_list)

        model.transmat_ = np.array(transmat_prob_list)

    elif train_type == "advance":
        dict_of_path = analyze_taken_path(user_value_list)

        start_grid_dict = {}
        for user_true_values in user_value_list:
            init_grid = user_true_values.item(0)
            start_grid_dict[init_grid] = start_grid_dict.get(init_grid, 0) + 1

        start_grid_dict = dict(sorted(start_grid_dict.items()))
        sum_grid_counts = sum(start_grid_dict.values())
        start_prob_list = list()
        for grid_count in start_grid_dict.values():
            start_prob_list.append(grid_count / sum_grid_counts)

        for _ in range(k - len(start_prob_list)):
            start_prob_list.append(0)

        model.startprob_ = np.array(start_prob_list)

        adjacent_matrix = np.arange(20).reshape(5, 4)
        matrix_list = []
        for i in range(1, k + 1):
            sub_list = []
            adjacent_elements = getAdjacent(adjacent_matrix, i)
            sum_of_path = 0
            if i in dict_of_path and i in dict_of_path[i]:
                sum_of_path = dict_of_path[i][i]
            else:
                dict_of_path[i] = {}
                dict_of_path[i][i] = 1
                sum_of_path += 1
            for element in adjacent_elements:
                if element in dict_of_path[i]:
                    sum_of_path += dict_of_path[i][element]
                else:
                    dict_of_path[i][element] = 1
                    sum_of_path += 1
            for j in range(1, k + 1):
                if (j in adjacent_elements or j == i) and (j in dict_of_path[i]):
                    taken_path = dict_of_path[i][j]
                    sub_list.append(taken_path / sum_of_path)
                else:
                    sub_list.append(0)
            matrix_list.append(sub_list)

        model.transmat_ = np.array(matrix_list)

    oue_report_list = list()
    for x in range(2**k):
        oue_report_list.append((bin(x)[2:].zfill(k)))

    user_value_list = list()
    for i in range(k):
        bit_vector = ""
        for j in range(k):
            if i == j:
                bit_vector += "1"
            else:
                bit_vector += "0"
        user_value_list.append(bit_vector)

    emission_prob_list = list()
    for row_index in range(len(user_value_list)):
        row = user_value_list[row_index]
        row_prob_list = list()
        for column_index in range(len(oue_report_list)):
            column = oue_report_list[column_index]
            prob = 1
            for char_index in range(len(row)):
                if row[char_index] == "1":
                    if row[char_index] == column[char_index]:
                        prob *= p
                    else:
                        prob *= 1 - p
                else:
                    if row[char_index] == column[char_index]:
                        prob *= 1 - q
                    else:
                        prob *= q
            row_prob_list.append(prob)
        emission_prob_list.append(row_prob_list)

    model.emissionprob_ = np.array(emission_prob_list)

    return model


def hmm_model_OLH(epsilon, k, seed_counter, train_type, user_value_list=None):
    p = np.exp(epsilon) / (np.exp(epsilon) + k - 1)
    g = int(round(np.exp(epsilon))) + 1
    q = (1 - p) / (g - 1)

    model = hmm.MultinomialHMM(n_components=k, algorithm="viterbi")

    if train_type == "plain":
        model.startprob_ = np.full((1, k), 1 / k)[0]
        adjacent_matrix = np.arange(20).reshape(5, 4)
        matrix_list = []
        for obs_state in range(1, k + 1):
            sub_list = []
            adjacent_elements = getAdjacent(adjacent_matrix, obs_state)
            for hidden_state in range(1, k + 1):
                if hidden_state in adjacent_elements or hidden_state == obs_state:
                    sub_list.append(1 / (len(adjacent_elements) + 1))
                else:
                    sub_list.append(0)
            matrix_list.append(sub_list)

        model.transmat_ = np.array(matrix_list)

    elif train_type == "advance":
        dict_of_path = analyze_taken_path(user_value_list)

        start_grid_dict = {}
        for user_true_values in user_value_list:
            init_grid = user_true_values.item(0)
            start_grid_dict[init_grid] = start_grid_dict.get(init_grid, 0) + 1

        start_grid_dict = dict(sorted(start_grid_dict.items()))
        sum_grid_counts = sum(start_grid_dict.values())
        start_prob_list = list()
        for grid_count in start_grid_dict.values():
            start_prob_list.append(grid_count / sum_grid_counts)

        for _ in range(k - len(start_prob_list)):
            start_prob_list.append(0)

        model.startprob_ = np.array(start_prob_list)

        adjacent_matrix = np.arange(20).reshape(5, 4)
        matrix_list = []
        for i in range(1, k + 1):
            sub_list = []
            adjacent_elements = getAdjacent(adjacent_matrix, i)
            sum_of_path = 0
            if i in dict_of_path and i in dict_of_path[i]:
                sum_of_path = dict_of_path[i][i]
            else:
                dict_of_path[i] = {}
                dict_of_path[i][i] = 1
                sum_of_path += 1
            for element in adjacent_elements:
                if element in dict_of_path[i]:
                    sum_of_path += dict_of_path[i][element]
                else:
                    dict_of_path[i][element] = 1
                    sum_of_path += 1
            for j in range(1, k + 1):
                if (j in adjacent_elements or j == i) and (j in dict_of_path[i]):
                    taken_path = dict_of_path[i][j]
                    sub_list.append(taken_path / sum_of_path)
                else:
                    sub_list.append(0)
            matrix_list.append(sub_list)

        model.transmat_ = np.array(matrix_list)

    matrix_list = []
    for obs_state in range(k):
        row_list = []
        hash_value_of_obs_state = (
            xxhash.xxh32(str(obs_state), seed=seed_counter).intdigest() % g
        )
        for hidden_state in range(g):
            if hash_value_of_obs_state == hidden_state:
                row_list.append(p)
            else:
                row_list.append(q)
        matrix_list.append(row_list)

    model.emissionprob_ = np.array(matrix_list)

    return model


def hmm_model_GRR_MEMOIZED(epsilon, k):
    p = np.exp(epsilon) / (np.exp(epsilon) + k - 1)
    q = (1 - p) / (k - 1)

    discrete_model = hmm.MultinomialHMM(
        n_components=k,
        algorithm="viterbi",  # decoder algorithm.
    )
    discrete_model.startprob_ = np.array([1 / k] * k)
    adjacent_matrix = np.arange(20).reshape(5, 4)
    matrix_list = []
    for i in range(1, k + 1):
        sub_list = []
        adjacent_elements = getAdjacent(adjacent_matrix, i)
        for j in range(1, k + 1):
            if j in adjacent_elements or j == i:
                sub_list.append(1 / (len(adjacent_elements) + 1))
            else:
                sub_list.append(0)
        matrix_list.append(sub_list)
    discrete_model.transmat_ = np.array(matrix_list)

    matrix_list = []
    for i in range(k):
        row_list = []
        for j in range(k):
            if i == j:
                row_list.append((p**2) + ((k - 1) * (q**2)))
            else:
                row_list.append((2 * p * q) + ((k - 2) * (q**2)))
        matrix_list.append(row_list)

    discrete_model.emissionprob_ = np.array(matrix_list)

    return discrete_model
