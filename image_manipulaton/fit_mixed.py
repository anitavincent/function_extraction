import numpy as np

from util import *


def mixed(x, arg):
    a, b, c, d, e, f, g, h, i, k, m, n, o, p, q, r, s, t, u = arg
    exp = (
        np.exp(a*x+b) + c
    ) + (
        1 / (d*(x**2) + e*x + f)
    ) + (
        g*(x**2) + h*x + i
    ) + (
        k*np.log(np.abs(x*m)) + n
    ) + (
        o * np.sin(p*(x)+q) + r
    ) + (
        1 / (s * np.sqrt(2*np.pi)) * (np.exp(-0.5 * ((x-t)/u)**2)))
    return exp


def fit_mixed(x_points, y_points):

    a = np.std(y_points)
    b = 3*a/(2**0.5)
    vari = float(np.max(x_points)-np.min(x_points))
    c = np.mean(y_points)
    div_value = 10
    d = vari/div_value
    guess = [-0.9, -0.8, 1, 0, -0.0001, 0, 1,
             2, 3, a, 1, -300, b, d, 0, c, a, c, a]

    def lsq(arg):
        now = mixed(x_points, arg) - y_points
        return np.sum(now**2)

    try:
        res = get_mini(x_points, y_points, guess, lsq)
    except RuntimeWarning:
        print "An overflow happened - skipping this curve :("
        print ""
        return False, y_guess, y_result, "mixed"

    y_guess = mixed(x_points, guess)
    if (res):
        y_result = mixed(x_points, res.x)

        return res, y_guess, y_result, "mixed"
    else:
        return False, y_guess, y_result, "mixed"
