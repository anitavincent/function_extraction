import numpy as np
import cv2

MIN_ACCEPTABLE_PROPORTION = 0.20


def get_biggest_area(areas):
    max_area = -1
    for area in areas:
        if area > max_area:
            max_area = area

    return max_area


def erase_small_lines(image, stats, max_area):
    size, b = stats.shape
    for i in range(1, size):
        area = stats[i][cv2.CC_STAT_AREA]
        if area < max_area * MIN_ACCEPTABLE_PROPORTION:
            xi = stats[i][cv2.CC_STAT_LEFT]
            yi = stats[i][cv2.CC_STAT_TOP]
            width = stats[i][cv2.CC_STAT_WIDTH]
            height = stats[i][cv2.CC_STAT_HEIGHT]
            cv2.rectangle(image, (xi, yi), (xi+width, yi+height),
                          [0, 0, 0], -1)


def remove_noise(image):

    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY)
    output = cv2.connectedComponentsWithStats(thresh, 8, cv2.CV_32S)
    stats = output[2]

    areas = stats[1:, cv2.CC_STAT_AREA]
    max_area = get_biggest_area(areas)
    erase_small_lines(image, stats, max_area)

    return image
