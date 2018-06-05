import cv2
import numpy as np
import math
from lineList import LineList


def reduce_to_two(lines):
    # returns only the 2 lines most perpendicular
    visited = {}
    smallest_diff = math.pi / 2
    for line in lines:
        for line2 in lines:
            if line.hashify() != line2.hashify():
                if line.get_direction() != line2.get_direction():
                    if not visited.get(line.hashify()):
                        diff = math.fabs(math.pi / 2 - angle(line, line2))
                        if diff < smallest_diff:
                            smallest_diff = diff
                            result1 = line
                            result2 = line2
        visited[line.hashify()] = True

    results = LineList()
    results.add_line(result1)
    results.add_line(result2)
    return results


def angle(line, line2):
    u = [line.x2 - line.x1, line.y2 - line.y1]
    v = [line2.x2 - line2.x1, line2.y2 - line2.y1]
    norm_u = math.hypot(u[0], u[1])
    norm_v = math.hypot(v[0], v[1])
    inner_product = (u[0] * v[0]) + (u[1] * v[1])
    return math.acos(inner_product / (norm_u * norm_v))


def draw_lines(image, lines, thickness=3):
    # get image and a set of points that represents the lines
    # draws lines over image
    color = [255, 0, 0]
    if len(lines) == 0:
        return image

    for line in lines:
        if line.get_direction() == "vert":
            color = [0, 0, 255]
        if line.get_direction() == "hori":
            color = [0, 255, 0]
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

    return image


def find_first_axis_point(image, starting_point, direction):

    if direction == "verti":
        get_neighbours_radius(5, up)
