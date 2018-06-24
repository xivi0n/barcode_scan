import cv2 
import numpy as np

start = False # true if mouse is pressed
ix,iy = -20,-20
res = 32
base = np.array(cv2.imread('bar1.jpg'),order='F')

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

# mouse callback function
def draw_circle(event,x,y,flags,param):
    global ix,iy,start,base,res
    if event == cv2.EVENT_LBUTTONDOWN:
        start = True
        cv2.imshow('example',img)
    elif event == cv2.EVENT_MOUSEMOVE:
        if start == True:
            draw_rec(x,y)

    elif event == cv2.EVENT_LBUTTONUP:
        start = False

img = cv2.imread('bar1.jpg')
cv2.namedWindow('example')
cv2.setMouseCallback('example',draw_circle)
while(1):
    k = cv2.waitKey(1) & 0xFF
    if k ==27:
        break

cv2.destroyAllWindows()