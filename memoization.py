import csv
import random

import mmh3
import numpy as np

from bitarray import bitarray

from LDP.estimation_different_grid import GRR_estimated_guess, RAPPOR_estimated_guess, OUE_estimated_guess, \
    OLH_estimated_guess, GRR_advance_estimated_guess, RAPPOR_advance_estimated_guess, OUE_advance_estimated_guess, \
    OLH_advance_estimated_guess
from hidden_markov_model.hidden_markov_model import guess, hmm_model_RAPPOR
from metric.path_distance import ratio_of_guess


class BloomFilter:

    def __init__(self, size, hash_count):
        self.size = size
        self.hash_count = hash_count
        self.bit_array = bitarray(size)
        self.bit_array.setall(0)

    def add(self, string):
        for seed in range(self.hash_count):
            result = mmh3.hash(string, seed) % self.size
            self.bit_array[result] = 1

    def lookup(self, string):
        for seed in range(self.hash_count):
            result = mmh3.hash(string, seed) % self.size
            if self.bit_array[result] == 0:
                return "Nope"
        return "Probably"


def experiment(user_values_list, perturbed_reports, model):
    guess_metric = list()

    for index, user_perturbed_report in enumerate(perturbed_reports):
        guessed_users_value = guess(model, user_perturbed_report)

        guess_metric.append(ratio_of_guess(user_values_list[index], guessed_users_value))

    return np.average(guess_metric)


def binary_to_decimal(binary_number):
    decimal_number = 0
    index_counter = len(binary_number) - 1

    for number in binary_number:
        decimal_number += (int(number) * (2 ** index_counter))
        index_counter -= 1
    return decimal_number


def report(bf_prime):
    report = BloomFilter(k, 7)
    for index, bit in enumerate(bf_prime.bit_array):
        r = random.random()

        if bit == 1:
            if r < q:
                report.bit_array[index] = 1
            else:
                report.bit_array[index] = 0

        else:
            if r < p:
                report.bit_array[index] = 0
            else:
                report.bit_array[index] = 1
    return report.bit_array.to01()


k = 20
h = 1
f = 0.5

p = 0.5
q = 0.75
epsilon = 0.5

users_grid_value_list = list()
report_grid_value_list = list()
report_decimal_value_list = list()
probability_of_guess_rappor = list()

with open('dataset/brinkhoff/brinkhoff_grid_small.dat') as f:
    reader = csv.reader(f, delimiter="\t")
    for line in reader:
        grid_list = line[0].split(" ")
        grid_list_int = [eval(i) for i in grid_list]
        grid_list_int_nd = np.array(grid_list_int)
        users_grid_value_list.append(grid_list_int_nd)

for user in users_grid_value_list:

    memoized_values = {}

    for user_value in user:

        if user_value in memoized_values:
            user_report = report(memoized_values[user_value])
            report_grid_value_list.append(user_report)
            continue

        bf = BloomFilter(k, 7)
        bf_prime = BloomFilter(k, 7)

        bf.add(str(user_value))

        for index, bit in enumerate(bf.bit_array):
            r = random.random()

            if r < 0.25:
                bf_prime.bit_array[index] = 1
            elif r < 0.5:
                bf_prime.bit_array[index] = 0
            else:
                bf_prime.bit_array[index] = bf.bit_array[index]

        memoized_values[user_value] = bf_prime

        user_report = report(bf_prime)
        report_grid_value_list.append(user_report)

    for report in report_grid_value_list:
        report_decimal_value_list.append(binary_to_decimal(report))

    model = hmm_model_RAPPOR(epsilon, k, 'plain')

    result = experiment(user, report_grid_value_list, model)

    print(result)

    # probability_of_guess_rappor.append(RAPPOR_advance_estimated_guess(users_grid_value_list, k, epsilon, 3))
    print("RAPPOR is Ready")

    print(123)

print(memoized_values)
