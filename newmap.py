import numpy
import cv2

#create a write image
img = numpy.ones((900,900,3),numpy.uint8)*255

cv2.imwrite("newmap.png",img)
