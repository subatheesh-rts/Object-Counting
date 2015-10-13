__author__ = 'subath'

import numpy as np
import cv2

#initialise video input
cap = cv2.VideoCapture(0)
ret,frame = cap.read()
count=0
x=300
y=10
num=0
a=0
div=0
b=y
flag=1
firstarea=0
k=0
nm=0
#width=input("Enter width:")
#height=input("Enter Height:")
width=500
height=300
x1 = 300-(width/2)
y1 = 200-(height/2)
x4 = 300+(width/2)
y4 = 200+(height/2)

f1=open("C:/object_counting/file.txt",'w')
f1.write(str(x1)+"\n")
f1.write(str(y1)+"\n")
f1.write(str(x4)+"\n")
f1.write(str(y4)+"\n")
f1.close()
#loops for each frame

l=0
while(l<10):
    ret,frame = cap.read() 
    l+=1   
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
ret3,mask = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

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
            
f3=open("C:/object_counting/thresh.txt",'w')
f3.write(str(ret3)+"\n")
f3.write(str(area)+"\n")       
                    
f3.close()  

while(1):
    #displaying marker line and displaying count  
    
    frame=cv2.line(frame,(x1,y1),(x4,y1),(0,0,255),2)
    frame=cv2.line(frame,(x1,y4),(x4,y4),(0,0,255),2)      
    cv2.imshow('orgin',frame)

    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()