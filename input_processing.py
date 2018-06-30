from pymouse import PyMouseEvent,PyMouse
from time import time
import numpy as np
import cv2 
import sys

dpoints = []
start = False
lx,ly = 0, 0
ix,iy = 900,500
timeEl = 0
lastTime = 0
startingTime = 0

class ListenInterrupt(Exception):
    pass

class MouseEvent(PyMouseEvent):
    global start
    def __init__(self):
        PyMouseEvent.__init__(self)

    def move(self,x,y):
        global lx,ly,start,lastTime
        if (time()-lastTime>0.125) and start:
            print "dx:",x-lx,"dy:",y-ly
            dpoints.append([x-lx,y-ly])
            lastTime = time()
            lx,ly=ix,iy
            m = PyMouse()
            m.move(ix,iy)

    def click(self, x, y, button, press):
        global start,startingTime,lastTime,timeEl
        if button == 1:
            if press:
                start = True
                print "poceo"
                lastTime = time()
                startingTime = time()
            else:
                timeEl = time()-startingTime
                print "Total time:",timeEl
                raise ListenInterrupt("Input read.")
                

mouse = PyMouse()
ix,iy = mouse.screen_size()
ix /= 2
iy /= 2
print ix,iy
mouse.move(ix,iy)

img = np.zeros((500,500))
window_name = "input"
cv2.namedWindow(window_name,cv2.WINDOW_NORMAL)
cv2.imshow(window_name,img)
cv2.moveWindow(window_name,ix-200,iy-200) 
cv2.waitKey(1) 

try:
    mouse = MouseEvent()
    mouse.run()
except ListenInterrupt as e:
    print(e.args[0])

print "(dx,dy):",dpoints

cv2.destroyAllWindows()