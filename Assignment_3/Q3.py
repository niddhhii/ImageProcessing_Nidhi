import cv2
import numpy as np
import random

img = cv2.imread('tree.jpg')
h, w, c = img.shape
height = h // 7
width = w // 7
cv2.imshow('Frame', img)
count = 0
for x in range(0, h, height):
    if count % 2 == 0:
        for y in range(0, w, width):
            x1 = x + height
            y1 = y + width
            img = cv2.imread('tree.jpg')
            cv2.rectangle(img, (y, x), (y1, x1),
                          (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), -1)
            cv2.waitKey(500)
            cv2.imshow('Frame', img)
        count += 1
    else:
        area = np.array([[width * 7, x], [w, x], [w, x + height], [width * 7, x + height]])
        cv2.fillPoly(img, [area], (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
        for y in range(width*7, -width, -width):
            x1 = x + height
            y1 = y + width
            img = cv2.imread('tree.jpg')
            cv2.rectangle(img, (y, x), (y1, x1),
                          (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), -1)
            cv2.waitKey(500)
            cv2.imshow('Frame', img)
        count += 1
