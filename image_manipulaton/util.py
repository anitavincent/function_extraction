import cv2
import numpy as np
import math

import matplotlib.pyplot as plt
from scipy.optimize import curve_fit, minimize


def get_points(image, origin):
    ox = origin[0]
    oy = origin[1]

    points_x = []
    points_y = []

    for col in range(0, image.shape[1]):
        for row in range(0, image.shape[0]):
            if (image[row][col] == [255, 255, 255]).all():
                points_x.append(col-ox)
                points_y.append(oy-row)

    return np.array(points_x), np.array(points_y)


def draw_points(image, origin, points_x, points_y, color=[0, 255, 0]):
    ox = origin[0]
    oy = origin[1]

    # image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
    # blank_image = np.zeros((image.shape[0], image.shape[1], 3), np.uint8)

    for index in range(0, len(points_x)):
        if math.isinf(points_y[index]):
            continue
        i = int(oy - points_y[index])
        if i >= image.shape[0] or i < 0:
            continue
        j = ox + points_x[index]
        image[i][j] = color

    return image


def mat_plot(x_points, y_points, y_result):
    x = x_points
    y = y_points
    plt.plot(x, y)
    plt.axis('equal')

    plt.plot(x_points, y_result, color='red')
    plt.show()


def get_mini(x_points, y_points, guess, lsq, min_method='Nelder-mead'):
    # print "trying with value: "
    # print guess

    res = minimize(lsq, guess, method=min_method)

    return res
