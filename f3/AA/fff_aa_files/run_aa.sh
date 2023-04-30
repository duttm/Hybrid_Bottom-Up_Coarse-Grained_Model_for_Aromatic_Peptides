#!/bin/bash

# REMEMBER!!
# get in there and update topol.top! 

#REQUIRED_FILES="fff_box.gro fff.gro topol.top minim.mdp nvt.mdp npt.mdp md.mdp posre.itp"
#BREAKME=0

#for CHECK_FILE in $REQUIRED_FILES
#do
#if [! -f $CHECK_FILE]
#then
#echo "$CHECK_FILE is missing."
#BREAKME=1
#fi
#done

NMOL=$1

#cp ../fff_aa_files/topol.top ./
cp -r ../fff_aa_files ../fff$NMOL
cd ../fff$NMOL
echo "FFF     $NMOL" >> topol.top

gmx insert-molecules -f fff_box.gro -ci fff.gro -nmol $((NMOL-1)) -rot xyz -o fff$NMOL.gro

gmx solvate -cp fff$NMOL.gro -cs spc216.gro -o solv.gro -p topol.top

gmx grompp -f minim.mdp -c solv.gro -p topol.top -o em.tpr
gmx mdrun -v -deffnm em

gmx grompp -f nvt.mdp -c em.gro -r em.gro -p topol.top -o nvt.tpr
gmx mdrun -v -deffnm nvt

gmx grompp -f npt.mdp -c nvt.gro -r nvt.gro -t nvt.cpt -p topol.top -o npt.tpr
gmx mdrun -v -deffnm npt


