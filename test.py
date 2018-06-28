import cv2 
import numpy as np
import time
import math

file_name = 'bar1.jpg'
start = False
ix,iy = -20,-20
res = 32
base = cv2.imread(file_name)
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
num = -1
j = True
s = 0
dx = 0
px1 = 0
px2 = 0
px3 = 0
again = False

read_pos = []
read_pos_d = []
read_pos_n = []

def draw_rec(x,y):
    global ix,iy,res
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

def d(a,b):
    m=(b[0]-a[0])
    if (m==0):
        k = 0
    else:
        k=1.0*(b[1]-a[1])/m
    if (b[0]>=a[0]):
        j = 1
    else:
        j = -1
    return j*math.sqrt(pow(b[0]-a[0],2)+pow(b[1]-a[1],2))*pow(k*k+1,-0.5)

def make_read_pos(x,y):
    global crr,j,s,num,f
    if (abs(img[y,x,0]-crr)>20):
        num+=1
        read_pos.append(s)
        #font = cv2.FONT_HERSHEY_SIMPLEX
        #cv2.putText(img,'%.2f'%(d(read_pos[num-1],read_pos[num])),(read_pos[num][0]-10,read_pos[num][1]-40-num*10), font, 0.3,(0,0,255),1,cv2.LINE_AA)
        j=True
        if (f):
            crr = black
        else:
            crr = white
        f = not f
    else:
        if (j):
            s = [x,y]
        j=False

def check_read_pos_left():
    k = len(read_pos)-2
    x = read_pos[0][0]
    i = 1
    while (k>i):
        if (x>read_pos[i][0]):
            read_pos.pop(i)
            k-=1
        elif (abs(read_pos[i][0]-read_pos[i+1][0])<=5):
            x = read_pos[i][0]
            i+=1
        else:
            i+=1


def calc_read_pos():
    check_read_pos_left()
    print [x for x in read_pos]
    img = cv2.imread(file_name)
    cv2.namedWindow('example12',cv2.WINDOW_NORMAL)
    cv2.imshow('example12',img)
    for i in range(0,len(read_pos)-1):
        cv2.line(img,(read_pos[i][0],read_pos[i][1]),(read_pos[i+1][0],read_pos[i+1][1]),(255,0,0),2)
        read_pos_d.append(d(read_pos[i],read_pos[i+1]))
    read_pos_d.pop(0)
    cv2.imshow('example12',img)
    while(1):
        k = cv2.waitKey(1) & 0xFF
        if k ==27:
            break

def calc_px_pos():
    num = (len(read_pos_d)-8)/2
    read_pos_d.pop(0)
    read_pos_d.pop(0)
    read_pos_d.pop(0)
    read_pos_d.pop(num-1)
    read_pos_d.pop(num-1)
    read_pos_d.pop(num-1)
    read_pos_d.pop(num-1)
    read_pos_d.pop(num-1)
    read_pos_d.pop()
    read_pos_d.pop()

def make_pos_n():
    pom = []
    for i in range(1,len(read_pos_d)+1):
        if (i%4!=0):
            pom.append(read_pos_d[i-1])
        else:
            pom.append(read_pos_d[i-1])
            read_pos_n.append(pom)
            pom=[]
    #print read
    #print read_n


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

def calc_read():
    read.pop(0)
    for i in range(0,len(read)):
        read[i]=math.trunc(read[i]*100000)
    
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

def calcxpx(x,k):
    if (1.0*x<=1):
        return 1
    elif(10.0*x%10<k):
        return (math.trunc(1.0*x))
    elif(10.0*x%10>10-k):
        return (math.trunc(1.0*x)+1)
    else:
        return (-1)

def testtest():
    for aje in read_pos_n:
        px = 0
        for x in aje:
            px = x+px
        px /=7
        pxs.append(px)
        pom = []
        pom2 = []
        k = 0
        for x in aje:
            k+=1
            if (1.0*x/px<=1):
                pom.append(1)
            else:
                pom.append(1.0*x/px)
            pom2.append(calcxpx(1.0*x/px,2))
        
        tocmp.append(pom)
        flag.append(pom2)
    
    while(testtest2()!=0):
        continue
        # print "--------------------------"
        # print flag
        # print
        # print tocmp
        # print "--------------------------"

    #print 
    #print flag
    #print

def onek(m):
    k = 0
    for i in range(0,4):
        if (flag[m][i]!=-1):
            k+=flag[m][i]
        else:
            j = i
    flag[m][j]=7-k

def twok(m,ktor):
    probnum = []
    for x in numbers:
        if (cmparr(flag[m],x)==2):
            probnum.append(x)
    if (len(probnum)==1):
        flag[m]=probnum[0]
    else:
        cal = []
        inx = [j for j in range(0,len(flag[m])) if flag[m][j] == -1] 
        for i in range(0,len(probnum)):
            cal.append(sum([abs(tocmp[m][j]-probnum[i][j]) for j in inx]))
        #print cal
        # for i in range(0,len(cal)):
        #     cal[i]=cal[i][0]+cal[i][1]
        flag[m] = probnum[cal.index(min(cal))]

def calc_min(m,ktor):
    min = abs(tocmp[m][ktor[0]]%1-0.50)
    n = ktor[0]
    for i in range(1,len(ktor)):
        pom = abs(tocmp[m][ktor[i]]%1-0.50)
        if (pom>min):
            min = pom
            n = ktor[i]
    return n

def testtest2():
    global again
    again = False
    numk = 0
    for m in range(0,len(flag)):
        k = 0
        sum = 0
        n = 0
        ktor=[]
        for i in range(0,4):
            if (flag[m][i]==-1):
                ktor.append(i)
                k+=1

            elif (flag[m][i]>4):
                flag[m][i]=4
                #tocmp[m][i]=4
            
            if (flag[m][i]==4) and ((i==0) or (i==2)):
                flag[m][i]=3

            if (flag[m][i]!=-1):
                sum += flag[m][i]
        
        if (k==1):
            onek(m)
            k-=1
        # elif (k==2):
        #     twok(m,ktor)
        #     k-=2
        elif(k>1):
            n = calc_min(m,ktor)
            k-=1
            flag[m][n] = calcxpx(tocmp[m][n],5)
            again = True
        numk+=k
    return numk

def cmparr(a,b):
    pom = 0
    for i in range(0,4):
        if (a[i]==b[i]):
            pom+=1
    return pom

def calc_num():
    for x in flag:
        print x,
        for y in numbers:
            if (cmparr(x,y)==4):
                print numbers.index(y),
            elif (cmparr(x,y)==3):
                print numbers.index(y),
            # elif (cmparr(x,y)>1):
            #     print numbers.index(y),
        print "--"
                

# mouse callback function
def do_events(event,x,y,flags,param):
    global ix,iy,start,base,res
    if event == cv2.EVENT_LBUTTONDOWN:
        start = True
        cv2.imshow('example',img)

    elif event == cv2.EVENT_MOUSEMOVE:
        if start == True:
            draw_rec(x,y)
            make_read_pos(x,y)


    elif event == cv2.EVENT_LBUTTONUP:
        start = False

img = cv2.imread(file_name)
cv2.namedWindow('example',cv2.WINDOW_NORMAL)
cv2.setMouseCallback('example',do_events)
cv2.imshow('example',img)
while(1):
    k = cv2.waitKey(1) & 0xFF
    if k ==27:
        break

# read.pop(0)
# #calc_read()
# #print read
# #print len(read)
# #calc_dx()
# calc_px()
# #print read
# #print len(read)
# make_n()
# #remake_n()
# testtest()

calc_read_pos()
print read_pos_d
calc_px_pos()
make_pos_n()

testtest()

calc_num()

cv2.destroyAllWindows()