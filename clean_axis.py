import cv2
import numpy as np
import math
from line_operations import *
from line import Line
from copy import copy, deepcopy

BLOCK_SIZE = 15
VERT_ACCEPTABLE_MIN = 2.4
HORI_ACCEPTABLE_MAX = 0.40
POINT_DISTANCE = 8


def erase_lines(image, lines):

    if lines is None:
        return image

    for line in lines:
        image = erase_line(image, line)

    return image


def erase_line(image, line):

    starting_point = (line.x1, line.y1)

    if line.get_direction() == "vert":
        erase("up", image, starting_point)

        starting_point = line.get_pixel_on_line(starting_point, POINT_DISTANCE)
        starting_point = get_white_pixel_around(image, starting_point)

        erase("down", image, starting_point)
    else:
        erase("left", image, starting_point)
        starting_point = line.get_pixel_on_line(starting_point, POINT_DISTANCE)
        starting_point = get_white_pixel_around(image, starting_point)
        erase("right", image, starting_point)

    starting_point = (line.x2, line.y2)
    if (image[starting_point[1]][starting_point[0]] != [0, 0, 0]).all():

        if line.get_direction() == "vert":
            erase("up", image, starting_point)

            starting_point = line.get_pixel_on_line(starting_point,
                                                    POINT_DISTANCE)
            starting_point = get_white_pixel_around(image, starting_point)
            erase("down", image, starting_point)
        else:
            erase("left", image, starting_point)
            starting_point = line.get_pixel_on_line(starting_point,
                                                    POINT_DISTANCE)
            starting_point = get_white_pixel_around(image, starting_point)
            erase("right", image, starting_point)

    return image


def build_mask(image, starting_point, block_s, offset=1):
    h, w = image.shape[:2]
    mask = np.zeros((h+offset*2, w+offset*2), np.uint8)
    start_x = starting_point[0] + offset
    start_y = starting_point[1] + offset
    mask_start = (start_x-block_s,
                  start_y-block_s)
    mask_end = (start_x+block_s,
                start_y+block_s)
    cv2.rectangle(mask, mask_start, mask_end, 1)

    return mask


def get_white_pixel_around(image, point):
    offset = 3
    h, w = image.shape[:2]

    init_x, init_y = point
    if init_x >= w or init_x < 0:
        return None
    if init_y >= h or init_y < 0:
        return None
    if (image[init_y][init_x] == [255, 255, 255]).all():
        return point

    for x in range(init_x-offset, init_x+offset):
        if x >= w or x < 0:
            continue
        if (image[init_y][x] == [255, 255, 255]).all():
            return (x, init_y)

    for y in range(init_y-offset, init_y+offset):
        if y >= h or y < 0:
            continue
        if (image[y][init_x] == [255, 255, 255]).all():
            return (init_x, y)

    return None


def flood_fill(image, starting_point):
    block_s = BLOCK_SIZE+1
    mask = build_mask(image, starting_point, block_s)
    seed_pt = starting_point
    cv2.floodFill(image, mask, seed_pt, (0, 0, 255), flags=8)

    return image


def move(direction, image, starting_point):
    point = starting_point
    original = deepcopy(image)
    while True:
        next = get_next(direction, deepcopy(original), point)
        if next is None:
            break
        point = next

    return point


def erase(direction, image, starting_point):
    if starting_point is None:
        return

    point = starting_point
    original = deepcopy(image)
    while True:
        next_p = get_next(direction, deepcopy(original), point)
        if next_p is None:
            break
        cv2.line(image, point, next_p, [0, 0, 0], 2)
        point = next_p

    return point


def get_next(direction, image, last_point):
    image = flood_fill(image, last_point)
    points = get_valid_points(direction, image, last_point)
    if points == []:
        return None

    point = get_best_angle(direction, last_point, points)

    return point


# REFACTOR THIS PLS
def get_best_angle(direction, last_point, new_points):
    if direction == "up" or direction == "down":
        max_slope = -10
        return_point = None
        for point in new_points:
            line = Line([[last_point[0], last_point[1], point[0], point[1]]])
            l_slope = line.get_slope()
            # none slope means its perfectly vertical
            if l_slope is None:
                return point

            l_slope = math.fabs(l_slope)
            if l_slope < VERT_ACCEPTABLE_MIN:
                continue
            if l_slope > max_slope:
                return_point = point
                max_slope = l_slope
        return return_point
    else:
        min_slope = 1000000
        return_point = None
        for point in new_points:
            line = Line([[last_point[0], last_point[1], point[0], point[1]]])
            l_slope = line.get_slope()
            l_slope = math.fabs(l_slope)
            if l_slope > HORI_ACCEPTABLE_MAX:
                continue
            if l_slope < min_slope:
                return_point = point
                min_slope = l_slope
        return return_point


def get_valid_points(direction, image, last_point):
    mask = build_mask(image, last_point, BLOCK_SIZE, offset=0)
    points = []

    heigth, width = image.shape[:2]

    init_x = last_point[0]
    init_y = last_point[1]

    for x in range(init_x-BLOCK_SIZE-1, init_x+BLOCK_SIZE+1):
        for y in range(init_y-BLOCK_SIZE-1, init_y+BLOCK_SIZE+1):
            if x >= width or y >= heigth:
                continue
            if mask[y][x] != 1:
                continue
            if (image[y][x] == [0, 0, 255]).all():
                # import ipdb; ipdb.set_trace()
                if check_for_direction(direction, last_point, (x, y)):
                    points.append((x, y))

    # if direction=="up" or direction=="down":
    #     import ipdb; ipdb.set_trace()
    # cv2.imwrite("./bla2.jpg", image)
    return points


def check_for_direction(dir, point_init, point_b):
    if dir == "up":
        return point_init[1] > point_b[1]
    if dir == "down":
        return point_init[1] < point_b[1]
    if dir == "left":
        return point_init[0] > point_b[0]
    if dir == "right":
        return point_init[0] < point_b[0]


def clean_axis(image, axis_lines):
    # image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = erase_lines(image, axis_lines.lines.values())

    return image

    # cv2.imshow("", dilation)
    # cv2.waitKey(0)
