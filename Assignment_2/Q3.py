import cv2
import time
import math

capture = cv2.VideoCapture(0)
start = time.time()
while True:
	x,frame = capture.read()
	flip = cv2.flip(frame,-1)
	end = time.time()
	if math.floor(end-start)%5==0:
		cv2.imshow('Frame',flip)
	else: 
		cv2.imshow('Frame',frame)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break;

#This cycle will terminate when 'q' is pressed