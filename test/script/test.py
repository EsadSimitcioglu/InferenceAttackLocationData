import csv
import numpy as np
from LDP.estimation_different_grid import GRR_estimated_guess, RAPPOR_estimated_guess, OUE_estimated_guess, \
    OLH_estimated_guess, GRR_advance_estimated_guess, RAPPOR_advance_estimated_guess, OUE_advance_estimated_guess, \
    OLH_advance_estimated_guess

from LDP.estimation_same_grid import grr_estimated_guess, rappor_estimated_guess, oue_estimated_guess, \
    olh_estimated_guess

# Parameters for simulation
dataset_list = ['taxi.dat', 'brinkhoff_grid.dat', 'geolife_grid.dat']
dataset_name_list = ['Taxi', 'Brinkhoff', 'Geolife']
k = 20  # attribute's domain size (grid size)
epsilon_list = [0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 5]  # number of epsilon for test cases


for dataset_index in range(len(dataset_list)):

    users_grid_value_list = list()
    probability_of_guess_grr_plain = list()
    probability_of_guess_grr_trained = list()
    probability_of_guess_rappor = list()
    probability_of_guess_oue = list()
    probability_of_guess_olh = list()

    with open(dataset_list[dataset_index]) as f:
        reader = csv.reader(f, delimiter="\t")
        for line in reader:
            grid_list = line[0].split(" ")
            grid_list_int = [eval(i) for i in grid_list]
            grid_list_int_nd = np.array(grid_list_int)
            users_grid_value_list.append(grid_list_int_nd)

    for epsilon in epsilon_list:
        print("Epsilon Value: " + str(epsilon))
        probability_of_guess_grr_plain.append(grr_estimated_guess(users_grid_value_list, k, epsilon))
        print("GRR is Ready")
        probability_of_guess_rappor.append(rappor_estimated_guess(users_grid_value_list, k, epsilon))
        print("RAPPOR is Ready")
        probability_of_guess_oue.append(oue_estimated_guess(users_grid_value_list, k, epsilon))
        print("OUE is Ready")
        probability_of_guess_olh.append(olh_estimated_guess(users_grid_value_list, k, epsilon))
        print("OLH is Ready")

    # Write the result to file
    with open(dataset_name_list[dataset_index] + '_plain_attack.txt', 'w') as f:

        f.write(dataset_name_list[dataset_index] + '_plain_attack\n')

        f.write("GRR Plain\n")
        for item in probability_of_guess_grr_plain:
            f.write("%s\n" % item)

        f.write("RAPPOR\n")
        for item in probability_of_guess_rappor:
            f.write("%s\n" % item)

        f.write("OUE\n")
        for item in probability_of_guess_oue:
            f.write("%s\n" % item)

        f.write("OLH\n")
        for item in probability_of_guess_olh:
            f.write("%s\n" % item)

    for epsilon in epsilon_list:
        print("Epsilon Value: " + str(epsilon))
        probability_of_guess_grr_plain.append(GRR_estimated_guess(users_grid_value_list, k, epsilon, 'guess'))
        print("GRR is Ready")
        probability_of_guess_rappor.append(RAPPOR_estimated_guess(users_grid_value_list, k, epsilon, 'guess'))
        print("RAPPOR is Ready")
        probability_of_guess_oue.append(OUE_estimated_guess(users_grid_value_list, k, epsilon, 'guess'))
        print("OUE is Ready")
        probability_of_guess_olh.append(OLH_estimated_guess(users_grid_value_list, k, epsilon, 'guess'))
        print("OLH is Ready")

    # Write the result to file
    with open(dataset_name_list[dataset_index] + '_plain_attack.txt', 'w') as f:

        f.write(dataset_name_list[dataset_index] + '_plain_attack\n')

        f.write("GRR Plain\n")
        for item in probability_of_guess_grr_plain:
            f.write("%s\n" % item)

        f.write("RAPPOR\n")
        for item in probability_of_guess_rappor:
            f.write("%s\n" % item)

        f.write("OUE\n")
        for item in probability_of_guess_oue:
            f.write("%s\n" % item)

        f.write("OLH\n")
        for item in probability_of_guess_olh:
            f.write("%s\n" % item)

    probability_of_guess_grr_plain = list()
    probability_of_guess_grr_trained = list()
    probability_of_guess_rappor = list()
    probability_of_guess_oue = list()
    probability_of_guess_olh = list()

    for epsilon in epsilon_list:
        print("Epsilon Value: " + str(epsilon))
        probability_of_guess_grr_plain.append(GRR_advance_estimated_guess(users_grid_value_list, k, epsilon, 3))
        print("GRR is Ready")
        probability_of_guess_rappor.append(RAPPOR_advance_estimated_guess(users_grid_value_list, k, epsilon, 3))
        print("RAPPOR is Ready")
        probability_of_guess_oue.append(OUE_advance_estimated_guess(users_grid_value_list, k, epsilon, 3))
        print("OUE is Ready")
        probability_of_guess_olh.append(OLH_advance_estimated_guess(users_grid_value_list, k, epsilon, 3))
        print("OLH is Ready")

    # Write the result to file
    with open(dataset_name_list[dataset_index] + '_chain_attack' + '.txt', 'w') as f:

        f.write(dataset_name_list[dataset_index] + '_chain_attack\n')

        f.write("GRR Plain\n")
        for item in probability_of_guess_grr_plain:
            f.write("%s\n" % item)

        f.write("RAPPOR\n")
        for item in probability_of_guess_rappor:
            f.write("%s\n" % item)

        f.write("OUE\n")
        for item in probability_of_guess_oue:
            f.write("%s\n" % item)

        f.write("OLH\n")
        for item in probability_of_guess_olh:
            f.write("%s\n" % item)