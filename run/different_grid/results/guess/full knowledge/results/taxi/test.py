import numpy as np
from matplotlib import pyplot as plt
from shapely import geometry
from shapely import ops
import csv

max_lat = -8.58
min_lat = -8.68
lat_diff = max_lat - min_lat
lat_count = 4
cell_x = lat_diff / lat_count

max_long = 41.18
min_long = 41.14
long_diff = max_long - min_long
long_count = 5
cell_y = long_diff / long_count

grid_dict = {}

d_max = ((max_lat - min_lat) ** 2) + ((max_long - min_long) ** 2)


epsilon_list = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 5.0]
km_list = []

method_dict = {"GRR": [], "RAPPOR": [], "OUE": [], "OLH": []}


def create_grid():
    rec = [
        (min_lat, min_long),
        (min_lat, max_long),
        (max_lat, max_long),
        (max_lat, min_long),
    ]
    nx, ny = 4, 5  # number of columns and rows  4,5

    polygon = geometry.Polygon(rec)
    minx, miny, maxx, maxy = polygon.bounds
    dx = (maxx - minx) / nx  # width of a small part
    dy = (maxy - miny) / ny  # height of a small part
    horizontal_splitters = [
        geometry.LineString([(minx, miny + i * dy), (maxx, miny + i * dy)])
        for i in range(ny)
    ]
    vertical_splitters = [
        geometry.LineString([(minx + i * dx, miny), (minx + i * dx, maxy)])
        for i in range(nx)
    ]
    splitters = horizontal_splitters + vertical_splitters

    result = polygon
    for splitter in splitters:
        result = geometry.MultiPolygon(ops.split(result, splitter))

    parts = [list(part.exterior.coords) for part in result.geoms]  ####
    grids = list(result.geoms)

    # Initialize a list to store the middle points of each cell and their colors
    middle_points = []
    colors = []

    for grid in grids:
        # Calculate the centroid of each polygon (cell)
        centroid = grid.centroid
        middle_points.append(centroid)

        # Assign a color to each point (you can customize this as needed)
        colors.append("red")  # Change 'red' to your desired color

    # Now, `middle_points` contains the middle points of every cell, and `colors` contains their respective colors.

    # Plot the original polygon
    x, y = polygon.exterior.xy
    plt.plot(
        x, y, color="#6699cc", alpha=0.7, linewidth=3, solid_capstyle="round", zorder=2
    )

    # Plot the cells (polygons)
    for grid in grids:
        x, y = grid.exterior.xy
        plt.plot(
            x,
            y,
            color="#6699cc",
            alpha=0.7,
            linewidth=3,
            solid_capstyle="round",
            zorder=2,
        )

    index = 1

    # Plot all the middle points with their assigned colors
    for centroid, color in zip(middle_points, colors):
        grid_dict[index] = (centroid.x, centroid.y)
        index += 1
        plt.scatter(
            centroid.x, centroid.y, color=color, s=50
        )  # Adjust 's' for point size

    color_list = [
        "red",
        "blue",
        "green",
        "yellow",
        "black",
        "pink",
        "orange",
        "purple",
        "brown",
        "gray",
    ]

    for i in range(1, 21):
        plt.text(
            grid_dict[i][0],
            grid_dict[i][1],
            str(i),
            fontsize=12,
            color="black",
            weight="bold",
        )

    # find border value of each grid
    for i, grid in enumerate(grids):
        x, y = grid.exterior.xy

        # pick unique elements from array
        x_unique = np.unique(x)
        y_unique = np.unique(y)

        # sort the array
        x_unique.sort()
        y_unique.sort()

        # print(x_unique)
        # print(y_unique)

        grid_dict[i + 1] = (x_unique[0], x_unique[1], y_unique[0], y_unique[1])

        plt.plot(
            x,
            y,
            color=color_list[i % 10],
            alpha=0.7,
            linewidth=3,
            solid_capstyle="round",
            zorder=2,
        )

    print(grid_dict)
    plt.show()


def path_metric():
    users_grid_gt_list = []

    with open("../../../../../../../../run/taxi_grid.dat") as f:
        reader = csv.reader(f, delimiter="\t")
        for line in reader:
            grid_list = line[0].split(" ")
            grid_list_int = [eval(i) for i in grid_list]
            grid_list_int_nd = np.array(grid_list_int)
            users_grid_gt_list.append(grid_list_int_nd)

    for method in method_dict:
        for epsilon in epsilon_list:
            users_grid_guess_list = []

            with open(
                method + "/taxi-" + method + "-" + str(epsilon) + "_path_fk.csv"
            ) as f:
                reader = csv.reader(f, delimiter="\t")
                for line in reader:
                    grid_list = line[0].split(" ")
                    grid_list_int = [eval(i) for i in grid_list]
                    grid_list_int_nd = np.array(grid_list_int)
                    users_grid_guess_list.append(grid_list_int_nd)

                average_km = 0

                for guess, gt in zip(users_grid_guess_list, users_grid_gt_list):
                    sum_km = 0
                    for index in range(min(len(gt), len(guess))):
                        guess_value = grid_dict[guess[index]]
                        gt_value = grid_dict[gt[index]]

                        sum_km += (guess_value[0] - gt_value[0]) ** 2 + (
                            guess_value[1] - gt_value[1]
                        ) ** 2

                    average_km += (sum_km / d_max) / len(gt)

                average_km = average_km / len(users_grid_guess_list)
                method_dict[method].append(average_km)
        print(method_dict)


create_grid()
path_metric()
