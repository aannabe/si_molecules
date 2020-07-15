#! /usr/bin/env python

import sys,os
import pandas as pd
from scipy.optimize import curve_fit
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt


#~~~~~~~~ Input ~~~~~~~~~~~~
basis = np.array([2,3,4])
scf  = np.array([-6.22114104, -6.25183542, -6.26063723,])
#ccsd = np.array([-5.94301458, -5.95214538, -5.95475895, -5.95555698])
#~~~~~~~~~~~~~~~~~~~~~~~~~~~
#corr = ccsd - scf
   


def scf_cbs(n, e_cbs, c, d):	#SCF
        y=e_cbs+c*np.exp(-d*n)
        return y

def corr_cbs(n, e_cbs, c, d):	#Correlation
        y=e_cbs+c/(n+3.0/8.0)**3.0+d/(n+3.0/8.0)**5.0
        return y

####~~~~~~~~~~~~~~Corr~~~~~~~~~~~~~~~~~~~~~~
#
#xdata=basis
#ydata=corr
#
#initial=[min(ydata), 0.1, 1.0]
#limit=( [-np.inf, -np.inf, -np.inf], [min(ydata), np.inf, np.inf] )
#popt_corr, pcov_corr = curve_fit(corr_cbs, xdata, ydata, p0=initial, bounds=limit)
#print("Fit params:", popt_corr, np.sqrt(np.diag(pcov_corr)), "\n")
#
#x=np.linspace(xdata[0],xdata[-1],50)
#fig, ax = plt.subplots()
#plt.plot(xdata, ydata, 'o')
#plt.plot(x, corr_cbs(x, *popt_corr), '--', lw=1, label="Fitted Function")
#plt.axhline(y=popt_corr[0], ls='dashed', lw=1, color='red', label='CBS limit')
#ax.set(title='Extrapolation of Correlation',
#xlabel='Cardinal n',
#ylabel='E(hartree)')
#legend = ax.legend(loc='best', shadow=False)
##plt.savefig('extrap.png', format='png', dpi=100)
#plt.show()
#

#~~~~~~~~~~~SCF~~~~~~~~~~~~~~~~~~~~~~~~~

xdata=basis
ydata=scf

initial=[min(ydata), 0.01, 1.0]
limit=( [-np.inf, -np.inf, -np.inf], [min(ydata), np.inf, np.inf] )
popt_scf, pcov_scf = curve_fit(scf_cbs, xdata, ydata, p0=initial, bounds=limit)
print("SCF", popt_scf, np.sqrt(np.diag(pcov_scf)))

x=np.linspace(xdata[0],xdata[-1],50)
fig, ax = plt.subplots()
plt.plot(xdata, ydata, 'o')
plt.plot(x, scf_cbs(x, *popt_scf), '--', lw=1, label="Fitted Function")
plt.axhline(y=popt_scf[0], ls='dashed', lw=1, color='red', label='CBS limit')
ax.set(title='SCF Extrapolation Fit',
xlabel='Cardinal n',
ylabel='E(hartree)')
legend = ax.legend(loc='best', shadow=False)
#plt.savefig('extrap_scf.png', format='png', dpi=100)
plt.show()



