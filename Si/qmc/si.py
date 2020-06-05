import sys, os
from pyscf import gto, scf, cc, dft
from pyscf.cc import uccsd_t
import numpy as np
import pandas as pd


workdir = os.path.dirname(os.path.realpath(__file__))
#basfile = os.path.join(workdir,'si_cody.basis')
basfile = os.path.join(workdir,'cc-pv5z.basis')

mol = gto.Mole()
mol.atom = 'Si 0 0 0'
mol.basis = {'Si': gto.load(basfile,'Si')}
mol.verbose = 3
mol.spin = 2
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
''')}

mol.build()
#m = scf.ROHF(mol)
m = dft.UKS(mol)
m.xc = 'PBE'
m.max_cycle = 150
print ('E(HF)= %g' % m.kernel())
