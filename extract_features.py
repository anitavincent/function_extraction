import cv2

from extract_skeleton import extract_skeleton
from find_lines import *
from clean_axis import *
from remove_noise import *


def extract_features(image):

    image = extract_skeleton(image)
    clean_image = image.copy()

    # FileManager().save_image(image, img_path, "_skeleton")

    axis_lines, inter_point, image_lines = find_lines(image)

    # FileManager().save_image(image, img_path, "_lines")

    new_img = clean_axis(clean_image, axis_lines)

    # FileManager().save_image(new_img, img_path, "_clean")

    new_img = remove_noise(new_img)

    return new_img, axis_lines, inter_point
