import csv
# Traverse the directory tree

import os

from matplotlib import pyplot as plt

# Path to the directory containing the PLT files
plt_dir_path = 'Data'

is_path_plot = False

with open('geolife.csv', 'w') as csvfile:
    plots = csv.writer(csvfile, delimiter=',')
    plots.writerow(['file', 'date', 'latitude', 'longitude', 'time'])

    for root, dirs, files in os.walk(plt_dir_path):
        for file in files:
            if file.endswith(".plt"):

                # Read the PLT file
                with open(os.path.join(root, file), 'r') as plt_file:
                    plt_data = plt_file.readlines()
                    # Skip the first 6 lines
                    plt_data = plt_data[6:]

                    # Extract the latitude and longitude data
                    latitude = []
                    longitude = []
                    date = []
                    time = []

                    for plt_line in plt_data:
                        line = plt_line.strip().split(',')
                        latitude.append(float(line[0]))
                        longitude.append(float(line[1]))
                        date.append(line[5])
                        time.append(line[6])

                    plots.writerow([file, [date], [latitude], [longitude], [time]])

                    if is_path_plot:
                        # Create the scatter plot
                        plt.scatter(longitude, latitude, c='r', alpha=0.5, marker='o')

                        # Set labels and title
                        plt.xlabel("Longitude")
                        plt.ylabel("Latitude")

                        # Set the title
                        plt.title(file)

                        # Display the plot
                        plt.show()
