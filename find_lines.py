import cv2
import numpy as np
import math
from line_operations import *

def find_lines(image, group, filename, extension):

	original = image
	# retval, image = cv2.threshold(image, 2, 1, cv2.THRESH_BINARY)
	image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	
	lines = cv2.HoughLinesP(
		image,
		rho=6,
		theta=np.pi / 60,
		threshold=130,
		lines=np.array([]),
		minLineLength=45,
		maxLineGap=10
	)

	lines = clean_diagonal_lines(lines)
	lines = group_lines(lines)
	lines = extrapolate_lines(original, lines)
	lines = reduce_to_two(lines)

	# original = draw_lines(original, lines)
	original = erase_lines(original, lines)

	# cv2.getGaborKernel(ksize, sigma, theta, lambda, gamma, psi, ktype)
	# ksize - size of gabor filter (n, n)
	# sigma - standard deviation of the gaussian function
	# theta - orientation of the normal to the parallel stripes
	# lambda - wavelength of the sunusoidal factor
	# gamma - spatial aspect ratio
	# psi - phase offset
	# ktype - type and range of values that each pixel in the gabor kernel can hold

	# g_kernel = cv2.getGaborKernel((21, 21), 1.0, np.pi/16, 12.0, 0.5, 0, ktype=cv2.CV_32F)
	# original = cv2.filter2D(original, cv2.CV_8UC3, g_kernel)

	# print(lines)

	cv2.imwrite("./pictures/results/{}{}_hough{}".format(group,filename,extension), original)

	# cv2.imshow("", dilation)
	cv2.waitKey(0)