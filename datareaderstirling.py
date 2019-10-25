#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  7 10:52:31 2019

@author: Robin
"""
import os
import numpy as np
import matplotlib.pyplot as plt

# tries to import mpl styling function.
try:
    from mplstyler import makeMplStyle
    makeMplStyle()
    print('mpl styled')
except ImportError:
    pass

# main functions, takes in directory path of data folders.
def getPower(path):
    # change to directory of data files
    dirpath = path
    
    # counts number of folders inside the directory
    folders = 0
    for _, dirnames, _ in os.walk(dirpath):
        folders += len(dirnames)
    
    
    # sets number of sets equal to the amount of folders in dir
    nSets = folders
    
    # file names/directories
    fnames=[]
    for i in range(0,nSets):
        fnames.append("ALL{:04d}/F{:04d}".format(i,i))
    
    # empty lists to append data to
    data1_Arr = [] # pressure
    data2_Arr = [] # volume
    
    # reads all the p,v data from each dataset
    for fn in fnames:
        file = dirpath + fn
        with open(file+'CH1.CSV', 'r') as f:
            data1_Arr.append(np.genfromtxt(f,delimiter=',', usecols=4))
            
        with open(file+'CH2.CSV', 'r') as f:
            data2_Arr.append(np.genfromtxt(f,delimiter=',', usecols=4))
    
    '''
    On occasion the voltages recorded by the oscilloscope were negative.
    We take the absolute value of the voltage to prevent this from affecting
    the rest of the calculations.
    '''
    data1_Ar = np.abs(np.asarray(data1_Arr))
    data2_Ar = np.abs(np.asarray(data2_Arr))
    
    # converts voltage of pressure to pressure in hPa
    B = [108.34484944,20.47200596,-2.97859328]
    P_0 = 1010.7
    data1_Ar = (data1_Ar-B[2])*B[1]*P_0/B[0]
    
    # converts voltage of volume to volume in m^3
    data2_Ar = (32+data2_Ar*12/5)
    
    fx,ax=plt.subplots()
    line, = ax.plot(data2_Ar[3])
    ax.tick_params(axis='y', colors=line.get_color())
    ax2=ax.twinx()
    ax2.plot(data1_Ar[3],'r')
    ax2.tick_params(axis='y', colors='red')
    plt.show()
    
    # converts pressure array from hPa to Pa
    data1_Ar = data1_Ar*100
    # converts volume array from cm^3 to m^3
    data2_Ar = data2_Ar/10**6
    
    area_Ar = []
    
    # function to find the beginning and end of every full cycle in the data set
    def findcycles(p,v):
        zerosindex = np.where(np.diff(np.sign(p)))[0]
        th = 10
        # deletes all the zero indexes that are too close.
        zerosindex = np.delete(zerosindex, np.argwhere(np.ediff1d(zerosindex)<th)+1)
        length = len(zerosindex)-1
        fi = np.arange(0,length-(length%2),2)
        si = fi.copy() + 2
        
        # returns the indeces for the beginning and end of every cycle
        # and the number of cycles = len(fi)
        return zerosindex[fi], zerosindex[si], len(fi)
    
    
    for p,v in zip(data1_Ar,data2_Ar):
        # centers (p,v) around (0,0)
        p -= np.mean(p)
        v -= np.mean(v)
        
        first_i, second_i, ncycles = findcycles(p,v)
        
        # calculates the sum of time elapsed for each cycle
        tlen = np.sum(second_i-first_i)
        
        ar=[]
        
        # loop over all cycles
        for fi,si in zip(first_i,second_i):
            cp = np.copy(p[fi:si])
            cv = np.copy(v[fi:si])
            
            area = np.zeros(len(cp)-1)
            # calculates the area of the cycle
            for i in range(len(cp)-1):
                area[i]=(cp[i]*cv[i+1]-cp[i+1]*cv[i])/2
            ar.append(np.sum(area))
            
        ar=np.asarray(ar)
        
        area_Ar.append([ar.mean(),ar.std(),ncycles,tlen])
    
    area_Ar = np.asarray(area_Ar)
    Pi = area_Ar[:,0]*area_Ar[:,2]/(area_Ar[:,3]*0.0002) # internal power
    sPi = area_Ar[:,1]*area_Ar[:,2]/(area_Ar[:,3]*0.0002) # std of internal power
    
    # opens data file
    with open(dirpath+'Data.csv','r') as f:    
        Data_ar = np.genfromtxt(f,delimiter=',')
    
    if (len(Data_ar[0]) == 8):
        load = 'elec'
        Pe = Data_ar[:,-2]*Data_ar[:,-3]
    else:
        load = 'mech'
        Pe = Data_ar[:,-1]/1000*Data_ar[:,2]/60*(2*np.pi)
    
    # n, Pe, Pi, sig_pi, DT, T2, time(min.sec)
    return (Data_ar[:,2],Pe,Pi,sPi,Data_ar[:,3],Data_ar[:,4],Data_ar[:,1])
