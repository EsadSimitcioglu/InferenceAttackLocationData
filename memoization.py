import random

import mmh3

from bitarray import bitarray


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


k = 20
h = 1
f = 0.5

p = 0.25
q = 0.75

memoized_values = {}

for user_value in range(1, 21):

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

print(memoized_values)
