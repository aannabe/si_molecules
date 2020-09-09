#!/bin/bash

date

export OMP_NUM_THREADS=8
python triplet.py > triplet.out

sed -i '/^$/d' scf.out 
sed -i '/ERROR/d' scf.out 

python pyscf2qwalk.py scf.chkfile qwalk

date

