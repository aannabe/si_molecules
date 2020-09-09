#!/bin/bash -l
#SBATCH -J SiH4_tz
#SBATCH -q debug
#SBATCH -N 1
#SBATCH -C haswell
#SBATCH -t 00:10:00
#!SBATCH -o test_silane.o%j
#SBATCH -o tz.out

module load molpro

#molpro -s -n 32 2.com
molpro -s -n 16 3.com
#molpro -s -n 32 4.com
#molpro -s -n 32 5.com
#molpro -s -n 32 6.com

