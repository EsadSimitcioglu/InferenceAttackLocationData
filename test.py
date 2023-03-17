import csv

import xxhash
from hmmlearn import hmm
import numpy as np


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


epsilon = 10
k = 20
p = np.exp(epsilon) / (np.exp(epsilon) + k - 1)
g = int(round(np.exp(epsilon))) + 1
q = (1 - p) / (k - 1)


def create_model(seed_counter):
    # create an HMM object with precomputed start probabilities, transition probabilities, and emission probabilities
    model = hmm.MultinomialHMM(n_components=k)

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

    matrix_list = []
    for obs_state in range(1, k + 1):
        row_list = []
        hash_value_of_obs_state = (xxhash.xxh32(str(obs_state), seed=seed_counter).intdigest() % g)
        for hidden_state in range(g):
            if hash_value_of_obs_state == hidden_state:
                row_list.append(p)
            else:
                row_list.append(q)
        matrix_list.append(row_list)
    model.emissionprob_ = np.array(matrix_list)
    return model

users_grid_value_list = list()
guess_prob_list = list()
with open('grid/taxi_test_different_grid.dat') as f:
    reader = csv.reader(f, delimiter="\t")
    for line in reader:
        grid_list = line[0].split(" ")
        grid_list_int = [eval(i) for i in grid_list]
        grid_list_int_nd = np.array(grid_list_int)
        users_grid_value_list.append(grid_list_int_nd)

seed_counter = 1
for user_values in users_grid_value_list:
    for true_value in user_values:
        hash_value_of_obs_state = (xxhash.xxh32(str(true_value), seed=seed_counter).intdigest() % g)
        model = create_model(seed_counter)
        report_value = (xxhash.xxh32(str(true_value), seed=seed_counter).intdigest() % g)
        rnd = np.random.random()
        if rnd > p:
            report_value = np.random.randint(0, g)
        obs_sequence_list = [report_value]
        obs_sequence = np.array([obs_sequence_list]).T
        _, state_sequence = model.decode(obs_sequence)
        if hash_value_of_obs_state == obs_sequence[0][0]:
            guess_prob_list.append(1)
        else:
            guess_prob_list.append(0)
        print("True Value: " + str(hash_value_of_obs_state) + " , Guess Value: " + str(obs_sequence[0]))
        seed_counter += 1

print(np.average(guess_prob_list))