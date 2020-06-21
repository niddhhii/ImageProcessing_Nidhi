import cv2
import numpy as np

img = cv2.imread('page.jpg')

cv2.namedWindow('Frame',cv2.WINDOW_NORMAL)
x1,y1,w1,h1 = cv2.getWindowImageRect('Frame')
resize = cv2.resize(img, (w1,h1))

cv2.namedWindow('Contour',cv2.WINDOW_NORMAL)

img_gray = cv2.cvtColor(resize,cv2.COLOR_BGR2GRAY)
kernel = np.ones((5,5))
dilate = cv2.dilate(resize,kernel)
canny = cv2.Canny(dilate,55,200)
cv2.imshow('Frame', canny)

contours,hierarchy = cv2.findContours(canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
areas = [cv2.contourArea(c) for c in contours]
max_index = np.argmax(areas)
max_contour = contours[max_index]

perimeter = cv2.arcLength(max_contour, True)
ROI = cv2.approxPolyDP(max_contour, 0.01 * perimeter, True)
cv2.drawContours(resize, [ROI], -1, (0,255,0),1)

if len(ROI) == 4:

    p1 = np.array([ROI[1],ROI[0],ROI[2],ROI[3]],np.float32)
    p2 = np.array([(0,0),(700,0),(0,500),(700,500)],np.float32)

    perspective = cv2.getPerspectiveTransform(p1, p2)
    warped = cv2.warpPerspective(resize, perspective, (700,500))

    cv2.imshow('Contour', resize)
    cv2.imshow('Result', warped)

cv2.waitKey(0)
