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


def draw_lines(image, lines, thickness=3):
    color = [255, 0, 0]
    # get image and a set of points that represents the lines
    # draws lines over image
    if len(lines) == 0:
        return image

    for line in lines:
        if line.get_direction() == "vert":
            color = [0, 0, 255]
        if line.get_direction() == "hori":
            color = [0, 255, 0]
        if line.get_direction() == "none":
            print "ACHOU DIAGO"
        line.draw(image, color, thickness)

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
