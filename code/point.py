import cv2
import numpy as np

f1=open("C:/object_counting/file.txt",'w')

cap = cv2.VideoCapture(0)
ret,frame = cap.read()
frame = cv2.resize(frame,(600,400))
num=0
# mouse callback function
def draw_circle(event,x,y,flags,param):
    global num
    if event == cv2.EVENT_LBUTTONDBLCLK:
        cv2.circle(frame,(x,y),2,(255,0,0),-1)
        num+=1
        f1.write(str(x)+"\n")
        f1.write(str(y)+"\n")
        
# Create a black image, a window and bind the function to window

cv2.namedWindow('image')

cv2.setMouseCallback('image',draw_circle)

while(1):
    cv2.imshow('image',frame)
    if cv2.waitKey(20) & 0xFF == 27:
        break

f1.close()
cv2.destroyAllWindows()