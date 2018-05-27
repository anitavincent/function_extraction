from find_contour import *
from show_pixels import *
from extract_skeleton import extract_skeleton
from find_lines import *
from clean_axis import *
from FileManager import FileManager
import cv2


def run_all():
    all_imgs = FileManager().get_image_list()

    for img in all_imgs:
        run_one_image(img)


def run_one_image(img_path):

    image = FileManager().get_image(img_path)

    image = extract_skeleton(image)

    FileManager().save_image(image, img_path, "_skeleton")

    axis_lines = find_lines(image)

    # clean_axis(image, axis_lines, group, filename, extension)

run_all()
# run_one_image("group1/fun2.png")
