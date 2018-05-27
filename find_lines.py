import cv2
import numpy as np
import math
from line_operations import *


def find_lines(image):

    original = image
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    lines = cv2.HoughLinesP(
        image,
        rho=6,
        theta=np.pi / 60,
        threshold=130,
        lines=np.array([]),
        minLineLength=45,
        maxLineGap=10
    )

    lines = clean_diagonal_lines(lines)
    lines = group_lines(lines)
    lines = reduce_to_two(lines)
    # lines = extrapolate_lines(original, lines)

    # original = draw_lines(original, lines)
    # original = erase_lines(original, lines)



    return lines

    # cv2.imshow("", dilation)
    # cv2.waitKey(0)
