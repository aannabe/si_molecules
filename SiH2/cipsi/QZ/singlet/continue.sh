#!/usr/bin/env bash

#conda activate nexus2
source /home/gani/codes/quantum_package/quantum_package.rc
export OMP_NUM_THREADS=8
filename='SiH2'

#qp_create_ezfio_from_xyz -b "aug-cc-pvqz_ecp_ncsu" -p "ncsu" -m 1 ${filename}.xyz
#qp_run SCF ${filename}.ezfio &> ${filename}.scf &
#wait
#echo "SCF finished!"
#
#echo '2' > ${filename}.ezfio/determinants/n_states
##echo '64' > ${filename}.ezfio/davidson/n_states_diag
#
#### Get Natural Orbitals v0
#echo '3000' > ${filename}.ezfio/determinants/n_det_max
#qp_run fci_zmq ${filename}.ezfio &> ${filename}.zmq_0 &
#wait
#echo "ZMQ_0 finished!"
#qp_run save_natorb ${filename}.ezfio
#
#### Get Natural Orbitals v1
#echo '6000' > ${filename}.ezfio/determinants/n_det_max
#qp_run fci_zmq ${filename}.ezfio &> ${filename}.zmq_1 &
#wait
#echo "ZMQ_1 finished!"
#qp_run save_natorb ${filename}.ezfio

### Get Symmetry
qp_run cis ${filename}.ezfio &> ${filename}.cis &
echo 'T' > ${filename}.ezfio/determinants/read_wf
wait
echo "CIS finished!"

#### Run CIPSI
echo '500000' > ${filename}.ezfio/determinants/n_det_max
qp_run fci_zmq ${filename}.ezfio &> ${filename}.zmq_2 &
wait
echo "ZMQ_2 finished!"

