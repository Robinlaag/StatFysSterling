#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 21 11:31:27 2019

@author: Robin
"""

import matplotlib.pyplot as plt
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

ax.errorbar(D1[0],D1[2],fmt='.',label='Internal S4')

ax.errorbar(D2[0],D2[2],fmt='.',label='Internal S5')
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