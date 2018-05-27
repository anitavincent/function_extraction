import cv2
import numpy as np
from skimage.morphology import skeletonize
from crop import *

# parameter for adaptative media threshold
BLOCK_SIZE = 50
THRESHOLD = 65


def get_block_index(image_shape, yx, block_size):
    y = np.arange(max(0, yx[0] - block_size),
                  min(image_shape[0], yx[0] + block_size))
    x = np.arange(max(0, yx[1] - block_size),
                  min(image_shape[1], yx[1] + block_size))
    return np.meshgrid(y, x)


def adaptive_median_threshold(img_in, thr):
    # applies median threshold to a block
    med = np.median(img_in)
    img_out = np.zeros_like(img_in, np.uint8)
    img_out[img_in - med < thr] = 255
    return img_out


def block_image_process(image, block_size, thr):
    # applies adptive median threshold to every block
    # of the image
    image = cv2.bilateralFilter(image, 15, 25, 75)
    image = 255 - image

    out_image = np.zeros_like(image, np.uint8)
    for row in range(0, image.shape[0], block_size):
        for col in range(0, image.shape[1], block_size):
            idx = (row, col)
            block_idx = get_block_index(image.shape, idx, block_size)
            out_image[block_idx] = adaptive_median_threshold(
                image[block_idx], thr)

    return out_image


def calculate_percent(image):
    # calculates the amount of white pixels in the image
    white_amnt = 0
    total = 0

    for i in range(0, image.shape[0]):
        for j in range(0, image.shape[1]):
            if image[i][j] > 0.0:
                white_amnt += 1
            total += 1

    return (white_amnt / float(total)) * 10


def get_skeleton(img, thr):
    # processes bw image and extracts skeleton
    # using threshold value 'thr'
    dst = block_image_process(img, BLOCK_SIZE, thr)

    skeleton = skeletonize(dst < 255)
    skeleton = skeleton.astype(float)

    return skeleton


def extract_skeleton(original_image):
    original = original_image
    img = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)

    thr = THRESHOLD
    skeleton = get_skeleton(img, thr)
    baseI, baseJ, skeleton = crop_binary(skeleton)
    percent = calculate_percent(skeleton)
    if percent < 0.001:
        thr = THRESHOLD * 0.5
        skeleton = find_sk(img, thr)
        baseI, baseJ, skeleton = crop_binary(skeleton)

    # cv2.waitKey(0)
    return 255 - blank_image
