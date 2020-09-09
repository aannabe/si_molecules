import sys, os
from pyscf import gto, scf, cc, dft
from pyscf.cc import uccsd_t
import numpy as np
import pandas as pd


workdir = os.path.dirname(os.path.realpath(__file__))
#basfile = os.path.join(workdir,'si_cody.basis')
si_basfile = os.path.join(workdir,'Si.aug-cc-pVQZ.nwchem')
h_basfile = os.path.join(workdir,'H.aug-cc-pVQZ.nwchem')

mol = gto.Mole()
mol.atom = '''
Si;
H,  1,  1.51402;
H,  1,  1.51402,  2,   91.9830;
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


mol.build()
m = scf.RHF(mol)
#m = dft.RKS(mol)
#m.xc = 'PBE'
m.max_cycle = 150
m.chkfile='sih2.chkfile'
m.kernel()
#print ('E(HF)= %g' % m.kernel())
