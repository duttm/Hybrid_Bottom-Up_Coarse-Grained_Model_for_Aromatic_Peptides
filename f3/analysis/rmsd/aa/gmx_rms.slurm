#!/bin/bash

#SBATCH --mail-user=mh1314@scarletmail.rutgers.edu
#SBATCH --mail-type=ALL
#SBATCH --job-name=ana
#SBATCH --partition RM-shared
#SBATCH -N 1 --ntasks-per-node=16
#SBATCH --time=1:00:00
#SBATCH --output=slurm.%N.%j.out
#SBATCH --export=ALL

module load gromacs/2018

MODELNO=$1
PEPCT=$2

INPUT=fff${PEPCT}_aa_500_mapped-${MODELNO}cg.xtc
REFERENCE=topol-aa${MODELNO}cg${PEPCT}.tpr
#REFERENCE=fff${PEPCT}_aa_300ns_mapped-${MODELNO}cg.gro
STARTns=300
ENDns=500
echo 1 1 | mpirun -np 1 gmx_mpi rms -f $INPUT -s $REFERENCE -n index-${MODELNO}cg${PEPCT}.ndx -o rmsd-aa${MODELNO}cg${PEPCT}.xvg -pbc yes -b ${STARTns}000 -e ${ENDns}000

