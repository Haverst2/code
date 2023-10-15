import cv2
import numpy as np
a = cv2.imread('map.png',0)
kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(10,10))
b = cv2.dilate(a,kernel)
ret,c = cv2.threshold(b,150,255,cv2.THRESH_BINARY)
cv2.imshow("w",c)
cv2.waitKey(0)
cv2.imwrite('amp.pgm',c)