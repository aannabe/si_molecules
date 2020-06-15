#!/usr/bin/env python3

import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import uncertainties
from uncertainties import ufloat
from uncertainties import unumpy
from uncertainties import ufloat_fromstr
from scipy.optimize import curve_fit
import re
import string

toev = 27.211386245988
pd.options.display.float_format = "{:,.6f}".format

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

def f2s(x):   # float to string
    try:
        y = frmtr.format("{0:.1u}", x)
    except:
        y = x
    if "nan" in y:
        y = ' '
    return y

def s2f(x):   # string to float
    try:
        y = ufloat_fromstr(x)
    except:
        y = x
    return y

def pd_s2f(df):   # df to df with uncertainties
    udf = df.copy()
    for column in df.columns:
        try:
            udf[column] = list(map(s2f,list(df[column])))
        except:
            udf[column] = "pd_s2f failed"
    return udf

def pd_f2s(udf):   # df to df with uncertainties
    df = udf.copy()
    for column in udf.columns:
        try:
            df[column] = list(map(f2s,list(udf[column])))
        except:
            df[column] = "pd_f2s failed"
    return df

def rm_errors(df_row):
    ### df_row is something like df.loc['some_index']
    ### Usage : df.loc['some_index'] = rm_errors(df.loc['some_index'])
    row_values = df_row.values
    new_values = []
    for i in row_values:
        new_values.append(re.sub(r'\(.\)', '', i))
    return new_values

def size_linear(x, a, b):
        y = a + b*x
        return y

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

files = ['SiH2.csv','SiH4.csv','Si2H6.csv',]

for i in files:
	print('\n', i)
	energy = pd.read_csv(i, delim_whitespace=True, index_col=False, engine='python') #sep='\s*&\s*',
	energy = energy.set_index('Method')
	energy = pd_s2f(energy)
	energy_gaps = energy.sub(energy['GS'], axis=0)*toev
	energy_gaps['GS'] = energy['GS']
	energy_gaps = pd_f2s(energy_gaps)
	if 'CIPSI' in list(energy_gaps.index):
		energy_gaps.loc['CIPSI'] = rm_errors(energy_gaps.loc['CIPSI'])
	print(energy_gaps.to_latex())

#h_scf = s2f('-0.49999965(1)')
#si_rccsd_t = s2f('-0.088641(52)') + s2f('-3.6724778(1)')
#si_ccsdt_q = s2f('-0.089575(57)') + s2f('-3.6724778(1)')
#si_dmc = s2f('-3.7601(1)')
#print(f2s(si_rccsd_t))
#print(f2s(si_ccsdt_q))

print("\nBINDING ENERGIES:")

atoms = pd.read_csv('atoms.csv', delim_whitespace=True, index_col=False, engine='python') #sep='\s*&\s*',
atoms = atoms.set_index('Method')
atoms = pd_s2f(atoms)
#print(atoms)

print('\nSiH2:')
energy = pd.read_csv('SiH2.csv', delim_whitespace=True, index_col=False, engine='python') #sep='\s*&\s*',
energy = energy.set_index('Method')
energy = pd_s2f(energy)
energy = energy.drop(index='CIPSI')
#print(energy)
binding = pd.DataFrame(index = energy.index)
binding['De'] = -(energy['GS'] - atoms['Si'] - 2*atoms['H'])
binding['D0'] = binding['De'] - 0.0114
binding = pd_f2s(binding)
print(binding)

print('\nSiH4:')
energy = pd.read_csv('SiH4.csv', delim_whitespace=True, index_col=False, engine='python') #sep='\s*&\s*',
energy = energy.set_index('Method')
energy = pd_s2f(energy)
#print(energy)
binding = pd.DataFrame(index = energy.index)
binding['De'] = -(energy['GS'] - atoms['Si'] - 4*atoms['H'])
binding['D0'] = binding['De'] - 0.0306
binding = pd_f2s(binding)
print(binding)

print('\nSi2H6:')
energy = pd.read_csv('Si2H6.csv', delim_whitespace=True, index_col=False, engine='python') #sep='\s*&\s*',
energy = energy.set_index('Method')
energy = pd_s2f(energy)
#print(energy)
binding = pd.DataFrame(index = energy.index)
binding['De'] = -(energy['GS'] - 2*atoms['Si'] - 6*atoms['H'])
binding['D0'] = binding['De'] - 0.0479
binding = pd_f2s(binding)
print(binding)







