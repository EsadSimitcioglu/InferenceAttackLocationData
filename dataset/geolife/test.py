import csv

import numpy as np

users_grid_value_list = list()
data_point_count = 8

with open('geolife_stationary_grid.dat') as f:
    reader = csv.reader(f, delimiter="\t")
    for line in reader:
        grid_list = line[0].split(" ")
        grid_list_int = [eval(i) for i in grid_list]
        grid_list_int_nd = np.array(grid_list_int)
        if len(grid_list_int_nd) >= data_point_count:
            asd = grid_list_int_nd[:data_point_count]
            users_grid_value_list.append(asd)



with open('geolife_grid_stationary_' + str(data_point_count) + '.dat', 'w', newline='') as csv_file:
    # Create a CSV writer object
    csv_writer = csv.writer(csv_file, delimiter=' ')

    # Write each list as a row in the CSV file
    for row in users_grid_value_list:
        csv_writer.writerow(row)
