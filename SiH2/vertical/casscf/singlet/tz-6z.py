import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import os,sys
import pandas as pd

ai = 1.0
bi = 1.0
toev = 27.211386

pd.options.display.float_format = '{:.6f}'.format

def scf_fit(x,*parms):
        return parms[0] + parms[1]*np.exp(-parms[2]*x)

#def corr_fit(x,*parms):
#        return parms[0]+parms[1]/(x+3./8.)**3 + parms[2]/(x+3./8.)**5
def corr_fit(x,a,b,c):
        return a+b/(x+3./8.)**3 + c/(x+3./8.)**5


df=pd.DataFrame()

n = [3,4,5,6]
for basis in ['tz','qz','5z','6z']:
#n = [3,4,5]
#for basis in ['tz','qz','5z']:
	x = pd.read_csv('./'+basis+'.table1.txt',skip_blank_lines=True,skipinitialspace=True)
	df[basis+'_scf'] = x['SCF']

scf = df.filter(regex='scf')


scf_extrap = []
corr_extrap=[]
for i in df.index:
	y1 = scf.iloc[i, :].values
	#print(ycorr)
	if y1[-1] < y1[-2]:
		initial = [2*y1[-1]-y1[-2], ai, bi]
		limit = ([2*y1[-1]-y1[0]-0.2, 0, 0], [y1[-1], 100, 100])
		popt1, pcov1 = curve_fit(scf_fit, n, y1, p0=initial, bounds=limit) 
		scf_extrap.append(popt1[0])
	else:
		scf_extrap.append(min(y1[:]))

print(popt1, pcov1)

print(popt1[0], '+/-', pcov1[0][0]**0.5)

scf['extrap'] = scf_extrap

#print(scf)
#print(cc)

##Extrapolation is done here. I am doing formating for the SCF Table, namely hf and Correlation Table, namely corr

hf = pd.DataFrame()

hf['T'] = scf['tz_scf']
hf['Q'] = scf['qz_scf']
hf['5'] = scf['5z_scf']
hf['6'] = scf['6z_scf']
hf['Extrap.'] = scf['extrap']


print(hf.to_latex(index=False))
#corr['extrap'] = corr_extrap
