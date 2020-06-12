import cv2
import numpy as np

cap = cv2.VideoCapture(0)
x,frame = cap.read()
h,w,c=frame.shape
print("Frame Dimensions:"+ str(h),str(w))

def mouse(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(frame[y,x])

cv2.namedWindow('img')
x1,y1,w1,h1 = cv2.getWindowImageRect('img')
print("Window Dimensions:"+ str(w1),str(h1))

cv2.setMouseCallback('img', mouse)

while True:
    x,frame = cap.read()
    cv2.imshow('img', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
        