__author__ = 'subath'

import numpy as np
import cv2

#initialise video input
cap = cv2.VideoCapture(0)
ret,frame = cap.read()
count=0

y=10
num=0
a=0
div=0
b=y
flag=0
firstarea=0
k=0
nm=0

f2=open("C:/object_counting/file.txt",'r')
for line in f2:
    nm+=1
f2.close()
f2=open("C:/object_counting/file.txt",'r')
x1=int(f2.readline())
y1=int(f2.readline())
x4=int(f2.readline())
y4=int(f2.readline())

f2.close()
x=((x4-x1)/2)+x1




f=open("C:/object_counting/thresh.txt",'r')

thr=f.readline()
thr=thr[:-1]
thr=int(float(thr))

firstarea =f.readline()
firstarea = firstarea[:-1]
firstarea = float(firstarea)

f.close()

#loops for each frame
while(1):
    
    #capturinging frames
    ret,frame = cap.read()
    
    #resizing frames to specific width and height
    frame = cv2.resize(frame,(600,400))
    frame1 = frame[y1:y4,x1:x4]
    num+=1
    
    #converting to grayscale
    hsv = cv2.cvtColor(frame1 , cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(hsv,(5,5),0)
  
    #applying binary threshold
    ret3,mask = cv2.threshold(blur,thr,255,cv2.THRESH_BINARY)
    kernel = np.ones((5,5),np.uint8)
    closing = cv2.morphologyEx(mask,cv2.MORPH_CLOSE,kernel, iterations = 3)
    opening = cv2.morphologyEx(closing,cv2.MORPH_OPEN,kernel, iterations = 3)
    sure_bg = cv2.dilate(closing,kernel,iterations=50)
    
    #finding distance transform
    dist_transform = cv2.distanceTransform(opening,cv2.DIST_L2,5)
    ret, sure_fg = cv2.threshold(dist_transform,0.2*dist_transform.max(),255,0)
    sure_fg = np.uint8(sure_fg)
         
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
    if(nm==4):
        frame=cv2.line(frame,(x1,y1),(x4,y1),(0,0,255),2)
        frame=cv2.line(frame,(x1,y4),(x4,y4),(0,0,255),2)                            
    frame=cv2.line(frame,(x,0),(x,500),(255,0,0),2)
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame,str(count),(300,30), font, 1,(255,255,255),2,cv2.LINE_AA)
    cv2.imshow('orgin',frame)

    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()