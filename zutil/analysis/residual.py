# practice creating and writing to a csv file

import csv

##function which takes the new and old variable, and then checks them against a tolerance

def rescalc(old,new,tol):
    difference = new - old
    if abs(difference) <= tol:
        return True
    else:
        return False
    

#def resdata(oldset,newset,tolerances): ## eg. tolerances = [1, 1, 1e-5, 1e-7, 1e-2, 1e-4, 1e-2, 1e-6, 1e-1]
    ##open old data
def resopendata(dataset,p): ## if p is 1 then it returns headers, if 0 returns final cycle        
    with open(dataset) as f:
        readCSV = list(csv.reader(f))
        n = sum(1 for row in readCSV)
        if p == 0:
            fin = readCSV[n-1][0].split()
        elif p == 1:
            fin = readCSV[0][0].split()
    return fin


## separate variables and declarations
def resdata(data1,data2,tolerances):
    old_data = resopendata(data1,0)
    new_data = resopendata(data2,0)
    X = True
    ## loop over all variables to calculate and returns false if one is outside the tolerance

    for i in range(0,9): #num of var
        y = rescalc(float(old_data[i]),float(new_data[i]), tolerances[i])
        if y != True:
            X = False
    return X

tolerances = [1, 1, 1e-5, 1e-7, 1e-2, 1e-4, 1e-2, 1e-6, 1e-1]
resdata('testdata.csv','testdata2.csv',tolerances)
       

