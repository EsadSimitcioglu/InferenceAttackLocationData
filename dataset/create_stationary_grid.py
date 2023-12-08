import csv
import numpy as np
users_grid_value_list = list()
with open('brinkhoff/brinkhoff_grid.dat') as f:
    reader = csv.reader(f, delimiter="\t")
    for line in reader:
        grid_list = line[0].split(" ")
        grid_list_int = [eval(i) for i in grid_list]
        grid_list_int_nd = np.array(grid_list_int)
        grid_value = grid_list_int_nd[0]
        asd = [grid_value] * len(grid_list_int_nd)
        users_grid_value_list.append(asd)
with open('brinkhoff/brinkhoff_stationary_grid.dat', 'w', newline='') as csv_file:
    # Create a CSV writer object
    csv_writer = csv.writer(csv_file, delimiter=' ')
    # Write each list as a row in the CSV file
    for row in users_grid_value_list:
        csv_writer.writerow(row)