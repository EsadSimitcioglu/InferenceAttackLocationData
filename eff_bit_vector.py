import csv
from collections import defaultdict

import numpy as np
import xxhash

from hidden_markov_model.helper import decimal_to_binary


def create_emission_matrix_rows(k):
    row_list = list()
    for x in range(2 ** k):
        row_list.append((bin(x)[2:].zfill(k)))
    return row_list


def create_emission_matrix_column(k):
    column_list = list()
    for i in range(k):
        bit_vector = ''
        for j in range(k):
            if i == j:
                bit_vector += '1'
            else:
                bit_vector += '0'
        column_list.append(bit_vector)
    return column_list

def binary_to_decimal(binary_number):
    decimal_number = 0
    index_counter = len(binary_number) - 1

    for number in binary_number:
        decimal_number += (int(number) * (2 ** index_counter))
        index_counter -= 1
    return decimal_number

seed = 1
k = 20
epsilon =0.5
p = (np.exp(epsilon / 2)) / (np.exp(epsilon / 2) + 1)
q = 1 / (np.exp(epsilon / 2) + 1)
g = int(round(np.exp(epsilon))) + 1
row_value_list = create_emission_matrix_rows(k)

order = 0
emission_prob_list = list()
for row in range(k):
    bit_vector_of_hidden_state = decimal_to_binary(row, k)
    row_prob_list = list()
    for column_index in range(len(row_value_list)):
        column = row_value_list[column_index]
        p_counter = 0
        q_counter = 0
        for char_index in range(k):
            if bit_vector_of_hidden_state[char_index] == column[char_index]:
                p_counter += 1
            else:
                q_counter += 1

        row_prob_list.append((order, p_counter, q_counter))
        order += 1
    emission_prob_list.append(row_prob_list)

order = -1
revised_column_dict_order = defaultdict(lambda: -1)
q_counter_dict = defaultdict(lambda: 0)
q_counter_to_value_dict = defaultdict(lambda: -1)

for column_index in range(len(emission_prob_list[0])):
    q_counter = 0
    for row_index in range(len(emission_prob_list)):
        element = emission_prob_list[row_index][column_index]
        q_counter += element[2]

    if q_counter <= (k // 4) * k:
        order += 1
        revised_column_dict_order[row_value_list[column_index]] = order
    else:
        if q_counter not in q_counter_dict:
            order += 1
            q_counter_dict[q_counter] = order
            revised_column_dict_order[row_value_list[column_index]] = order
    q_counter_to_value_dict[row_value_list[column_index]] = order

emission_prob_list = list()
for row in range(k):
    bit_vector_of_hidden_state = decimal_to_binary(row, k)
    row_prob_list = list()
    for column in revised_column_dict_order:
        prob = 1
        for char_index in range(k):
            if bit_vector_of_hidden_state[char_index] == column[char_index]:
                prob *= p
            else:
                prob *= q
        row_prob_list.append(prob)
    emission_prob_list.append(row_prob_list)

# Normalzie emission_prob_list
for row_index in range(len(emission_prob_list)):
    row = emission_prob_list[row_index]
    sum_row = sum(row)
    for column_index in range(len(row)):
        emission_prob_list[row_index][column_index] = emission_prob_list[row_index][column_index] / sum_row

a = sum(emission_prob_list[0])
print('q_counter_to_value_dict', len(q_counter_to_value_dict))
print('revised_column_dict_order', len(revised_column_dict_order))

