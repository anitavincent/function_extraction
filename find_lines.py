import cv2
import numpy as np
import math
from line_operations import *


def find_lines(image, group, filename, extension):

    original = image
    # retval, image = cv2.threshold(image, 2, 1, cv2.THRESH_BINARY)
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
    lines = extrapolate_lines(original, lines)
    lines = reduce_to_two(lines)

    # original = draw_lines(original, lines)
    original = erase_lines(original, lines)

    cv2.imwrite("./pictures/results/{}{}_hough{}".format(group,
                                                         filename, extension), original)

    # cv2.imshow("", dilation)
    cv2.waitKey(0)
