import csv
import numpy as np
import sys

from guess_trajectory import guess_advance_user_trajectory, guess_advance_user_trajectory_olh
from LDP import GRR
from hidden_markov_model import HMM

method_name_list = ['GRR', 'RAPPOR', 'OUE', 'OLH']
method_func_list = [guess_advance_user_trajectory, guess_advance_user_trajectory_olh]

dataset_file = sys.argv[1]
method_name = sys.argv[2]
epsilon = float(sys.argv[3])

if method_name == "OLH":
    method = 1
else:
    method = 0

user_grid_value_list = []
probability_of_guess = []

with open(dataset_file) as f:
    reader = csv.reader(f, delimiter='\t')
    for line in reader:
        grid_list = line[0].split(" ")
        grid_list_int = [int(i) for i in grid_list]
        grid_list_int_nd = np.array(grid_list_int)
        user_grid_value_list.append(grid_list_int_nd)

