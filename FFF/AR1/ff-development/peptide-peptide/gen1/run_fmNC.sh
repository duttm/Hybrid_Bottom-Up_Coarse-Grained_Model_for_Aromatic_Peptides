#!/bin/bash

# Run force matching on Bridges2 in Fall 2021. 

#SBATCH --mail-user=mh1314@scarletmail.rutgers.edu
#SBATCH --mail-type=ALL
#SBATCH --job-name=bridges_fm_NC
#SBATCH --partition RM-shared
#SBATCH -N 1 --ntasks-per-node=32
#SBATCH --time=02:00:00
#SBATCH --output=slurm.%N.%j.out
#SBATCH --export=ALL

module load gromacs/2018

AA_DIR=../..
CG_DIR=..

#equilibration time in Gromacs units (ps)
equi=399999
echo equi = $equi

echo "Running force matching"
csg_fmatch -v --top topol_fm.tpr --trj traj.trr --begin $equi --options settings_NC.xml --cg "fff_cg_s.xml;water.xml"
csg_call table integrate NH3-COO.force NH3-COO.pot
csg_call table linearop NH3-COO.pot NH3-COO.pot -1 0
cp NH3-COO.pot input_NH3-COO.pot
csg_call --ia-type non-bonded --ia-name NH3-COO --options settings_NC.xml convert_potential gromacs --clean input_NH3-COO.pot table_NH3_COO.xvg
