from matplotlib import pyplot as plt
import csv
import numpy as np

from LDP.protocols.GRR import GRR

from LDP.protocols.HBV import HBV

def calculate_average_error(actual_hist, noisy_hist):
    err_sum = 0
    for bar_key in range(len(actual_hist)):
        err_sum += abs(noisy_hist[bar_key] - actual_hist[bar_key])

    avg_err = err_sum / len(actual_hist)
    return avg_err

def calculate_mean_square_error(actual_hist, noisy_hist):
    err_sum = 0
    for bar_key in range(len(actual_hist)):
        err_sum += (noisy_hist[bar_key] - actual_hist[bar_key]) ** 2

    avg_err = err_sum / len(actual_hist)
    return avg_err

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

    # Calculate the percentage of users in each grid
    total_users = sum(grid_count)
    for grid in range(k):
        grid_count[grid] = grid_count[grid] / total_users

    a = sum(grid_count)

    #


    create_histogram(grid_count, k)
    return grid_count

def grr_client_aggregator(users_grid_value_list, epsilon):

    grr = GRR(k, epsilon)
    grr_report_list = list()
    for user_trajectory in users_grid_value_list:
        user_perturb_list = list()
        for user_value in user_trajectory:
            user_perturb_list.append(grr.client(user_value))
        grr_report_list.append(user_perturb_list)
    est = grr.server(grr_report_list)
    create_histogram(est, k)

    return est




def hbv_client_aggregator(users_grid_value_list, epsilon):
    grr_report_list = list()
    seed = 1

    hbv = HBV(k, epsilon)
    for user_trajectory in users_grid_value_list:
        grr_report_list.append(hbv.client(user_trajectory, seed))
        seed += 1

    est = hbv.server(grr_report_list)

    create_histogram(est, k)

    return est


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

    with open('../../../dataset/taxi/taxi_grid_2.dat') as f:
        reader = csv.reader(f, delimiter="\t")
        for line in reader:
            grid_list = line[0].split(" ")
            grid_list_int = [eval(i) for i in grid_list]
            grid_list_int_nd = np.array(grid_list_int)
            users_grid_value_list.append(grid_list_int_nd)

    actual_hist = dataset_histogram(users_grid_value_list, k)
    a = sum(actual_hist)
    for epsilon in epsilon_list:
        print("*" * 50)
        print("Epsilon Value: " + str(epsilon))
        noisy_hist = hbv_client_aggregator(users_grid_value_list, epsilon)
        avg_err = calculate_average_error(actual_hist, noisy_hist)
        mse_err = calculate_mean_square_error(actual_hist, noisy_hist)
        print("Average Error: " + str(avg_err))
        print("Mean Square Error: " + str(mse_err))