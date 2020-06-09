import cv2
import random

img = cv2.imread('tree.jpg')
h,w,c = img.shape
height = h//7
width = w//7

for x in range(0,h,height):
	for y in range(0,w,width):
		x1=x+height
		y1=y+width
		cv2.rectangle(img,(y,x),(y1,x1),(random.randint(0,255),random.randint(0,255),random.randint(0,255)),-1)

cv2.imwrite("Q1_Output.png",img)