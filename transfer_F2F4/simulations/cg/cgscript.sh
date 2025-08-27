#!/bin/bash

# get an input AA config and its topology
cp -a ~/oligo/F2/AA/F2_25/npt.gro ./AA25npt.gro
cp -a ~/oligo/F2/AA/F2_25/npt.tpr ./AA25npt.tpr

# CG map it
~/code/containers/votca1.6.4.sif csg_map --trj AA32npt.gro --cg "/home/mason/oligo/mappings/mapping_F2.xml;/home/mason/oligo/mappings/mapping_water.xml" --top AA32npt.tpr --out AA32npt_CG.gro

# get a topology or make one
cp -a ../../ff-development/bonded/gen2/dihedrals/topol.top ./

# make a index
echo "a NH3
a CA1 CA2 CA3 CA4
name 7 CA
a AMD1 AMD2 AMD3
name 8 AMD
a PHA1 PHA2 PHA3 PHA4
name 9 PHA
a PHB1 PHB2 PHB3 PHB4
name 10 PHB
a PHC1 PHC2 PHC3 PHC4
name 11 PHC
a COO
q
" | gmx make_ndx -f conf.gro -o index.ndx

# gromp it
gmx grompp -f grompp.mdp -p topol.top -c AA25npt_CG.gro -n index.ndx

###########################
######################################################

# FIX TOPOL AFTER SETUP AND BEFORE MD

######################################################
###########################

# then email it to your big computer and laissez les bontemps roulez
rsync -vazhP ./* mh1314@amarel.rutgers.edu:/scratch/mh1314/oligo/F2/CG/F2_25/


# DON'T FORGET TO ALSO EMAIL A FORCE FIELD
# END OF THIS TUTORIAL
