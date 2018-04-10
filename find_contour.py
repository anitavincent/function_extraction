import cv2
import numpy as np

def find_contour(filename, extension):
	original = cv2.imread("{}{}".format(filename,extension))
	img = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)

	median = cv2.medianBlur(img,3)

	# laplace
	laplacian = np.array((
		[0, 1, 0],
		[1, -4, 1],
		[0, 1, 0]), dtype="int")
	kernel = laplacian
	dst = cv2.filter2D(median,-1,kernel)

	retval, dst = cv2.threshold(dst, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

	height,width = dst.shape[:2]


	file = open("border_results.txt","w") 

	for i in range(0,height):
		for j in range(0,width):
			if dst[i][j] > 250:
				file.write("{},{}\n".format(i,j)) 
				original[i][j][0] = 0
				original[i][j][1] = 255
				original[i][j][2] = 0

 

	 
	file.close()

	cv2.imwrite("./results/{}_contour{}".format(filename,extension), dst)
	cv2.imwrite("./results/{}_highlight{}".format(filename,extension), original)

	cv2.imshow("Filtered Image", dst)
	cv2.imshow("Highlight borders", original)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
