import cv2
import numpy as np
import math
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
    line_list.extrapolate_lines(original)
    # lines = reduce_to_two(lines)

    original = draw_lines(original, line_list.lines.values())
    # original = erase_lines(original, lines)

    return line_list, original

    # cv2.imshow("", dilation)
    # cv2.waitKey(0)
