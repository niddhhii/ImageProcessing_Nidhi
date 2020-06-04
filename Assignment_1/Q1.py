import cv2
capture = cv2.VideoCapture(0)
n = int(input("Enter n:"))
count = 0
while True:
	x,frame = capture.read()
	flip = cv2.flip(frame,-1)
	if count%n==0:
		cv2.imshow('Frame',flip)
	else:
		cv2.imshow('Frame',frame)
	if cv2.waitKey(1000) & 0xFF == ord('q'):
		break;
	count += 1