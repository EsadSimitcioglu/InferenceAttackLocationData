from hmmlearn import hmm
import numpy as np


def isValidPos(i, j, n, m):
    if i < 0 or j < 0 or i > n - 1 or j > m - 1:
        return 0
    return 1


# Function that returns all adjacent elements
def getAdjacent(arr, number):
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


def hmm_model_GRR(epsilon, k):
    seed = 90
    p = np.exp(epsilon) / (np.exp(epsilon) + k - 1)
    q = (1 - p) / (k - 1)

    discrete_model = hmm.MultinomialHMM(n_components=k,
                                        algorithm='viterbi',  # decoder algorithm.
                                        random_state=seed,
                                        )

    discrete_model.startprob_ = np.full((1, k), 1 / k)[0]
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
                row_list.append(p)
            else:
                row_list.append(q)
        matrix_list.append(row_list)

    discrete_model.emissionprob_ = np.array(matrix_list)

    return discrete_model


discrete_model = hmm_model_GRR(1, 20)
