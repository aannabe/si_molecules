import matplotlib
matplotlib.use('TkAgg')
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

#Fit function
def fit(x,a,b): 
     return a*x+b

timestep   = np.array([0.01, 0.005, 0.002, 0.001])
energy     = np.array([-6.27799161, -6.277774769, -6.277642797, -6.277843103])
energy_err = np.array([ 0.000168861, 0.000133437,  0.000134408,  0.000145074])

# Plot energy with error bar vs. timestep
fig = plt.figure()
plt.errorbar(timestep, energy, yerr=energy_err, fmt='*')

#Fit
popt,pcov=curve_fit(fit,timestep,energy,p0=(0.0,0.0),sigma=energy_err) 


a=popt[0]
err_a=np.sqrt(pcov[0,0])
b=popt[1]
err_b=np.sqrt(pcov[1,1])

print(popt)
print(a,err_a)
print(b,err_b)


plt.plot(timestep, fit(timestep,*popt),'r-')
#plt.plot(timestep, ,'r-')

plt.show()
