import csv
import numpy as np
import matplotlib.pyplot as plt
import math
import os
import os.path
import pandas as pd
import operator

# greatest common divisor function.
def gcd(a,b):
    while b > 0:
        a, b = b, a % b
    return a
    
# lowest common multiple function.
def lcm(a, b):
    return a * b / gcd(a, b)


# function which opens a data file and returns its data.
def open_file(file_path,header_TF):
    if header_TF is True:
        df = pd.read_csv(file_path, skipinitialspace=True,delim_whitespace=True)
        return df
    else:
        df = pd.read_csv(file_path, skipinitialspace=True,delim_whitespace=True,header = None)
        return df


# function which checks the frequency of the cycles if the cycle column exists and returns it.
def cycle_freq(df):
    freq = df.Cycle[3]-df.Cycle[2]
    return freq

# function which calculates the difference between two numbers and returns it
def calc(num1,num2,var_diff_temp):
    diff = float(num1) - float(num2)
    var_diff_temp.append(diff)
    return [diff,var_diff_temp]
    
# function which checks against a tolerance
def check_tol(value,tol):
    if abs(value) <= tol:
        return True
    else:
        return False


def main(df,df2,headerTF):
    num_rows_1 = df.shape[0]
    num_rows_2 = df2.shape[0]
    var_diff = []
    incorrect = []
    flag = True
    
        
    if headerTF is True:
        max_cycle = min(df.loc[:, 'Cycle'][num_rows_1 - 1],  df.loc[:, 'Cycle'][num_rows_2 - 1])
            
        headers = list(df)           
        cycle_frequency_1 = cycle_freq(df)
        cycle_frequency_2 = cycle_freq(df2)
 
        
        cycle_increments = lcm(cycle_frequency_1,cycle_frequency_2)
        nt = cycle_increments / cycle_frequency_1
        mt = cycle_increments / cycle_frequency_2 
        
        max_iterations_1 = max_cycle / nt
        max_iterations_2 = max_cycle / mt
        max_iterations = min(max_iterations_1,max_iterations_2)
        
        j = max_iterations / cycle_increments
        
        
        for var in headers:  #selects variable
            var_diff_temp = []
            value1 = df.loc[:, var][0]
            value2 = df2.loc[:, var][0]
            x = calc(value1,value2,var_diff_temp)
            diff = x[0]
            var_diff_temp = x[1]
            
            if check_tol(diff,tol[var]) is False:
                flag = False
                incorrect.append([df.loc[:, 'Cycle'][0],var])
            
            
            for i in range(1,j+1):
                value1 = df.loc[:, var][nt*i]
                value2 = df2.loc[:, var][mt*i]
                #print [var,df.loc[:, 'Cycle'][i],value1,value2]
                x = calc(value1,value2,var_diff_temp)
                diff = x[0]
                var_diff_temp = x[1]
                
                if check_tol(diff,tol[var]) is False:
                    flag = False
                    incorrect.append([df.loc[:, 'Cycle'][i],var])
                    
            y = max(var_diff_temp, key=abs)
            var_diff.append(y)
        
        
        if flag is True:
            print "###############################################\n"
            print "Validation Passed :-)\n"
            print "###############################################\n"
        else:
            incorrect = sorted(incorrect, key=operator.itemgetter(0))
            print "###############################################\n"
            print "Validation Failed :-(\n"
            print "###############################################\n"
            print "The validation failed in "+str(len(incorrect))+" places.\n"
            
            print "Failure(s) detected at:\n"
            for j in range(0,len(incorrect)):
                print "Error: " + str(j+1)
                print "Cycle: " + str(incorrect[j][0]) + "\nVariable: "+ incorrect[j][1]+"\n"
            
            
            print "###############################################\n"
            print "Max Differences:\n"
            for k in range(2,df.shape[1] - 1):
                print "max "+ headers[k] +" difference: "+ str(var_diff[k])
            
            print "\n###############################################"
            
################################################################################################################
        
headerTF = True  # Set if your data will have headers

tol = dict([('RealTimeStep', 1),
       ('Cycle',1),
       ('rho',1e-15),
       ('rhoV[0]',1e-15),
       ('rhoV[1]',1e-15),
       ('rhoV[2]',1e-15),
       ('rhoE',1e-15),
       ('rhok',1e-15),
       ('rhoOmega',1e-15)]) #set tolerances for each variable

df = open_file('testdata.csv', headerTF)
df2 = open_file('testdata2.csv', headerTF)
        
main(df,df2,headerTF)
        

