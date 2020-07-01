***,SiH4
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

include,Si.aug-cc-pV6Z.basis

ECP,H,0,1,0
3;
2,   21.77696655044365 ,     -10.85192405303825 ; 
1,   21.24359508259891 ,       1.00000000000000;
3,   21.24359508259891 ,      21.24359508259891;
1; 2,                   1.,                      0.;

include,H.aug-cc-pV6Z.basis
}

geometry={
  5
 Silane
 Si          0.0000        0.0000        0.0000
  H          0.8544        0.8544        0.8544
  H         -0.8544       -0.8544        0.8544
  H         -0.8544        0.8544       -0.8544
  H          0.8544       -0.8544       -0.8544
}

! HARTREE-FOCK
{RHF
   wf,8,1,0   ! nelec,symm,spin 
}
scf=energy
pop;

!NOTE: Perturbative MRCC works only with UHF reference. So, here we will trick MRCC by doing zero UHF iteration right after ROHF.
{uhf
wf,8,1,0
maxit,0
}
scf=energy
pop;


{mrcc,method=CISDTQ
orbital,ignore_error=1  !Ignore the fact that UHF WF is not converged
maxit,100
core
}
posthf=energy

table,scf,posthf
save
type,csv

