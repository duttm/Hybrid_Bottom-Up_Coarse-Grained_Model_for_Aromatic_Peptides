#!/bin/bash

#SBATCH --mail-user=mh1314@scarletmail.rutgers.edu
#SBATCH --mail-type=ALL
#SBATCH --job-name=ibi
#SBATCH --partition RM-shared
#SBATCH -N 1 --ntasks-per-node=8
#SBATCH --time=24:00:00
#SBATCH --output=slurm.%N.%j.out
#SBATCH --export=ALL

#GMX_APP=/ocean/projects/dmr170002p/hooten/dmref/gmx21_5.sif

module load gromacs/2018

tpr=table
minim=grompp_CG
TOP=topol_cg.top
NDX=index_cg.ndx

#mpirun -np 1 gmx_mpi grompp -f "${minim}.mdp" -c $GRO -o $tpr -p $TOP -n $NDX

mpirun -np 8 gmx_mpi mdrun -ntomp 1 -deffnm $tpr -cpi table.cpt -v -tableb \
table_b1.xvg table_b2.xvg table_b3.xvg table_b4.xvg table_b5.xvg \
table_b6.xvg table_b7.xvg table_b8.xvg table_b9.xvg table_b10.xvg \
table_b11.xvg table_b12.xvg table_b13.xvg table_b14.xvg table_b15.xvg \
table_b16.xvg table_b17.xvg table_b18.xvg \
table_a1.xvg table_a2.xvg table_a3.xvg table_a4.xvg table_a5.xvg \
table_a6.xvg table_a7.xvg table_a8.xvg table_a9.xvg table_a10.xvg \
table_a11.xvg table_a12.xvg table_a13.xvg table_a14.xvg table_a15.xvg \
table_a16.xvg table_a17.xvg table_a18.xvg table_a19.xvg table_a20.xvg \
table_a21.xvg table_a22.xvg table_a23.xvg table_a24.xvg table_a25.xvg \
table_a26.xvg \
table_d1.xvg table_d2.xvg table_d3.xvg table_d4.xvg table_d5.xvg \
table_d6.xvg table_d7.xvg table_d8.xvg table_d9.xvg table_d10.xvg \
table_d11.xvg table_d12.xvg table_d13.xvg table_d14.xvg table_d15.xvg \
table_d16.xvg table_d17.xvg table_d18.xvg table_d19.xvg table_d20.xvg \
table_d21.xvg table_d22.xvg table_d23.xvg table_d24.xvg table_d25.xvg \
table_d26.xvg

