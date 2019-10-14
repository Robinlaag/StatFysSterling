# -*- coding: utf-8 -*-
"""
Created on Mon Dec 11 11:33:01 2017

@author: capel102
Uitleg bij de functionaliteit van ODR
"""
## (0) Importeer het ODR pakket (ODR = Orthogonal Distance Regression)
import scipy.odr as odr
import numpy as np
import matplotlib.pyplot as plt

# Fictieve dataset x- en y-waarden, beide met onzekerheid
x = np.array([0,1,2,3,4,5,6,7,8,9,10,11])
sig_x = x*0+0.1
y = np.array([2.36,2.60,2.92,3.24,3.36,4.04,4.56,5.12,5.72,6.48,7.40,8.40])
sig_y = y*0+0.1

# =============================================================================
#  we maken aan deze data een aanpassing met de functie y = a + b x
#  het is goed om deze dataset te plotten, en op basis hiervan een schatting te
#  maken voor startwaarden voor de parameters a en b. voor deze specifieke 
#  dataset kunnen we als schatting voor a de waarde gemeten bij de asafsnede 
#  nemen (0.5 dus), en voor b, de helling, ongeveer 1.5
#  met deze opzet kun je overigens eerst een plot maken met data (activeer dan
#  ax.show), en op een later moment de beste rechte lijn erbij plotten
#  nb dit is een niet opgemaakte plot
# =============================================================================
f,ax = plt.subplots(1)
ax.errorbar(x,y,xerr=sig_x,yerr=sig_y,fmt='k.')
#ax.show()
Bstart=[40,15,-5]

# =============================================================================
#  (1) Definieer een Python-functie die het model bevat, in dit geval een 
#  rechte lijn
#  B is een vector met parameters, in dit geval twee (A = B[0], B = B[1])
#  x is de array met x-waarden
# =============================================================================
def f(B, x):
    return B[2]+B[0] / (B[1]-x)

## (2) Definieer het model-object om te gebruiken in odr
odr_model = odr.Model(f)

## (3) Definieer een RealData object
## Een RealData-object vraagt om de onzekerheden in beide richtingen. 
## !! De onzekerheid in de x-richting mag ook nul zijn (dan mag je sx=0 weglaten), 
## maar dan moet bij onderdeel (4)/(4a) wel gekozen worden voor een
## kleinste-kwadratenaanpassing !!
odr_data  = odr.RealData(x,y,sx=sig_x,sy=sig_y)

## (4) Maak een ODR object met data, model en startwaarden
## Je geeft startwaarden voor parameters mee bij keyword beta0
odr_obj   = odr.ODR(odr_data,odr_model,beta0=Bstart)
## (4a) Stel in op kleinste kwadraten (optioneel)
## Als de onzekerheden in de x-richting gelijk zijn aan nul, dan faalt de 
## default-aanpak van ODR. Je moet dan als methode een kleinste-kwadraten- 
## aanpassing instellen. Dit gaat met het volgende commando (nu uit):
#odr_obj.set_job(fit_type=2)

## (5) Voer de fit uit
## Dit gebeurt expliciet door functie .run() aan te roepen
odr_res   = odr_obj.run()

## (6) Haal resultaten uit het resultaten-object:
# (6a) De beste schatters voor de parameters
par_best = odr_res.beta
# (6b) De (EXTERNE!) onzekerheden voor deze parameters
par_sig_ext = odr_res.sd_beta

# (6c) De (INTERNE!) covariantiematrix
par_cov = odr_res.cov_beta 
print(" De (INTERNE!) covariantiematrix  = \n", par_cov)

# (6d) De chi-kwadraat en de gereduceerde chi-kwadraat van deze aanpassing
chi2 = odr_res.sum_square
print("\n Chi-squared         = ", chi2)
chi2red = odr_res.res_var
print(" Reduced chi-squared = ", chi2red, "\n")

# (6e) Een compacte weergave van de belangrijkste resultaten als output
odr_res.pprint()

# Hier plotten we ter controle de aanpassing met de dataset (niet opgemaakt)
xplot=np.arange(-1,13,1)
ax.plot(xplot,f(par_best,xplot),'r-')
