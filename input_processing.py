from pymouse import PyMouseEvent,PyMouse
import matplotlib.pyplot as plt
from time import time
import numpy as np
import cv2 
import sys

dpoints = []
xpoints = []
ypoints = []
tel = []
normdata = []
start = False
lx,ly = 0, 0
ix,iy = 900,500
timeEl = 0
lastTime = 0
startingTime = 0

physical_dist = 0
v = 0

class ListenInterrupt(Exception):
    pass

class MouseEvent(PyMouseEvent):
    global start
    def __init__(self):
        PyMouseEvent.__init__(self)

    def move(self,x,y):
        global lx,ly,start,lastTime,startingTime
        t = time()
        if (t-lastTime>0.1) and start:
            #print "dx:",x-lx,"dy:",y-ly
            #dpoints.append([x-lx,y-ly])
            xpoints.append(x-lx)
            ypoints.append(y-ly)
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

def draw_canvas():
    img = np.zeros((500,500))
    window_name = "input"
    cv2.namedWindow(window_name,cv2.WINDOW_NORMAL)
    cv2.imshow(window_name,img)
    cv2.moveWindow(window_name,ix-200,iy-200) 
    cv2.waitKey(1) 

def recalc_x(xpoints,k):
    pom = np.abs(xpoints)
    rez = []
    for x in pom:
        if (x<k):
            rez.append(0)
        else:
            rez.append(k)
    return rez


def normalize(dpoints):
    avrg = 1.0*np.sum(dpoints)/len(dpoints)
    dpoints = np.abs(dpoints)
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
            pom.append(k)
    return pom

def remake(data,k):
    pom = [i for i in data]
    for i in range(len(pom)-1):
        if (pom[i]!=0):
            while(i+1<len(pom)) and (pom[i+1]!=0):
                pom[i+1]=0
                i+=1
        elif (pom[i]<k):
            pom[i]=0
    print pom
    return pom

def make_dis(tel,datax,k,v):
    pomx = []
    pomy = []
    for i in range(len(datax)):
        if (datax[i]!=0):
            start = tel[i]
            n = i
            i+=1
            while(i<len(datax)-1) and (datax[i]<datax[i+1]):
                i+=1
            if (i!=len(datax)):
                pomx.append(tel[i]-start)
                pomy.append((tel[i]-start)*v)
    print len(pomx)
    pomx = [abs(x) for x in pomx]
    pomy = [abs(x) for x in pomy]
    print "Time: ", pomx
    print "Distance: ", pomy
    return pomx,pomy

mouse = PyMouse()
ix,iy = mouse.screen_size()
ix /= 2
iy /= 2
print ix,iy
mouse.move(ix,iy)

draw_canvas()
try:
    mouse = MouseEvent()
    mouse.run()
except ListenInterrupt as e:
    print(e.args[0])
    cv2.destroyAllWindows()

#print "(dx,dy):",[x,y for x,y in xpoints,ypoints]

#physical_dist = int(input("Enter physical distance: "))
physical_dist = 7
k = 0.5
v = 1.0*physical_dist/timeEl

xpoints.pop(0)
ypoints.pop(0)
tel.pop(0)

ax = plt.gca()
# fig = plt.figure()
# #ax.set_ylim()
# plt.subplot(2, 1, 1)
# ax.set_xlim([0,max(tel)])
xpoints = np.abs(xpoints)
# plt.plot(tel, xpoints,'.-')

# #xpoints = recalc_x(xpoints,1)

# plt.plot(tel, xpoints,'.-') 	
# plt.grid(True)
# plt.ylabel('movement on x') 	

# plt.subplot(2, 1, 2)
# plt.plot(tel, ypoints,'o-')
# ax.set_xlim([0,max(tel)])
# plt.ylabel('movement on y')
# pom = []
# #for i in range(len(tel)):
# #    pom.append(np.sum(dpoints)/len(dpoints))

# #plt.plot(tel,pom)
# plt.grid(True)
# plt.draw()
# plt.waitforbuttonpress(0)
# plt.close(fig)

xnormdata, avrgx = normalize(xpoints)
ynormdata, avrgy = normalize(ypoints)

# pom = []
# for i in range(len(tel)):
#     pom.append(avrgx)

# #xrecalc = recalculate(xnormdata,k)
xrecalc = xnormdata
yrecalc = recalculate(ynormdata,0.6)

# fig = plt.figure()

# plt.subplot(2, 1, 1)
# plt.plot(tel,xnormdata,'.-')
# plt.plot(tel,xrecalc,'.-')
# ax.set_ylim([-1,1])
# ax.set_xlim([0,max(tel)])
# plt.ylabel('movement on x')
# plt.grid(True)

# plt.subplot(2, 1, 2)
# plt.plot(tel,ynormdata,'o-')
# plt.plot(tel,yrecalc,'o-')
# ax.set_ylim([-1,1])
# ax.set_xlim([0,max(tel)])
# plt.ylabel('movement on y')
# plt.grid(True)

# plt.draw()
# plt.waitforbuttonpress(0)
# plt.close(fig)

fig2 = plt.figure()
plt.grid(True)
ax.set_ylim([0,1])
ax.set_xlim([0,max(tel)])
plt.plot(tel, xrecalc,'o-')
xrecalc = remake(xrecalc,k)
plt.plot(tel,xrecalc,'.-')
plt.draw()
plt.waitforbuttonpress(0)
plt.close(fig2)
dist = []
ttm = []

ttm,dist = make_dis(tel,xrecalc,k,v)

from by_distance import *

flag = []
tocmp = []
#dist.pop(0)
read_pos_n = make_pos_n(dist)
classify(read_pos_n,tocmp,flag)

print "\n",flag
print tocmp
print ""
get_number(flag)
#plt.show()

f = open("time_recalc_dist0.txt", "a")
f.write(str(len(ttm))+"\n")
f.write(" ".join(str(x) for x in ttm)+"\n")
f.write(" ".join(str(x) for x in xrecalc)+"\n")
f.write(" ".join(str(x) for x in dist)+"\n")
f.close()