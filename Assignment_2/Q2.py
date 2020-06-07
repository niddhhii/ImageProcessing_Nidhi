import cv2
capture = cv2.VideoCapture(0)
count = 0
while True:
	x,frame = capture.read()
	count+=1
	if(count<=100):
		cv2.imshow('Frame',frame)
		cv2.imwrite('IMG_'+str(count)+'.jpg',frame)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break;

#This will store first 100 images to form a dataset 