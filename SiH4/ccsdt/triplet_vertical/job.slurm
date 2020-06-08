#!/bin/bash -l
#SBATCH -J SiH4
#SBATCH -q regular
#SBATCH -N 1
#!SBATCH -n 16
#SBATCH -C haswell
#SBATCH -t 01:59:00
#!SBATCH -o test_silane.o%j
#SBATCH -o job.out

module load molpro

molpro -s -n 8 2.com
molpro -s -n 8 3.com
molpro -s -n 8 4.com
molpro -s -n 8 5.com
#molpro -s -n 1 6.com
