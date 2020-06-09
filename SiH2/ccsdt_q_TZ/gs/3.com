***,SiH2
memory,8,g
gthresh,twoint=1.0E-13

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

angstrom
geometry={
 Si         
 H1     Si     1.51402
 H2     Si     1.51402      H1     91.9830 
}

{rhf
wf,6,1,0   ! nelec,symm,spin 
}

!NOTE: Perturbative MRCC works only with UHF reference. So, here we will trick MRCC by doing zero UHF iteration right after ROHF.
{uhf
wf,6,1,0   ! nelec,symm,spin 
maxit,0
}
scf = energy

pop;

_CC_NORM_MAX=2.0
{mrcc,method=CCSDT(Q)
orbital,ignore_error=1  !Ignore the fact that UHF WF is not converged
maxit,100
core
}
ccsd = energy

table,scf,ccsd
save, 3.csv, new

