import cv2
import numpy as np

def nothing(x):
    pass

cap = cv2.VideoCapture(0)

cv2.namedWindow('Frame')
cv2.namedWindow('Output')

cv2.createTrackbar('HL', 'Frame',0,180,nothing)
cv2.createTrackbar('SL', 'Frame',0,255,nothing)
cv2.createTrackbar('VL', 'Frame',0,255,nothing)

while True:
    x,frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    hul=cv2.getTrackbarPos('HL', 'Frame')
    sal=cv2.getTrackbarPos('SL', 'Frame')
    val=cv2.getTrackbarPos('VL', 'Frame')

    lower = np.array([hul,sal,val])
    higher = np.array([180,255,255])

    mask1 = cv2.inRange(hsv, lower, higher)
    res = cv2.bitwise_and(frame, frame, mask=mask1)

    contours,hierarchy = cv2.findContours(mask1, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(frame, contours, -1, (0,255,0),1)
    cv2.imshow('Frame', frame)
    cv2.imshow('Output', res)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break