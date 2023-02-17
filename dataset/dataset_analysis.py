
row_count = 4

def analyze_taken_path(users_value_list):
    path_dict = {}
    for user_value in users_value_list:
        for value_index, value in enumerate(user_value):
            if value_index == 0:
                continue

            prev_grid = user_value[value_index - 1]

            if value == prev_grid:
                continue

            path = str(prev_grid) + "->" + str(value)

            if path in path_dict:
                path_dict[path] += 1
            else:
                path_dict[path] = 1

    return {k: v for k, v in sorted(path_dict.items(), key=lambda item: item[1], reverse=True)}


def analyze_not_taken_path(analyzed_path_dict):
    untaken_dict = {}

    value = 0

    for column in range(1, 5):
        for row in range(1, 6):
            value += 1
            if value == 1:

                path = str(value) + "->" + str(value + 1)

                if path not in analyzed_path_dict:
                    untaken_dict[path] = 1

                path = str(value) + "->" + str(value + row_count)

                if path not in analyzed_path_dict:
                    untaken_dict[path] = 1

                path = str(value) + "->" + str(value + row_count + 1)

                if path not in analyzed_path_dict:
                    untaken_dict[path] = 1

            elif value == 17:

                path = str(value) + "->" + str(value + 1)

                if path not in analyzed_path_dict:
                    untaken_dict[path] = 1

                path = str(value) + "->" + str(value - row_count)

                if path not in analyzed_path_dict:
                    untaken_dict[path] = 1

                path = str(value) + "->" + str(value - row_count + 1)

                if path not in analyzed_path_dict:
                    untaken_dict[path] = 1

            elif value % row_count == 1:
                path = str(value) + "->" + str(value - row_count)

                if path not in analyzed_path_dict:
                    untaken_dict[path] = 1

                path = str(value) + "->" + str(value - row_count + 1)

                if path not in analyzed_path_dict:
                    untaken_dict[path] = 1

                path = str(value) + "->" + str(value + 1)

                if path not in analyzed_path_dict:
                    untaken_dict[path] = 1

                path = str(value) + "->" + str(value + row_count)

                if path not in analyzed_path_dict:
                    untaken_dict[path] = 1

                path = str(value) + "->" + str(value + row_count + 1)

                if path not in analyzed_path_dict:
                    untaken_dict[path] = 1

            if value == 4:
                path = str(value) + "->" + str(value - 1)

                if path not in analyzed_path_dict:
                    untaken_dict[path] = 1

                path = str(value) + "->" + str(value + row_count)

                if path not in analyzed_path_dict:
                    untaken_dict[path] = 1

                path = str(value) + "->" + str(value + row_count - 1)

                if path not in analyzed_path_dict:
                    untaken_dict[path] = 1

            elif value == 20:
                path = str(value) + "->" + str(value - 1)

                if path not in analyzed_path_dict:
                    untaken_dict[path] = 1

                path = str(value) + "->" + str(value - row_count)

                if path not in analyzed_path_dict:
                    untaken_dict[path] = 1

                path = str(value) + "->" + str(value - row_count - 1)

                if path not in analyzed_path_dict:
                    untaken_dict[path] = 1

            elif value % row_count == 0:
                path = str(value) + "->" + str(value - 1)

                if path not in analyzed_path_dict:
                    untaken_dict[path] = 1

                path = str(value) + "->" + str(value + row_count)

                if path not in analyzed_path_dict:
                    untaken_dict[path] = 1

                path = str(value) + "->" + str(value + row_count - 1)

                if path not in analyzed_path_dict:
                    untaken_dict[path] = 1

                path = str(value) + "->" + str(value - row_count)

                if path not in analyzed_path_dict:
                    untaken_dict[path] = 1

                path = str(value) + "->" + str(value - row_count - 1)

                if path not in analyzed_path_dict:
                    untaken_dict[path] = 1

            if value % row_count != 0 and value % row_count != 1:
                path = str(value) + "->" + str(value - 1)

                if path not in analyzed_path_dict:
                    untaken_dict[path] = 1

                path = str(value) + "->" + str(value + 1)

                if path not in analyzed_path_dict:
                    untaken_dict[path] = 1

                path = str(value) + "->" + str(value + row_count)

                if path not in analyzed_path_dict:
                    untaken_dict[path] = 1

                path = str(value) + "->" + str(value + row_count - 1)

                if path not in analyzed_path_dict:
                    untaken_dict[path] = 1

                path = str(value) + "->" + str(value + row_count + 1)

                if path not in analyzed_path_dict:
                    untaken_dict[path] = 1

                path = str(value) + "->" + str(value - row_count)

                if path not in analyzed_path_dict:
                    untaken_dict[path] = 1

                path = str(value) + "->" + str(value - row_count - 1)

                if path not in analyzed_path_dict:
                    untaken_dict[path] = 1

                path = str(value) + "->" + str(value - row_count + 1)

                if path not in analyzed_path_dict:
                    untaken_dict[path] = 1

    return untaken_dict


def check_possibility(perturb_value_list, row_count):
    possibility_list = list()

    for value_index, value in enumerate(perturb_value_list):
        if value_index == 0:
            possibility_list.append(1)
            continue

        prev_grid_location = perturb_value_list[value_index - 1]

        if value % row_count == 1:
            if prev_grid_location in [value, value + 1] or (
                    prev_grid_location in [value - row_count, value - row_count + 1]) or (
                    prev_grid_location in [value + row_count, value + row_count + 1]):
                possibility_list.append(1)
                continue
        elif value % row_count == 0:
            if prev_grid_location in [value, value - 1] or (
                    prev_grid_location in [value - row_count, value - row_count - 1]) or (
                    prev_grid_location in [value + row_count, value + row_count - 1]):
                possibility_list.append(1)
                continue
        else:
            if (prev_grid_location in [value - 1, value, value + 1]) or \
                    (prev_grid_location in [value - row_count - 1, value - row_count, value - row_count + 1]) or \
                    (prev_grid_location in [value + row_count - 1, value + row_count, value + row_count + 1]):
                possibility_list.append(1)
                continue
        possibility_list.append(0)

    return possibility_list