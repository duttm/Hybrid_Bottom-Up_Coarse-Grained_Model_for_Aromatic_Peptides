#!/bin/bash

# Run force matching on Bridges2 in Fall 2021. 

#SBATCH --mail-user=mh1314@scarletmail.rutgers.edu
#SBATCH --mail-type=ALL
#SBATCH --job-name=bridges_fm_NN
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
csg_fmatch -v --top topol_fm.tpr --trj traj.trr --begin $equi --options settings_NN.xml --cg "fff_cg_s.xml;water.xml"
csg_call table integrate NH3-NH3.force NH3-NH3.pot
csg_call table linearop NH3-NH3.pot NH3-NH3.pot -1 0
cp NH3-NH3.pot input_NH3-NH3.pot
csg_call --ia-type non-bonded --ia-name NH3-NH3 --options settings_NN.xml convert_potential gromacs --clean input_NH3-NH3.pot table_NH3_NH3.xvg
