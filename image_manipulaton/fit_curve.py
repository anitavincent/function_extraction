import numpy as np
import math


def calculate_polinomial(sol, x):
    p = np.poly1d(sol)

    return p(x)


def fit_poli(x_points, y_points, degree):

    sol, residual, _, _, _ = np.polyfit(x_points, y_points, degree, full=True)
    y_result = calculate_polinomial(sol, x_points)
    y_guess = y_result

    error = residual[0]

    return sol, y_guess, y_result, error


def fit_all_poli(x_points, y_points, top_degree=8):

    acceptable_error = 5 * len(x_points)
    dictio = {}

    for i in [0, 1, 2, 3, 4, 5, 6, 7, 8]:
        sol, y_guess, y_result, error = fit_poli(x_points, y_points, i)
        dictio[i] = error

        if error <= acceptable_error:
            return sol, y_guess, y_result, error, i
        elif (i == top_degree):
            break

    insignificant_diff = 2 * len(x_points)
    big = 8
    for i in range(0, 8):
        if np.abs(dictio[8] - dictio[i]) <= insignificant_diff:
            sol, y_guess, y_result, error = fit_poli(x_points, y_points, i)
            return sol, y_guess, y_result, error, i

    return sol, y_guess, y_result, error, i
