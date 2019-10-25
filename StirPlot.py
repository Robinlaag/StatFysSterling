#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 21 11:31:27 2019

@author: Robin
"""

import matplotlib.pyplot as plt
import matplotlib.patheffects as PathEffects
import numpy as np
from datareaderstirling import getPower

try:
    from mplstyler import makeMplStyle
    makeMplStyle()
    print('mpl styled')
except ImportError:
    pass

D1 = np.asarray(getPower(r'S4/'))
D2 = np.asarray(getPower(r'S5/'))
Data = np.concatenate((D1,D2),axis=1)


T1 = D1[4,4:]-D1[5,4:]
T2 = D1[5,4:]


def plot45():
    cycle = plt.rcParams['axes.prop_cycle'].by_key()['color']
    
    # fig1 - Power external and internal
    f, ax = plt.subplots()
    ax.set_xlabel('$n$ (rpm)')
    ax.set_ylabel('$P$ (W)')
    
    ax.errorbar(Data[0],Data[2],fmt='.',label='Internal')
    ax.errorbar(Data[0],Data[1],fmt='.',label='External')
    
    #ax.legend(bbox_to_anchor=(1.04,0.5), loc='center left', borderaxespad=0)
    ax.legend()
    
    plt.savefig('images/S4S5-PePi.pdf',dpi=300)
    plt.show()
    
    # fig2 - Power external
    f, ax = plt.subplots()
    ax.set_xlabel('$n$ (rpm)')
    ax.set_ylabel('$P$ (W)')
    
    ax.errorbar(Data[0],Data[1],fmt='.',label='External')
    #ax.errorbar(Data[0,:4],Data[1,:4],fmt='.')
    plt.savefig('images/S4S5-Pe.pdf',dpi=300)
    plt.show()
    
    # fig3 - Power internal
    f, ax = plt.subplots()
    ax.set_xlabel('$n$ (rpm)')
    ax.set_ylabel('$P$ (W)')
    
    ax.errorbar(Data[0],Data[2],yerr=Data[3],fmt='.',label='Internal')
    plt.savefig('images/S4S5-Pi.pdf',dpi=300)
    plt.show()
    
    # fig4 - efficiency
    f, ax = plt.subplots()
    ax.set_xlabel('$n$ (rpm)')
    ax.set_ylabel('$\eta$ $(P_e/P_i)$')
    
    ax.errorbar(Data[0],Data[1]/Data[2],fmt='.',label='$P_e/P_i$')
    
    #ax.legend(bbox_to_anchor=(1.04,0.5), loc='center left', borderaxespad=0)
    
    plt.savefig('images/S4S5-n.pdf',dpi=300)
    plt.show()
    
    ####
    f, ax = plt.subplots()
    ax.set_xlabel('$n$ (rpm)')
    
    
    ax.errorbar(Data[0],Data[2],fmt='.',label='Internal')
    ax.set_ylabel('Internal Power (W)')
    ax2=ax.twinx()
    ax2.errorbar(Data[0],Data[1],fmt='.',label='External',color=cycle[1])
    ax2.set_ylabel('External Power (W)')
    f.text(.2,.7,'External',fontsize=15,color=cycle[1],weight='bold')
    f.text(.4,.42,'Internal',fontsize=15,color=cycle[0],rotation=33,weight='bold')
    #ax.legend(bbox_to_anchor=(1.04,0.5), loc='center left', borderaxespad=0)
    #f.legend(bbox_to_anchor=(.1,.93),loc="upper left")
    
    plt.savefig('images/S4S5-PePiscaled1.pdf',dpi=300)
    plt.show()
    ####
    f, ax = plt.subplots()
    ax.set_xlabel('$n$ (rpm)')
    
    
    ax.errorbar(Data[0],Data[2],fmt='.',label='Internal')
    ax.set_ylabel('$P_i$ (W)')
    ax2=ax.twinx()
    ax2.errorbar(Data[0],Data[1],fmt='.',label='External',color=cycle[1])
    ax2.set_ylabel('$P_e$ (W)')
    ax2.yaxis.label.set_color(cycle[1])
    ax.yaxis.label.set_color(cycle[0])
    #ax.legend(bbox_to_anchor=(1.04,0.5), loc='center left', borderaxespad=0)
    f.legend(bbox_to_anchor=(.1,.93),loc="upper left")
    
    plt.savefig('images/S4S5-PePiscaled2.pdf',dpi=300)
    plt.show()
    ####
    f, ax = plt.subplots()
    ax.set_xlabel('$n$ (rpm)')
    
    
    ax.errorbar(Data[0],Data[2],fmt='.',label='Internal')
    ax.set_ylabel('$P_i$ (W)')
#    ax.spines['left'].set_color(cycle[0])
#    ax.spines['right'].set_color(cycle[1])
    ax2=ax.twinx()
    ax2.errorbar(Data[0],Data[1],fmt='.',label='External',color=cycle[1])
    ax2.set_ylabel('$P_e$ (W)')
#    ax2.spines['left'].set_color(cycle[0])
#    ax2.spines['right'].set_color(cycle[1])
    ax.tick_params(axis='y', colors=cycle[0])
    ax2.tick_params(axis='y', colors=cycle[1])
    #ax.legend(bbox_to_anchor=(1.04,0.5), loc='center left', borderaxespad=0)
    f.legend(bbox_to_anchor=(.1,.93),loc="upper left")
    
    plt.savefig('images/S4S5-PePiscaled3.pdf',dpi=300)
    plt.show()
    #########
    



def plot45sep():    
    f, ax = plt.subplots()
    
    ax.errorbar(D1[0],D1[2],fmt='.',label='Internal S4')
    ax.errorbar(D1[0],D1[1],fmt='.',label='External S4')
    
    ax.errorbar(D2[0],D2[2],fmt='.',label='Internal S5')
    ax.errorbar(D2[0],D2[1],fmt='.',label='External S5')
    
    ax.set_xlabel('$n$ (rpm)')
    ax.set_ylabel('$P$ (W)')
    ax.legend(bbox_to_anchor=(1.04,0.5), loc="center left", borderaxespad=0)
    plt.savefig('images/PiPe-{}{}.pdf'.format('elec',45),dpi=300)
    plt.show()
    
    f, ax = plt.subplots()
    
    ax.errorbar(D1[0],D1[1],fmt='.',label='External S4')
    
    ax.errorbar(D2[0],D2[1],fmt='.',label='External S5')
    
    ax.set_xlabel('$n$ (rpm)')
    ax.set_ylabel('$P$ (W)')
    plt.savefig('images/Pe-{}{}.pdf'.format('elec',45),dpi=300)
    plt.show()
    
    f, ax = plt.subplots()
    
    print(D1[3],D2[3])
    
    ax.errorbar(D1[0],D1[2],yerr=D1[3],fmt='.',label='Internal S4')
    
    ax.errorbar(D2[0],D2[2],yerr=D2[3],fmt='.',label='Internal S5')
    ax.set_xlabel('$n$ (rpm)')
    ax.set_ylabel('$P$ (W)')
    plt.savefig('images/Pi-{}{}.pdf'.format('elec',45),dpi=300)
    plt.show()
    
    
    f, ax = plt.subplots()
    
    ax.errorbar(D1[0],D1[1]/D1[2],fmt='.',label='Internal S4')
    
    ax.errorbar(D2[0],D2[1]/D2[2],fmt='.',label='Internal S5')
    
    ax.set_xlabel('$n$ (rpm)')
    ax.set_ylabel('$\eta$')
    plt.savefig('images/PeDIVPi-{}{}.pdf'.format('elec',45),dpi=300)
    plt.show()
