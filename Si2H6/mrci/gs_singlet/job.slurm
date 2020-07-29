#!/bin/bash -l
#SBATCH -J Si2H6_gs
#SBATCH -q regular
#SBATCH -N 1
#SBATCH -C haswell
#SBATCH -t 48:00:00
#!SBATCH -o test_silane.o%j
#SBATCH -o job.out

module load molpro

#molpro -s -n 4 2.com
#molpro -s -n 4 3.com
#molpro -s -n 4 4.com
molpro -s -n 16 5.com
#molpro -s -n 1 6.com
