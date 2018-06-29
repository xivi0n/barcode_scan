import cv2 
import numpy as np
import sys,getopt
from by_distance import *

file_name = ''
img = []
start = False

def draw_trajectory():
    img = cv2.imread(file_name)
    cv2.namedWindow('example12',cv2.WINDOW_NORMAL)
    cv2.imshow('example12',img)
    for i in range(1,len(read_pos)-1):
        img[read_pos[i-1][1],read_pos[i-1][0]] = [0,0,255]
        if (abs(read_pos[i][0]-read_pos[i+1][0])>2):
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
            #draw_rec(x,y)
            get_points(x,y,img)


    elif event == cv2.EVENT_LBUTTONUP:
        start = False

def make_argv(argv):
    global file_name
    try:
        opts, args = getopt.getopt(argv,"hi:",["ifile="])
    except getopt.GetoptError:
        print('main.py -i <inputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('main.py -i <file_name>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            file_name = arg

if __name__ == "__main__":
   make_argv(sys.argv[1:])

print('Reading barcode from file:', file_name)
img = cv2.imread(file_name)
cv2.namedWindow('example',cv2.WINDOW_NORMAL)
cv2.setMouseCallback('example',do_events)
cv2.imshow('example',img)
while(1):
    k = cv2.waitKey(1) & 0xFF
    if k ==27:
        break

remove_left()
draw_trajectory()
get_distance()
remove_indicators()
make_pos_n()
classify()
get_number()
cv2.destroyAllWindows()
