import numpy as np

from util import *


def sin(x, a, b, c, d):
    return (a * np.sin(b*(x)+c) + d)


def try_multiple_guesses(x_points, y_points, lsq):
    a = 3*np.std(y_points)/(2**0.5)
    vari = float(np.max(x_points)-np.min(x_points))
    d = guess_offset = np.mean(y_points)
    div_value = 1000
    b = vari/div_value
    guess = [a, b, 0, d]
    res = get_mini(x_points, y_points, guess, lsq, min_method='powell')
    found_min = res.fun

    while True:
        div_value = div_value*5
        b = vari/div_value
        next_guess = [a, b, 0, d]
        next_res = get_mini(x_points, y_points, guess,
                            lsq, min_method='powell')
        next_min = res.fun
        acceptable = (1000)*len(x_points)
        if (next_min >= found_min and found_min < acceptable):
            break
        else:
            guess = next_guess
            found_min = next_min
            res = next_res

        if b < 0.0001:
            break

    return res, guess


def fit_sin(x_points, y_points):

    def lsq(arg):
        a = arg[0]
        b = arg[1]
        c = arg[2]
        d = arg[3]

        now = (a * np.sin(b*(x_points)+c) + d) - y_points
        return np.sum(now**2)

    res, guess = try_multiple_guesses(x_points, y_points, lsq)

    y_guess = sin(x_points, guess[0], guess[1], guess[2], guess[3])

    if (res):
        y_result = sin(x_points, res.x[0], res.x[1], res.x[2], res.x[3])

        return res, y_guess, y_result, "sin"
    else:
        return False, y_guess, y_result, "sin"
