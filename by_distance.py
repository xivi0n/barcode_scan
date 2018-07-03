import math,random

#variables for precalculation
#read_pos   = [] #raw points of bar edges locations on image
#read_pos_d = [] #distance between edges of bars (bar width)
#read_pos_n = [] #group of 4 for each 4 elements in read_pos_d

#variables for calculating bar size
#tocmp = [] #raw ratio distance/average bar1 size
#flag  = [] #calculated numbers

#variables for reading inputs
black = 0   #black color
white = 255 #white color
crr = white #current color

f = True    #true if white false if black
j = True    #true if changing colors
s = []      #point

#UPC numbers written as bar sizes
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

#calculating distance between two x=a[0] and x=b[0] lines of bars
def width(a,b):
    m=(b[0]-a[0])
    if (m==0):
        k = 0               #undefined
    else:
        k=1.0*(b[1]-a[1])/m #gradient of the line
    #distance*cos(arctg(k)) optimized distance*(1/(k^2+1))
    return math.sqrt(pow(b[0]-a[0],2)+pow(b[1]-a[1],2))*pow(k*k+1,-0.5) 

#creating read_pos
def get_points(x,y,img,read_pos):
    global crr,j,s,f,black,white
    if (abs(img[y,x,0]-crr)>20):    #if contrast between current color and current point location exist
        read_pos.append(s)          #append to read_pos
        j=True                      #color changed
        if (f):                     #if white
            crr = black             #then current color is black
        else:                       
            crr = white             #else current color is white
        f = not f                   #changing color
    else:
        if (j):                     #if color changed
            s = [x,y]               #save bar point
        j=False                     #not changing color

#making read_pos constant array of dx>0
def remove_left(read_pos):
    k = len(read_pos)-2             #first and last removed
    x = read_pos[0][0]              #first maximum x element
    i = 1                           #starting index
    while (k>i):                    #while max index>current index
        if (x>read_pos[i][0]):      #if current element[x] < maximum element 
            read_pos.pop(i)         #POP IT
            k-=1                    #max index-=1
        elif (abs(read_pos[i][0]-read_pos[i+1][0])<=5): #changed direction 
            x = read_pos[i][0]      #new maximum x element
            i+=1                    #going on next index
        else:    
            i+=1                    #going on next index

#creating read_pos_d
def get_distance(read_pos):            
    read_pos_d = []                             #removing surplus elements
    for i in range(1,len(read_pos)-1):                          #removed first and last point
        if (abs(read_pos[i][0]-read_pos[i+1][0])>2):            #if two points are not on same x axis
            read_pos_d.append(width(read_pos[i],read_pos[i+1])) #calculate width and append
    return read_pos_d

#removing indicator bars (first 3, middle 5 and last 3)
def remove_indicators(read_pos_d):
    num = int((len(read_pos_d)-8)/2) #calculating middle index
    read_pos_d.pop(0)           #removing first bar1   
    read_pos_d.pop(0)           
    read_pos_d.pop(0)           
    read_pos_d.pop(num-1)       #removing middle bar1
    read_pos_d.pop(num-1)
    read_pos_d.pop(num-1)
    read_pos_d.pop(num-1)
    read_pos_d.pop(num-1)
    read_pos_d.pop()            #removing last bar1
    read_pos_d.pop()

#creating read_pos_n
def make_pos_n(read_pos_d):
    pom = []                                #temp list
    read_pos_n = []
    for i in range(1,len(read_pos_d)+1):    
        if (i%4!=0):                        #if current index isn't 4th one
            pom.append(read_pos_d[i-1])     #append to temp list
        else:
            pom.append(read_pos_d[i-1])     #append 4th one
            read_pos_n.append(pom)          #append temp to read_pos_n
            pom=[]                          #reset temp list
    return read_pos_n

#classificating barX based on coefficient k
def classifyBar(x,k):
    if (1.0*x<=1):                      #if barX size is less than 1
        return 1                        #must be bar1
    elif(10.0*x%10<k):                  #if barX size is closer to floor value
        return (math.trunc(1.0*x))      #must be barX
    elif(10.0*x%10>10-k):               #if barX size is closer to ceil value
        return (math.trunc(1.0*x)+1)    #must be barX+1
    else:                               #else
        return (-1)                     #unkown

#classificating each number
def classify(read_pos_n,tocmp,flag):
    for num in read_pos_n:
        #calculating average bar1 size
        avrgBar = 0
        for x in num:
            avrgBar = x+avrgBar
        avrgBar /=7              

        pom = []    #temp array for appending on tocmp
        pom2 = []   #temp array for appending on flag
        k = 0
        for x in num:   #for each bar in number
            k+=1
            if (1.0*x/avrgBar<=1):          #if ratio is <=1 
                pom.append(1)               #append 1
            else:                           #else
                pom.append(1.0*x/avrgBar)   #append ratio
            pom2.append(classifyBar(1.0*x/avrgBar,2)) #append classificated bar
        
        tocmp.append(pom) #append ratio
        flag.append(pom2) #append classificated number
    
    while(classify_less_precision(flag,tocmp)!=0): #while not classificated numbers!=0
        continue

#calculates number of different elements between two lists (index matters)
def cmparr(a,b):
    pom = 0
    for i in range(0,4):
        if (a[i]==b[i]):
            pom+=1
    return pom

#calculate bar size for one unknown value
def onek(m,flag):
    sum = 0
    for i in range(0,4):        #for each bar
        if (flag[m][i]!=-1):    #if isnt unknown
            sum+=flag[m][i]     #add on sum
        else:
            j = i               #else save index
    flag[m][j]=7-sum            #number size = 7*bar1

#calculate bar size for two unknown values
def twok(m,ktor,tocmp,flag):
    probnum = [] #array of possible numbers
    for num in numbers:             
        if (cmparr(flag[m],num)==2): #if given number has 2 elements as default
            probnum.append(num)      #append possible number   

    if (len(probnum)==1):            #if 1 possible number
        flag[m]=probnum[0]           #must be that number
    elif (len(probnum)!=0):
        inx = [j for j in range(0,len(flag[m])) if flag[m][j] == -1] #getting index for unknown values
        cal = [] #array of difference between possible numbers and tocmp[m]
        for i in range(0,len(probnum)):
            cal.append(sum([abs(tocmp[m][j]-probnum[i][j]) for j in inx])) #calculating sum of differences
        print cal
        flag[m] = probnum[cal.index(min(cal))] #flag[m] must be possible number which has the lowest difference with tocmp[m]
    else:
        flag[m] = random.choice(numbers)

#getting index of number with minimum chance of being wrong
def calc_min(m,ktor,tocmp):
    max = abs(tocmp[m][ktor[0]]%1-0.50) 
    n = ktor[0] #index = index of first unknown
    for i in range(1,len(ktor)):
        pom = abs(tocmp[m][ktor[i]]%1-0.50) #calculating difference between decimals and 0.50
        if (pom>max):
            max = pom   
            n = ktor[i]
    return n

#classify with less precision
def classify_less_precision(flag,tocmp):
    numk = 0    #number of unknown bars
    for m in range(0,len(flag)): #for each number
        k = 0   #number of unknown bars in current number
        ktor=[] #index of unknown bars
        for i in range(0,4):
            if (flag[m][i]==-1): #if unknown
                ktor.append(i)   #append index
                k+=1             #increment k

            elif (tocmp[m][i]>4): #if bar is higher than 4
                if (i==0) or (i==2):
                    flag[m][i]=3      
                else:
                    flag[m][n]=4
                #tocmp[m][i]=4
            
            if (flag[m][i]==4) and ((i==0) or (i==2)): #if bar=4 isn't on 1 or 3 positions
                flag[m][i]=3                           #must be 3

        if (k==1):         #if numbers of unknown is 1 
            onek(m,flag)        #calculate it
            k-=1           #decrement k
        #elif (k==2):       #if numbers of unknown is 2
        #    k-=2
        #    twok(m,ktor,tocmp,flag)          #calculate it; decrement k 
        elif(k>1):         #if numbers of unknown is >2
            n = calc_min(m,ktor,tocmp) #calculate index of most precise number
            k-=1  #decrement k
            flag[m][n] = classifyBar(tocmp[m][n],5) #classify bar
        numk+=k   #add number of unknown bars for each number
    return numk

#compares calculated numbers and barcode default numbers
def get_number(flag):
    for x in flag:
        print(x), #calculated number written as bar sizes
        for y in numbers:
            if (cmparr(x,y)==4):    #must be that number
                print(numbers.index(y)),
            elif (cmparr(x,y)==3):  #probably that number
                print(numbers.index(y)),
        print("--")