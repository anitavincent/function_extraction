import cv2
import numpy as np

def reduce(filename):
	with open("border_results.txt", "r+") as f:
		data = f.read().splitlines()

		maxX = -1
		maxY = -1
		baseX = 99999999999999999999
		baseY = 99999999999999999999
		for line in data:
			words = line.split(',')
			i,j = words
			i = int(i)
			j = int(j)
			if i < baseY:
				baseY = i
			if i > maxY:
				maxY = i
			if j < baseX:
				baseX = j
			if j > maxX:
				maxX = j

		height, width = maxY-baseY, maxX-baseX
		f.seek(0)
		for line in data:
			words = line.split(',')
			i,j = words
			i = int(i)
			j = int(j)
			f.write("{},{}\n".format(i-baseY,j-baseX))
		f.truncate()
		print "heigh: {} widhth: {}".format(height, width)
		return height+1, width+1

height, width = reduce("border_results.txt")
blank_image = np.zeros((height,width,3), np.uint8)
blank_image[:,:] = (255,255,255)

with open("border_results.txt", "r") as f:
	data = f.read().splitlines()

	for line in data:
		words = line.split(',')
		i,j = words
		i = int(i)
		j = int(j)
		blank_image[i,j] = (0,0,0)

	cv2.imshow("Foto", blank_image)
	cv2.waitKey(0)
	cv2.destroyAllWindows()