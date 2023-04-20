#!/bin/bash

#SBATCH --mail-user=mh1314@scarletmail.rutgers.edu
#SBATCH --mail-type=ALL
#SBATCH --job-name=BRIDGES2_ibi500ind
#SBATCH --partition RM-shared
#SBATCH -N 1 --ntasks-per-node=16
#SBATCH --time=04:00:00
#SBATCH --output=slurm.%N.%j.out
#SBATCH --export=ALL

module load gromacs/2018

#calculate bonded potentials with csg_boltzmann

AA_DIR=/ocean/projects/dmr170002p/hooten/fff1_500ns
CG_DIR=/ocean/projects/dmr170002p/hooten/fff1_500ns/cg
#NEW_DIR=$1
SCRIPT_DIR=/ocean/projects/dmr170002p/hooten
TRAJ=fff1_500.xtc

#mkdir $NEW_DIR
#cp $CG_DIR/boltzmann_cmds500 $NEW_DIR/
#cp $CG_DIR/run_Boltzmann500a.sh $NEW_DIR/
#cd $NEW_DIR

#convert bonded potentials to GROMACS tables
if [ -d table ]
then
  rm -r table
fi
mkdir table

# use this line to run all at once. comment out this one and uncomment individual to run individually.
#csg_boltzmann --top $AA_DIR/md_fff1_200_500.tpr --trj $AA_DIR/$TRAJ --cg "$CG_DIR/cgs/fff_cg.xml;$CG_DIR/water.xml" < boltzmann_cmds500

##
for dihedral in \
F1B1A1B2 NB1A1B2 B1A1B2F2 B1A1B2A2 A1B2A2B3 F2B2A2B3 B2A2B3F3 B2A2B3C
do
#cp $CG_DIR/bis/bi_$dihedral.xml .
#cp $CG_DIR/bcmds/bcmds_$dihedral .
csg_boltzmann --top $AA_DIR/md_fff1_200_500.tpr --trj $AA_DIR/$TRAJ --cg "$CG_DIR/cgs/fff_${dihedral}.xml;$CG_DIR/water.xml" < $CG_DIR/bcmds/bcmds_$dihedral
csg_call --sloppy-tables table smooth $dihedral.pot.ib input_$dihedral.pot

#csg_call --ia-type dihedral --ia-name $dihedral --options bi_$dihedral.xml convert_potential gromacs --clean input_$dihedral.pot ./table/table_$dihedral.xvg
csg_call --ia-type dihedral --ia-name $dihedral --options $CG_DIR/bis/bi_dihedrals.xml convert_potential gromacs --clean input_$dihedral.pot ./table/table_$dihedral.xvg
done

##
for bond in \
F1B1 NB1 B1A1 A1B2 B2F2 B2A2 A2B3 B3F3 B3C endend F1F2 F1F3 F2F3
do
#cp $CG_DIR/bis/bi_$bond.xml .
#cp $CG_DIR/bcmds/bcmds_$bond .
csg_boltzmann --top $AA_DIR/md_fff1_200_500.tpr --trj $AA_DIR/$TRAJ --cg "$CG_DIR/cgs/fff_${bond}.xml;$CG_DIR/water.xml" < $CG_DIR/bcmds/bcmds_$bond
csg_call --sloppy-tables table smooth $bond.pot.ib input_$bond.pot

#csg_call --ia-type bond --ia-name $bond --options $CG_DIR/bis/bi_$bond.xml convert_potential gromacs --clean input_$bond.pot ./table/table_$bond.xvg
csg_call --ia-type bond --ia-name $bond --options $CG_DIR/bis/bi_bonds.xml convert_potential gromacs --clean input_$bond.pot ./table/table_$bond.xvg
done

##
for angle in \
F1B1N F1B1A1 NB1A1 B1A1B2 A1B2F2 A1B2A2 B2A2B3 F2B2A2 A2B3F3 A2B3C F3B3C
do
#cp $CG_DIR/bis/bi_$angle.xml .
#cp $CG_DIR/bcmds/bcmds_$angle .
csg_boltzmann --top $AA_DIR/md_fff1_200_500.tpr --trj $AA_DIR/$TRAJ --cg "$CG_DIR/cgs/fff_${angle}.xml;$CG_DIR/water.xml" < $CG_DIR/bcmds/bcmds_$angle
csg_call --sloppy-tables table smooth $angle.pot.ib input_$angle.pot

#csg_call --ia-type angle --ia-name $angle --options bi_$angle.xml convert_potential gromacs --clean input_$angle.pot ./table/table_$angle.xvg
csg_call --ia-type angle --ia-name $angle --options $CG_DIR/bis/bi_angles.xml convert_potential gromacs --clean input_$angle.pot ./table/table_$angle.xvg
done


cd table
gnuplot $SCRIPT_DIR/plot_ibi_potentials.plt

cd ../..

