import cv2
capture = cv2.VideoCapture(0)
count = 0
while True:
	x,frame = capture.read()
	count+=1
	flip = cv2.flip(frame,1)
	if count%2 == 0:
		cv2.imshow('Frame',frame)
	else:
		cv2.imshow('Frame',flip)

	if cv2.waitKey(1000) & 0xFF == ord('q'):
		break;