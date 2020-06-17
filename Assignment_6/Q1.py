import cv2
import numpy as np

img = cv2.imread('page.jpg')
img_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

cv2.namedWindow('Frame')
x1,y1,w1,h1 = cv2.getWindowImageRect('Frame')
resize = cv2.resize(img_gray, (w1,h1))

kernel = np.ones((5,5))
dilate = cv2.dilate(resize,kernel)
canny = cv2.Canny(dilate,55,200)
cv2.imwrite('Q1_Output.jpg', canny)

cv2.imshow('Frame', canny)
cv2.waitKey(0)