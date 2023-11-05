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
        report_value = (xxhash.xxh32(str(input_data - 1), seed=seed).intdigest() % self.g)
        rnd = np.random.random()
        if rnd > self.p:
            report_value = np.random.randint(0, self.g)
        return report_value

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
