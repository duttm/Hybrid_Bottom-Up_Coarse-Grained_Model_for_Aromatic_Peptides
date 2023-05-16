#!/bin/bash

#SBATCH --mail-user=mh1314@scarletmail.rutgers.edu
#SBATCH --mail-type=ALL
#SBATCH --job-name=BRIDGES2_IBI_angles
#SBATCH --partition RM-shared
#SBATCH -N 1 --ntasks-per-node=4
#SBATCH --time=12:00:00
#SBATCH --output=slurm.%N.%j.out
#SBATCH --export=ALL

module load gromacs/2018

echo "start $(date)"

csg_inverse --options settings.xml

echo "stop $(date)"


