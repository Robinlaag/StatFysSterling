#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  9 09:16:59 2019

@author: Robin
"""

import matplotlib as mpl

def makeMplStyle():
    mpl.rcParams['axes.prop_cycle']=mpl.cycler('color', ['0C5DA5', '00B945', 'FF9500', 'FF2C00', '845B97', '474747', '9e9e9e'])
    mpl.rcParams['figure.figsize']=(3.5,2.625)
    
    mpl.rcParams['xtick.direction'] = 'in'
    mpl.rcParams['xtick.major.size']=3
    mpl.rcParams['xtick.major.width']=0.5
    mpl.rcParams['xtick.minor.size']=1.5
    mpl.rcParams['xtick.minor.width']=0.5
    mpl.rcParams['xtick.minor.visible']=True
    mpl.rcParams['xtick.top']=True
    
    mpl.rcParams['ytick.direction'] = 'in'
    mpl.rcParams['ytick.major.size']=3
    mpl.rcParams['ytick.major.width']=0.5
    mpl.rcParams['ytick.minor.size']=1.5
    mpl.rcParams['ytick.minor.width']=0.5
    mpl.rcParams['ytick.minor.visible']=True
    mpl.rcParams['ytick.right']=True
    
    mpl.rcParams['axes.linewidth']=0.5
    mpl.rcParams['grid.linewidth']=0.5
    mpl.rcParams['lines.linewidth']=1
    
    mpl.rcParams['legend.frameon']=False
    
    mpl.rcParams['savefig.bbox']='tight'
    mpl.rcParams['savefig.pad_inches']=0.05
    
    mpl.rcParams['font.serif']='Times New Roman'
    mpl.rcParams['font.family']='serif'
    
    mpl.rcParams['text.usetex']=True
    mpl.rcParams['text.latex.preamble']=r'\usepackage{amsmath}, \usepackage[T1]{fontenc}'
    
