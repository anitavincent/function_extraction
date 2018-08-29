import cv2

from FileManager import FileManager
from extract_features import *
from fit_curve import *


def run_all():
    all_imgs = FileManager().get_image_list()

    for img in all_imgs:
        run_one_image(img)


def run_one_image(img_path):

    image = FileManager().get_image(img_path)

    curve, lines, origin_point = extract_features(image)

    image = fit_curve(curve, origin_point)

    FileManager().save_image(image, img_path, "_fit")

run_all()
# run_one_image("group1/fun1.png")
