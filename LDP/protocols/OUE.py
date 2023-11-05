import numpy as np

from LDP.helper import binary_to_decimal


class OUE:

    def __init__(self, k, epsilon):
        self.name = 'oue'
        self.k = k
        self.epsilon = epsilon
        self.p = 1 / 2
        self.q = 1 / (np.exp(epsilon) + 1)

        self.is_bit_vector = True
        self.is_hash_used = False


    def client(self, input_data):
        bit_vector = np.zeros(self.k)
        bit_vector[input_data - 1] = 1

        perturbed_bit_vector = bit_vector.copy()
        for bit_index in range(self.k):
            if perturbed_bit_vector[bit_index] == 0:
                rnd = np.random.random()
                if rnd <= self.q:
                    perturbed_bit_vector[bit_index] = 1
            else:
                rnd = np.random.random()
                if rnd > self.p:
                    perturbed_bit_vector[bit_index] = 0
        return perturbed_bit_vector

    def server(self, reports):
        n = len(reports)
        perturbed_sum_bit_vector = sum(reports)
        est_freq_vector = list()

        for sum_bit in perturbed_sum_bit_vector:
            numerator = 2 * ((np.exp(self.epsilon) + 1) * sum_bit - n)
            denominator = np.exp(self.epsilon) - 1
            est_freq_vector.append(numerator / denominator)

        # Re-normalized estimated frequencies
        norm_est_freq = np.nan_to_num(est_freq_vector / sum(est_freq_vector))
        return norm_est_freq

    def convert_binary_report_to_decimal(self, perturbed_trajectory):
        report_string = str()
        for index in perturbed_trajectory:
            report_string += str(int(index))
        report = (binary_to_decimal(report_string))
        return report
