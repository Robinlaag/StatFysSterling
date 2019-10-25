import scipy.odr as odr
import numpy as np
import matplotlib.pyplot as plt

try:
    from mplstyler import makeMplStyle
    makeMplStyle()
    print('mpl styled')
except ImportError:
    pass

x = np.array([0,1,2,3,4,5,6,7,8,9,10,11])
sig_x = x*0+0.1
y = np.array([2.36,2.60,2.92,3.24,3.36,4.04,4.56,5.12,5.72,6.48,7.40,8.40])
sig_y = y*0+0.1

f,ax = plt.subplots(1)

#ax.show()
Bstart=[40,15,-5]

def f(B, x):
    return B[2]+B[0] / (B[1]-x)

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


chi2 = odr_res.sum_square
chi2red = odr_res.res_var

# (6c) De (INTERNE!) covariantiematrix
par_cov = odr_res.cov_beta
print(" De (INTERNE!) covariantiematrix  = \n", par_cov)

C=par_cov*chi2red**.5
# (6d) De chi-kwadraat en de gereduceerde chi-kwadraat van deze aanpassing

print("\n Chi-squared         = ", chi2)
print(" Reduced chi-squared = ", chi2red, "\n")

# (6e) Een compacte weergave van de belangrijkste resultaten als output
odr_res.pprint()

# Hier plotten we ter controle de aanpassing met de dataset (niet opgemaakt)
xplot=np.arange(-1,13,1)

ax.errorbar(par_best[1]-x,y,xerr=sig_x,yerr=sig_y,fmt='k.',label="Data")
ax.plot(par_best[1]-xplot,f(par_best,xplot),'r-', label="Model")

ax.set_xlabel("Volume (ml)")
ax.set_ylabel("Output voltage (V)")
ax.legend()
plt.savefig("images\pplot_f.pdf",dpi=300)
