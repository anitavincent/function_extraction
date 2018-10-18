import numpy as np

from util import *


def normal(x, a, b, c):
    return (1 / (a * np.sqrt(2*np.pi)) * (np.exp( -0.5 * ((x-b)/c)**2 ) ))


def fit_gauss(x_points, y_points):
    a = np.std(y_points)
    b = np.mean(y_points)
    c = a
    guess = [a, b, c]

    def lsq(arg):
        a = arg[0]
        b = arg[1]
        c = arg[2]
        now = (1 / (a * np.sqrt(2*np.pi)) * (np.exp( -0.5 * ((x_points-b)/c)**2 ) )) - y_points
        return np.sum(now**2)

    res = get_mini(x_points, y_points, guess, lsq)

    y_guess = normal(x_points, guess[0], guess[1], guess[2])
    if (res):
        y_result = normal(x_points, res.x[0], res.x[1], res.x[2])

        return res, y_guess, y_result, "gaussian"
    else:
        return False, y_guess, False, "gaussian"

