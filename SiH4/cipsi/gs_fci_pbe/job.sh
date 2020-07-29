#!/usr/bin/env bash

#conda activate nexus2
source /home/gani/codes/qp2/quantum_package.rc
export OMP_NUM_THREADS=8
filename='SiH4'

###qp_create_ezfio -b "aug-cc-pvqz_ecp_ncsu" -p "ncsu" -m 1 ${filename}.xyz
###echo '0.00' > ${filename}.ezfio/dft_keywords/hf_exchange
###echo 'pbe' > ${filename}.ezfio/dft_keywords/exchange_functional
###echo 'pbe' > ${filename}.ezfio/dft_keywords/correlation_functional
####echo '20' > ${filename}.ezfio/scf_utils/max_dim_diis
####echo '0.1' > ${filename}.ezfio/scf_utils/level_shift
###qp_run ks_scf ${filename}.ezfio &> ${filename}.scf &
#####qp_run scf ${filename}.ezfio &> ${filename}.scf &
###wait
###echo "SCF finished!"

#qp_convert_output_to_ezfio ${filename}.out -o ${filename}.ezfio > convert.out

echo '200000' > ${filename}.ezfio/determinants/n_det_max
echo '2' > ${filename}.ezfio/determinants/n_states
##echo '64' > ${filename}.ezfio/davidson/n_states_diag

##### Run CIPSI
qp_run fci ${filename}.ezfio &> ${filename}.fci &
#echo 'T' > ${filename}.ezfio/determinants/read_wf
wait
echo "FCI finished!"

#echo '1e-20' > ${filename}.ezfio/qmcpack/ci_threshold
#qp_run truncate_wf_spin ${filename}.ezfio &> ${filename}.trunc
#QP_STATE=2 qp_run save_for_qmcpack ${filename}.ezfio > ${filename}.dump
#
#mv ${filename}.dump qmc.dump
#mv QP2QMCACK.h5 qmc.h5

