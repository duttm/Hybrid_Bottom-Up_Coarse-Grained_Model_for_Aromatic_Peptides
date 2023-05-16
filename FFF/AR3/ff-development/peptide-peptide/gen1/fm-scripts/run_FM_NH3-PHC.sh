#!/bin/bash

# Run force matching on Bridges2 in Fall 2022.

#SBATCH --mail-user=mh1314@scarletmail.rutgers.edu
#SBATCH --mail-type=ALL
#SBATCH --job-name=NH3PHC
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
csg_fmatch -v --top topol_fm.tpr --trj traj.trr --options settings_FM_NH3-PHC.xml --cg "second_cg.xml;water.xml"
csg_call table integrate NH3-PHC.force NH3-PHC.pot
csg_call table linearop NH3-PHC.pot NH3-PHC.pot -1 0
cp NH3-PHC.pot input_NH3-PHC.pot
csg_call --ia-type non-bonded --ia-name NH3-PHC --options settings_FM_NH3-PHC.xml convert_potential gromacs --clean input_NH3-PHC.pot table_NH3-PHC.xvg

