import cv2
import numpy as np
import math

def angle(x1, y1, x2, y2):
    inner_product = x1*x2 + y1*y2
    len1 = math.hypot(x1, y1)
    len2 = math.hypot(x2, y2)
    return math.acos(inner_product/(len1*len2))

def draw_lines(image, lines, color=[255, 0, 0], thickness=3):
	if lines is None:
		print "No lines found"
		return image

	for line in lines:
		for x1, y1, x2, y2 in line:
			print "sfsdf"
			cv2.line(image, (x1, y1), (x2, y2), color, thickness)
    
	return image

def get_most_perpendicular_lines(lines):
	for line in lines:
		for x1, y1, x2, y2 in line:
			print "sfsdf"
			cv2.line(image, (x1, y1), (x2, y2), color, thickness)

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

	original = draw_lines(original, lines)

	print(lines)

	cv2.imwrite("./pictures/results/{}{}_hough{}".format(group,filename,extension), original)

	# cv2.imshow("", original)
	cv2.waitKey(0)