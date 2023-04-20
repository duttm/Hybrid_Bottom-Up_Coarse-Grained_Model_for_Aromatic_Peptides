#!/bin/bash

#SBATCH --mail-user=mh1314@scarletmail.rutgers.edu
#SBATCH --mail-type=ALL
#SBATCH --job-name=ibi
#SBATCH --partition RM-shared
#SBATCH -N 1 --ntasks-per-node=1
#SBATCH --time=24:00:00
#SBATCH --output=slurm.%N.%j.out
#SBATCH --export=ALL

#GMX_APP=/ocean/projects/dmr170002p/hooten/dmref/gmx21_5.sif

module purdge
module load gromacs/2018

echo 'running csg_inverse --options "settings.xml"'
# csg_inverse --debug --options settings.xml
csg_inverse --options settings_angles.xml


