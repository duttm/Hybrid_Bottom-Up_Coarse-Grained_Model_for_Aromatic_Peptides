#!/bin/bash

# Run force matching on Bridges2 in Fall 2022.

#SBATCH --mail-user=mh1314@scarletmail.rutgers.edu
#SBATCH --mail-type=ALL
#SBATCH --job-name=AMDAMD
#SBATCH --partition RM-shared
#SBATCH -N 1 --ntasks-per-node=16
#SBATCH --time=04:00:00
#SBATCH --output=slurm.%N.%j.out
#SBATCH --export=ALL

module load gromacs/2018

#equilibration time in Gromacs units (ps)
equi=399999
echo equi = $equi

echo "Running force matching"
csg_fmatch -v --top topol_fm.tpr --trj traj.trr --options settings_FM_AMD-AMD.xml --cg "second_cg.xml;water.xml"
csg_call table integrate AMD-AMD.force AMD-AMD.pot
csg_call table linearop AMD-AMD.pot AMD-AMD.pot -1 0
cp AMD-AMD.pot input_AMD-AMD.pot
csg_call --ia-type non-bonded --ia-name AMD-AMD --options settings_FM_AMD-AMD.xml convert_potential gromacs --clean input_AMD-AMD.pot table_AMD-AMD.xvg

