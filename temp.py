numbers = [[3,2,1,1],#0
           [2,2,2,1],#1
           [2,1,2,2],#2
           [1,4,1,1],#3
           [1,1,3,2],#4
           [1,2,3,1],#5
           [1,1,1,4],#6
           [1,3,1,2],#7
           [1,2,1,3],#8
           [3,1,1,2]]#9
read = []
read_n = []
tocmp = [] 
flag = []
pxs = []

black = 0
white = 255
crr = white
f = True
j = True
s = []

dx = 0
px1 = 0
px2 = 0
px3 = 0
again = False

def remake_n():
    global px1,px2,px3
    print "kurac"
    j = 0
    for x in read_n:
        j+=1
        xm = x[0]
        k = 0
        for m in x:
            if (m<xm):
                xm = m
                k = x.index(m)
        if (j<=4):
            px = px1-px2
            px /=4
        else:
            px = px2-px3
            px /=4

def make_n():
    pom = []
    for i in range(1,len(read)+1):
        if (i%4!=0):
            pom.append(read[i-1])
        else:
            pom.append(read[i-1])
            read_n.append(pom)
            pom=[]
    #print read
    #print read_n

def calc_px():
    global px1,px2,px3
    num = (len(read)-9)/2
    px1=read.pop(0)+read.pop(0)+read.pop(0)
    px2=read.pop(num)+read.pop(num)+read.pop(num)
    px3=read.pop()+read.pop()+read.pop()
    read.pop(num-1)
    read.pop(num-1)
    px = (px1+px2+px2)/9
    p12 = (px1+px2)/6
    p23 = (px2+px3)/6
    #print "px1: %d; px2: %d; px3: %d;"%(px1,px2,px3)

def calc_read():
    read.pop(0)
    for i in range(0,len(read)):
        read[i]=math.trunc(read[i]*100000)
    def make_read(x,y):
    global crr,j,s,num,f
    if (abs(img[y,x,0]-crr)>20):
        num+=1
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
