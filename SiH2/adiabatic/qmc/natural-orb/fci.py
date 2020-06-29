import sys, os
from pyscf import gto, scf, cc, dft, ci, lib, mp, fci
from pyscf.cc import uccsd_t
import numpy as np
import scipy
import pandas as pd


workdir = os.path.dirname(os.path.realpath(__file__))
#basfile = os.path.join(workdir,'si_cody.basis')
si_basfile = os.path.join(workdir,'Si.aug-cc-pVDZ.basis')
h_basfile = os.path.join(workdir,'H.cc-pVDZ.basis')

mol = gto.Mole()
mol.atom = '''
Si;
H,  1,  1.48532;
H,  1,  1.48532,  2,   122.4416;
'''

mol.basis = {'Si': gto.load(si_basfile,'Si'), 'H': gto.load(h_basfile,'H')}
mol.verbose = 3
mol.spin = 0
mol.charge = 0
mol.ecp = {'Si': gto.basis.parse_ecp('''
Si nelec 10
Si ul
1 5.168316 4.000000
3 8.861690 20.673264
2 3.933474 -14.818174
Si S
2 9.447023 14.832760
2 2.553812 26.349664
Si P
2 3.660001 7.621400
2 1.903653 10.331583
'''),
'H': gto.basis.parse_ecp('''
H nelec 0
H ul
1 21.24359508259891 1.00000000000000
3 21.24359508259891 21.24359508259891
2 21.77696655044365 -10.85192405303825
H S
2 1.000000000000000 0.00000000000000
''')}

#mol.irrep_nelec = {'A1': (2,1), 'B1': (0,1), 'B2': (1,1), 'A2': (0,0)}
mol.build()



###### RHF -> CISD ######
#m = scf.RHF(mol)
##m = dft.RKS(mol)
##m.xc = 'PBE'
#m.max_cycle = 150
#m.chkfile='sih2.chkfile'
#hf_en = m.kernel()
#mycc = m.CISD()
#ci_en = mycc.kernel()
#print('\n\n\nCalculation Done:\n')
#print('With tz basis, CISD calculation')
#print('E(SCF) = %.14f' % hf_en)
#print('E(CISD corr) = %.14f' % ci_en[0])
#print('CISD total energy:', ci_en[0] + hf_en)



m = scf.RHF(mol)
#m = dft.RKS(mol)
#m.xc = 'PBE'
m.max_cycle = 150
m.chkfile='ini_hf.chkfile'
scf_en = m.kernel()

#mf_hf = scf.RHF(mol)
#mf_hf.__dict__.update(m.__dict__)
#mf_hf.max_cycle = 0
#
#hf_en = mf_hf.kernel()


mycc = fci.FCI(mol,m.mo_coeff)
#mycc = mp.MP2(m)
ci_en, fcivec = mycc.kernel()
#print('\n\n\nCalculation Done:\n')
#print('With tz basis, CISD calculation')
#print('E(PBE) = %.14f' % scf_en)
#print('E(HF) = %.14f' % hf_en)
#print('E(CISD corr) = %.14f' % ci_en[0])
#print('CISD total energy:', ci_en[0] + hf_en)

norb = m.mo_coeff.shape[1]
rdm1 = mycc.make_rdm1(fcivec,norb,(3,3))
occ, no = scipy.linalg.eigh(rdm1)

occ = occ[::-1]
on = no[:, ::-1]


final_hf = scf.RHF(mol)
final_hf.chkfile = 'fci.chkfile'
final_hf.max_cycle = 0 
final_hf.occ = occ
final_hf.mo_coeff = no
final_en = final_hf.kernel()
scf.chkfile.dump_scf(mol,'fci.chkfile',m.e_tot, m.mo_energy, m.mo_coeff.dot(on), m.mo_occ)


print('\n\n\nCalculation Done:\n')
print('With tz basis, CISD calculation')
print('E(PBE) = %.14f' % scf_en)
#print('E(HF) = %.14f' % hf_en)
print('E(CISD corr) = %.14f' % ci_en)
print('CISD total energy:', ci_en + scf_en)


print(m.mo_coeff)
#print(mycc.mo_coeff)
print(occ)
print(np.sum(occ))
print(no)
print(m.mo_coeff.dot(no))
print(on)
print(m.mo_coeff.dot(on))
print(m.mo_coeff.dot(on)[:,0])

print(final_hf.mo_coeff)

print('Check my scf.chkfile orbital')
scf_mo_coeff = lib.chkfile.load('fci.chkfile', 'scf/mo_coeff')
print(scf_mo_coeff)


#mf_hf.mo_coeff = no
#mycc.mo_coeff = no


#final_ci = mf_hf.CISD()
#print(final_ci.kernel())

