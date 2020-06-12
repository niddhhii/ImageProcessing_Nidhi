import cv2
import numpy as np

img = cv2.imread('page.jpg')
h,w,c = img.shape
print(h,w,c)

cv2.namedWindow('Frame')
x1,y1,w1,h1 = cv2.getWindowImageRect('Frame')
print(x1,y1,w1,h1)

resize = cv2.resize(img, (w1,h1))
cv2.imshow('Frame', resize)

point = []
def click(event,x,y,flags,param):
    global point
    if event == cv2.EVENT_LBUTTONDOWN:
        point.append((x,y))
        cv2.circle(resize, (x,y), 5, (100,38,255),-1)
        if len(point) == 4:
            pts_1 = np.array([point[1], point[0], point[2], point[3]],np.int32)
            poly = cv2.polylines(resize,[pts_1],True,(170,54,255),2)
            cv2.imshow('Frame', poly)
    
cv2.setMouseCallback('Frame',click)

while True:
    cv2.imshow('Frame',resize)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

if len(point)==4:
    pts_1 = np.array([point[0], point[1], point[2], point[3]],np.float32)
    pts_2 = np.array([(0, 0), (700, 0), (0, 600), (700, 600)],np.float32)
    perspective = cv2.getPerspectiveTransform(pts_1,pts_2)
    transformed = cv2.warpPerspective(resize, perspective, (700,600))
    cv2.imshow('Warped Frame',transformed)
    cv2.imwrite('Q3_Output.jpg', transformed)
    cv2.waitKey(3000)