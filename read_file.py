dataset = []
def make_dateset():
    global dataset
    file_names = ["0.txt","9.txt"]
    max = 0
    dists = {}

    for file_name in file_names:

        f = open(file_name, "r")
        lines = f.readlines()
        count = len(lines)
        group = int(file_name.split(".")[0])
        k = 0
        maxl = 0
        dist = []
        for i in range(0,count,4):
            if ((int(lines[i])>2) and (int(lines[i])<8)):
                dist.append([float(x) for x in lines[i+3].split(" ")])
                if (len(dist[k])>maxl):
                    maxl = len(dist[k])
                k+=1

        if (maxl>max):
            max = maxl
        dists[group] = dist

    for key,value in dists.items():
        for x in value:
            temp = []
            for i in range(max):
                if len(x)>i:
                    temp.append(x[i])
                else:
                    temp.append(0)
            temp.append(key)
            dataset.append(temp)

