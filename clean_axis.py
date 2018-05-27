import cv2
import numpy as np
from line_operations import *


def clean_axis(image, lines, group, filename, extension):

    original = image
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    original = erase_lines(original, lines)

    cv2.imwrite("./pictures/results/{}{}_hough{}".format(group,
                                                         filename, extension), original)

    # cv2.imshow("", dilation)
    cv2.waitKey(0)
