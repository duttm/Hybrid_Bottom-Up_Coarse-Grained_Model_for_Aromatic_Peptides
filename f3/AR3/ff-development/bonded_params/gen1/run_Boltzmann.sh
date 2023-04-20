#!/bin/bash

#SBATCH --mail-user=mh1314@scarletmail.rutgers.edu
#SBATCH --mail-type=ALL
#SBATCH --job-name=BRIDGES2_ibi500ind
#SBATCH --partition RM-shared
#SBATCH -N 1 --ntasks-per-node=16
#SBATCH --time=04:00:00
#SBATCH --output=slurm.%N.%j.out
#SBATCH --export=ALL

#module load gromacs/2018

AA_DIR=/home/mason/dutt_lab/fff/aa_and_FF_development/fff1_aa_500
CG_DIR=/home/mason/dutt_lab/fff/second_cg
SCRIPT_DIR=/ocean/projects/dmr170002p/hooten
TRAJ=fff1_500.xtc

#convert bonded potentials to GROMACS tables
#if [ -d table ]; then
#  rm -r table
#fi
mkdir table

# use this line to run all at once. comment out this one and uncomment individual to run individually.
#csg_boltzmann --top $AA_DIR/md_fff1_200_500.tpr --trj $AA_DIR/$TRAJ --cg "$CG_DIR/cgs/fff_cg.xml;$CG_DIR/water.xml" < boltzmann_cmds500

##
#for bond in \
#NH3-CA1 CA1-PHA1 PHA1-PHB1 PHB1-PHC1 PHC1-PHA1 \
#CA1-AMD1 AMD1-CA2 CA2-PHA2 PHA2-PHB2 PHB2-PHC2 \
#PHC2-PHA2 CA2-AMD2 AMD2-CA3 CA3-PHA3 PHA3-PHB3 \
#PHB3-PHC3 PHC3-PHA3 CA3-COO
#do
#csg_boltzmann --top $AA_DIR/md_fff1_200_500.tpr --trj $AA_DIR/$TRAJ --cg "$CG_DIR/second_cg.xml;$CG_DIR/water.xml" < ./bcmds/bcmds_$bond
#csg_call --sloppy-tables table smooth $bond.pot.ib input_$bond.pot
#csg_call --ia-type bond --ia-name $bond --options ./settings_bonds.xml convert_potential gromacs --clean input_$bond.pot ./table/table_$bond.xvg
#done

##
#for angle in \
#NH3-CA1-AMD1 CA1-AMD1-CA2 AMD1-CA2-AMD2 CA2-AMD2-CA3 \
#AMD2-CA3-COO NH3-CA1-PHA1 CA1-PHA1-PHB1 CA1-PHA1-PHC1 \
#PHA1-PHB1-PHC1 PHB1-PHC1-PHA1 PHC1-PHA1-PHB1 AMD1-CA1-PHA1 \
#AMD1-CA2-PHA2 CA2-PHA2-PHB2 CA2-PHA2-PHC2 PHA2-PHB2-PHC2 \
#PHB2-PHC2-PHA2 PHC2-PHA2-PHB2 AMD2-CA2-PHA2 AMD2-CA3-PHA3 \
#CA3-PHA3-PHB3 CA3-PHA3-PHC3 PHA3-PHB3-PHC3 PHB3-PHC3-PHA3 \
#PHC3-PHA3-PHB3 COO-CA3-PHA3
#do
#csg_boltzmann --top $AA_DIR/md_fff1_200_500.tpr --trj $AA_DIR/$TRAJ --cg "$CG_DIR/second_cg.xml;$CG_DIR/water.xml" < ./bcmds/bcmds_$angle
#csg_call --sloppy-tables table smooth $angle.pot.ib input_$angle.pot
#csg_call --ia-type angle --ia-name $angle --options ./settings_angles.xml convert_potential gromacs --clean input_$angle.pot ./table/table_$angle.xvg
#done

##
for dihedral in \
NH3-CA1-AMD1-CA2 CA1-AMD1-CA2-AMD2 AMD1-CA2-AMD2-CA3 \
CA2-AMD2-CA3-COO NH3-CA1-PHA1-PHB1 NH3-CA1-PHA1-PHC1 \
CA1-AMD2-CA2-PHA2 CA1-PHA1-PHB1-PHC1 CA1-PHA1-PHC1-PHB1 \
AMD1-CA1-PHA1-PHB1 AMD1-CA1-PHA1-PHC1 AMD1-CA2-PHA2-PHB2 \
AMD1-CA2-PHA2-PHC2 CA2-AMD1-CA1-PHA1 CA2-AMD2-CA3-PHA3 \
CA2-PHA2-PHB2-PHC2 CA2-PHA2-PHC2-PHB2 AMD2-CA2-PHA2-PHB2 \
AMD2-CA2-PHA2-PHC2 AMD2-CA3-PHA3-PHB3 AMD2-CA3-PHA3-PHC3 \
CA3-AMD2-CA2-PHA2 CA3-PHA3-PHB3-PHC3 CA3-PHA3-PHC3-PHB3 \
COO-CA3-PHA3-PHB3 COO-CA3-PHA3-PHC3 PHA1-PHB1-PHC1-PHA1 \
PHA2-PHB2-PHC2-PHA2 PHA3-PHB3-PHC3-PHA3
do
csg_boltzmann --top $AA_DIR/md_fff1_200_500.tpr --trj $AA_DIR/$TRAJ --cg "$CG_DIR/second_cg.xml;$CG_DIR/water.xml" < ./bcmds/bcmds_$dihedral
csg_call --sloppy-tables table smooth $dihedral.pot.ib input_$dihedral.pot
csg_call --ia-type dihedral --ia-name $dihedral --options ./settings_dihedrals.xml convert_potential gromacs --clean input_$dihedral.pot ./table/table_$dihedral.xvg
done

