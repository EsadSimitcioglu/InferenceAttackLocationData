from shapely import geometry
from shapely import ops

DATASET_COORDINATES = {
    "taxi": {
        "max_lat": -8.58,
        "min_lat": -8.68,
        "max_long": 41.18,
        "min_long": 41.14,
    },
    "geolife": {
        "max_lat": 40.05,
        "min_lat": 39.8,
        "max_long": 116.55,
        "min_long": 116.2,
    },
    "brinkhoff": {
        "max_lat": 30851.0,
        "min_lat": 3935.0,
        "max_long": 23854.0,
        "min_long": 281.0,
    },
}


def create_grid(dataset_name):
    coordinates = DATASET_COORDINATES[dataset_name]
    max_lat = coordinates["max_lat"]
    min_lat = coordinates["min_lat"]
    max_long = coordinates["max_long"]
    min_long = coordinates["min_long"]

    d_max = ((max_lat - min_lat) ** 2) + ((max_long - min_long) ** 2)

    grid_dict = {}

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

    grids = list(result.geoms)

    index = 1
    for grid in grids:
        centroid = grid.centroid
        grid_dict[index] = (centroid.x, centroid.y)
        index += 1

    return [grid_dict, d_max]


def normalized_distance_error(dataset_name, true_list, guess_list):
    grid_dict, d_max = create_grid(dataset_name)
    average_km = 0
    for guess, gt in zip(guess_list, true_list):
        sum_km = 0
        for index in range(min(len(gt), len(guess))):
            guess_value = grid_dict[guess[index]]
            gt_value = grid_dict[gt[index]]

            sum_km += (guess_value[0] - gt_value[0]) ** 2 + (
                guess_value[1] - gt_value[1]
            ) ** 2
        average_km += (sum_km / d_max) / len(gt)

    average_km = average_km / len(guess_list)
    return average_km


def prediction_accuracy(true_list, guess_list):
    prob_sum = 0
    index_counter = 0

    for guess_trajectory, true_trajectory in zip(guess_list, true_list):
        for guess_value, true_value in zip(guess_trajectory, true_trajectory):
            if guess_value == true_value:
                prob_sum += 1
            index_counter += 1

    return prob_sum / index_counter


def experiment_metrics(test_type, true_list, guess_list, dataset_name=None):
    result = 0
    if test_type == "PA":
        result = prediction_accuracy(true_list, guess_list)
    elif test_type == "NDE":
        result = normalized_distance_error(dataset_name, true_list, guess_list)

    return result
