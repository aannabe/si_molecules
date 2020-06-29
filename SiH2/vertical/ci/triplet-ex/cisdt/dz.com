***,SiH4
memory,8,g
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

include,Si.aug-cc-pVDZ.basis

ECP,H,0,1,0
3;
2,   21.77696655044365 ,     -10.85192405303825 ; 
1,   21.24359508259891 ,       1.00000000000000;
3,   21.24359508259891 ,      21.24359508259891;
1; 2,                   1.,                      0.;

include,H.aug-cc-pVDZ.basis
}

angstrom
geometry={
 Si         
 H1     Si     1.51402
 H2     Si     1.51402      H1     91.9830 
}

! HARTREE-FOCK
{RHF
   wf,6,2,2   ! nelec,symm,spin 
   print,orbitals=2
}
scf = energy

!!NOTE: Perturbative MRCC works only with UHF reference. So, here we will trick MRCC by doing zero UHF iteration right after ROHF.
!{uhf
!print,orbitals=2
!wf,6,2,2
!maxit,0
!}
!scf=energy
!pop;

{mrcc,method=CISDT
orbital,ignore_error=1  !Ignore the fact that UHF WF is not converged
maxit,100
core
}
posthf1=energy

table,scf,posthf1
save
type,csv

