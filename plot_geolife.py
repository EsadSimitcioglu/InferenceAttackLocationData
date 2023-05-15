import csv

import matplotlib.pyplot as plt
import numpy as np

csv.field_size_limit(int(1e9))


# Fetch value from csv file
latitude = []
longitude = []
with open('output4.csv', 'r') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')

    # Skip the header
    next(plots)

    for row in plots:
        latitude_longitude_list = row[1].strip('[]').split('], [')
        for latitude_longitude in latitude_longitude_list:
            latitude_longitude = latitude_longitude.split(', ')
            latitude.append(float(latitude_longitude[0]))
            longitude.append(float(latitude_longitude[1]))


# Create the scatter plot
plt.scatter(longitude, latitude)

# Set labels and title
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.title("Location Scatter Plot")

# Display the plot
plt.show()