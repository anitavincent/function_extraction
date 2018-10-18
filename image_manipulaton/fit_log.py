import numpy as np

from util import *


def log(x, a, b, c):
    return (a*np.log(x*b) + c)


def fit_log(x_points, y_points):

    a = np.std(y_points)
    c = a
    guess = [a/3, 1, c]
    y_guess = log(x_points, guess[0], guess[1], guess[2])

    def lsq(arg):
        a = arg[0]
        b = arg[1]
        c = arg[2]
        now = ((a*np.log(x_points*b) + c)) - y_points
        return np.sum(now**2)

    if np.max(x_points) > 0 and np.min(x_points) < 0:
        return False, y_guess, False, "log"
    elif np.max(x_points) <= 0:
        guess = np.multiply(guess, [1, -1, 1])
        y_guess = log(x_points, guess[0], guess[1], guess[2])
        res = get_mini(x_points, y_points, guess, lsq)
    else:
        res = get_mini(x_points, y_points, guess, lsq)

    if (res):
        y_result = log(x_points, res.x[0], res.x[1], res.x[2])

        return res, y_guess, y_result, "log"
    else:
        return False, y_guess, False, "log"
