import numpy as np


class GRR:

    def __init__(self, k, epsilon):
        self.name = 'grr'
        self.k = k
        self.epsilon = epsilon
        self.p = np.exp(epsilon) / (np.exp(epsilon) + k - 1)
        self.q = 1 / (np.exp(epsilon) + k - 1)

        self.is_bit_vector = False
        self.is_hash_used = False

    def client(self, input_data):
        # GRR parameters
        p = np.exp(self.epsilon) / (np.exp(self.epsilon) + self.k - 1)

        # Mapping domain size k to the range [0, ..., k-1]
        domain = np.arange(1, self.k + 1)

        # GRR perturbation function
        rnd = np.random.random()
        if rnd <= p:
            return input_data - 1
        else:
            return np.random.choice(domain[domain != input_data] - 1)

    def server(self, reports):
        # Number of reports
        n = len(reports)

        # GRR parameters
        p = np.exp(self.epsilon) / (np.exp(self.epsilon) + self.k - 1)
        q = (1 - p) / (self.k - 1)

        # Count how many times each value has been reported
        count_report = np.zeros(self.k)
        for rep in reports:
            count_report[rep] += 1

        # Ensure non-negativity of estimated frequency
        est_freq = np.array((count_report - n * q) / (p - q)).clip(0)

        # Re-normalized estimated frequency
        norm_est_freq = np.nan_to_num(est_freq / sum(est_freq))

        return norm_est_freq

    def client_memoized(self, input_list):
        perturbed_list = list()

        for user_trajectory in input_list:
            user_list = list()
            memoization_dict = dict()
            prev_value = -1
            for input_data in user_trajectory:
                if input_data == prev_value:
                    if input_data not in memoization_dict:
                        memoization_dict[input_data] = self.client(input_data)
                    user_list.append(self.client(memoization_dict[input_data]))
                else:
                    user_list.append(self.client(input_data))
                prev_value = input_data
            perturbed_list.append(user_list)

        return perturbed_list
