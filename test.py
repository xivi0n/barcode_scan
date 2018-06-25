import cv2 
import numpy as np
import time

start = False # true if mouse is pressed
ix,iy = -20,-20
res = 32
base = cv2.imread('bar1.jpg')
numbers = [[1,1,1,0],[1,0,1,1],
           [0,3,0,0],[0,0,2,1],
           [0,1,2,0],[0,0,0,3],
           [0,2,0,1],[0,1,0,2],
           [2,0,0,1],[2,1,0,0]]
read = []     
black = 0
white = 255
crr = white
f = True
num = 0
j = True
s = 0

def draw_rec(x,y):
    global ix,iy,base,res
    s = ix-res
    if (s<0):
            s = 0 
    k = iy-res
    if (k<0):
            k = 0 
    img[k:iy+res+1,s:ix+res+1] = base[k:iy+res+1,s:ix+res+1].copy()
    cv2.imshow('example',img)
    cv2.rectangle(img,(x-res,y-res),(x+res,y+res),(0,255,0),1)
    cv2.imshow('example',img)
    ix, iy = x,y

def make_read(x,y):
    global crr,j,s,num,f
    if (abs(img[y,x,0]-crr)>20):
        num+=1
        #start = time.time()
        read.append(time.time()-s)
        j=True
        if (f):
            crr = black
        else:
            crr = white
        f = not f
    else:
        if (j):
            s = time.time()
        j=False

# mouse callback function
def draw_circle(event,x,y,flags,param):
    global ix,iy,start,base,res
    if event == cv2.EVENT_LBUTTONDOWN:
        start = True
        cv2.imshow('example',img)

    elif event == cv2.EVENT_MOUSEMOVE:
        if start == True:
            draw_rec(x,y)
            make_read(x,y)
            


    elif event == cv2.EVENT_LBUTTONUP:
        start = False

img = cv2.imread('bar1.jpg')
cv2.namedWindow('example')
cv2.setMouseCallback('example',draw_circle)
cv2.imshow('example',img)
while(1):
    k = cv2.waitKey(1) & 0xFF
    if k ==27:
        print num
        break
print read
cv2.destroyAllWindows()