from matplotlib import pyplot as plt
import csv
import numpy as np

from LDP.protocols import GRR_Aggregator, GRR_Client, ESAD_CLIENT, ESAD_AGGREGATOR


def create_histogram(est_frequency, k):
    plt.rcParams.update({'font.size': 12})
    plt.bar(range(k), est_frequency, color='grey', edgecolor='black', linewidth=1.2)
    plt.xticks(range(k), fontsize=15)
    plt.xlabel("Grid ID")
    plt.ylabel("Number of Users")
    plt.show()


def dataset_histogram(users_grid_value_list, k):
    grid_count = list()
    for grid in range(k):
        grid_count.append(0)
    for user_trajectory in users_grid_value_list:
        for user_value in user_trajectory:
            grid_count[user_value - 1] += 1
    create_histogram(grid_count, k)


def grr_client_aggregator():
    for epsilon in epsilon_list:
        print("Epsilon Value: " + str(epsilon))
        grr_report_list = list()
        for user_trajectory in users_grid_value_list:
            user_perturb_list = list()
            for user_value in user_trajectory:
                user_perturb_list.append(GRR_Client(user_value, k, epsilon))
            grr_report_list.append(user_perturb_list)
        est = GRR_Aggregator(grr_report_list, k, epsilon)
        create_histogram(est, k)


def hbv_client_aggregator(users_grid_value_list, epsilon_list):
    grr_report_list = list()
    seed = 1

    for epsilon in epsilon_list:
        print("Epsilon Value: " + str(epsilon))
        for user_trajectory in users_grid_value_list:
            grr_report_list.append(ESAD_CLIENT(user_trajectory, epsilon, seed))
            seed += 1

        est = ESAD_AGGREGATOR(grr_report_list, 100, k, epsilon)

        create_histogram(est, k)


if __name__ == '__main__':
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

    dataset_histogram(users_grid_value_list, k)
    hbv_client_aggregator(users_grid_value_list, epsilon_list)
