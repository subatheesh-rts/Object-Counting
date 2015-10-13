__author__ = 'subath'

import numpy as np
import cv2

#initialise video input
cap = cv2.VideoCapture("C:\object_counting\count.mp4")
count=0
x=300
y=5
num=0
a=0
div=0

b=y
flag=1
firstarea=0

#loops for each frame
while(1):
    
    #capturinging frames
    ret,frame = cap.read()
    
    #resizing frames to specific width and height
    frame = cv2.resize(frame,(600,400))
    num+=1
    
    #converting to grayscale
    hsv = cv2.cvtColor(frame , cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(hsv,(5,5),0)
    
    #applying binary threshold
    ret3,mask = cv2.threshold(blur,150,255,cv2.THRESH_BINARY)
    kernel = np.ones((5,5),np.uint8)
    closing = cv2.morphologyEx(mask,cv2.MORPH_CLOSE,kernel, iterations = 3)
    opening = cv2.morphologyEx(closing,cv2.MORPH_OPEN,kernel, iterations = 3)
    sure_bg = cv2.dilate(closing,kernel,iterations=5)
    
    #finding distance transform
    dist_transform = cv2.distanceTransform(mask,cv2.DIST_L2,5)
    ret, sure_fg = cv2.threshold(dist_transform,0.7*dist_transform.max(),255,0)
    sure_fg = np.uint8(sure_fg)
    cv2.imshow("image",sure_fg)
    
    #finding contours
    img,contours, hierarchy = cv2.findContours(sure_fg,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    if (contours != []):
        i=0
        for cnt in contours:
            
            #finding moments for each contour
            M = cv2.moments(cnt)
            
            if(M['m00']!=0):
                
                #finding centroid and area for each contour
                cx = int(M['m10']/M['m00'])
                cy = int(M['m01']/M['m00'])
                area = cv2.contourArea(cnt)
                
                
                #finding count
                if (cx>=x and cx<x+y):
                    if(flag==1):
                        firstarea=area
                        flag=0
                    if(i==0):
                        div=area/firstarea+0.1;
                        a=cx-x
                        
                        if(a-b<0):
                            if(div>1):
                                count+=int(round(div))
                            else:
                                count+=1
                        b=a
                        i+=1
                   
    
    #displaying marker line and displaying count                              
    frame=cv2.line(frame,(x,0),(x,500),(255,0,0),2)
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame,str(count),(300,30), font, 1,(255,255,255),2,cv2.LINE_AA)
    cv2.imshow('orgin',frame)

    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()