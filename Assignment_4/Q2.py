import cv2

img = cv2.imread('tree.jpg')
point = []
def click(event,x,y,flags,param):
    global point
    if event == cv2.EVENT_LBUTTONDOWN:
        point.append((x,y))
        cv2.circle(img, (x,y), 5, (100,38,255),-1)
        if len(point) == 2:
            cv2.rectangle(img, point[0], point[1], (28,43,190),2)

cv2.namedWindow('Frame')
cv2.setMouseCallback('Frame',click)

while True:
    cv2.imshow('Frame',img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

if len(point) == 2:
    cropped = img[point[0][1]:point[1][1], point[0][0]:point[1][0]]
    cv2.imshow('Cropped Frame',cropped)
    cv2.imwrite('Q2_Output.jpg', cropped)
    cv2.waitKey(2000)