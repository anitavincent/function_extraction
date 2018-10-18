import numpy as np

from util import *


def expo(x, a, b, c):
    return (np.exp(a*x+b) + c)


def fit_exponential(x_points, y_points, guess=[-0.9, -0.8, 1]):

    def lsq(arg):
        a = arg[0]
        b = arg[1]
        c = arg[2]
        now = (np.exp(a * x_points + b) + c) - y_points
        return np.sum(now**2)

    res = get_mini(x_points, y_points, guess, lsq)

    y_guess = expo(x_points, guess[0], guess[1], guess[2])
    if (res):
        y_result = expo(x_points, res.x[0], res.x[1], res.x[2])

        return res, y_guess, y_result, "exponential"
    else:
        return False, y_guess, y_result, "exponential"

    return drawing
