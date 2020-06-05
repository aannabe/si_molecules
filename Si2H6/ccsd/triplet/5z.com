***,Si2H6
memory,2000,m
gthresh,twoint=1.0E-13
symmetry,nosym

basis={
ECP,Si,10,2,0;
3;  !Vd
1,5.168316,    4.000000
3,8.861690,   20.673264
2,3.933474,  -14.818174
2;  !Vs-Vd
2,9.447023,   14.832760
2,2.553812,   26.349664
2;  !Vp-Vd
2,3.660001,    7.621400
2,1.903653,   10.331583

include,Si.aug-cc-pV5Z.basis

ECP,H,0,1,0
3;
2,   21.77696655044365 ,     -10.85192405303825 ; 
1,   21.24359508259891 ,       1.00000000000000;
3,   21.24359508259891 ,      21.24359508259891;
1; 2,                   1.,                      0.;

include,H.aug-cc-pV5Z.basis
}

geometry={
8 
Si2H6
Si   0.0000   0.0000   1.1600
Si   0.0000   0.0000  -1.1600
H    0.0000   1.3865   1.6483
H   -1.2008  -0.6933   1.6483
H    1.2008  -0.6933   1.6483
H    0.0000  -1.3865  -1.6483
H   -1.2008   0.6933  -1.6483
H    1.2008   0.6933  -1.6483
}

{rks,pbe0
wf,14,2,2
orbital,2102.2
}
dften = energy

! HARTREE-FOCK
{RHF
start,2102.2
wf,14,2,2   ! nelec,symm,spin 
}
scf = energy
pop;

{rccsd(t);maxit,100;core}
ccsd = energy

table, scf, ccsd
save
type,csv

