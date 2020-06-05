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

n = [2,3,4,5]
for basis in ['dz', 'tz','qz','5z']:
#n = [3,4,5]
#for basis in ['tz','qz','5z']:
	x = pd.read_csv('./'+basis+'.table1.txt',skip_blank_lines=True,skipinitialspace=True)
	df[basis+'_scf'] = x['SCF']
	df[basis+'_ccsd'] = x['CCSD']

scf = df.filter(regex='scf')
cc = df.filter(regex='ccsd')


scf_extrap = []
corr_extrap=[]
for i in df.index:
	y1 = scf.iloc[i, :].values
	y2 = cc.iloc[i, :].values
	ycorr = y2 - y1
	#print(ycorr)
	if y1[-1] < y1[-2]:
		initial = [2*y2[-1]-y2[-2], ai, bi]
		limit = ([2*y2[-1]-y2[0]-0.2, 0, 0], [y1[-1], 100, 100])
		popt1, pcov1 = curve_fit(scf_fit, n, y1, p0=initial, bounds=limit) 
		scf_extrap.append(popt1[0])
	else:
		scf_extrap.append(min(y1[:]))
	popt2, pcov2 = curve_fit(corr_fit, n, ycorr)
	corr_extrap.append(popt2[0])

print(popt1, pcov1)
print(popt2, pcov2)


print(popt1[0], '+/-', pcov1[0][0]**0.5)
print(popt2[0], '+/-', pcov2[0][0]**0.5)

scf['extrap'] = scf_extrap
cc['extrap'] = np.array(corr_extrap)+np.array(scf_extrap)


#print(scf)
#print(cc)

##Extrapolation is done here. I am doing formating for the SCF Table, namely hf and Correlation Table, namely corr

hf = pd.DataFrame()

hf['D'] = scf['dz_scf']
hf['T'] = scf['tz_scf']
hf['Q'] = scf['qz_scf']
hf['5'] = scf['5z_scf']
hf['Extrap.'] = scf['extrap']


corr = pd.DataFrame()
corr['D'] = cc['dz_ccsd']-scf['dz_scf']
corr['T'] = cc['tz_ccsd']-scf['tz_scf']
corr['Q'] = cc['qz_ccsd']-scf['qz_scf']
corr['5'] = cc['5z_ccsd']-scf['5z_scf']
corr['Extrap.'] = corr_extrap
print(hf.to_latex(index=False))
print(corr.to_latex(index=False))
print(cc.to_latex(index=False))
#corr['extrap'] = corr_extrap
