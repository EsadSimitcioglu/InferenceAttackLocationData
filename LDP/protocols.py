import numpy
import numpy as np
import xxhash
from sys import maxsize

# [1] Erlingsson, Pihur, and Korolova (2014) "RAPPOR: Randomized aggregatable privacy-preserving ordinal response" (ACM CCS).
# [2] Arcolezi et al (2022) "Improving the Utility of Locally Differentially Private Protocols for Longitudinal and Multidimensional Frequency Estimates" (Digital Communications and Networks).
# [3] Ding, Kulkarni, and Yekhanin (2017) "Collecting telemetry data privately." (NeurIPS).
from numpy import exp

seeds = np.arange(200)
seed_counter = 0


def setting_seed(seed):
    """ Function to set seed for reproducibility.
    Calling numpy.random.seed() from interpreted code will 
    seed the NumPy random generator, not the Numba random generator.
    Check: https://numba.readthedocs.io/en/stable/reference/numpysupported.html"""

    np.random.seed(seed)


def GRR_Client(input_data, k, epsilon):
    """
    Generalized Randomized Response (GRR) protocol, a.k.a., direct encoding [1] or k-RR [2].
    :param input_data: user's true value;
    :param k: attribute's domain size;
    :param epsilon: privacy guarantee;
    :return: sanitized value.
    """

    if epsilon is not None or k is not None:

        # GRR parameters
        p = np.exp(epsilon) / (np.exp(epsilon) + k - 1)

        # Mapping domain size k to the range [0, ..., k-1]
        domain = np.arange(1, k + 1)

        # GRR perturbation function
        rnd = np.random.random()
        if rnd <= p:
            return input_data - 1
        else:
            return np.random.choice(domain[domain != input_data] - 1)

    else:
        raise ValueError('k (int) and epsilon (float) need a numerical value.')


def GRR_Aggregator(reports, k, epsilon):
    """
    Statistical Estimator for Normalized Frequency (0 -- 1) with post-processing to ensure non-negativity.
    :param reports: list of all GRR-based sanitized values;
    :param k: attribute's domain size;
    :param epsilon: privacy guarantee;
    :return: normalized frequency (histogram) estimation.
    """

    if len(reports) == 0:

        raise ValueError('List of reports is empty.')

    else:

        if epsilon is not None or k is not None:

            # Number of reports
            n = len(reports)

            # GRR parameters
            p = np.exp(epsilon) / (np.exp(epsilon) + k - 1)
            q = (1 - p) / (k - 1)

            # Count how many times each value has been reported
            count_report = np.zeros(k)
            for rep in reports:
                count_report[rep] += 1

            # Ensure non-negativity of estimated frequency
            est_freq = np.array((count_report - n * q) / (p - q)).clip(0)

            # Re-normalized estimated frequency
            norm_est_freq = np.nan_to_num(est_freq / sum(est_freq))

            return norm_est_freq

        else:
            raise ValueError('k (int) and epsilon (float) need a numerical value.')


def GRR_MEMOIZATION_Client(input_list, k, epsilon):
    """
        Generalized Randomized Response (GRR) protocol, a.k.a., direct encoding [1] or k-RR [2].
        :param input_data: user's true value;
        :param k: attribute's domain size;
        :param epsilon: privacy guarantee;
        :return: sanitized value.
        """

    perturbed_list = []

    for user_trajectory in input_list:
        user_list = list()
        memoization_dict = {}
        prev_value = -1
        for input_data in user_trajectory:
            if input_data == prev_value:
                if input_data not in memoization_dict:
                    memoization_dict[input_data] = GRR_Client(input_data, k, epsilon)
                else:
                    user_list.append(memoization_dict[input_data])
            else:
                user_list.append(GRR_Client(input_data, k, epsilon))
            prev_value = input_data
        perturbed_list.append(user_list)

    return perturbed_list

def SIMPLE_RAPPOR_Client(input_data, k, epsilon):
    bit_vector = np.zeros(k)
    bit_vector[input_data - 1] = 1

    p = (np.exp(epsilon / 2)) / (np.exp(epsilon / 2) + 1)

    perturbed_bit_vector = bit_vector.copy()
    for bit_index in range(len(bit_vector)):
        rnd = np.random.random()
        if rnd > p:
            if perturbed_bit_vector[bit_index] == 1:
                perturbed_bit_vector[bit_index] = 0
            else:
                perturbed_bit_vector[bit_index] = 1

    perturbed_bit_vector = perturbed_bit_vector.tolist()
    return perturbed_bit_vector


def SIMPLE_RAPPOR_Aggregator(perturbed_bit_vectors, epsilon):
    perturbed_bit_vectors = numpy.array(perturbed_bit_vectors)
    n = 2
    p = (np.exp(epsilon / 2)) / (np.exp(epsilon / 2) + 1)
    q = 1 / (np.exp(epsilon / 2) + 1)
    perturbed_sum_bit_vector = sum(perturbed_bit_vectors)
    est_freq_vector = list()

    for sum_bit in perturbed_sum_bit_vector:
        numerator = sum_bit - (n * q)
        denominator = p - q
        est_freq_vector.append(numerator / denominator)

    # Re-normalized estimated frequencies
    norm_est_freq = np.nan_to_num(est_freq_vector / sum(est_freq_vector))

    return norm_est_freq


def OLH_Client(input_data_list, k, epsilon, seed_init):
    p = exp(epsilon) / (exp(epsilon) + k - 1)
    g = int(round(np.exp(epsilon))) + 1
    report_list = list()

    for input_data in input_data_list:
        report_value = (xxhash.xxh32(str(input_data), seed=seed_init).intdigest() % g)
        rnd = np.random.random()
        if rnd > p:
            report_value = np.random.randint(0, g)
        report_list.append(report_value)
        seed_init += 1
    return report_list


def OLH_Client2(input_data_list, k, epsilon, seed_init):
    p = exp(epsilon) / (exp(epsilon) + k - 1)
    g = int(round(np.exp(epsilon))) + 1
    report_list = list()

    for input_data in input_data_list:
        input_data -= 1
        report_value = (xxhash.xxh32(str(input_data), seed=seed_init).intdigest() % g)
        rnd = np.random.random()
        if rnd > p:
            report_value = np.random.randint(0, g)
        report_list.append(report_value)
    return report_list


def ESAD_CLIENT(input_data_list, epsilon, seed_init):
    g = int(round(np.exp(epsilon))) + 1
    report_list = list()

    for input_data in input_data_list:
        input_data -= 1
        report_value = (xxhash.xxh32(str(input_data), seed=seed_init).intdigest() % g)
        bit_vector = SIMPLE_RAPPOR_Client(report_value, g, epsilon)
        report_list.append(bit_vector)

    return report_list


def ESAD_AGGREGATOR(perturbed_datas, n, k, epsilon):
    g = int(round(exp(epsilon))) + 1
    p = (np.exp(epsilon / 2)) / (np.exp(epsilon / 2) + 1)
    q = 1 / (np.exp(epsilon / 2) + 1)

    ESTIMATE_DIST = np.zeros(k)
    for seed, user_report in enumerate(perturbed_datas):
        for user_index, perturbed_vector in enumerate(user_report):
            for index, perturbed_value in enumerate(perturbed_vector):
                for v in range(k):
                    if perturbed_value == 1.0 and (index + 1) == (xxhash.xxh32(str(v), seed=seed + 1).intdigest() % g):
                        ESTIMATE_DIST[v] += 1

    # Ensure non-negativity of estimated frequency
    est_freq = np.array((ESTIMATE_DIST - n * q) / (p - q)).clip(0)

    # Re-normalized estimated frequency
    if sum(est_freq) > 0:
        norm_est_freq = np.nan_to_num(est_freq / sum(est_freq))
    else:
        norm_est_freq = est_freq

    return norm_est_freq


def OLH_Aggregator(reports, n, k, epsilon):
    # GRR parameters
    p = np.exp(epsilon) / (np.exp(epsilon) + k - 1)
    q = (1 - p) / (k - 1)

    # Count how many times each value has been reported
    count_report = np.zeros(k)

    for i in range(n):
        for v in range(k):
            if reports[i] == (xxhash.xxh32(str(v), seed=i).intdigest() % k):
                count_report[v] += 1

    # Ensure non-negativity of estimated frequency
    est_freq = np.array((count_report - n * q) / (p - q)).clip(0)

    # Re-normalized estimated frequency
    norm_est_freq = np.nan_to_num(est_freq / sum(est_freq))

    return norm_est_freq


def OUE_Client(input_data, k, epsilon):
    bit_vector = np.zeros(k)
    bit_vector[input_data - 1] = 1

    p = 1 / 2
    q = 1 / (np.exp(epsilon) + 1)

    perturbed_bit_vector = bit_vector.copy()
    for bit_index in range(k):
        if perturbed_bit_vector[bit_index] == 0:
            rnd = np.random.random()
            if rnd <= q:
                perturbed_bit_vector[bit_index] = 1
        else:
            rnd = np.random.random()
            if rnd > p:
                perturbed_bit_vector[bit_index] = 0
    return perturbed_bit_vector


def OUE_Aggregator(perturbed_bit_vectors, epsilon):
    n = 2
    perturbed_sum_bit_vector = sum(perturbed_bit_vectors)
    est_freq_vector = list()

    for sum_bit in perturbed_sum_bit_vector:
        numerator = 2 * ((np.exp(epsilon) + 1) * sum_bit - n)
        denominator = np.exp(epsilon) - 1
        est_freq_vector.append(numerator / denominator)

    # Re-normalized estimated frequencies
    norm_est_freq = np.nan_to_num(est_freq_vector / sum(est_freq_vector))
    return norm_est_freq
