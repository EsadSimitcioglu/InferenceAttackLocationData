import glob
import os
import pandas as pd
from shapely import geometry
from shapely import ops
import math

max_lat = 40.21096
max_long = 121.555706
min_lat = 31.095299
min_long = 116.071547

write_filename = "../dataset/geolife.dat"

data_folder = r"C:\\Users\\esat-\\OneDrive\\Masaüstü\\Geolife Trajectories 1.3\\Data"

# Get a list of user folders
user_folders = [folder for folder in os.listdir(data_folder) if os.path.isdir(os.path.join(data_folder, folder))]

user_folders = user_folders[2:3]

def preprocess_geolife():
    rec = [(min_lat, min_long), (min_lat, max_long), (max_lat, max_long), (max_lat, min_long)]
    nx, ny = 4, 5  # number of columns and rows

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

    grids = list(result.geoms)

    out_file = open(write_filename, "w", encoding="utf-8")

    for user_folder in user_folders:
        trajectory_folder = os.path.join(data_folder, user_folder, 'Trajectory')

        # Get a list of .plt files in the trajectory folder
        plt_files = glob.glob(os.path.join(trajectory_folder, '*.plt'))

        for plt_file in plt_files:
            data = pd.read_csv(plt_file,
                               skiprows=6,
                               header=None,
                               usecols=[0, 1],
                               names=['Latitude', 'Longitude'])

            for index, row in data.iterrows():
                lat = (row['Latitude'])
                lon = (row['Longitude'])
                seq = []
                for j, part in enumerate(grids):
                    if part.contains(geometry.Point(lat, lon)):
                        seq.append(str(j + 1))  # Number grids starting from 1
                if len(seq) == 0:
                    continue
                out_file.write(" ".join(seq))
                out_file.write("\n")

            print(seq)
            print(plt_file, "is done.")

    out_file.close()

preprocess_geolife()
