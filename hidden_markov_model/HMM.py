from collections import defaultdict

import numpy as np
import xxhash
from hmmlearn import hmm

from LDP.helper import binary_to_decimal
from hidden_markov_model.helper import getAdjacent, analyze_taken_path, create_emission_matrix_rows, \
    create_emission_matrix_column, decimal_to_binary, calculate_prob, calculate_q_counter, find_closest_hidden_state, \
    find_bit_vector_with_q_counter, flip_bits


class HMM:

    def __init__(self, k, epsilon):
        self.k = k
        self.epsilon = epsilon
        self.model = hmm.MultinomialHMM(n_components=k, algorithm='viterbi')
        self.grid = np.arange(k).reshape(k // 4, k // 5)

        self.is_bit_vector = True

        self.dict_order = {}

    def guess_user_values(self, protocol, user_perturbed_report):
        obs_sequence_list = []
        for perturbed_report in user_perturbed_report:

            if protocol.is_bit_vector:
                if decimal_to_binary(perturbed_report, self.k) in self.dict_order:
                    obs_sequence_list.append(self.dict_order[decimal_to_binary(perturbed_report, self.k)])
                else:
                    obs_sequence_list.append(0)
            else:
                obs_sequence_list.append(perturbed_report)

        obs_sequence = np.array([obs_sequence_list]).T

        _, state_sequence = self.model.decode(obs_sequence)

        for i in range(len(state_sequence)):
            state_sequence[i] = state_sequence[i] + 1

        return state_sequence

    def config_plain_model(self):
        self.create_plain_start_probability_vector()
        self.create_plain_transition_matrix()

    def config_advance_model(self, user_value_list):
        self.create_advance_start_probability_vector(user_value_list)
        self.create_advance_transition_matrix(user_value_list)

    def create_plain_start_probability_vector(self):
        self.model.startprob_ = np.array([1 / self.k] * self.k)

    def create_plain_transition_matrix(self):
        matrix_list = []
        for i in range(1, self.k + 1):
            sub_list = []
            adjacent_elements = getAdjacent(self.grid, i)
            for j in range(1, self.k + 1):
                if j in adjacent_elements or j == i:
                    sub_list.append(1 / (len(adjacent_elements) + 1))
                else:
                    sub_list.append(0)
            matrix_list.append(sub_list)
        self.model.transmat_ = np.array(matrix_list)

    def create_advance_start_probability_vector(self, user_value_list):
        start_grid_dict = {}
        for user_true_values in user_value_list:
            init_grid = user_true_values.item(0)
            start_grid_dict[init_grid] = start_grid_dict.get(init_grid, 0) + 1

        start_grid_dict = dict(sorted(start_grid_dict.items()))
        sum_grid_counts = sum(start_grid_dict.values())
        start_prob_list = list()
        for grid_count in start_grid_dict.values():
            start_prob_list.append(grid_count / sum_grid_counts)

        for _ in range(self.k - len(start_prob_list)):
            start_prob_list.append(0)

        self.model.startprob_ = np.array(start_prob_list)

    def create_advance_transition_matrix(self, user_value_list):
        dict_of_path = analyze_taken_path(user_value_list)
        matrix_list = []
        for i in range(1, self.k + 1):
            sub_list = []
            adjacent_elements = getAdjacent(self.grid, i)
            sum_of_path = 0
            if i in dict_of_path and i in dict_of_path[i]:
                sum_of_path = dict_of_path[i][i]
            else:
                dict_of_path[i] = {}
                dict_of_path[i][i] = 1
                sum_of_path += 1
            for element in adjacent_elements:
                if element in dict_of_path[i]:
                    sum_of_path += dict_of_path[i][element]
                else:
                    dict_of_path[i][element] = 1
                    sum_of_path += 1
            for j in range(1, self.k + 1):
                if (j in adjacent_elements or j == i) and (j in dict_of_path[i]):
                    taken_path = dict_of_path[i][j]
                    sub_list.append(taken_path / sum_of_path)
                else:
                    sub_list.append(0)
            matrix_list.append(sub_list)

        self.model.transmat_ = np.array(matrix_list)

    def create_grr_emission_matrix(self, grr, seed):
        matrix_list = []
        for i in range(self.k):
            row_list = []
            for j in range(self.k):
                if i == j:
                    row_list.append(grr.p)
                else:
                    row_list.append(grr.q)
            matrix_list.append(row_list)

        self.model.emissionprob_ = np.array(matrix_list)

    def create_rappor_emission_matrix(self, rappor, seed):
        hidden_state_list = create_emission_matrix_column(self.k)
        revised_column_dict_order = defaultdict(lambda: -1)
        q_counter_to_value_dict = defaultdict(lambda: -1)

        order = -1
        esad = dict()
        for hidden_state in hidden_state_list:
            for q_counter in range(self.k // 4 + 1):
                binary_number_list = flip_bits(hidden_state, q_counter)
                for binary_number in binary_number_list:
                    if binary_number not in esad:
                        esad[binary_to_decimal(binary_number)] = binary_number

        # Sort dictionary by key
        esad = {k: v for k, v in sorted(esad.items(), key=lambda item: item[0])}

        for key in esad:
            column = esad[key]
            q_counter = 0
            for hidden_state in hidden_state_list:
                for char_index in range(self.k):
                    if hidden_state[char_index] != column[char_index]:
                        q_counter += 1
            if q_counter <= (self.k // 4) * self.k:
                order += 1
                revised_column_dict_order[column] = order
            q_counter_to_value_dict[column] = order


        emission_prob_list = list()
        for hidden_state in hidden_state_list:
            row_prob_list = list()
            for column in revised_column_dict_order:
                prob = 1
                for char_index in range(self.k):
                    if hidden_state[char_index] == column[char_index]:
                        prob *= rappor.p
                    else:
                        prob *= rappor.q
                row_prob_list.append(prob)
            emission_prob_list.append(row_prob_list)

        # Normalzie emission_prob_list
        for row_index in range(len(emission_prob_list)):
            row = emission_prob_list[row_index]
            sum_row = sum(row)
            for column_index in range(len(row)):
                emission_prob_list[row_index][column_index] = emission_prob_list[row_index][column_index] / sum_row

        self.dict_order = q_counter_to_value_dict
        self.model.emissionprob_ = np.array(emission_prob_list)

    def create_rapporOld_emission_matrix(self, rappor, seed):
        rappor_report_list = list()
        for x in range(2 ** self.k):
            rappor_report_list.append((bin(x)[2:].zfill(self.k)))

        user_value_list = list()
        for i in range(self.k):
            bit_vector = ''
            for j in range(self.k):
                if i == j:
                    bit_vector += '1'
                else:
                    bit_vector += '0'
            user_value_list.append(bit_vector)

        emission_prob_list = list()
        p_counter = 0
        q_counter = 0
        for row_index in range(len(user_value_list)):
            row = user_value_list[row_index]
            row_prob_list = list()
            for column_index in range(len(rappor_report_list)):
                column = rappor_report_list[column_index]
                prob = 1
                for char_index in range(len(row)):
                    if row[char_index] == column[char_index]:
                        p_counter += 1
                        prob *= rappor.p
                    else:
                        q_counter += 1
                        prob *= rappor.q
                row_prob_list.append(prob)
            emission_prob_list.append(row_prob_list)

        self.model.emissionprob_ = np.array(emission_prob_list)

    def create_oue_emission_matrix(self, oue, seed):
        hidden_state_list = create_emission_matrix_column(self.k)
        revised_column_dict_order = defaultdict(lambda: -1)
        q_counter_to_value_dict = defaultdict(lambda: -1)

        order = -1
        esad = dict()
        for hidden_state in hidden_state_list:
            for q_counter in range(self.k // 4 + 1):
                binary_number_list = flip_bits(hidden_state, q_counter)
                for binary_number in binary_number_list:
                    if binary_number not in esad:
                        esad[binary_to_decimal(binary_number)] = binary_number

        # Sort dictionary by key
        esad = {k: v for k, v in sorted(esad.items(), key=lambda item: item[0])}

        for key in esad:
            column = esad[key]
            q_counter = 0
            for hidden_state in hidden_state_list:
                for char_index in range(self.k):
                    if hidden_state[char_index] != column[char_index]:
                        q_counter += 1
            if q_counter <= (self.k // 4) * self.k:
                order += 1
                revised_column_dict_order[column] = order
            q_counter_to_value_dict[column] = order

        emission_prob_list = list()
        for hidden_state in hidden_state_list:
            row_prob_list = list()
            for column in revised_column_dict_order:
                prob = 1
                for char_index in range(self.k):
                    if hidden_state[char_index] == column[char_index]:
                        prob *= oue.p
                    else:
                        prob *= oue.q
                row_prob_list.append(prob)
            emission_prob_list.append(row_prob_list)

        # Normalzie emission_prob_list
        for row_index in range(len(emission_prob_list)):
            row = emission_prob_list[row_index]
            sum_row = sum(row)
            for column_index in range(len(row)):
                emission_prob_list[row_index][column_index] = emission_prob_list[row_index][column_index] / sum_row

        self.dict_order = q_counter_to_value_dict
        self.model.emissionprob_ = np.array(emission_prob_list)

    def create_olh_emission_matrix(self, olh, seed):
        matrix_list = []
        for obs_state in range(self.k):
            row_list = []
            hash_value_of_obs_state = (xxhash.xxh32(str(obs_state), seed=seed).intdigest() % olh.g)
            for hidden_state in range(olh.g):
                if hash_value_of_obs_state == hidden_state:
                    row_list.append(olh.p)
                else:
                    row_list.append(olh.q)
            matrix_list.append(row_list)

        self.model.emissionprob_ = np.array(matrix_list)

    def create_hbv_emission_matrix(self, hbv, seed):

        hidden_state_list = create_emission_matrix_column(hbv.g)
        revised_column_dict_order = defaultdict(lambda: -1)
        q_counter_to_value_dict = defaultdict(lambda: -1)

        order = -1
        esad = dict()
        for hidden_state in hidden_state_list:
            for q_counter in range(hbv.g // 4 + 1):
                binary_number_list = flip_bits(hidden_state, q_counter)
                for binary_number in binary_number_list:
                    if binary_number not in esad:
                        esad[binary_to_decimal(binary_number)] = binary_number

        # Sort dictionary by key
        esad = {k: v for k, v in sorted(esad.items(), key=lambda item: item[0])}

        for key in esad:
            column = esad[key]
            q_counter = 0
            for hidden_state in hidden_state_list:
                for char_index in range(hbv.g):
                    if hidden_state[char_index] != column[char_index]:
                        q_counter += 1
            if q_counter <= (hbv.g // 4) * hbv.g:
                order += 1
                revised_column_dict_order[column] = order
            q_counter_to_value_dict[column] = order

        emission_prob_list = list()
        for hidden_state in hidden_state_list:
            row_prob_list = list()
            for column in revised_column_dict_order:
                prob = 1
                for char_index in range(hbv.g):
                    if hidden_state[char_index] == column[char_index]:
                        prob *= hbv.p
                    else:
                        prob *= hbv.q
                row_prob_list.append(prob)
            emission_prob_list.append(row_prob_list)

        # Normalzie emission_prob_list
        for row_index in range(len(emission_prob_list)):
            row = emission_prob_list[row_index]
            sum_row = sum(row)
            for column_index in range(len(row)):
                emission_prob_list[row_index][column_index] = emission_prob_list[row_index][column_index] / sum_row

        self.dict_order = q_counter_to_value_dict
        self.model.emissionprob_ = np.array(emission_prob_list)

    def create_plain_protocol_model(self, protocol, seed=None):
        emission_function = f"create_{protocol.name}_emission_matrix"
        self.config_plain_model()
        getattr(self, emission_function)(protocol, seed)

    def create_advance_protocol_model(self, protocol, users_trajectory_list, seed=None):

        emission_function = f"create_{protocol.name}_emission_matrix"
        self.config_advance_model(users_trajectory_list)
        getattr(self, emission_function)(protocol, seed)
