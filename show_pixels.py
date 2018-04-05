import cv2
import numpy as np

with open("border_results.txt", "r") as f:
	data = f.read().splitlines()
	
	first_line = data[0].split(',')
	height, width = int(first_line[0]), int(first_line[1])
	blank_image = np.zeros((height,width,3), np.uint8)
	blank_image[:,:] = (255,255,255)

	for line in data[1:]:
		words = line.split(',')
		i,j = words
		i = int(i)
		j = int(j)
		blank_image[i,j] = (0,0,0)
		# print words

	cv2.imshow("Foto", blank_image)
	cv2.waitKey(0)
	cv2.destroyAllWindows()