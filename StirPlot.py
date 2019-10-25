#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 21 11:31:27 2019

@author: Robin
"""

import matplotlib.pyplot as plt
import numpy as np
from datareaderstirling import getPower

# tries to import mpl styling function.
try:
    from mplstyler import makeMplStyle
    makeMplStyle()
    print('mpl styled')
except ImportError:
    pass

# gets data using datareaderstirling.py for session 4 and 5
D1 = np.asarray(getPower(r'S4/'))
D2 = np.asarray(getPower(r'S5/'))

# combines the data from both sessions
Data = np.concatenate((D1,D2),axis=1)

# the indeces of the 5 outliers due to low temps
outliers = [0,1,2,3,43]

x = np.delete(Data[0],outliers,0) # n (rpm) without outliers
y = np.delete(Data[2],outliers,0) # P_i (W) without outliers

xs = np.linspace(x.min(),x.max(),len(x))
x = x[:,np.newaxis]
a, _, _, _ = np.linalg.lstsq(x,y,rcond=None) # least square fit
print('Least square fit for internal power:\nP_i = n*{}'.format(a[0]))

# main plot function
def plot45():
    # gets the current colour cycle
    cycle = plt.rcParams['axes.prop_cycle'].by_key()['color']
    
    # fig1 - Power external and internal
    f, ax = plt.subplots()
    ax.set_xlabel('$n$ (rpm)')
    ax.set_ylabel('$P$ (W)')
    
    ax.errorbar(Data[0],Data[2],fmt='.',label='Internal')
    ax.errorbar(Data[0],Data[1],fmt='.',label='External')
    ax.legend()
    
    plt.savefig('images/S4S5-PePi.pdf',dpi=300)
    plt.show()
    
    
    # fig2 - Power external
    f, ax = plt.subplots()
    ax.set_xlabel('$n$ (rpm)')
    ax.set_ylabel('$P$ (W)')
    
    ax.errorbar(Data[0],Data[1],fmt='k.',label='External')
    plt.savefig('images/S4S5-Pe.pdf',dpi=300)
    plt.show()
    
    
    # fig3 - Power internal
    f, ax = plt.subplots()
    ax.set_xlabel('$n$ (rpm)')
    ax.set_ylabel('$P$ (W)')
    
    ax.errorbar(Data[0],Data[2],yerr=Data[3],fmt='k.',label='Internal')
    ax.plot(xs,a*xs,'r-')
    plt.savefig('images/S4S5-Pi.pdf',dpi=300)
    plt.show()
    
    
    # fig4 - efficiency
    f, ax = plt.subplots()
    ax.set_xlabel('$n$ (rpm)')
    ax.set_ylabel('$\eta$ $(P_e/P_i)$')
    
    # main data points
    ax.errorbar(Data[0],Data[1]/Data[2],fmt='k.',label='$P_e/P_i$')
    # encircled outliers
    ax.errorbar(Data[0,outliers],Data[1,outliers]/Data[2,outliers],fmt='ro',label='External',markersize=9,fillstyle='none',zorder=-5)
    
    plt.savefig('images/S4S5-n.pdf',dpi=300)
    plt.show()
    
    # fig 5 - Power external and internal (twin x)
    f, ax = plt.subplots()
    ax.set_xlabel('$n$ (rpm)')
    
    # main data points
    ax.errorbar(Data[0],Data[2],fmt='o',label='Internal',markersize=3)
    # encircled outliers
    ax.errorbar(Data[0,outliers],Data[2,outliers],fmt='ro',label='External',markersize=9,fillstyle='none',zorder=-5)
    # lin fit
    ax.plot(xs,a*xs,'k--',label='Model')
    ax.set_ylabel('Internal Power (W)')
    
    # calulates rotation for text
    p1 = ax.transData.transform_point((xs[0], a[0]*xs[0]))
    p2 = ax.transData.transform_point((xs[1], a[0]*xs[1]))
    dy = (p2[1] - p1[1])
    dx = (p2[0] - p1[0])
    rotn = np.degrees(np.arctan2(dy, dx))
    
    ax2=ax.twinx()
    ax2.errorbar(Data[0],Data[1],fmt='v',label='External',color=cycle[1],markersize=3.5)
    ax2.errorbar(Data[0,outliers],Data[1,outliers],fmt='ro',label='External',markersize=9,fillstyle='none',zorder=-5)
    ax2.set_ylabel('External Power (W)')
    
    f.text(.2,.7,'External',fontsize=15,color=cycle[1],weight='bold')
    f.text(.4,.43,'Internal',fontsize=15,color=cycle[0],rotation=rotn,weight='bold')
    
    ax2.spines['right'].set_visible(False)
    ax2.spines['top'].set_visible(False)
    ax2.spines['left'].set_visible(False)
    ax2.spines['bottom'].set_visible(False)
    
    plt.savefig('images/S4S5-PePiscaled1.pdf',dpi=300)
    plt.show()
    

if __name__ == '__main__':
    plot45()
    