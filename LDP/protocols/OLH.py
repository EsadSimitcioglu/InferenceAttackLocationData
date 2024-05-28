import numpy as np
import xxhash


class OLH:

    def __init__(self, k, epsilon):
        self.name = "olh"
        self.k = k
        self.epsilon = epsilon
        self.p = np.exp(epsilon) / (np.exp(epsilon) + k - 1)
        self.g = int(round(np.exp(epsilon))) + 1
        self.q = (1 - self.p) / (self.g - 1)

        self.is_bit_vector = False
        self.is_hash_used = True

    def client(self, input_data, seed):
        report_value = self.hash_input(input_data, seed)
        return self.apply_grr(report_value)

    def hash_input(self, input_data, seed):
        return xxhash.xxh32(str(input_data - 1), seed=seed).intdigest() % self.g

    def apply_grr(self, report_value):
        domain = np.arange(0, self.g)
        rnd = np.random.random()
        if rnd <= self.p:
            return report_value
        else:
            return np.random.choice(domain[domain != report_value])

    def server(self, reports):
        # Count how many times each value has been reported
        count_report = np.zeros(self.g)

        n = len(reports)

        for i in range(n):
            for v in range(self.g):
                if reports[i] == (xxhash.xxh32(str(v), seed=i).intdigest() % self.g):
                    count_report[v] += 1

        # Ensure non-negativity of estimated frequency
        est_freq = np.array((count_report - n * self.q) / (self.p - self.q)).clip(0)

        # Re-normalized estimated frequency
        norm_est_freq = np.nan_to_num(est_freq / sum(est_freq))

        return norm_est_freq

    def memoized(self, input_list, seed):
        user_list = list()
        memoization_dict = dict()
        prev_value = -1
        for input_data in input_list:
            if input_data != prev_value:
                fake_input_value = self.client(input_data, seed)
                memoization_dict[input_data] = fake_input_value
                user_list.append(self.apply_grr(memoization_dict[input_data]))
            else:
                user_list.append(self.apply_grr(memoization_dict[input_data]))
            prev_value = input_data

        return user_list

    def recall(self, input_list, seed):
        user_list = list()
        memoization_dict = dict()
        for input_data in input_list:
            if input_data not in memoization_dict:
                fake_input_value = self.client(input_data, seed)
                memoization_dict[input_data] = fake_input_value
                user_list.append(memoization_dict[input_data])
            else:
                user_list.append(memoization_dict[input_data])
        return user_list



    def memoized_recall(self, input_list, seed):
        user_list = list()
        fake_input_value = -1
        prev_value = -1
        for input_data in input_list:
            if input_data != prev_value:
                fake_input_value = self.client(input_data, seed)
                user_list.append(fake_input_value)
            else:
                user_list.append(fake_input_value)
            prev_value = input_data
        return user_list