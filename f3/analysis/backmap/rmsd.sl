#!/bin/bash

# Run AA MD on Bridges2 in Summer 2021.
# General script to be used for 200ns runs.
# Usually change "fff" to e.g. "fff16" for 16 peptides. 

#SBATCH --mail-user=mh1314@scarletmail.rutgers.edu
#SBATCH --mail-type=ALL
#SBATCH --job-name=rmsd
#SBATCH --partition RM-shared
#SBATCH -N 1 --ntasks-per-node=16
#SBATCH --time=23:00:00
#SBATCH --output=slurm.%N.%j.out
#SBATCH --export=ALL

module load gromacs/2018

# production npt
#mpirun -np 1 gmx_mpi grompp -f md.mdp -c back-em.gro -p topol.top -o md-backmap

#mpirun -np 16 gmx_mpi mdrun -v -ntomp 1 -deffnm md-backmap

for i in 1 8 32
do
cd /ocean/projects/dmr170002p/hooten/fff/backmap/1fg$i/sim
echo 0 0 | mpirun -np 1 gmx_mpi rms -f md-backmap.xtc -s md-backmap.tpr -n ../backmapped.ndx -o rmsd-1fg$i.xvg -pbc yes
done

for i in 1 8 32
do
cd /ocean/projects/dmr170002p/hooten/fff/backmap/2fg$i/sim
echo 0 0 | mpirun -np 1 gmx_mpi rms -f md-backmap.xtc -s md-backmap.tpr -n ../backmapped.ndx -o rmsd-2fg$i.xvg -pbc yes
done
