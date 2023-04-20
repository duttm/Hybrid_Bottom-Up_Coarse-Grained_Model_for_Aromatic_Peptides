#!/bin/bash -e

#SBATCH --mail-user=mh1314@scarletmail.rutgers.edu
#SBATCH --mail-type=ALL
#SBATCH --job-name=csgstat
#SBATCH --partition RM-shared
#SBATCH -N 1 --ntasks-per-node=8
#SBATCH --time=48:00:00
#SBATCH --output=slurm.%N.%j.out
#SBATCH --export=ALL

#module purge
#module load gromacs/2018

#AA_DIR=/ocean/projects/dmr170002p/hooten/fff1_500ns
#CG_DIR=/ocean/projects/dmr170002p/hooten/fff1_500ns/cg
#SCRIPT_DIR=/ocean/projects/dmr170002p/hooten
#TRAJ=fff1_500.xtc
#TPR=md_fff1_200_500.tpr

csg_stat -v --nt 4 --top ../topol.tpr \
--cg "fff_cg_CG_s.xml;water_CG.xml" \
--options settings2_s.xml \
--trj ../traj.xtc
