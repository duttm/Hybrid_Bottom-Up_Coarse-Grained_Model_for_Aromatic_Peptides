#!/bin/bash

# Run force matching on Bridges2 in Fall 2021. 

#SBATCH --mail-user=mh1314@scarletmail.rutgers.edu
#SBATCH --mail-type=ALL
#SBATCH --job-name=bridges_fm_FF
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
csg_fmatch -v --top topol_fm.tpr --trj traj.trr --begin $equi --options settings_FF.xml --cg "fff_cg_s.xml;water.xml"
csg_call table integrate PHE-PHE.force PHE-PHE.pot
csg_call table linearop PHE-PHE.pot PHE-PHE.pot -1 0
cp PHE-PHE.pot input_PHE-PHE.pot
csg_call --ia-type non-bonded --ia-name PHE-PHE --options settings_FF.xml convert_potential gromacs --clean input_PHE-PHE.pot table_PHE_PHE.xvg
