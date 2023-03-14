import numpy as np
from hmmlearn import hmm

epsilon =1
k = 8
p = np.exp(epsilon / 2) / (np.exp(epsilon / 2) + 1)
q = 1 / (np.exp(epsilon / 2) + 1)
seed = 93
np.random.seed(seed)

states = ["1", "2", "3", "4", "5", "6", "7", "8"]

observations = list()
for x in range(256):
    observations.append((bin(x)[2:].zfill(8)))


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


def binary_to_decimal(binary_number):
    decimal_number = 0
    index_counter = len(binary_number) - 1

    for number in binary_number:
        decimal_number += (int(number) * (2 ** index_counter))
        index_counter -= 1
    return decimal_number


adjacent_matrix = np.arange(8).reshape(2, 4)
transmat_prob_list = []
for i in range(1, 8 + 1):
    sub_list = []
    adjacent_elements = getAdjacent(adjacent_matrix, i)
    for j in range(1, 8 + 1):
        if j in adjacent_elements or j == i:
            sub_list.append(1 / (len(adjacent_elements) + 1))
        else:
            sub_list.append(0)
    transmat_prob_list.append(sub_list)

rappor_report_list = list()
for x in range(256):
    rappor_report_list.append((bin(x)[2:].zfill(8)))

user_value_list = list()
for i in range(8):
    bit_vector = ''
    for j in range(8):
        if i == j:
            bit_vector += '1'
        else:
            bit_vector += '0'
    user_value_list.append(bit_vector)

emission_prob_list = list()
for row_index in range(len(user_value_list)):
    row = rappor_report_list[row_index]
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

model = hmm.MultinomialHMM(n_components=8, algorithm='viterbi', random_state=seed)
model.startprob_ = np.array([1 / 8] * 8)
model.transmat_ = np.array(transmat_prob_list)
model.emissionprob_ = np.array(emission_prob_list)

user_values = [3, 3, 3, 3, 3, 3]
grr_reports = [1, 51, 172, 256, 64, 209]
obs_sequence_list = []
for grr_report in grr_reports:
    obs_sequence_list.append(grr_report - 1)
obs_sequence = np.array([obs_sequence_list]).T
# Find most likely state sequence corresponding to obs_sequence
logprob, state_sequence = model.decode(obs_sequence)

prob_sum = 0
index_counter = 0

for o, s in zip(obs_sequence.T[0], state_sequence):
    true_value = user_values[index_counter]
    if int(states[int(s)]) == true_value:
        prob_sum += 1
    index_counter += 1
    print("{} -> {}".format(states[int(s)], true_value))
print(prob_sum / len(user_values))
