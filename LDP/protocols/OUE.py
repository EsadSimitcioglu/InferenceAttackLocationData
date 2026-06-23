import numpy as np

from LDP.helper import bit_vector_to_decimal, normalize_distribution


class OUE:
    def __init__(self, k, epsilon):
        self.name = "oue"
        self.k = k
        self.epsilon = epsilon
        self.p = 1 / 2
        self.q = 1 / (np.exp(epsilon) + 1)

        self.is_bit_vector = True
        self.is_hash_used = False

    def client(self, input_data):
        if not isinstance(input_data, (list, np.ndarray)):
            bit_vector = np.zeros(self.k)
            bit_vector[input_data - 1] = 1
        else:
            bit_vector = np.array(input_data)

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

        return normalize_distribution(np.array(est_freq_vector))

    def convert_binary_report_to_decimal(self, perturbed_trajectory):
        return bit_vector_to_decimal(perturbed_trajectory)

    def memoized(self, input_list):
        perturbed_list = []

        for user_trajectory in input_list:
            user_list = list()
            memoization_dict = {}
            prev_value = -1
            for input_data in user_trajectory:
                if input_data != prev_value:
                    fake_input_value = self.client(input_data)
                    memoization_dict[input_data] = fake_input_value
                    user_list.append(self.client(fake_input_value))
                else:
                    user_list.append(self.client(memoization_dict[input_data]))
                prev_value = input_data
            report = [
                self.convert_binary_report_to_decimal(report_string)
                for report_string in user_list
            ]
            perturbed_list.append(report)

        return perturbed_list

    def recall(self, input_list):
        perturbed_list = []

        for user_trajectory in input_list:
            user_list = list()
            memoization_dict = {}
            for input_data in user_trajectory:
                if input_data not in memoization_dict:
                    perturbed = self.client(input_data)
                    memoization_dict[input_data] = perturbed
                    user_list.append(perturbed)
                else:
                    user_list.append(self.client(memoization_dict[input_data]))
            report = [
                self.convert_binary_report_to_decimal(report_string)
                for report_string in user_list
            ]
            perturbed_list.append(report)

        return perturbed_list

    def memoized_recall(self, input_list):
        perturbed_list = []

        for user_trajectory in input_list:
            user_list = list()
            prev_fake_value = -1
            prev_value = -1
            for input_data in user_trajectory:
                if input_data != prev_value:
                    fake_input_value = self.client(input_data)
                    prev_fake_value = fake_input_value
                    user_list.append(prev_fake_value)
                else:
                    user_list.append(prev_fake_value)
                prev_value = input_data
            report = [
                self.convert_binary_report_to_decimal(report_string)
                for report_string in user_list
            ]
            perturbed_list.append(report)

        return perturbed_list
