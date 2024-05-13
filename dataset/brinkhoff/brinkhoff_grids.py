import csv
from matplotlib import pyplot as plt
from shapely import geometry
from shapely import ops

users_grid_value_list = list()


# min and max values for float
min_x = 9999999999
max_x = -9999999999

min_y = 9999999999
max_y = -9999999999

max_long = 23854.0
max_lat = 30851.0

min_long = 281.0
min_lat = 3935.0

write_filename = "brinkhoff_grid_1_5.dat"


def preprocess_brinkhoff():

    global min_x  # Declare min_x as global
    global min_y  # Declare min_y as global

    global max_x  # Declare max_x as global
    global max_y  # Declare max_y as global

    with open('brinkhoff.dat') as f:
        reader = csv.reader(f, delimiter="\t")
        for line in reader:
            line_str = line[0]

            if (line_str[0] != '#'):
                trajectory_list = line_str[3:]
                trajectory_list = trajectory_list.split(";")
                user_grid_list = list()
                for trajectory in trajectory_list:

                    if (trajectory != ""):
                        trajectory_line = trajectory.split(",")

                        # convert string to float
                        trajectory_line = [float(i) for i in trajectory_line]

                        if trajectory_line[0] < min_x:
                            min_x = trajectory_line[0]
                        if trajectory_line[0] > max_x:
                            max_x = trajectory_line[0]

                        if trajectory_line[1] < min_y:
                            min_y = trajectory_line[1]
                        if trajectory_line[1] > max_y:
                            max_y = trajectory_line[1]

                        user_grid_list.append(trajectory_line)

                users_grid_value_list.append(user_grid_list)


def create_grid_brinkhoff():
    ##construct the rectangle using shapely
    rec = [(min_lat, min_long), (min_lat, max_long), (max_lat, max_long), (max_lat, min_long)]
    nx, ny = 1, 5

    polygon = geometry.Polygon(rec)
    minx, miny, maxx, maxy = polygon.bounds
    dx = (maxx - minx) / nx
    dy = (maxy - miny) / ny
    horizontal_splitters = [geometry.LineString([(minx, miny + i * dy), (maxx, miny + i * dy)]) for i in range(ny)]
    vertical_splitters = [geometry.LineString([(minx + i * dx, miny), (minx + i * dx, maxy)]) for i in range(nx)]
    splitters = horizontal_splitters + vertical_splitters

    result = polygon
    for splitter in splitters:
        result = geometry.MultiPolygon(ops.split(result, splitter))

    grids = list(result.geoms)

    # Plot the grids
    x, y = polygon.exterior.xy
    plt.plot(x, y, color='#6699cc', alpha=0.7, linewidth=3, solid_capstyle='round', zorder=2)
    for grid in grids:
        x, y = grid.exterior.xy
        plt.plot(x, y, color='#6699cc', alpha=0.7, linewidth=3, solid_capstyle='round', zorder=2)
    plt.show()

    with open(write_filename, 'w', newline='') as file:
        for user in users_grid_value_list:
            sequence_list = []
            for user_trajectory in user:
                lon = user_trajectory[0]
                lat = user_trajectory[1]
                point = geometry.Point(lon, lat)

                for i, part in enumerate(grids):
                    if part.contains(point):
                        sequence_list.append(str(i + 1))
                        break

            if len(sequence_list) == 0:
                continue

            file.write(" ".join(sequence_list))
            file.write("\n")

        file.close()


# Call the function to preprocess the Brinkhoff dataset
preprocess_brinkhoff()

# Call the modified function to preprocess the Microsoft Geolife dataset
create_grid_brinkhoff()
