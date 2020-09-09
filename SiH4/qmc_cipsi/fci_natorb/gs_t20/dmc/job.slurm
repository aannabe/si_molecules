#!/bin/bash
#SBATCH -A m2113
#SBATCH -p regular
#SBATCH -C knl
#SBATCH -J gs_qmc
#SBATCH -t 17:00:00
#SBATCH -N 32
#SBATCH --tasks-per-node=68
#SBATCH --cpus-per-task=4
#SBATCH -o gs_qmc.out
#SBATCH -e gs_qmc.err
#SBATCH --export=ALL

echo $SLURM_SUBMIT_DIR
cd $SLURM_SUBMIT_DIR


export HDF5_USE_FILE_LOCKING=FALSE
#module load espresso
module unload cray-libsci
module load cray-hdf5/1.10.2.0
module load gcc
module list


export OMP_NUM_THREADS=1
srun /global/cscratch1/sd/aannabe/build_cori_knl/bin/qmcpack qmc.dump.qmc.in-wfj.xml


