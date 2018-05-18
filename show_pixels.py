import cv2
import numpy as np


def show_pixels(group, filename):
    height, width = reduce("border_results.txt")
    blank_image = np.zeros((height, width, 3), np.uint8)
    blank_image[:, :] = (255, 255, 255)

    with open("border_results.txt", "r") as f:
        data = f.read().splitlines()

        for line in data:
            words = line.split(',')
            i, j = words
            i = int(i)
            j = int(j)
            blank_image[i, j] = (0, 0, 0)

        # cv2.imshow("Foto", blank_image)
        cv2.imwrite(
            "./pictures/results/{}{}_border_results.jpeg".format(group, filename), blank_image)
        print "./pictures/results/{}{}_border_results.jpeg".format(group, filename)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
