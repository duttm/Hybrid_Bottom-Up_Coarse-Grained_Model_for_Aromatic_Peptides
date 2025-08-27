#!/bin/bash

# convert some pdbs to some gros

ROOTDIR=$PWD
GMX="/home/mason/code/containers/gmx18_4.sif gmx"

for i in 2 4
do
    mol=F$i
    cd $ROOTDIR
    mkdir $mol; cd $mol
    cp -a ../$mol.pdb ./
    echo "4
    6
    " | $GMX pdb2gmx -f $mol.pdb -o $mol.gro -ignh
    
    # topology needs to be modified at this point
    # and so does the gro file
    # for you see
    # i think that votca needs it that way ???
    

~/code/containers/gmx18_4.sif gmx editconf -f F2.gro -box 4 4 4 -o F2_box.gro


#cp -a ../F2_1/F2_1_box.gro ./
#cp -a ../F2_1/posre.itp ./
#cp -a ../F2_1/#topol.top.1# ./topol.top

#$GMX insert-molecules -f ${mol}_box.gro -ci ${mol}.gro -nmol $((j-1)) -rot xyz -o ${mol}_$j.gro -o ${mol}_25_box.gro

$GMX solvate -cp F2_box.gro -cs spc216.gro -o F2_solv.gro -p topol.top


cp -a ~/fff/fff_aa_files/*.mdp ./

#export GMX=gmx
$GMX grompp -f minim.mdp -c F2_solv.gro -p topol.top -o em.tpr
$GMX mdrun -v -deffnm em

$GMX grompp -f nvt.mdp -c em.gro -r em.gro -p topol.top -o nvt.tpr
$GMX mdrun -v -deffnm nvt

$GMX grompp -f npt.mdp -c nvt.gro -r nvt.gro -t nvt.cpt -p topol.top -o npt.tpr
$GMX mdrun -v -deffnm npt

