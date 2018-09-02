import numpy as np
import math

import cv2

from line_operations import *
from line import Line
from lineList import LineList


def find_lines(image):

    original = image
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    unprocessed_lines = cv2.HoughLinesP(
        image,
        rho=6,
        theta=np.pi / 60,
        threshold=130,
        lines=np.array([]),
        minLineLength=45,
        maxLineGap=10
    )

    line_list = LineList(unprocessed_lines)

    line_list.remove_diagonal_lines()
    line_list.group_lines()
    # line_list.extrapolate_lines(original)
    new_list = reduce_to_two(line_list.lines.values())
    image_with_lines = draw_lines(original, new_list.lines.values())

    line1 = new_list.lines.values()[0]
    line2 = new_list.lines.values()[1]
    px, py = line1.find_intersection(line2)
    image_with_lines[py][px] = [255, 0, 0]

    return new_list, (px, py), image_with_lines
