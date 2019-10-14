#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  7 10:52:31 2019

@author: Robin
"""
import numpy as np
import matplotlib.pyplot as plt
from mplstyler import makeMplStyle

# does the styling of the figures.

makeMplStyle() # if mplstyler.py is missing comment this line out.

# change to directory of data files
dirpath = r'/home/Robin/StatFys/S2/'

# number of data sets 
nSets = 15

# file names/directories
fnames=[]
for i in range(0,nSets):
    fnames.append("ALL{:04d}/F{:04d}".format(i,i))

data1_Arr = []
data2_Arr = []

# reads all the p,v data from each dataset
for fn in fnames:
    file = dirpath + fn
    with open(file+'CH1.CSV', 'r') as f:
        data1_Arr.append(np.genfromtxt(f,delimiter=',', usecols=4))
        
    with open(file+'CH2.CSV', 'r') as f:
        data2_Arr.append(np.genfromtxt(f,delimiter=',', usecols=4))


# the channels were switched around for measurements data_M

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

for px,vy,i in zip(data1_Ar,data2_Ar,range(0,len(data1_Ar))):
    plt.plot(px,vy)
    plt.ylabel('$V$ (ml)')
    plt.xlabel('$p$ (hPa)')
    plt.savefig('images/P-V-meting{}{}.pdf'.format(i,'Session1M'),dpi=300)
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
    
    zerosindex = np.delete(zerosindex, np.argwhere(np.ediff1d(zerosindex)<th)+1)
    length = len(zerosindex)-1
    fi = np.arange(0,length-(length%2),2)
    si = fi.copy() + 2
    
    return zerosindex[fi], zerosindex[si], len(fi)
    

for p,v in zip(data1_Ar,data2_Ar):
    # centers (p,v) around (0,0)
    p -= np.mean(p)
    v -= np.mean(v)
    
    first_i, second_i, ncycles = findcycles(p,v)
    # tlen = second_i[-1]-first_i[0]
    tlen = np.sum(second_i-first_i)
    ar=[]
    for fi,si in zip(first_i,second_i):
        cp = np.copy(p[fi:si])
        cv = np.copy(v[fi:si])
        
        area = np.zeros(len(cp)-1)
        for i in range(len(cp)-1):
            area[i]=(cp[i]*cv[i+1]-cp[i+1]*cv[i])/2
        ar.append(np.sum(area))
        
    ar=np.asarray(ar)
    area_Ar.append([ar.mean(),ar.std(),ncycles,tlen])


x=range(0,nSets)

for a,i in zip(area_Ar,x):
    print("Meting {}: {:.4f} J/s".format(i,a[0]*a[2]/(a[3]*0.0002)))
        
        

