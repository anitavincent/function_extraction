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


def sin(x, a, b, c, d):
    return (a * np.sin(b*(x)+c) + d)


def draw_points(image, origin, points_x, points_y, color=[0, 255, 0]):
    ox = origin[0]
    oy = origin[1]

    # image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
    # blank_image = np.zeros((image.shape[0], image.shape[1], 3), np.uint8)

    for index in range(0, len(points_x)):
        i = int(oy - points_y[index])
        if i >= image.shape[0] or i < 0:
            continue
        j = ox + points_x[index]
        image[i][j] = color

    return image


def try_multiple_guesses(x_points, y_points):
    a = 3*np.std(y_points)/(2**0.5)
    vari = float(np.max(x_points)-np.min(x_points))
    d = guess_offset = np.mean(y_points)
    div_value = 1000
    b = vari/div_value
    guess = [a, b, 0, d]
    res, found_min = get_mini(x_points, y_points, guess)

    while True:
        div_value = div_value*5
        b = vari/div_value
        next_guess = [a, b, 0, d]
        next_res, next_min = get_mini(x_points, y_points, guess)
        acceptable = (1000)*len(x_points)
        if (next_min >= found_min and found_min < acceptable):
            break
        else:
            guess = next_guess
            found_min = next_min
            res = next_res

        if b < 0.0001:
            break

    return res, found_min, guess


def fit_sin(curve, origin):
    x_points, y_points = get_points(curve, origin)

    res, found_min, guess = try_multiple_guesses(x_points, y_points)

    if (res):
        # x = x_points
        # y = y_points
        # plt.plot(x, y)
        # plt.axis('equal')

        # plt.plot(x_points, expo(x_points, *popt), color='red')
        # plt.show()
        print res.x
        curve = cv2.cvtColor(curve, cv2.COLOR_GRAY2RGB)
        y_result = sin(x_points, res.x[0], res.x[1], res.x[2], res.x[3])

        drawing = draw_points(curve, origin, x_points, y_result)

        y_result = sin(x_points, guess[0], guess[1], guess[2], guess[3])

        drawing = draw_points(drawing, origin, x_points, y_result, [0, 0, 255])
    else:
        drawing = 0

    return drawing


def get_mini(x_points, y_points, guess=[500, 0.1, 0, 0]):
    # bom resulguess=[90, 0.017, 0, 0]
    print "trying with value: "
    print guess

    def lsq(arg):
        a = arg[0]
        b = arg[1]
        c = arg[2]
        d = arg[3]

        now = (a * np.sin(b*(x_points)+c) + d) - y_points
        return np.sum(now**2)

    guesses = guess
    res = minimize(lsq, guesses, method='powell')
    # res = minimize(lsq, guesses, method='Nelder-Mead')

    return res, res.fun
