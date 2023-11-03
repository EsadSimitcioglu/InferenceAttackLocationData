import csv
import numpy as np
from matplotlib import pyplot as plt

from LDP.estimation_different_grid import GRR_estimated_guess
from hidden_markov_model.hidden_markov_model import hmm_model_GRR_MEMOIZED, guess

from LDP.protocols import GRR_MEMOIZATION_Client
from metric.path_distance import ratio_of_guess


def experiment(epsilon, k, user_values_list):
    guess_metric = list()

    perturbed_reports = GRR_MEMOIZATION_Client(users_grid_value_list, k, epsilon)

    for index, user_perturbed_report in enumerate(perturbed_reports):
        model = hmm_model_GRR_MEMOIZED(epsilon,k)
        guessed_users_value_first_layer = guess(model, user_perturbed_report)
        guess_metric.append(ratio_of_guess(user_values_list[index], guessed_users_value_first_layer))

    return np.average(guess_metric)

# Parameters for simulation
k = 20  # attribute's domain size (grid size)
epsilon_list = [0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 5]  # number of epsilon for test cases
iter_list = [1, 2, 3, 4, 5]
users_grid_value_list = list()
probability_of_guess_grr_plain = list()
probability_of_guess_grr_memoized = list()
probability_of_guess_grr_trained = list()
probability_of_guess_rappor = list()
probability_of_guess_oue = list()
probability_of_guess_olh = list()
probability_of_guess_olh_bit_vector = list()

with open('../../../dataset/taxi/taxi_test_different_grid.dat') as f:
    reader = csv.reader(f, delimiter="\t")
    for line in reader:
        grid_list = line[0].split(" ")
        grid_list_int = [eval(i) for i in grid_list]
        grid_list_int_nd = np.array(grid_list_int)
        users_grid_value_list.append(grid_list_int_nd)


for epsilon in epsilon_list:
    print("Epsilon Value: " + str(epsilon))
    probability_of_guess_grr_memoized.append(experiment(epsilon, k, users_grid_value_list))
    probability_of_guess_grr_plain.append(GRR_estimated_guess(users_grid_value_list, k, epsilon, 'guess'))


plt.rcParams.update({'font.size': 12})
plt.figure(figsize=(4 * 1.33, 4 * 1.33))
plt.plot(epsilon_list, probability_of_guess_grr_memoized, linewidth=2, color='purple', marker='o', markersize=10, mew=1.5,
         fillstyle='none', clip_on=False, label="GRR-Memoized")
plt.plot(epsilon_list, probability_of_guess_grr_plain, linewidth=2, color='grey', marker='o', markersize=10, mew=1.5,
         fillstyle='none', clip_on=False, label="GRR")
plt.xticks(fontsize=15)
plt.ylim(0, 1)
plt.ylabel("Ratio Of Guess")
plt.xlabel('Epsilon Values')
plt.grid(linestyle=':')
plt.legend(prop={'size': 12}, ncol=2, columnspacing=0.75)
plt.show()