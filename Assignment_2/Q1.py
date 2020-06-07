import cv2
import random

img = cv2.imread('tree.jpg')
h,w,c = img.shape
cv2.line(img,(0,0),(w,h),(random.randint(0,255),random.randint(0,255),random.randint(0,255)),15)
cv2.imshow('Frame',img)
cv2.waitKey(0)
