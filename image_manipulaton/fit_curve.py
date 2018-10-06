import cv2
import numpy as np
import math

import scipy.sparse.linalg as spla
import matplotlib.pyplot as plt


def get_points(image, origin):
    ox = origin[0]
    oy = origin[1]

    points_x = []
    points_y = []

    for col in range(0, image.shape[1]):
        for row in range(0, image.shape[0]):
            if (image[row][col] == [255, 255, 255]).all():
                # print ("{},{}".format(col-ox, oy-row))
                points_x.append(col-ox)
                points_y.append(oy-row)

    return np.array(points_x), np.array(points_y)


def calculate_polinomial(sol, x):
    p = np.poly1d(sol)

    return p(x)


def print_results(solution, points_x, image, origin):

    image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
    for j in points_x:
        i = calculate_polinomial(solution, j)
        j = int(math.floor(j)) + origin[0]
        i = (int(math.floor(i)) - origin[1]) * -1
        if (abs(i) > image.shape[0]):
            continue
        image[i][j] = [0, 255, 0]

    return image


def fit_curve(image, origin_point):
    points_x, points_y = get_points(image, origin_point)
    x = points_x
    y = points_y
    plt.plot(x, y)

    sol = np.polyfit(x, y, 3)
    image = print_results(sol, points_x, image, origin_point)

    points_x.sort()
    x = points_x
    y = calculate_polinomial(sol, x)
    plt.plot(x, y, color='blue')
    plt.axis('equal')
    plt.show()

    return image
