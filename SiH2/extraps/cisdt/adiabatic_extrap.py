#! /usr/bin/env python

import sys,os
import pandas as pd
from scipy.optimize import curve_fit
#import glob
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import uncertainties
from uncertainties import ufloat
import string

toev = 27.211386245988

#~~~~~~~~ Input ~~~~~~~~~~~~
pd.options.display.float_format = '{:,.6f}'.format
np.set_printoptions(precision=6)
states = ['gs_vertical.csv', 'triplet_adiabatic.csv', 'singlet_adiabatic.csv']
#~~~~~~~~~~~~~~~~~~~~~~~~~~~

def scf_cbs(n, e_cbs, c, d):	#SCF
        y=e_cbs+c*np.exp(-d*n)
        return y

def corr_cbs(n, e_cbs, c, d):	#Correlation
        y=e_cbs+c/(n+3.0/8.0)**3.0+d/(n+3.0/8.0)**5.0
        return y

class ShorthandFormatter(string.Formatter):
    def format_field(self, value, format_spec):
        if isinstance(value, uncertainties.UFloat):
            return value.format(format_spec+'S')  # Shorthand option added
        # Special formatting for other types can be added here (floats, etc.)
        else:
            # Usual formatting:
            return super(ShorthandFormatter, self).format_field(
                value, format_spec)
frmtr = ShorthandFormatter()


#scf = pd.DataFrame(columns=basis, index=folders)
#corr = pd.DataFrame(columns=basis, index=folders)
#extr = pd.DataFrame(columns=["CBS"], index=folders)
#my_corr=0.0

energies = []

for i in states:
	print("Working on %s" % i)
	df = pd.read_csv(i, sep='\s* \s*', engine='python')	# \s*,\s* gets rid of empty spaces in column names
	#print(df)

	#### Total ####
	xdata = df['cardinal'].values
	ydata = df['total'].values
	try:
		initial=[min(ydata), 0.1, 1.0]
		limit=( [-np.inf, -np.inf, -np.inf], [min(ydata), np.inf, np.inf] )
		popt_scf, pcov_scf = curve_fit(scf_cbs, xdata, ydata, p0=initial, bounds=limit)
		print("Total params:", popt_scf, np.sqrt(np.diag(pcov_scf)))
		total_extrap = popt_scf[0]

		x=np.linspace(xdata[0],xdata[-1],50)
		fig, ax = plt.subplots()
		plt.plot(xdata, ydata, 'o')
		plt.plot(x, scf_cbs(x, *popt_scf), '--', lw=1, label="Fitted Function")
		plt.axhline(y=popt_scf[0], ls='dashed', lw=1, color='red', label='CBS limit')
		ax.set(title='Total Energy Fit %s' % i,
		xlabel='Cardinal n',
		ylabel='E(hartree)')
		legend = ax.legend(loc='best', shadow=False)
		plt.show()

		print("Total Energy: %s %s" % (i, total_extrap))
		energies.append(total_extrap)

	except:
		print("Unexpected error at %s:" % i, sys.exc_info()[0])
	

energies = np.array(energies)
energies = (energies - energies[0])*toev
print(energies)


df_gs = pd.read_csv('gs_vertical.csv', sep='\s* \s*', engine='python')	# \s*,\s* gets rid of empty spaces in column names
df_triplet = pd.read_csv('triplet_adiabatic.csv', sep='\s* \s*', engine='python')	# \s*,\s* gets rid of empty spaces in column names
df_singlet = pd.read_csv('singlet_adiabatic.csv', sep='\s* \s*', engine='python')	# \s*,\s* gets rid of empty spaces in column names

print((df_triplet['total'] - df_gs['total'])*toev)
print((df_singlet['total'] - df_gs['total'])*toev)

