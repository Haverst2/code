import cv2

a = cv2.imread('newmap.png',0)
cv2.imwrite('newmap.pgm',a)