import csv

import numpy as np


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


k = 20
epsilon = 0.5
p = (np.exp(epsilon / 2)) / (np.exp(epsilon / 2) + 1)
q = 1 / (np.exp(epsilon / 2) + 1)
row_value_list = create_emission_matrix_rows(k)
column_value_list = create_emission_matrix_column(k)

order = 0
emission_prob_list = list()
for row_index in range(len(column_value_list)):
    row = column_value_list[row_index]
    row_prob_list = list()
    for column_index in range(len(row_value_list)):
        column = row_value_list[column_index]
        prob = ""
        p_counter = 0
        q_counter = 0
        for char_index in range(len(row)):
            if row[char_index] == column[char_index]:
                p_counter += 1
            else:
                q_counter += 1
        row_prob_list.append((order, p_counter, q_counter))
        order+=1
    emission_prob_list.append(row_prob_list)

order = -1
dict_order = {}
temp_dict_order = {}

for column_index in range(len(emission_prob_list[0])):
    q_counter = 0
    for row_index in range(len(emission_prob_list)):
        element = emission_prob_list[row_index][column_index]
        q_counter += element[2]

    if q_counter <= (k//4)*k:
        order+=1
        temp_dict_order[row_value_list[column_index]] = order
        dict_order[row_value_list[column_index]] = order
    else:
        dict_order[row_value_list[column_index]] = order

emission_prob_list = list()
for row_index in range(len(column_value_list)):
    row = column_value_list[row_index]
    row_prob_list = list()
    for column in temp_dict_order:
        prob = 1
        for char_index in range(len(row)):
            if row[char_index] == column[char_index]:
                prob *= p
            else:
                prob *= q
        row_prob_list.append(prob)
    emission_prob_list.append(row_prob_list)

# Initialize an empty dictionary to store grouped keys
grouped_dict = {}

# Iterate through the original dictionary
for key, value in dict_order.items():
    # Check if the value is already a key in the grouped_dict
    if value in grouped_dict:
        grouped_dict[value].append(key)
    else:
        # If not, create a new list with the current key as the first element
        grouped_dict[value] = [key]

for key in grouped_dict:
        # Remove the first element from the list
        first_element = grouped_dict[key][0]
        grouped_dict[key].remove(first_element)

        for row_index in range(len(column_value_list)):
            row = column_value_list[row_index]
            row_prob_list = list()
            for column in grouped_dict[key]:
                prob = 1
                for char_index in range(len(row)):
                    if row[char_index] == column[char_index]:
                        prob *= p
                    else:
                        prob *= q
                emission_prob_list[row_index][key] += prob



"""

# Normalzie emission_prob_list
for row_index in range(len(emission_prob_list)):
    row = emission_prob_list[row_index]
    sum_row = sum(row)
    for column_index in range(len(row)):
        emission_prob_list[row_index][column_index] = emission_prob_list[row_index][column_index] / sum_row
        
"""
print('dict order: ' , len(dict_order))
print('dict order values' , max(dict_order.values()))
print('temp dict order', len(temp_dict_order))


