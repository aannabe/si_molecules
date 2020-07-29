#!/usr/bin/env python

import sys, os
from pyscf import gto, scf, cc, dft
from pyscf.cc import uccsd_t
import numpy as np
import pandas as pd

workdir = os.path.dirname(os.path.realpath(__file__))
si_basfile = os.path.join(workdir,'Si.aug-cc-pVDZ.basis')
h_basfile = os.path.join(workdir,'H.aug-cc-pVDZ.basis')

mol = gto.Mole()
mol.atom = '''
Si 0.0000  0.0000  0.0000; 
H  0.8544  0.8544  0.8544; 
H -0.8544 -0.8544  0.8544; 
H -0.8544  0.8544 -0.8544; 
H  0.8544 -0.8544 -0.8544;
'''
mol.basis = {'Si': gto.load(si_basfile,'Si'), 'H': gto.load(h_basfile,'H')}
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

#hf = scf.ROHF(mol)
hf = dft.RKS(mol)
hf.xc = 'pbe0'
hf.max_cycle = 50
hf.verbose=4
#hf.level_shift = 1.0
#hf.diis_space = 60
#dm=hf.init_guess_by_chkfile('guess/scf.chkfile')
hf.chkfile='scf.chkfile'

#en=hf.kernel(dm)
en=hf.kernel()
hf.analyze()

kpts=[]
title="qmc"
from PyscfToQmcpack import savetoqmcpack
savetoqmcpack(mol,hf,title=title,kpts=kpts)

