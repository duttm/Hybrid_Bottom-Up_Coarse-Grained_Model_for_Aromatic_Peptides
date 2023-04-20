#!/bin/bash

# Run AA MD on Bridges2 in Summer 2021.
# General script to be used for 200ns runs.
# Usually change "fff" to e.g. "fff16" for 16 peptides. 

#SBATCH --mail-user=mh1314@scarletmail.rutgers.edu
#SBATCH --mail-type=ALL
#SBATCH --job-name=bridges_fff_aa_200
#SBATCH --partition RM
#SBATCH -N 1 --ntasks-per-node=16
#SBATCH --time=48:00:00
#SBATCH --output=slurm.%N.%j.out
#SBATCH --export=ALL

module load gromacs/2018

# production md

# skip grompp if it was done on another machine. be careful that grompp was done with gromacs 2018!
mpirun -np 1 gmx_mpi grompp -f md.mdp -c npt.gro -p topol.top -r npt.gro -t npt.cpt -o fff_aa_200

mpirun -np 16 gmx_mpi mdrun -v -deffnm fff_aa_200

