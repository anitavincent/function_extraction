import cv2
import numpy as np
import math

from fit_curve import fit_all_poli
from fit_exponential import fit_exponential
from fit_sin import fit_sin
from fit_log import fit_log
from fit_gauss import fit_gauss
from fit_fraction import fit_fraction
from fit_mixed import fit_mixed
from util import *

complexity = {
    "polynomial0": 1,
    "polynomial1": 1,
    "polynomial2": 1,
    "polynomial3": 1,
    "polynomial4": 1,
    "polynomial5": 1,
    "exponential": 2,
    "fraction": 3,
    "log": 3,
    "polynomial6": 4,
    "sin": 4,
    "gauss": 4,
    "polynomial7": 5,
    "polynomial8": 5,
    "mixed": 50,
}


def fits_better(res, best_diff, current, name):
    significant_difference = 50
    if (np.abs(res.fun-best_diff) >= significant_difference):
        if (res.fun > best_diff):
            return False
        return True

    if (complexity[name] <= complexity[current]):
        return True
    else:
        return False


def find_best_fit(curve, origin, plot_guess=True):
    x_points, y_points = get_points(curve, origin)

    # best_res = 0
    # y_guess_plot = 0
    # y_result_plot = 0
    # best_diff = float('Inf')
    # winning_curve = ""

    sol, y_guess, y_result, error, degree = fit_all_poli(x_points, y_points)
    best_res = sol
    y_guess_plot = y_guess
    y_result_plot = y_result
    best_diff = error
    winning_curve = ("polynomial{}".format(degree))

    for func in (
        fit_log, fit_fraction, fit_sin, fit_gauss, fit_exponential
    ):
        res, y_guess, y_result, name = func(x_points, y_points)

        if (res):
            if (fits_better(res, best_diff, winning_curve, name)):
                best_res = res
                y_guess_plot = y_guess
                y_result_plot = y_result
                best_diff = res.fun
                winning_curve = name
                break

    print "fit with:"
    print winning_curve
    print "with solution"
    try:
        best_res = best_res.x
    except:
        pass
    print best_res
    print ""

    if (best_diff >= 0):
        curve = cv2.cvtColor(curve, cv2.COLOR_GRAY2RGB)

        drawing = draw_points(curve, origin, x_points, y_result_plot)

        if plot_guess:
            drawing = draw_points(drawing, origin, x_points,
                                  y_guess_plot, [0, 0, 255])
    else:
        drawing = 0

    return drawing, best_diff
