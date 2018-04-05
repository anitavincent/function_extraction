import cv2
import numpy as np

original = cv2.imread("graph_simples_colorido.jpeg")
img = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)

median = cv2.medianBlur(img,5)

# laplace
laplacian = np.array((
	[0, 1, 0],
	[1, -4, 1],
	[0, 1, 0]), dtype="int")
kernel = laplacian
dst = cv2.filter2D(median,-1,kernel)

height,width = dst.shape[:2]


file = open("border_results.txt","w") 

file.write("{},{}\n".format(height,width)) 

for i in range(0,height):
	for j in range(0,width):
		if dst[i][j] > 50:
			file.write("{},{}\n".format(i,j)) 
			original[i][j][0] = 0
			original[i][j][1] = 255
			original[i][j][2] = 0

 

 
file.close()

cv2.imshow("Foto", img)
cv2.imshow("Foto com filtro", dst)
cv2.imshow("Original Marcado", original)
cv2.waitKey(0)
cv2.destroyAllWindows()
