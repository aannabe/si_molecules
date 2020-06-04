#!/bin/bash
#SBATCH -J LDA_EX
#!SBATCH -q low
#SBATCH -q debug
#SBATCH -C knl 
#SBATCH -N 8
#SBATCH -n 512                # total number of mpi tasks requested
#!SBATCH --time=02:00:00
#SBATCH --time=00:30:00      #the max walltime allowed for flex QOS jobs
#!SBATCH --time-min=2:00:00   #the minimum amount of time the job should run

### ~~~~~ Input ~~~~~~~~~

solid='qwalk'
nconfig=1                       # Walkers per core
dmc_timestep="0.0025"          # DMC timestep
dmc_blocks=400                  # DMC blocks

compile='-cori'
runner=srun                    # mpirun vs ibrun
#cores=$SLURM_NTASKS             # Total number of cores
cores=512

###~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#module load python/2.7-anaconda-2019.07; source activate nexus2;


#mkdir ex
#cd ex
#cp ../pyscf2qwalk.py .
#cp ../scf.chkfile .
#cp ../qwalk.dmc .
#gen_qw qwalk $nconfig $dmc_blocks
#python pyscf2qwalk.py scf.chkfile qwalk
##run_qw_opt qwalk $cores $compile $runner
##con_qw_lin qwalk $cores $compile $runner
##con_qw_lin qwalk 544 $compile $runner
##run_qw_dmc qwalk $cores $compile $runner $dmc_blocks $dmc_timestep
##srun -n 2176 -c 1 --cpu_bind=threads qwalk-cori qwalk.dmc > DMC.log
##analyze_qw_dmc qwalk.dmc.log $compile $dmc_timestep
#cd ../

cd ex
#run_qw_opt_jast3 qwalk $cores $compile $runner
#con_qw_lin qwalk 544 $compile $runner
#echo "OPT ENDED"
srun -n 2176 -c 1 --cpu_bind=threads qwalk-cori qwalk.dmc > DMC.log
cd ../

