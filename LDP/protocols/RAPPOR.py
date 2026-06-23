import numpy as np

from LDP.helper import bit_vector_to_decimal, normalize_distribution


class RAPPOR:
    def __init__(self, k, epsilon):
        self.name = "rappor"
        self.k = k
        self.epsilon = epsilon
        self.p = (np.exp(epsilon / 2)) / (np.exp(epsilon / 2) + 1)
        self.q = 1 / (np.exp(epsilon / 2) + 1)

        self.is_bit_vector = True
        self.is_hash_used = False
        self.is_memoized = True

    def client(self, input_data):
        if not isinstance(input_data, (list, np.ndarray)):
            bit_vector = np.zeros(self.k)
            bit_vector[input_data - 1] = 1
        else:
            bit_vector = np.array(input_data)

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
                    fake_input_data = self.client(input_data)
                    memoization_dict[input_data] = fake_input_data
                    user_list.append(fake_input_data)
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
