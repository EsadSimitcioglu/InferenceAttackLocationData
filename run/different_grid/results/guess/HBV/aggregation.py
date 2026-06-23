import csv
import numpy as np
import matplotlib.pyplot as plt


from LDP.protocols import (
    HBV_Client,
    HBV_Aggregator,
)

# Parameters for simulation
k = 20  # attribute's domain size (grid size)
epsilon_list = [5, 10, 15]  # number of epsilon for run cases
iter_list = [1, 2, 3, 4, 5]
users_grid_value_list = list()
perturbed_bit_vector_list = list()

with open("../../../../../dataset/taxi/taxi_test_different_grid.dat") as f:
    reader = csv.reader(f, delimiter="\t")
    for line in reader:
        grid_list = line[0].split(" ")
        grid_list_int = [eval(i) for i in grid_list]
        grid_list_int_nd = np.array(grid_list_int)
        users_grid_value_list.append(grid_list_int_nd)

# calculate frequency for each grid value
true_freq = np.zeros(k)
for user_true_values in users_grid_value_list:
    for grid_value in user_true_values:
        true_freq[grid_value - 1] += 1

# normalize true frequency
true_freq = true_freq / len(users_grid_value_list)

# Create histogram
plt.bar(np.arange(len(true_freq)), true_freq, color="red", align="center", alpha=0.5)
plt.xticks(np.arange(len(true_freq)), np.arange(len(true_freq)))
plt.ylabel("True Frequency")
plt.xlabel("Grid Value")
plt.title("True Histogram")
plt.show()

for epsilon in epsilon_list:
    print("Epsilon Value: " + str(epsilon))

    seed_value = 1
    for user_true_values in users_grid_value_list:
        perturbed_bit_vector_list.append(
            HBV_Client(user_true_values, epsilon, seed_value)
        )
        seed_value += 1

    est_freq = HBV_Aggregator(perturbed_bit_vector_list, 100, k, epsilon)

    # for user_true_values in users_grid_value_list:
    # perturbed_bit_vector_list.append(SIMPLE_RAPPOR_Client(user_true_values,k, epsilon))

    # est_freq = SIMPLE_RAPPOR_Aggregator(perturbed_bit_vector_list, epsilon)

    # Create histogram
    plt.bar(np.arange(len(est_freq)), est_freq, align="center", alpha=0.5)
    plt.xticks(np.arange(len(est_freq)), np.arange(len(est_freq)))
    plt.ylabel("Estimated Frequency")
    plt.xlabel("Grid Value")
    plt.title("ESAD Histogram for Epsilon = " + str(epsilon))
    plt.show()
