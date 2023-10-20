import matplotlib.pyplot as plt
from shapely import geometry, ops
from shapely.geometry import Polygon, polygon
from PIL import Image

max_lat = 40.05
max_long = 116.55
min_lat = 39.8
min_long = 116.2


##construct the rectangle using shapely
rec = [(min_lat, min_long), (min_lat, max_long), (max_lat, max_long), (max_lat, min_long)]
nx, ny = 9, 9

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


# Load the map image (replace 'map_image.jpg' with the actual path to your map image)
map_image = Image.open('../ss.png')

# Create a new figure
fig, ax = plt.subplots()

# Plot the map image as the background for the entire plot
ax.imshow(map_image, extent=[minx, maxx, miny, maxy], aspect='auto')

# Your existing code to plot polygons and grids
x, y = polygon.exterior.xy
plt.plot(x, y, color='#000000', alpha=0.7, linewidth=3, solid_capstyle='round', zorder=2)

for grid in grids:
    x, y = grid.exterior.xy
    plt.plot(x, y, color='#000000', alpha=0.7, linewidth=3, solid_capstyle='round', zorder=2)

# Remove axis labels and ticks
ax.set_xticks([])
ax.set_yticks([])

# Remove grid lines
ax.grid(False)

# Show the plot
plt.show()