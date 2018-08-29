import cv2
import numpy as np
import math

import scipy.sparse.linalg as spla
import matplotlib.pyplot as plt


def get_points(image, origin):
    ox = origin[0]
    oy = origin[1]

    points_x = []
    points_y = []

    for row in range(0, image.shape[0]):
        for col in range(0, image.shape[1]):
            if (image[row][col] == [255, 255, 255]).all():
                # print ("{},{}".format(col-ox, oy-row))
                points_x.append(col-ox)
                points_y.append(oy-row)

    return np.array(points_x), np.array(points_y)


def calculate_polinomial(a_vec, x):
    result = 0
    for i in range(0, len(a_vec)):
        a = a_vec[i]
        result = result + a * x**i

    return result


def get_eq_polinomial(degree, x_points, y_points):

    mat_trans = []
    for i in range(0, degree+1):
        mat_trans.append(np.power(x_points, i))

    mat_trans = np.array(mat_trans)
    mat = mat_trans.transpose()

    A = np.dot(mat_trans, mat)
    b = np.dot(mat_trans, y_points)

    return A, b


def print_results(solution, points_x, image, origin):

    image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
    for j in points_x:
        i = calculate_polinomial(solution, j)
        j = int(math.floor(j)) + origin[0]
        i = (int(math.floor(i)) - origin[1]) * -1
        if (abs(i) > image.shape[0]):
            continue
        image[i][j] = [0, 255, 0]

    return image


def save_txt(image, origin):
    ox = origin[0]
    oy = origin[1]

    points_x = []
    points_y = []

    with open('somefile.txt', 'a') as the_file:
        the_file.write("{} {}\n".format(oy, ox))
        for row in range(0, image.shape[0]):
            for col in range(0, image.shape[1]):
                if (image[row][col] == [255, 255, 255]).all():
                    the_file.write("{} {}\n".format(row, col))


def fit_curve(image, origin_point):
    points_x, points_y = get_points(image, origin_point)
    save_txt(image, origin_point)

    A, b = get_eq_polinomial(2, points_x, points_y)

    sol = np.linalg.solve(A, b)
    print sol
    image = print_results(sol, points_x, image, origin_point)

    # points_x.sort()
    # x = points_x
    # y = calculate_polinomial(sol, x)
    # plt.plot(x, y)
    # plt.show()

    return image
