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
    clean_image = image.copy()

    # FileManager().save_image(image, img_path, "_skeleton")

    axis_lines, image_lines = find_lines(image)

    # FileManager().save_image(image, img_path, "_lines")

    new_img = clean_axis(clean_image, axis_lines)

    FileManager().save_image(new_img, img_path, "_flood")

run_all()
# run_one_image("group2/grid4.jpg")
