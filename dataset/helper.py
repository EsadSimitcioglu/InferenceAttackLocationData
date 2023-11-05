import csv
import numpy as np


def read_dataset(file_path):
    users_trajectory_list = list()

    with open(file_path) as f:
        reader = csv.reader(f, delimiter="\t")
        for line in reader:
            grid_list = line[0].split(" ")
            grid_list_int = [eval(i) for i in grid_list]
            grid_list_int_nd = np.array(grid_list_int)
            users_trajectory_list.append(grid_list_int_nd)

    return users_trajectory_list
