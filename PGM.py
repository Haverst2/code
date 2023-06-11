import cv2

a = cv2.imread('map.jpg',0)
cv2.imwrite('map.pgm',a)