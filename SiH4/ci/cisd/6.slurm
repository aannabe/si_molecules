#!/bin/bash -l
#SBATCH -J cisd_5
#SBATCH -q regular
#SBATCH -N 1
#!SBATCH -n 16
#SBATCH -C haswell
#SBATCH -t 47:59:59
#!SBATCH -o test_silane.o%j
#SBATCH -o job.out

module load molpro
#molpro -s -n 1 2.com
#molpro -s -n 1 3.com
#molpro -s -n 1 4.com
#molpro -s -n 1 5.com
molpro -s -n 1 6.com
