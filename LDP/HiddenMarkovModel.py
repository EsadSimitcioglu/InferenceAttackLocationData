from hmmlearn import hmm
import numpy as np
from collections import Counter


def isValidPos(i, j, n, m):
    if (i < 0 or j < 0 or i > n - 1 or j > m - 1):
        return 0
    return 1


# Function that returns all adjacent elements
def getAdjacent(arr, i, j):
    # Size of given 2d array
    n = len(arr)
    m = len(arr[0])

    # Initialising a vector array
    # where adjacent element will be stored
    v = []

    # Checking for all the possible adjacent positions
    if (isValidPos(i - 1, j - 1, n, m)):
        v.append(arr[i - 1][j - 1])
    if (isValidPos(i - 1, j, n, m)):
        v.append(arr[i - 1][j])
    if (isValidPos(i - 1, j + 1, n, m)):
        v.append(arr[i - 1][j + 1])
    if (isValidPos(i, j - 1, n, m)):
        v.append(arr[i][j - 1])
    if (isValidPos(i, j + 1, n, m)):
        v.append(arr[i][j + 1])
    if (isValidPos(i + 1, j - 1, n, m)):
        v.append(arr[i + 1][j - 1])
    if (isValidPos(i + 1, j, n, m)):
        v.append(arr[i + 1][j])
    if (isValidPos(i + 1, j + 1, n, m)):
        v.append(arr[i + 1][j + 1])

    # Returning the vector
    return v


def hmm_model_GRR(epsilon, k):
    seed = 90
    np.random.seed(seed)

    p = np.exp(epsilon) / (np.exp(epsilon) + k - 1)
    q = (1 - p) / (k - 1)

    states = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
    observations = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]

    discrete_model = hmm.MultinomialHMM(n_components=9,
                                        algorithm='viterbi',  # decoder algorithm.
                                        random_state=seed,
                                        n_iter=10,
                                        tol=0.01  # EM convergence threshold (gain in log-likelihood)
                                        )

    discrete_model.startprob_ = np.array(
        [1 / 9, 1 / 9, 1 / 9, 1 / 9, 1 / 9, 1 / 9, 1 / 9, 1 / 9, 1 / 9]
    )

    discrete_model.transmat_ = np.array(
        [
            [1 / 4, 1 / 4, 0, 1 / 4, 1 / 4, 0, 0, 0, 0],
            [1 / 6, 1 / 6, 1 / 6, 1 / 6, 1 / 6, 1 / 6, 0, 0, 0],
            [0, 1 / 4, 1 / 4, 0, 1 / 4, 1 / 4, 0, 0, 0],
            [1 / 6, 1 / 6, 0, 1 / 6, 1 / 6, 0, 1 / 6, 1 / 6, 0],
            [1 / 9, 1 / 9, 1 / 9, 1 / 9, 1 / 9, 1 / 9, 1 / 9, 1 / 9, 1 / 9],
            [0, 1 / 6, 1 / 6, 0, 1 / 6, 1 / 6, 0, 1 / 6, 1 / 6],
            [0, 0, 0, 1 / 4, 1 / 4, 0, 1 / 4, 1 / 4, 0],
            [0, 0, 0, 1 / 6, 1 / 6, 1 / 6, 1 / 6, 1 / 6, 1 / 6],
            [0, 0, 0, 0, 1 / 4, 1 / 4, 0, 1 / 4, 1 / 4]
        ]
    )
    discrete_model.emissionprob_ = np.array(
        [
            [p, q, q, q, q, q, q, q, q],
            [q, p, q, q, q, q, q, q, q],
            [q, q, p, q, q, q, q, q, q],
            [q, q, q, p, q, q, q, q, q],
            [q, q, q, q, p, q, q, q, q],
            [q, q, q, q, q, p, q, q, q],
            [q, q, q, q, q, q, p, q, q],
            [q, q, q, q, q, q, q, p, q],
            [q, q, q, q, q, q, q, q, p],
        ]
    )

    return discrete_model

def hmm_model_GRR_20(epsilon, k):
    seed = 90
    np.random.seed(seed)

    p = np.exp(epsilon) / (np.exp(epsilon) + k - 1)
    q = (1 - p) / (k - 1)

    states = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
    observations = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]

    discrete_model = hmm.MultinomialHMM(n_components=9,
                                        algorithm='viterbi',  # decoder algorithm.
                                        random_state=seed,
                                        n_iter=10,
                                        tol=0.01  # EM convergence threshold (gain in log-likelihood)
                                        )

    discrete_model.startprob_ = np.array(
        [1 / 9, 1 / 9, 1 / 9, 1 / 9, 1 / 9, 1 / 9, 1 / 9, 1 / 9, 1 / 9]
    )
    discrete_model.transmat_ = np.array(
        [
            [1 / 4, 1 / 4, 0, 1 / 4, 1 / 4, 0, 0, 0, 0],
            [1 / 6, 1 / 6, 1 / 6, 1 / 6, 1 / 6, 1 / 6, 0, 0, 0],
            [0, 1 / 4, 1 / 4, 0, 1 / 4, 1 / 4, 0, 0, 0],
            [1 / 6, 1 / 6, 0, 1 / 6, 1 / 6, 0, 1 / 6, 1 / 6, 0],
            [1 / 9, 1 / 9, 1 / 9, 1 / 9, 1 / 9, 1 / 9, 1 / 9, 1 / 9, 1 / 9],
            [0, 1 / 6, 1 / 6, 0, 1 / 6, 1 / 6, 0, 1 / 6, 1 / 6],
            [0, 0, 0, 1 / 4, 1 / 4, 0, 1 / 4, 1 / 4, 0],
            [0, 0, 0, 1 / 6, 1 / 6, 1 / 6, 1 / 6, 1 / 6, 1 / 6],
            [0, 0, 0, 0, 1 / 4, 1 / 4, 0, 1 / 4, 1 / 4]
        ]
    )
    discrete_model.emissionprob_ = np.array(
        [
            [p / 4, p / 4 + q, q, p / 4 + q, p / 4 + q, q, q, q, q],
            [p / 6 + q, p / 6, p / 6 + q, p / 6 + q, p / 6 + q, p / 6 + q, q, q, q],
            [q, p / 4 + q, p / 4, q, p / 4 + q, p / 4 + q, q, q, q],
            [p / 6 + q, p / 6 + q, q, p / 6, p / 6 + q, q, p / 6 + q, p / 6 + q, q], \
            [p / 9 + q, p / 9 + q, p / 9 + q, p / 9 + q, p / 9, p / 9 + q, p / 9 + q, p / 9 + q, p / 9 + q],
            [q, p / 6 + q, p / 6 + q, q, p / 6 + q, p / 6, q, p / 6 + q, p / 6 + q],
            [q, q, q, p / 4 + q, p / 4 + q, q, p / 4, p / 4 + q, q],
            [q, q, q, p / 6 + q, p / 6 + q, p / 6 + q, p / 6 + q, p / 6, p / 6 + q],
            [q, q, q, q, p / 4 + q, p / 4 + q, q, p / 4 + q, p / 4],
        ]
    )

    return discrete_model
