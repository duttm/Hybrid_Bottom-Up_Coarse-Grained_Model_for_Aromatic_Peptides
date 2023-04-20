#!/bin/bash

# Run AA MD on Bridges2 in Summer 2021.
# General script to be used for 200ns runs.
# Usually change "fff" to e.g. "fff16" for 16 peptides. 

#SBATCH --mail-user=mh1314@scarletmail.rutgers.edu
#SBATCH --mail-type=ALL
#SBATCH --job-name=bak
#SBATCH --partition RM-shared
#SBATCH -N 1 --ntasks-per-node=16
#SBATCH --time=23:00:00
#SBATCH --output=slurm.%N.%j.out
#SBATCH --export=ALL

module load gromacs/2018

# production npt
mpirun -np 1 gmx_mpi grompp -f nvt.mdp -c back-em.gro -p topol.top -o nvt -r back-em.gro

mpirun -np 16 gmx_mpi mdrun -v -ntomp 1 -deffnm nvt

# production npt
mpirun -np 1 gmx_mpi grompp -f npt.mdp -c nvt.gro -p topol.top -o npt -r nvt.gro

mpirun -np 16 gmx_mpi mdrun -v -ntomp 1 -deffnm npt

# production npt
mpirun -np 1 gmx_mpi grompp -f md.mdp -c npt.gro -p topol.top -o md-backmap

mpirun -np 16 gmx_mpi mdrun -v -ntomp 1 -deffnm md-backmap
