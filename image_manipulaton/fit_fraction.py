import numpy as np

from util import *


def poly_inverse(x, a, b, c):
    return 1 / (a*(x**2) + b*x + c)


def fit_fraction(x_points, y_points, guess=[0, -0.0001, 0]):

    y_guess = poly_inverse(x_points, guess[0], guess[1], guess[2])

    def lsq(arg):
        a = arg[0]
        b = arg[1]
        c = arg[2]
        now = poly_inverse(x_points, a, b, c) - y_points
        return np.sum(now**2)

    res = get_mini(x_points, y_points, guess, lsq)

    if (res):
        y_result = poly_inverse(x_points, res.x[0], res.x[1], res.x[2])
        return res, y_guess, y_result, "fraction"

    return False, y_guess, False, "fraction"
