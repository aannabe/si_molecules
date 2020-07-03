***,Si2H6
memory,4,g
gthresh,twoint=1.0E-12

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

include,Si.aug-cc-pVTZ.basis

ECP,H,0,1,0
3;
2,   21.77696655044365 ,     -10.85192405303825 ; 
1,   21.24359508259891 ,       1.00000000000000;
3,   21.24359508259891 ,      21.24359508259891;
1; 2,                   1.,                      0.;

include,H.aug-cc-pVTZ.basis
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

! PBE0
{rks,pbe0
wf,14,2,2
orbital,2102.2
}
dften = energy

! HARTREE-FOCK
{RHF
wf,14,2,2   ! nelec,symm,spin 
}
scf = energy
pop;

{mrcc,method=CISD;
maxit,100;core}
posthf1 = energy

table, scf, posthf1
save
type,csv
