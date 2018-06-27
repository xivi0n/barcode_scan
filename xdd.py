cal = []
flag = [[1,-1,1,-1]]
inx = [j for j in range(0,len(flag[0])) if flag[0][j] == -1] 

probnum=[[1,4,1,1],[1,1,1,4],[1,3,1,2],[1,2,1,3]]

tocmp = [[1,2.4,1,2.5]]
m = 0
for i in range(0,len(probnum)):
    cal.append([abs(tocmp[m][j]-probnum[i][j]) for j in inx] )
for i in range(0,len(cal)):
            cal[i]=cal[i][0]+cal[i][1]
flag[m] = probnum[cal.index(min(cal))]
print flag
print cal