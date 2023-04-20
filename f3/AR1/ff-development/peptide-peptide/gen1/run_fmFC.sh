#!/bin/bash

# Run force matching on Bridges2 in Fall 2021. 

#SBATCH --mail-user=mh1314@scarletmail.rutgers.edu
#SBATCH --mail-type=ALL
#SBATCH --job-name=bridges_fm_FC
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
csg_fmatch -v --top topol_fm.tpr --trj traj.trr --begin $equi --options settings_FC.xml --cg "fff_cg_s.xml;water.xml"
csg_call table integrate PHE-COO.force PHE-COO.pot
csg_call table linearop PHE-COO.pot PHE-COO.pot -1 0
cp PHE-COO.pot input_PHE-COO.pot
csg_call --ia-type non-bonded --ia-name PHE-COO --options settings_FC.xml convert_potential gromacs --clean input_PHE-COO.pot table_PHE_COO.xvg
