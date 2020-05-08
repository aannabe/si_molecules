#!/bin/bash -l
#SBATCH -J disilane_5
#SBATCH -q regular
#SBATCH -N 1
#SBATCH -C haswell
#SBATCH -t 03:00:00
#!SBATCH -o test_silane.o%j
#SBATCH -o job.out

module load molpro
#molpro -s -n 1 2.com
#molpro -s -n 1 3.com
#molpro -s -n 4 4.com
molpro -s -n 8 5.com
#molpro -s -n 8 6.com
