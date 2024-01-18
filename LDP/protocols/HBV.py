import numpy as np
import xxhash

from LDP.protocols.RAPPOR import RAPPOR


class HBV:

    def __init__(self, k, epsilon):
        self.k = k
        self.epsilon = epsilon
        self.p = (np.exp(epsilon / 2)) / (np.exp(epsilon / 2) + 1)
        self.q = 1 / (np.exp(epsilon / 2) + 1)
        self.g = int(round(np.exp(epsilon))) + 1

    def client(self, input_data_list, seed):
        rappor = RAPPOR(self.g, self.epsilon)
        report_list = list()
        for input_data in input_data_list:
            input_data -= 1
            report_value = (xxhash.xxh32(str(input_data), seed=seed).intdigest() % self.g)
            bit_vector = rappor.client(report_value)
            report_list.append(bit_vector)

        return report_list

    def server(self, reports):

        n = len(reports)

        ESTIMATE_DIST = np.zeros(self.k)
        for seed, user_report in enumerate(reports):
            for user_index, perturbed_vector in enumerate(user_report):
                for index, perturbed_value in enumerate(perturbed_vector):
                    for v in range(self.k):
                        if perturbed_value == 1.0 and (index + 1) == (xxhash.xxh32(str(v), seed=seed + 1).intdigest() % self.g):
                            ESTIMATE_DIST[v] += 1

        # Ensure non-negativity of estimated frequency
        est_freq = np.array((ESTIMATE_DIST - n * self.q) / (self.p - self.q)).clip(0)

        # Re-normalized estimated frequency
        if sum(est_freq) > 0:
            norm_est_freq = np.nan_to_num(est_freq / sum(est_freq))
        else:
            norm_est_freq = est_freq

        return norm_est_freq
