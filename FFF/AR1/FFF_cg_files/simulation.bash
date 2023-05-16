#!/bin/bash

#SBATCH --mail-user=
#SBATCH --mail-type=ALL
#SBATCH --job-name=cg16_200
#SBATCH --partition RM-shared
#SBATCH -N 1 --ntasks-per-node=8
#SBATCH --time=48:00:00
#SBATCH --output=slurm.%N.%j.out
#SBATCH --export=ALL

module load gromacs/2018

input=cg16_aa10 # Name of the input file, i.e. the CG coordinates Mapped onto the AA system

GRO="${input}.gro"

tpr=table
minim=grompp_CG
TOP=topol_cg.top
NDX=index_cg.ndx

mpirun -np 1 gmx_mpi grompp -f "${minim}.mdp" -c $GRO -o $tpr -p $TOP -n $NDX

mpirun -np 8 gmx_mpi mdrun -deffnm $tpr -cpi table.cpt -v -tableb \
table_b1.xvg table_b2.xvg table_b3.xvg table_b4.xvg table_b5.xvg \
table_b6.xvg table_b7.xvg table_b8.xvg table_b9.xvg \
table_a21.xvg table_a22.xvg table_a23.xvg table_a24.xvg table_a25.xvg \
table_a26.xvg table_a27.xvg table_a28.xvg table_a29.xvg table_a30.xvg \
table_a31.xvg \
table_d32.xvg table_d33.xvg table_d34.xvg table_d35.xvg table_d36.xvg \
table_d37.xvg table_d38.xvg table_d39.xvg


