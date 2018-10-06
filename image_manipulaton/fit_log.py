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


def log(x, a, b, c):
    return (a*np.log(x*b) + c)


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


def fit_log(curve, origin):
    x_points, y_points = get_points(curve, origin)
    a = np.std(y_points)
    guess = [a, 1, -300]
    if np.max(x_points) > 0 and np.min(x_points) < 0:
        return 0
    elif np.max(x_points) <= 0:
        guess = np.multiply(guess, [1, -1, 1])
        res, found_min = get_mini(x_points, y_points, guess)
    else:
        res, found_min = get_mini(x_points, y_points, guess)

    if (res):
        # x = x_points
        # y = y_points
        # plt.plot(x, y)
        # plt.axis('equal')

        # plt.plot(x_points, expo(x_points, *popt), color='red')
        # plt.show()
        print res.x
        curve = cv2.cvtColor(curve, cv2.COLOR_GRAY2RGB)

        y_result = log(x_points, res.x[0], res.x[1], res.x[2])

        drawing = draw_points(curve, origin, x_points, y_result)

        y_result = log(x_points, guess[0], guess[1], guess[2])

        drawing = draw_points(drawing, origin, x_points, y_result, [0, 0, 255])
    else:
        drawing = 0

    return drawing


def get_mini(x_points, y_points, guess=[-0.9, -0.8, 1]):
    print "trying with value: "
    print guess

    def lsq(arg):
        a = arg[0]
        b = arg[1]
        c = arg[2]
        now = ((a*np.log(x_points*b) + c)) - y_points
        return np.sum(now**2)

    guesses = guess
    # res = minimize(lsq, guesses, method='powell')
    res = minimize(lsq, guesses, method='Nelder-Mead')

    return res, res.fun
