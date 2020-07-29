***,SiH4
memory,1,g
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
  5
 Silane
 Si          0.0000        0.0000        0.0000
  H          0.8544        0.8544        0.8544
  H         -0.8544       -0.8544        0.8544
  H         -0.8544        0.8544       -0.8544
  H          0.8544       -0.8544       -0.8544
}

{rhf
wf,8,1,0   ! nelec,symm,spin 
}
scf = energy
!1   1   1   1

pop;

{multi
occ,2,2,2,2;
closed,0,0,0,0;
wf,8,1,0
STATE,2,root;
natorb;
}

{ci
STATE,2,root;
}

ccsd = energy

table,scf,ccsd
save, 5.csv, new
