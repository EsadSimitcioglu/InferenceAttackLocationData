import pandas as pd
import numpy as np
import json
from matplotlib import pyplot as plt
from shapely import geometry
from shapely import ops

## This script builds the sequential data file by constructing grids from coordinates

max_lat = -8.58  ##-8.28    ### 52.900803
max_long = 41.18  ### 51.037119
min_lat = -8.68  ##-8.78    ### -9.781308
min_long = 41.14  ### 31.992111

write_filename = "../dataset/taxi.dat"


def preprocess_kaggle():
    ##construct the rectangle using shapely
    rec = [(min_lat, min_long), (min_lat, max_long), (max_lat, max_long), (max_lat, min_long)]
    nx, ny = 4, 5  # number of columns and rows  4,5

    polygon = geometry.Polygon(rec)
    minx, miny, maxx, maxy = polygon.bounds
    dx = (maxx - minx) / nx  # width of a small part
    dy = (maxy - miny) / ny  # height of a small part
    horizontal_splitters = [geometry.LineString([(minx, miny + i * dy), (maxx, miny + i * dy)]) for i in range(ny)]
    vertical_splitters = [geometry.LineString([(minx + i * dx, miny), (minx + i * dx, maxy)]) for i in range(nx)]
    splitters = horizontal_splitters + vertical_splitters

    result = polygon
    for splitter in splitters:
        result = geometry.MultiPolygon(ops.split(result, splitter))

    parts = [list(part.exterior.coords) for part in result.geoms]  ####
    print(parts)  ####
    print(len(list(result.geoms)))

    # read the coordinate data
    data = pd.read_csv("../dataset/kaggle-taxi-data.csv",
                       chunksize=10000,
                       usecols=['POLYLINE', 'TIMESTAMP'],
                       converters={'POLYLINE': lambda x: json.loads(x)})
    with open("../dataset/kaggle.csv", 'w') as f:
        f.write("timestamp,lat,lon\n")

    out_file = open(write_filename, "w", encoding="utf-8")
    grids = list(result.geoms)

    for i, chunk in enumerate(data):
        for path in chunk.POLYLINE:
            if len(path) > 0:  ##0 lat 1 long

                # for cor in path:
                #     if cor[0]<-8 and cor[0]>-9:  ##to eliminate outliers  ## -6 and -10
                #         lats.append(cor[0])
                #     else:
                #         lat_outliers += 1
                #     if cor[1]<42 and cor[1]>41:  ## 42 and 40
                #         longs.append(cor[1])
                #     else:
                #         long_outliers += 1
                seq = []
                for cor in path:
                    for j, part in enumerate(grids):
                        if part.contains(geometry.Point(cor[0], cor[1])):  ## if it is in this grid
                            # print(i,end=" ")
                            seq.append(str(j + 1))  ##number grids starting from 1
                # print()
                if len(seq) == 0:
                    continue
                out_file.write(" ".join(seq))
                out_file.write("\n")
        print("Chunk", i, "done.")
        if i == 10:
            break


def create_path_list(chunk):
    ##construct the rectangle using shapely
    rec = [(min_lat, min_long), (min_lat, max_long), (max_lat, max_long), (max_lat, min_long)]
    nx, ny = 4, 5  # number of columns and rows  4,5

    polygon = geometry.Polygon(rec)
    minx, miny, maxx, maxy = polygon.bounds
    dx = (maxx - minx) / nx  # width of a small part
    dy = (maxy - miny) / ny  # height of a small part
    horizontal_splitters = [geometry.LineString([(minx, miny + i * dy), (maxx, miny + i * dy)]) for i in range(ny)]
    vertical_splitters = [geometry.LineString([(minx + i * dx, miny), (minx + i * dx, maxy)]) for i in range(nx)]
    splitters = horizontal_splitters + vertical_splitters

    result = polygon
    for splitter in splitters:
        result = geometry.MultiPolygon(ops.split(result, splitter))

    parts = [list(part.exterior.coords) for part in result.geoms]  ####
    print(parts)  ####
    print(len(list(result.geoms)))
    grids = list(result.geoms)

    location_data = dict()

    path_index = 0

    for id in chunk.TRIP_ID:

        if path_index == 10:
            break

        #print(id)
        path = chunk.POLYLINE[path_index]
        grid_number_of_id = list()
        #print(path)
        #print("******************************************************")

        for cor in path:
            for j, part in enumerate(grids):
                if part.contains(geometry.Point(cor[0], cor[1])):  ## if it is in this grid
                    grid_number_of_id.append(j+1)
                    print("TRIP ID : " + str(id) + " is in " + str(j + 1))

        location_data[id] = grid_number_of_id
        path_index += 1
    return location_data

data = pd.read_csv("../dataset/kaggle-taxi-data.csv",
                   chunksize=10,
                   usecols=['POLYLINE', 'TRIP_ID'],
                   converters={'POLYLINE': lambda x: json.loads(x), 'TRIP_ID': lambda y: json.loads(y)})


location_data = dict()
for i, chunk in enumerate(data):
    location_data = create_path_list(chunk)
    break

print(location_data)