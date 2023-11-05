def binary_to_decimal(binary_number):
    decimal_number = 0
    index_counter = len(binary_number) - 1

    for number in binary_number:
        decimal_number += (int(number) * (2 ** index_counter))
        index_counter -= 1
    return decimal_number
