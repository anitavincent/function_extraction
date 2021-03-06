import cv2

from find_best_fit import find_best_fit
from FileManager import FileManager
from extract_features import *


def run_all():
    all_imgs = FileManager().get_image_list()

    for img in all_imgs:
        run_one_image(img)


def run_one_image(img_path):
    print img_path
    image = FileManager().get_image(img_path)

    try:
        curve, lines, origin_point = extract_features(image, img_path)
    except AxisNotFound:
        print "Axis not found - skipping this image"
        print ""
        return

    image, found_min = find_best_fit(curve, origin_point)

    FileManager().save_image(image, img_path, "_bestfit")
    # FileManager().save_txt(img_path, curve, origin_point)


run_all()
# run_one_image("group1/fun2.png")
