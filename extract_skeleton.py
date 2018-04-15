import cv2
import numpy as np
from skimage.morphology import skeletonize

def find_sk(group, filename, extension):
	original = cv2.imread("./pictures/originals/{}{}{}".format(group,filename,extension))
	height,width = original.shape[:2]
	blank_image = np.zeros((height, width,3), np.uint8)
	blank_image[:,:] = (255,255,255)

	img = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
	img = cv2.bilateralFilter(img,15,25,75)


	dst = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
            cv2.THRESH_BINARY_INV,11,2)
	kernel = np.ones((5,5),np.uint8)
	# dst = cv2.morphologyEx(dst, cv2.MORPH_CLOSE, kernel)

	skeleton = skeletonize(dst>0)
	skeleton = skeleton.astype(float)

	file = open("border_results.txt","w") 

	height,width = skeleton.shape[:2]

	for i in range(0,height):
		for j in range(0,width):
			if skeleton[i][j] > 0.0:
				file.write("{},{}\n".format(i,j)) 
				original[i][j][0] = 0
				original[i][j][1] = 255
				original[i][j][2] = 0	
				blank_image[i,j] = (0,0,0)
 

	 
	file.close()

	cv2.imwrite("./pictures/results/{}{}_contour{}".format(group,filename,extension), blank_image)
	cv2.imwrite("./pictures/results/{}{}_highlight{}".format(group,filename,extension), original)

	cv2.waitKey(0)
	cv2.destroyAllWindows()
