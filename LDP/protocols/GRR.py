import numpy as np

from LDP.helper import normalize_distribution


class GRR:
    def __init__(self, k, epsilon):
        self.name = "grr"
        self.k = k
        self.epsilon = epsilon
        self.p = np.exp(epsilon) / (np.exp(epsilon) + k - 1)
        self.q = 1 / (np.exp(epsilon) + k - 1)

        self.is_bit_vector = False
        self.is_hash_used = False

    def client(self, input_data):
        # Mapping domain size k to the range [0, ..., k-1]
        domain = np.arange(0, self.k)

        # GRR perturbation function
        rnd = np.random.random()
        if rnd <= self.p:
            return input_data - 1
        return np.random.choice(domain[domain != input_data] - 1)

    def server(self, reports):
        # Number of reports
        n = len(reports)

        # Count how many times each value has been reported
        count_report = np.zeros(self.k)
        for rep in reports:
            count_report[rep] += 1

        # Ensure non-negativity of estimated frequency
        est_freq = np.array((count_report - n * self.q) / (self.p - self.q)).clip(0)
        return normalize_distribution(est_freq)

    def memoized(self, input_list):
        perturbed_list = list()

        for user_trajectory in input_list:
            user_list = list()
            memoization_dict = dict()
            prev_value = -1
            for input_data in user_trajectory:
                if input_data != prev_value:
                    fake_input_value = self.client(input_data)
                    memoization_dict[input_data] = fake_input_value + 1
                    user_list.append(self.client(fake_input_value))
                else:
                    user_list.append(self.client(memoization_dict[input_data]))
                prev_value = input_data
            perturbed_list.append(user_list)

        return perturbed_list

    def recall(self, input_list):
        perturbed_list = list()

        for user_trajectory in input_list:
            user_list = list()
            memoization_dict = dict()
            for input_data in user_trajectory:
                if input_data not in memoization_dict:
                    fake_input_value = self.client(input_data)
                    memoization_dict[input_data] = fake_input_value
                    user_list.append(fake_input_value)
                else:
                    user_list.append(memoization_dict[input_data])
            perturbed_list.append(user_list)
        return perturbed_list

    def memoized_recall(self, input_list):
        perturbed_list = list()

        for user_trajectory in input_list:
            user_list = list()
            prev_fake_value = -1
            prev_value = -1
            for input_data in user_trajectory:
                if input_data != prev_value:
                    fake_input_value = self.client(input_data)
                    prev_fake_value = fake_input_value
                    user_list.append(fake_input_value)
                else:
                    user_list.append(prev_fake_value)
                prev_value = input_data
            perturbed_list.append(user_list)

        return perturbed_list
