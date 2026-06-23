import numpy as np


def binary_to_decimal(binary_number):
    decimal_number = 0
    index_counter = len(binary_number) - 1

    for number in binary_number:
        decimal_number += int(number) * (2**index_counter)
        index_counter -= 1
    return decimal_number


def bit_vector_to_decimal(bit_vector):
    return binary_to_decimal("".join(str(int(index)) for index in bit_vector))


def normalize_distribution(values):
    total = np.sum(values)
    if total == 0:
        return np.nan_to_num(values)
    return np.nan_to_num(values / total)
