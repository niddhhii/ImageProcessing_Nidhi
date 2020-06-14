import cv2
import numpy as np

cap = cv2.VideoCapture(0)

point = []
def click(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDOWN:
        point.append((x,y))
        if len(point) == 2:
            template = frame[point[0][1]:point[1][1], point[0][0]:point[1][0]]
            cv2.imwrite('template.jpg', template)

cv2.namedWindow('Frame')
cv2.setMouseCallback('Frame',click)

while True:
    x,frame = cap.read()
    if len(point) == 2:
        template = cv2.imread('template.jpg')
        cv2.imshow('Cropped Frame',template) 
        template_gray = cv2.cvtColor(template,cv2.COLOR_BGR2GRAY)
        width = template.shape[1]
        height = template.shape[0]
        frame_gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        res = cv2.matchTemplate(frame_gray,template_gray,cv2.TM_CCOEFF_NORMED)
        loc = np.where(res>=0.9)
        for x,y in zip(*loc[::-1]):
            cv2.rectangle(frame,(x,y),(x+width,y+height),(0,255,0),1)
            cv2.putText(frame,'Object',(x,y),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),1)
    
    cv2.imshow('Frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
            break