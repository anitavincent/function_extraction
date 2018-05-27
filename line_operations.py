import cv2
import numpy as np
import math


def reduce_to_two(lines):
    # returns only the 2 lines most perpendicular
    orientation = classify_lines(lines)
    visited = {}
    smallest_diff = math.pi / 2
    for line in lines:
        for line2 in lines:
            if hashify(line) != hashify(line2):
                if orientation[hashify(line)] != orientation[hashify(line2)]:
                    if not visited.get(hashify(line2)):
                        diff = math.fabs(math.pi / 2 - angle(line, line2))
                        if diff < smallest_diff:
                            smallest_diff = diff
                            result1 = line
                            result2 = line2
        visited[hashify(line)] = True

    results = add_line_to_list([result1], result2)
    return results

# COPIADO
# TODO


def find_intersection(line1, line2):
    # extract points
    x1, y1, x2, y2 = line1[0]
    x3, y3, x4, y4 = line2[0]
    # compute determinant
    Px = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) /  \
        ((x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4))
    Py = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) /  \
        ((x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4))
    return Px, Py


def angle(line, line2):
    for x1, y1, x2, y2 in line:
        for X1, Y1, X2, Y2 in line2:
            u = [x2 - x1, y2 - y1]
            v = [X2 - X1, Y2 - Y1]
            norm_u = math.hypot(u[0], u[1])
            norm_v = math.hypot(v[0], v[1])
            inner_product = (u[0] * v[0]) + (u[1] * v[1])
            return math.acos(inner_product / (norm_u * norm_v))


def extrapolate_lines(image, lines):
    # extrapolates all lines until they reach the borders
    extra_lines = lines
    for line in lines:
        slope = 0
        for x1, y1, x2, y2 in line:
            slope = get_slope(line)
        line_ex = extrapolated_line(image, line, slope)
        extra_lines = remove_line_from_list(extra_lines, line)
        extra_lines = add_line_to_list(extra_lines, line_ex)
    return extra_lines


def extrapolated_line(image, line, slope):
    # extrapolates a single line
    height, width = image.shape[:2]

    for x1, y1, x2, y2 in line:
        if slope is None:
            return [[x1, 0, x2, height - 1]]
        elif slope == 0.0:
            return [[0, y1, width - 1, y2]]
        else:
            m = slope
            b = y1 - m * x1
            x1b = (0 - b) / m
            x2b = (height - 1 - b) / m
            return [[int(x1b), 0, int(x2b), height - 1]]


def draw_lines(image, lines, color=[255, 0, 0], thickness=1):
    # get image and a set of points that represents the lines
    # draws lines over image
    dicio = classify_lines(lines)

    if lines is None:
        return image

    for line in lines:
        colur = color
        if dicio[hashify(line)] == "vert":
            colur = [0, 0, 255]
        if dicio[hashify(line)] == "hori":
            colur = [0, 255, 0]
        for x1, y1, x2, y2 in line:
            cv2.line(image, (x1, y1), (x2, y2), colur, thickness)

    return image


def erase_lines(image, lines):

    dicio = classify_lines(lines)
    acceptable_angle_variation = 10

    if lines is None:
        return image

    for line in lines:
        for x1, y1, x2, y2 in line:
            point = (x1, y1)
            first_point = find_first_axis_point(image, point, dici[hashify])
            # image = erase_line(image, point, dicio[hashify],
            #                     acceptable_angle_variation)

    return image


def find_first_axis_point(image, starting_point, direction):

    if direction == "verti":
        get_neighbours_radius(5, up)


def group_lines(lines):
    # gets set of lines and returns reduced set
    # for each line looks for lines that are close
    # and merge them
    close_lines = lines
    while(True):
        if close_lines is None or close_lines.shape[0] == 1:
            break
        for line in lines:
            close_lines = find_close_lines(line, lines)
            if close_lines is None:
                continue
            lines = merge_close_lines(close_lines, lines)
            if close_lines is not None and not close_lines.shape[0] == 1:
                break

    return lines


def merge_close_lines(close_lines, lines):
    # receives set of close_lines (lines to be merged)
    # and full set of lines
    # returns full set now with close_lines merged
    lines_orientation = classify_lines(close_lines)
    for line in close_lines:
        orientation = lines_orientation[hashify(line)]
        break

    if orientation == "hori":
        full_line = interpolate_hori(close_lines)
    else:
        full_line = interpolate_vert(close_lines)

    for line in close_lines:
        lines = remove_line_from_list(lines, line)

    lines = add_line_to_list(lines, full_line)
    return lines


def interpolate_hori(lines):
    # gets set of horizontal lines
    # returns single interpolated line
    most_left = []
    most_right = []
    low_x = 1000000
    high_x = -10
    for line in lines:
        for x1, y1, x2, y2 in line:
            if x1 < low_x:
                low_x = x1
                most_left = [x1, y1]
            if x2 < low_x:
                low_x = x2
                most_left = [x2, y2]
            if x1 > high_x:
                high_x = x1
                most_right = [x1, y1]
            if x2 > high_x:
                high_x = x2
                most_right = [x2, y2]

    return [[most_left[0], most_left[1], most_right[0], most_right[1]]]


def interpolate_vert(lines):
    # gets set of vertical lines
    # returns single interpolated line
    most_top = []
    most_bottom = []
    low_y = 1000000
    high_y = -10
    for line in lines:
        for x1, y1, x2, y2 in line:
            if y1 < low_y:
                low_y = y1
                most_bottom = [x1, y1]
            if y2 < low_y:
                low_y = y2
                most_bottom = [x2, y2]
            if y1 > high_y:
                high_y = y1
                most_top = [x1, y1]
            if y2 > high_y:
                high_y = y2
                most_top = [x2, y2]

    return [[most_bottom[0], most_bottom[1], most_top[0], most_top[1]]]


def find_close_lines(line, lines):
    # gets set of lines and a pivot line
    # looks for lines that are close in space to pivot line
    # returns set of lines that are close, including the pivot
    tolerance = 30

    lines_class = classify_lines(lines)
    if lines_class[hashify(line)] == "none":
        return None

    for line2 in lines:
        if lines_class[hashify(line)] != lines_class[hashify(line2)]:
            lines = remove_line_from_list(lines, line2)

    for line2 in lines:
        if lines_class[hashify(line)] == "hori":
            if not check_close_horizontal(line, line2, tolerance):
                lines = remove_line_from_list(lines, line2)
        elif lines_class[hashify(line)] == "vert":
            if not check_close_vertical(line, line2, tolerance):
                lines = remove_line_from_list(lines, line2)

    return lines


def check_close_horizontal(line1, line2, thr):
    for x1, y1, x2, y2 in line1:
        for X1, Y1, X2, Y2 in line2:
            if Y1 >= (y1 - thr) and Y1 <= (y1 + thr):
                return True
            if Y2 >= (y1 - thr) and Y2 <= (y1 + thr):
                return True
    return False


def check_close_vertical(line1, line2, thr):
    for x1, y1, x2, y2 in line1:
        for X1, Y1, X2, Y2 in line2:
            if X1 >= (x1 - thr) and X1 <= (x1 + thr):
                return True
            if X2 >= (x1 - thr) and X2 <= (x1 + thr):
                return True
    return False


def hashify(line):
    # returns a unique hash to represent a line
    return tuple(line.tolist()[0])


def classify_lines(lines):
    # gets set of lines
    # returns dictionary with the orientation of each line
    dicti = {}
    for line in lines:
        slope = get_slope(line)
        if(slope is not None):
            slope = math.fabs(slope)
            if slope > 7.5:
                dicti[hashify(line)] = "vert"
            elif slope < 0.15:
                dicti[hashify(line)] = "hori"
            else:
                dicti[hashify(line)] = "none"
        else:
            dicti[hashify(line)] = "vert"
    return dicti


def clean_diagonal_lines(lines):
    lines_class = classify_lines(lines)
    clean_lines = lines
    for line in lines:
        if lines_class[hashify(line)] == "none":
            clean_lines = remove_line_from_list(clean_lines, line)

    return clean_lines


def remove_line_from_list(lista, line):
    index = lista.tolist().index(line.tolist())
    return np.delete(lista, index, axis=0)


def add_line_to_list(lista, line):
    return np.vstack([lista, [line]])


def get_slope(line):
    for x1, y1, x2, y2 in line:
        if x1 == x2:
            return None
        return float(y2 - y1) / float(x2 - x1)
