import cv2
import numpy as np

img = cv2.imread('dotpy/morphology.jpg', cv2.IMREAD_GRAYSCALE)

kernel = np.ones((5,5),np.uint8)
erode = cv2.erode(img,kernel,iterations=1)
dilate = cv2.dilate(erode, kernel, iterations=2)

cv2.imshow("dilate",dilate)
cv2.waitKey(0)
cv2.destroyAllWindows()