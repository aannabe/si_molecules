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
kcalMoltoev = 0.0433641153087705
cmtoev = 0.00012398425731484318
cmtoHa = 0.0000045563352812122295
pd.options.display.float_format = "{:,.5f}".format

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
    #if "nan" in y:
    #    y = ' '
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

#def rm_errors(df_row):
#    ### df_row is something like df.loc['some_index']
#    ### Usage : df.loc['some_index'] = rm_errors(df.loc['some_index'])
#    row_values = df_row.values
#    new_values = []
#    for i in row_values:
#        new_values.append(re.sub(r'\(.\)', '', i))
#    #energy_gaps.loc['CIPSI'] = rm_errors(energy_gaps.loc['CIPSI'])
#    return new_values

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
	if 'Exp' in list(energy.index):
		energy.loc['Exp'] = energy.loc['Exp']*cmtoHa
	energy_gaps = energy.sub(energy['GS'], axis=0)*toev
	energy_gaps = pd_f2s(energy_gaps)
	energy = pd_f2s(energy)
	if 'CIPSI' in list(energy_gaps.index):
		energy_gaps.loc['CIPSI'] = energy_gaps.loc['CIPSI'].str.replace('\(.\)', ' ', regex=True)
		energy.loc['CIPSI'] = energy.loc['CIPSI'].str.replace('\(.\)', ' ', regex=True)
	if 'CISD/RHF' in list(energy_gaps.index):
		energy_gaps.loc['CISD/RHF'] = energy_gaps.loc['CISD/RHF'].str.replace('\(.\)', ' ', regex=True)
		energy.loc['CISD/RHF'] = energy.loc['CISD/RHF'].str.replace('\(.\)', ' ', regex=True)
	if 'CISDT/RHF' in list(energy_gaps.index):
		energy_gaps.loc['CISDT/RHF'] = energy_gaps.loc['CISDT/RHF'].str.replace('\(.\)', ' ', regex=True)
		energy.loc['CISDT/RHF'] = energy.loc['CISDT/RHF'].str.replace('\(.\)', ' ', regex=True)
	if 'CIPSI/N' in list(energy_gaps.index):
		energy_gaps.loc['CIPSI/N'] = energy_gaps.loc['CIPSI/N'].str.replace('\(.\)', ' ', regex=True)
		energy.loc['CIPSI/N'] = energy.loc['CIPSI/N'].str.replace('\(.\)', ' ', regex=True)
	if 'CISD/MR' in list(energy_gaps.index):
		energy_gaps.loc['CISD/MR'] = energy_gaps.loc['CISD/MR'].str.replace('\(.\)', ' ', regex=True)
		energy.loc['CISD/MR'] = energy.loc['CISD/MR'].str.replace('\(.\)', ' ', regex=True)

	#print(energy_gaps.to_latex())
	#final = final + ' & ' + energy_gaps
	final = pd.DataFrame()
	for i in range(0,len(list(energy.columns))):
		final[str(i)] = energy.iloc[:,i]
		final[str(i)+'gap'] = energy_gaps.iloc[:,i]
	final = final.fillna(' ')
	final = final.replace('0.0(0)', '0.0', regex=False)
	final = final.replace('nan.*', ' ', regex=True)
	del final['0gap']
	#print(energy_gaps.to_latex())
	print(final.to_latex(escape=False))

h_scf = s2f('-0.49999965(1)')
si_rccsd_t = s2f('-0.088641(52)') + s2f('-3.6724778(1)')
si_ccsdt_q = s2f('-0.089575(57)') + s2f('-3.6724778(1)')
si_dmc = s2f('-3.7601(1)')
print('Si ccsd(t):',  f2s(si_rccsd_t))
print('Si ccsdt(q):', f2s(si_ccsdt_q))

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
binding['De'] = -(energy['GS'] - atoms['Si'] - 2*atoms['H'])*toev
#binding['D0'] = binding['De'] - 0.0114
binding = pd_f2s(binding)
print(binding)

print('\nSiH4:')
energy = pd.read_csv('SiH4.csv', delim_whitespace=True, index_col=False, engine='python') #sep='\s*&\s*',
energy = energy.set_index('Method')
energy = pd_s2f(energy)
#print(energy)
binding = pd.DataFrame(index = energy.index)
binding['De'] = -(energy['GS'] - atoms['Si'] - 4*atoms['H'])*toev
#binding['D0'] = binding['De'] - 0.0306
binding = pd_f2s(binding)
print(binding)

print('\nSi2H6:')
energy = pd.read_csv('Si2H6.csv', delim_whitespace=True, index_col=False, engine='python') #sep='\s*&\s*',
energy = energy.set_index('Method')
energy = pd_s2f(energy)
#print(energy)
binding = pd.DataFrame(index = energy.index)
binding['De'] = -(energy['GS'] - 2*atoms['Si'] - 6*atoms['H'])*toev
#binding['D0'] = binding['De'] - 0.0479
binding = pd_f2s(binding)
print(binding)


print('\nExperiments:')
energy = pd.read_csv('bind_exp.csv', delim_whitespace=True, index_col=False, engine='python') #sep='\s*&\s*',
energy = energy.set_index('Expt')
#print(energy)
energy = pd_s2f(energy)
energy.loc['Expmin'] = energy.loc['Expmin'] + energy.loc['ZPE']
energy.loc['Expmax'] = energy.loc['Expmax'] + energy.loc['ZPE']
#energy = energy.drop('ZPE')
#print(energy)
energy = energy * kcalMoltoev
energy = pd_f2s(energy)
print(energy)



print("\nFN ANALYSIS:")

fn_df = pd.read_csv('fn_analysis.csv', delim_whitespace=True, index_col=False, engine='python') #sep='\s*&\s*',
fn_df = pd_s2f(fn_df)

fn_df['corr'] = fn_df['CC'] - fn_df['SCF']
fn_df['error'] = fn_df['CC'] - fn_df['DMC']
fn_df['eta'] = (fn_df['error']/fn_df['corr'])*100.0
fn_df['eta2'] = (-fn_df['error']/fn_df['Ne'])*toev
fn_df['error'] = -fn_df['error']*toev

del fn_df['CC']
del fn_df['Ne']

error = np.array(fn_df['error'].values)
eta = np.array(fn_df['eta'].values)
eta2 = np.array(fn_df['eta2'].values)
print('FN error MAD [eV]:', f2s(np.mean(error)))
print('FN/corr MAD [perc.]:', f2s(np.mean(eta)))
print('FN/Nelec MAD [ev]:', f2s(np.mean(eta2)))

gs_mad = fn_df[fn_df['State']=='GS']
print(gs_mad)
gs_mad = np.array(gs_mad.loc[:,'error':'eta2'].values)
fn_df.loc['gs_mad','error'] = np.mean(gs_mad, axis=0)[0]
fn_df.loc['gs_mad','eta']   = np.mean(gs_mad, axis=0)[1]
fn_df.loc['gs_mad','eta2']  = np.mean(gs_mad, axis=0)[2]

ex_mad = fn_df[fn_df['State']=='EX']
print(ex_mad)
ex_mad = np.array(ex_mad.loc[:,'error':'eta2'].values)
fn_df.loc['ex_mad','error'] = np.mean(ex_mad, axis=0)[0]
fn_df.loc['ex_mad','eta']   = np.mean(ex_mad, axis=0)[1]
fn_df.loc['ex_mad','eta2']  = np.mean(ex_mad, axis=0)[2]


fn_df = pd_f2s(fn_df)
del fn_df['State']
del fn_df['Spin']
fn_df = fn_df.replace(np.nan, ' ', regex=True)
fn_df = fn_df.replace(np.nan, ' ', regex=True)
print(fn_df.to_latex(escape=False))

### All below are per atom
print('\nSi CRYSTAL NUMBERS: \n')
pbe0_dmc = s2f('-3.932200(22)')
hf_espress = s2f('-3.78878403(1)')
atom_fci = s2f('-3.762073(57)')
#corr_atom = pbe0_dmc-hf_espress
coh_exp = s2f('4.680(1)')/toev   # Exp: 4.68(8)
coh_dmc = -(pbe0_dmc-atom_fci)
corr_atom = (atom_fci-coh_exp)-hf_espress  # True estimated correlation
fn_err_atom = coh_exp-coh_dmc

print('Si crystal corr/atom [Ha]:', f2s(corr_atom))
print('Si crystal coh [eV]:', f2s(coh_dmc*toev))
print('Si crystal FN error/atom [eV]: ', f2s(fn_err_atom*toev))
print('Si crystal FN error/corr per atom [perc.]: ', f2s(-fn_err_atom/corr_atom*100.0))
print('Si crystal FN error/Ne per atom [eV]: ', f2s(fn_err_atom*toev/4.0))

