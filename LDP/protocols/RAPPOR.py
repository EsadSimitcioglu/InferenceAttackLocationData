import numpy as np

from LDP.helper import binary_to_decimal


class RAPPOR:

    def __init__(self, k, epsilon):
        self.name = 'rappor'
        self.k = k
        self.epsilon = epsilon
        self.p = (np.exp(epsilon / 2)) / (np.exp(epsilon / 2) + 1)
        self.q = 1 / (np.exp(epsilon / 2) + 1)

        self.is_bit_vector = True
        self.is_hash_used = False


    def client(self, input_data):
        bit_vector = np.zeros(self.k)
        bit_vector[input_data - 1] = 1

        perturbed_bit_vector = bit_vector.copy()
        for bit_index in range(len(bit_vector)):
            rnd = np.random.random()
            if rnd > self.p:
                if perturbed_bit_vector[bit_index] == 1:
                    perturbed_bit_vector[bit_index] = 0
                else:
                    perturbed_bit_vector[bit_index] = 1

        perturbed_bit_vector = perturbed_bit_vector.tolist()
        return perturbed_bit_vector

    def server(self, reports):
        perturbed_bit_vectors = np.array(reports)
        n = len(reports)

        perturbed_sum_bit_vector = sum(perturbed_bit_vectors)
        est_freq_vector = list()

        for sum_bit in perturbed_sum_bit_vector:
            numerator = sum_bit - (n * self.q)
            denominator = self.p - self.q
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

    def client_memoized(self, input_list):
        perturbed_list = []

        for user_trajectory in input_list:
            user_list = list()
            memoization_dict = {}
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
