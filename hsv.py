
import numpy as np
import cv2

cap = cv2.VideoCapture(0)

count=0

def nothing(x):
    pass

cv2.namedWindow('image')


cv2.createTrackbar('Hmin','image',0,179,nothing)
cv2.createTrackbar('Hmax','image',0,179,nothing)
cv2.createTrackbar('Smin','image',0,255,nothing)
cv2.createTrackbar('Smax','image',0,255,nothing)
cv2.createTrackbar('Vmin','image',0,255,nothing)
cv2.createTrackbar('Vmax','image',0,255,nothing)

while(1):
    ret,frame = cap.read()
    frame=cv2.line(frame,(600,0),(600,500),(255,0,0),2)

    hsv = cv2.cvtColor(frame , cv2.COLOR_BGR2HSV)

    lower = np.array([cv2.getTrackbarPos('Hmin','image'),cv2.getTrackbarPos('Smin','image'),cv2.getTrackbarPos('Vmin','image')])
    upper = np.array([cv2.getTrackbarPos('Hmax','image'),cv2.getTrackbarPos('Smax','image'),cv2.getTrackbarPos('Vmax','image')])

    #lower = np.array([173,116,83])
    #upper = np.array([179,220,245])


    mask = cv2.inRange(hsv, lower, upper)
    kernel = np.ones((5,5),np.uint8)
    dilate=cv2.dilate(mask,kernel,iterations=1)

    imgray = dilate
    ret,thresh = cv2.threshold(dilate,127,255,0)



    cv2.imshow('orgin',frame)
    cv2.imshow('orgin2',thresh)
    #cv2.imshow('con',img)

    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
