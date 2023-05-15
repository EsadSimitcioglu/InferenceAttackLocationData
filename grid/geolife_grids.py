import datetime

import pandas as pd
from matplotlib import pyplot as plt
from shapely import geometry
from shapely import ops

# Update the bounding box values to match the Microsoft Geolife dataset
max_lat = 40.05
max_long = 116.55
min_lat = 39.8
min_long = 116.2

write_filename = "../grid/geolife.dat"


def preprocess_geolife():
    ##construct the rectangle using shapely
    rec = [(min_lat, min_long), (min_lat, max_long), (max_lat, max_long), (max_lat, min_long)]
    nx, ny = 4, 5

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

    # Read the Microsoft Geolife dataset
    data = pd.read_csv("../output.csv",
                       chunksize=10000,
                       usecols=['Latitude', 'Longitude', 'Date', 'Time'])

    out_file = open(write_filename, "w", encoding="utf-8")

    for i, chunk in enumerate(data):
        latitudes = chunk['Latitude'].tolist()
        longitudes = chunk['Longitude'].tolist()
        dates = chunk['Date'].tolist()
        times = chunk['Time'].tolist()

        first_day = dates[0]
        first_time = times[0]

        is_point_founded = False
        sequence_list = []

        # Convert the date and time to a datetime object
        datetime_str = first_day + " " + first_time
        previous_datetime_obj = datetime.datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")

        for lat, lon, date, times in zip(latitudes, longitudes, dates, times):
            datetime_str = date + " " + times
            datetime_obj = datetime.datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")

            # Calculate the time difference between the current point and the first point
            time_difference = datetime_obj - previous_datetime_obj

            if time_difference.seconds > 1000 and is_point_founded:
                print("New trajectory : " + datetime_str)
                out_file.write(" ".join(sequence_list))
                out_file.write("\n")
                sequence_list = []
                previous_datetime_obj = datetime_obj
                is_point_founded = False
            elif time_difference.seconds > 60:
                print("New point : " + datetime_str)
                point = geometry.Point(lat, lon)
                for j, part in enumerate(grids):
                    if part.contains(point):
                        is_point_founded = True
                        sequence_list.append(str(j + 1))
                        break
                previous_datetime_obj = datetime_obj


# Call the modified function to preprocess the Microsoft Geolife dataset
preprocess_geolife()
