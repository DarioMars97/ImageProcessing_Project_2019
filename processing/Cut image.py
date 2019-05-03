import cv2
import numpy as np


img=cv2.imread("img.jpg")
im = cv2.imread("img.JPG")

imgray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(img,100,200)
im2, contours, hierarchy = cv2.findContours(edges,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

na = []
b = 0
y,x,_ =img.shape  
h =0
w=0
firstx = 0
area = 1000
for i in hierarchy[0]:
    M = cv2.moments(contours[b])
    if M['m00'] > area:
        na.append(contours[b])
        print(M['m00'])
        cx,cy,cw,ch = cv2.boundingRect(contours[b])
        if cx < x :
            x=cx
        if firstx < cx:
            firstx = int(cx+(cw/2)) 
            
        if cy < y:
            y=cy
        if ch > h:
            h = ch
        
        
    b= b+1


cv2.drawContours(img,contours , -1, (0,255,0), 3)
imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
(thresh, im_bw) = cv2.threshold(imgray, 200, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

print(x,y,w,y,firstx,img.shape)
cv2.imwrite("out.jpg",im_bw[y:y+h,x:firstx+x])