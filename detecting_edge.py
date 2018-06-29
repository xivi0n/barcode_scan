from pymouse import PyMouseEvent

class Mouse(PyMouseEvent):
    def __init__(self):
        PyMouseEvent.__init__(self)

    def move(self,x,y):
        print "Location:",x,y

    def click(self, x, y, button, press):
        if button == 1:
            if press:
                exit()
C = Mouse()
C.run()
