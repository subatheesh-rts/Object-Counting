__author__ = 'subath'

import numpy as np
import cv2

cap = cv2.VideoCapture(0)

count=0
x=320
#def nothing(x):
#    pass

#cv2.namedWindow('image')


#cv2.createTrackbar('Hmin','image',0,179,nothing)
#cv2.createTrackbar('Hmax','image',0,179,nothing)
#cv2.createTrackbar('Smin','image',0,255,nothing)
#cv2.createTrackbar('Smax','image',0,255,nothing)
#cv2.createTrackbar('Vmin','image',0,255,nothing)
#cv2.createTrackbar('Vmax','image',0,255,nothing)

while(1):
    ret,frame = cap.read()
    frame=cv2.line(frame,(x,0),(x,500),(255,0,0),2)

    hsv = cv2.cvtColor(frame , cv2.COLOR_BGR2HSV)

    #lower = np.array([cv2.getTrackbarPos('Hmin','image'),cv2.getTrackbarPos('Smin','image'),cv2.getTrackbarPos('Vmin','image')])
    #upper = np.array([cv2.getTrackbarPos('Hmax','image'),cv2.getTrackbarPos('Smax','image'),cv2.getTrackbarPos('Vmax','image')])

    lower = np.array([134,44,56])
    upper = np.array([179,133,104])


    mask = cv2.inRange(hsv, lower, upper)
    kernel = np.ones((5,5),np.uint8)
    dilate=cv2.dilate(mask,kernel,iterations=1)

    imgray = dilate
    ret,thresh = cv2.threshold(dilate,127,255,0)


    img,contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    if (contours != []):
        cnt = contours[0]
        #frame = cv2.approxPolyDP(cnt,0.1*cv2.arcLength(cnt,True),True)
        #print(contours)
        #cv2.drawContours(frame,[cnt],-1,(0,0,255),2)
        #for cnt in contours:
        rect = cv2.minAreaRect(cnt)
        pts = cv2.boxPoints(rect)
        pts = np.int0(pts)
        frame = cv2.polylines(frame,[pts],True, 255,2)
        #cnt = contours[0]
        M = cv2.moments(cnt)
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        if (cx>x-1 and cx<x+2):
            count+=1

    print count

    cv2.imshow('orgin',frame)
    cv2.imshow('orgin2',thresh)
    #cv2.imshow('con',img)

    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
