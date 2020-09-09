#!/bin/bash -l
#SBATCH -J Si2H6_dz
#SBATCH -q regular
#SBATCH -N 1
#SBATCH -C haswell
#SBATCH -t 03:00:00
#!SBATCH -o test_silane.o%j
#SBATCH -o dz.out

module load molpro

molpro -s -n 16 2.com
#molpro -s -n 32 3.com
#molpro -s -n 32 4.com
#molpro -s -n 32 5.com
#molpro -s -n 32 6.com
