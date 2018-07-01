from pymouse import PyMouseEvent,PyMouse
import matplotlib.pyplot as plt
from time import time
import numpy as np
import cv2 
import sys

dpoints = []
tel = []
normdata = []
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
        global lx,ly,start,lastTime,startingTime
        t = time()
        if (t-lastTime>0.125) and start:
            print "dx:",x-lx,"dy:",y-ly
            #dpoints.append([x-lx,y-ly])
            dpoints.append(x-lx)
            tel.append(t-startingTime)
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
                
def normalize(dpoints):
    avrg = 1.0*np.sum(dpoints)/len(dpoints)
    normdata = []
    minx = min(dpoints)
    maxx = max(dpoints)
    for x in dpoints:
        normdata.append(1.0*(x-minx)/(maxx-minx))
    avrg = 1.0*(avrg-minx)/(maxx-minx)
    return normdata,avrg

def recalculate(normdata,k):
    pom = []
    for x in normdata:
        if (x<k):
            pom.append(x)
        else:
            pom.append(0)
    return pom

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

dpoints.pop(0)
tel.pop(0)

ax = plt.gca()
fig = plt.figure()
#ax.set_ylim()
ax.set_xlim([0,max(tel)])
plt.plot(tel, dpoints)
pom = []
for i in range(len(tel)):
    pom.append(np.sum(dpoints)/len(dpoints))

plt.plot(tel,pom)
plt.grid(True)
plt.draw()
plt.waitforbuttonpress(0)
plt.close(fig)

normdata,avrg = normalize(dpoints)
pom = []
for i in range(len(tel)):
    pom.append(avrg)

plt.plot(tel,normdata)
plt.plot(tel,pom)
recalc = recalculate(normdata,0.2)
#plt.plot(tel,recalc)
ax.set_ylim([0,1])
ax.set_xlim([0,max(tel)])
plt.grid(True)
plt.draw()
plt.waitforbuttonpress(0)
plt.close(fig)

cv2.destroyAllWindows()