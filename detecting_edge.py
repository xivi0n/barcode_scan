from pymouse import PyMouseEvent,PyMouse
from time import time

ix,iy = 900,500
lx = 0
ly = 0
start = time()
class Mouse(PyMouseEvent):
    def __init__(self):
        PyMouseEvent.__init__(self)

    def move(self,x,y):
        global lx,ly,start
        if (time()-start>0.1):
            print "dx:",x-lx,"dy:",y-ly
            start = time()
            lx,ly=ix,iy
            m = PyMouse()
            m.move(ix,iy)

    def click(self, x, y, button, press):
        if button == 1:
            if press:
                exit()

mouse = PyMouse()
ix,iy = mouse.screen_size()
ix /= 2
iy /= 2
mouse = Mouse()
mouse.run()
