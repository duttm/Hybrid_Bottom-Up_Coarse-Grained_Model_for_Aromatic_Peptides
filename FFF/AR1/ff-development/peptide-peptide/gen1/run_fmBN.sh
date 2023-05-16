#!/bin/bash

# Run force matching on Bridges2 in Fall 2021. 

#SBATCH --mail-user=mh1314@scarletmail.rutgers.edu
#SBATCH --mail-type=ALL
#SBATCH --job-name=bridges_fm_BN
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
csg_fmatch -v --top topol_fm.tpr --trj traj.trr --begin $equi --options settings_BN.xml --cg "fff_cg_s.xml;water.xml"
csg_call table integrate CAB-NH3.force CAB-NH3.pot
csg_call table linearop CAB-NH3.pot CAB-NH3.pot -1 0
cp CAB-NH3.pot input_CAB-NH3.pot
csg_call --ia-type non-bonded --ia-name CAB-NH3 --options settings_BN.xml convert_potential gromacs --clean input_CAB-NH3.pot table_CAB_NH3.xvg
