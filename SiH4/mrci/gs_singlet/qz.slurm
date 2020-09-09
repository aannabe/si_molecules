#!/bin/bash -l
#SBATCH -J SiH4_qz
#SBATCH -q regular
#SBATCH -N 1
#SBATCH -C haswell
#SBATCH -t 24:00:00
#!SBATCH -o test_silane.o%j
#SBATCH -o qz.out

module load molpro

#molpro -s -n 32 2.com
#molpro -s -n 32 3.com
molpro -s -n 16 4.com
#molpro -s -n 32 5.com
#molpro -s -n 32 6.com

