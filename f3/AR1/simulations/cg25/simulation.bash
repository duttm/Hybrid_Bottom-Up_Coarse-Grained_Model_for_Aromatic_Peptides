#!/bin/bash

#SBATCH --mail-user=mh1314@scarletmail.rutgers.edu
#SBATCH --mail-type=ALL
#SBATCH --job-name=25cg1111
#SBATCH --partition RM-shared
#SBATCH -N 1 --ntasks-per-node=8
#SBATCH --time=24:00:00
#SBATCH --output=slurm.%N.%j.out
#SBATCH --export=ALL

#We have run this simulation on the following GROMACS versions : GROMACS 5.1.2 and 2018.3
#The simulation has been tested on the following machines: 
#1. Stampede2 (1 node that has 64 cores) : The peptides begin to assemble into a nanorod after a 1 ns simulation. An addtional 4 ns simulation stabilizes the nanorod.   
# link to stampede2: https://portal.xsede.org/tacc-stampede2
#2. Local desktop computer (runs on 8 threads) : The peptide assembly behavior approximately the same as above. 


#Please note that the MDP file may need to be changed if :
#1. You are using a different version of GROMACS
#2. A different machine (may need to change timestep)
#3. Any other possible configuration other than the ones this simulation has been tested on.

module load gromacs/2018

input=fff25_cg_0 # Name of the input file, i.e. the CG coordinates Mapped onto the AA system

GRO="${input}.gro"

tpr=table
minim=grompp_CG # the default run time is set to 1ns in this file (grompp_CG.mdp). The simulation needs to run for longer to stablize the nanorod.  
TOP=topol_cg.top
NDX=index_cg.ndx


# DIR=$PWD
# cp ./pots/table_*.xvg $DIR

#mpirun -np 1 gmx_mpi grompp -f "${minim}.mdp" -c $GRO -o $tpr -p  $TOP -n $NDX 

#mpirun -np 4 gmx_mpi mdrun -deffnm $tpr -ntomp 1 -cpi table.cpt -v -tableb \
#table_b1.xvg table_b2.xvg table_b3.xvg table_b4.xvg table_b5.xvg \
#table_b6.xvg table_b7.xvg table_b8.xvg table_b9.xvg \
#table_a21.xvg table_a22.xvg table_a23.xvg table_a24.xvg table_a25.xvg \
#table_a26.xvg table_a27.xvg table_a28.xvg table_a29.xvg table_a30.xvg \
#table_a31.xvg \
#table_d32.xvg table_d33.xvg table_d34.xvg table_d35.xvg table_d36.xvg \
#table_d37.xvg table_d38.xvg table_d39.xvg

# after the initial 100ns, we need to go further.
# note this will #backup the original table.tpr, so don't delete it!
#echo 0 | mpirun -np 1 gmx_mpi convert-tpr -s table.tpr -n index_cg.ndx -extend 100000 -o table.tpr

#mpirun -np 8 gmx_mpi mdrun -deffnm $tpr -ntomp 1 -cpi table.cpt -v -tableb \
#table_b1.xvg table_b2.xvg table_b3.xvg table_b4.xvg table_b5.xvg \
#table_b6.xvg table_b7.xvg table_b8.xvg table_b9.xvg \
#table_a21.xvg table_a22.xvg table_a23.xvg table_a24.xvg table_a25.xvg \
#table_a26.xvg table_a27.xvg table_a28.xvg table_a29.xvg table_a30.xvg \
#table_a31.xvg \
#table_d32.xvg table_d33.xvg table_d34.xvg table_d35.xvg table_d36.xvg \
#table_d37.xvg table_d38.xvg table_d39.xvg

# Extension to 1us 3/17/22
#echo 0 | mpirun -np 1 gmx_mpi convert-tpr -s $tpr -n $NDX -o $tpr.tpr -until 1000000

mpirun -np 8 gmx_mpi mdrun -ntomp 1 -deffnm $tpr -cpi table.cpt -v -noappend -tableb \
table_b1.xvg table_b2.xvg table_b3.xvg table_b4.xvg table_b5.xvg \
table_b6.xvg table_b7.xvg table_b8.xvg table_b9.xvg \
table_a21.xvg table_a22.xvg table_a23.xvg table_a24.xvg table_a25.xvg \
table_a26.xvg table_a27.xvg table_a28.xvg table_a29.xvg table_a30.xvg \
table_a31.xvg \
table_d32.xvg table_d33.xvg table_d34.xvg table_d35.xvg table_d36.xvg \
table_d37.xvg table_d38.xvg table_d39.xvg

