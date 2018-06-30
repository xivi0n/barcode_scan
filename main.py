import cv2 
import numpy as np
import sys,getopt
from by_distance import *

file_name = ''
img = []
start = False
ix,iy = -20,-20
res = 32
base = 0

tocmp = []
flag = []

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

def draw_trajectory():
    img = cv2.imread(file_name)
    cv2.namedWindow('example12',cv2.WINDOW_NORMAL)
    cv2.imshow('example12',img)
    for i in range(1,len(read_pos)-1):
        if (abs(read_pos[i][0]-read_pos[i+1][0])>5):
            cv2.line(img,(read_pos[i][0],read_pos[i][1]),(read_pos[i+1][0],read_pos[i+1][1]),(255,0,0),3)
            img[read_pos[i][1],read_pos[i][0]] = [0,0,255]
    img[read_pos[i+1][1],read_pos[i+1][0]] = [0,0,255]
    cv2.imshow('example12',img)
    while(1):
        k = cv2.waitKey(1) & 0xFF
        if k ==27:
            break

# mouse callback function
def do_events(event,x,y,flags,param):
    global ix,iy,start,base,res
    if event == cv2.EVENT_LBUTTONDOWN:
        start = True
        cv2.imshow('example',img)

    elif event == cv2.EVENT_MOUSEMOVE:
        if start == True:
            draw_rec(x,y)
            get_points(x,y,img,read_pos)


    elif event == cv2.EVENT_LBUTTONUP:
        start = False

def make_argv(argv):
    global file_name
    try:
        opts, args = getopt.getopt(argv,"hi:",["ifile="])
    except getopt.GetoptError:
        print 'main.py -i <inputfile>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'main.py -i <file_name>'
            sys.exit()
        elif opt in ("-i", "--ifile"):
            file_name = arg

if __name__ == "__main__":
   make_argv(sys.argv[1:])

print 'Reading barcode from file:', file_name
img = cv2.imread(file_name)
base = cv2.imread(file_name)
cv2.namedWindow('example',cv2.WINDOW_NORMAL)
cv2.setMouseCallback('example',do_events)
cv2.imshow('example',img)
while(1):
    k = cv2.waitKey(1) & 0xFF
    if k ==27:
        break

remove_left(read_pos)
draw_trajectory()
read_pos_d = get_distance(read_pos)
remove_indicators(read_pos_d)
read_pos_n = make_pos_n(read_pos_d)
classify(read_pos_n,tocmp,flag)
get_number(flag)
cv2.destroyAllWindows()
