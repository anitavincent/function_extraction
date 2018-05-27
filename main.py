from find_contour import *
from show_pixels import *
from extract_skeleton import *
from find_lines import *
from clean_axis import *
from FileManager import FileManager
import cv2

def run_all():
    all_imgs = FileManager().get_image_list()

    for img in all_imgs:
        run_one_image(img)


def separate_name(st):
    lst = st.split('/')
    first = "{}/".format(lst[0])
    lst = lst[1].split('.')
    second = lst[0]
    third = ".{}".format(lst[1])
    print first, second, third
    return [first, second, third]


def run_one_image(img_path):

    image = FileManager().get_image(img_path)

    image = process_sk(image)

    FileManager().save_image(image, img_path, "_skeleton")

    axis_lines = find_lines(image)

    # clean_axis(image, axis_lines, group, filename, extension)

run_all()
# run_one_image("group1/fun2.png")
