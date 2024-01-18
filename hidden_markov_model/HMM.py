import numpy as np
import xxhash
from hmmlearn import hmm
from hidden_markov_model.helper import getAdjacent, analyze_taken_path, create_emission_matrix_rows, create_emission_matrix_column

class HMM:

    def __init__(self, k, epsilon):
        self.k = k
        self.epsilon = epsilon
        self.model = hmm.MultinomialHMM(n_components=k, algorithm='viterbi')
        self.grid = np.arange(k).reshape(k // 4, k // 5)

        self.is_bit_vector = True


    def guess_user_values(self, user_perturbed_report):
        obs_sequence_list = []
        for index, perturbed_report in enumerate(user_perturbed_report):
            obs_sequence_list.append(index)
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
        row_value_list = create_emission_matrix_rows(self.k)

        column_value_list = create_emission_matrix_column(self.k)

        keep_bit_prob = ((rappor.p ** 2) + (rappor.q ** 2)) if rappor.is_memoized else rappor.p
        flip_bit_prob = (2 * rappor.p * rappor.q) if rappor.is_memoized else rappor.q

        emission_prob_list = list()
        for row_index in range(len(column_value_list)):
            row = column_value_list[row_index]
            row_prob_list = list()
            for column_index in range(len(row_value_list)):
                column = row_value_list[column_index]
                prob = 1
                for char_index in range(len(row)):
                    if row[char_index] == column[char_index]:
                        prob *= keep_bit_prob
                    else:
                        prob *= flip_bit_prob
                row_prob_list.append(prob)
            emission_prob_list.append(row_prob_list)

        self.model.emissionprob_ = np.array(emission_prob_list)

    def create_rappor_eff(self, rappor, user_value_list):
        self.model = hmm.MultinomialHMM(n_components=self.k, algorithm='viterbi')
        self.config_plain_model()

        row_value_list = list()
        for user_val in user_value_list:
            row_value_list.append((bin(user_val)[2:].zfill(rappor.k)))

        column_value_list = create_emission_matrix_column(self.k)

        keep_bit_prob = ((rappor.p ** 2) + (rappor.q ** 2)) if rappor.is_memoized else rappor.p
        flip_bit_prob = (2 * rappor.p * rappor.q) if rappor.is_memoized else rappor.q

        emission_prob_list = list()
        for row_index in range(len(column_value_list)):
            row = column_value_list[row_index]
            row_prob_list = list()
            for column_index in range(len(row_value_list)):
                column = row_value_list[column_index]
                prob = 1
                for char_index in range(len(row)):
                    if row[char_index] == column[char_index]:
                        prob *= keep_bit_prob
                    else:
                        prob *= flip_bit_prob
                row_prob_list.append(prob)

            # Normalize row_prob_list
            sum_prob = sum(row_prob_list)
            for i in range(len(row_prob_list)):
                row_prob_list[i] /= sum_prob
            emission_prob_list.append(row_prob_list)

        self.model.emissionprob_ = np.array(emission_prob_list)



    def create_oue_emission_matrix(self, oue, seed):
        row_value_list = create_emission_matrix_rows(self.k)

        column_value_list = create_emission_matrix_column(self.k)

        emission_prob_list = list()
        for row_index in range(len(column_value_list)):
            row = column_value_list[row_index]
            row_prob_list = list()
            for column_index in range(len(row_value_list)):
                column = row_value_list[column_index]
                prob = 1
                for char_index in range(len(row)):
                    if row[char_index] == '1':
                        if row[char_index] == column[char_index]:
                            prob *= oue.p
                        else:
                            prob *= (1 - oue.p)
                    else:
                        if row[char_index] == column[char_index]:
                            prob *= (1 - oue.q)
                        else:
                            prob *= oue.q
                row_prob_list.append(prob)
            emission_prob_list.append(row_prob_list)

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

    def create_plain_protocol_model(self, protocol, seed=None):

        emission_function = f"create_{protocol.name}_emission_matrix"
        self.config_plain_model()
        getattr(self, emission_function)(protocol, seed)

    def create_advance_protocol_model(self, protocol, users_trajectory_list, seed=None):

        emission_function = f"create_{protocol.name}_emission_matrix"
        self.config_advance_model(users_trajectory_list)
        getattr(self, emission_function)(protocol, seed)

