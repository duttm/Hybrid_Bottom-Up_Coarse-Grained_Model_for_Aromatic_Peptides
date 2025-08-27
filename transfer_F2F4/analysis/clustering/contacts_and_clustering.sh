#!/bin/bash

#********************************************************************************
#********************************************************************************
#***************************************     CONTACTS
#Contacts and Clustering Figure (last figure in FFF paper)

# bottom up models
printf '%s\n' "9 | 10 | 11" q | gmx make_ndx -f topol.tpr -n index.ndx
#Group     0 (         System) has 10160 elements
#Group     1 (          Other) has  1408 elements
#Group     2 (             F2) has  1408 elements
#Group     3 (          Water) has  8752 elements
#Group     4 (            SOL) has  8752 elements
#Group     5 (      non-Water) has  1408 elements
#Group     6 (            NH3) has   128 elements
#Group     7 (             CA) has   256 elements
#Group     8 (            AMD) has   128 elements
#Group     9 (            PHA) has   256 elements
#Group    10 (            PHB) has   256 elements
#Group    11 (            PHC) has   256 elements
#Group    12 (            COO) has   128 elements
#Group    13 (    PHA_PHB_PHC) has   768 elements

export ENDTIME=25000
export DTTIME=1

#export ENDTIME=500000
#export DTTIME=1000

export TRAJNAME=md # F2 -25 -32 -64 -128 F4-25
export TRAJNAME=traj_comp # F4

for i in {0..9};
do
cd /home/mason/exdrive/oligo/F2/CG/F4_64-$i
printf '7 7' | gmx mindist -f $TRAJNAME.xtc -s topol.tpr -n index.ndx -on numcont_MCMC.xvg -od mindist_MCMC.xvg -dt $DTTIME -e $ENDTIME
printf '13 13' | gmx mindist -f $TRAJNAME.xtc -s topol.tpr -n index.ndx -on numcont_SCSC.xvg -od mindist_SCSC.xvg -dt $DTTIME -e $ENDTIME
printf '7 13' | gmx mindist -f $TRAJNAME.xtc -s topol.tpr -n index.ndx -on numcont_MCSC.xvg -od mindist_MCSC.xvg -dt $DTTIME -e $ENDTIME
printf '8 8' | gmx mindist -f $TRAJNAME.xtc -s topol.tpr -n index.ndx -on numcont_AMDAMD.xvg -od mindist_AMDAMD.xvg -dt $DTTIME -e $ENDTIME
printf '6 12' | gmx mindist -f $TRAJNAME.xtc -s topol.tpr -n index.ndx -on numcont_NH3COO.xvg -od mindist_NH3COO.xvg -dt $DTTIME -e $ENDTIME
mkdir contacts-0-end-dt1ns
mv numcont* contacts-0-25/
mv mindist* contacts-0-25/
done

printf '7 7' | gmx mindist -f md.xtc -s topol.tpr -n index.ndx -on numcont_MCMC.xvg -od mindist_MCMC.xvg -e 25000

printf '13 13' | gmx mindist -f md.xtc -s topol.tpr -n index.ndx -on numcont_SCSC.xvg -od mindist_SCSC.xvg -e 25000

printf '7 13' | gmx mindist -f md.xtc -s topol.tpr -n index.ndx -on numcont_MCSC.xvg -od mindist_MCSC.xvg -e 25000

printf '8 8' | gmx mindist -f md.xtc -s topol.tpr -n index.ndx -on numcont_AMDAMD.xvg -od mindist_AMDAMD.xvg -e 25000

printf '6 12' | gmx mindist -f md.xtc -s topol.tpr -n index.ndx -on numcont_NH3COO.xvg -od mindist_NH3COO.xvg -e 25000



#MARTINI
printf '%s\n' "a BB" "! a BB" q | gmx make_ndx -f md.tpr

# usual Martini 3
#  0 System              :   696 atoms
#  1 Protein             :   256 atoms
#  2 Protein-H           :   256 atoms
#  3 C-alpha             :     0 atoms
#  4 Backbone            :     0 atoms
#  5 MainChain           :     0 atoms
#  6 MainChain+Cb        :     0 atoms
#  7 MainChain+H         :     0 atoms
#  8 SideChain           :   256 atoms
#  9 SideChain-H         :   256 atoms
# 10 Prot-Masses         :   256 atoms
# 11 non-Protein         :   440 atoms
# 12 Other               :   440 atoms
# 13 W                   :   440 atoms
# 14 BB                  :    64 atoms
# 15 !BB                 :   632 atoms

# usual Martini 2
#  0 System              :   696 atoms
#  1 Protein             :   256 atoms
#  2 Protein-H           :   256 atoms
#  3 C-alpha             :     0 atoms
#  4 Backbone            :     0 atoms
#  5 MainChain           :     0 atoms
#  6 MainChain+Cb        :     0 atoms
#  7 MainChain+H         :     0 atoms
#  8 SideChain           :   256 atoms
#  9 SideChain-H         :   256 atoms
# 10 Prot-Masses         :   256 atoms
# 11 non-Protein         :   440 atoms
# 12 Other               :   440 atoms
# 13 W                   :   440 atoms
# 14 WF                  :    64 atoms
# 15 BB                  :    64 atoms
# 16 !BB                 :   632 atoms

printf '14 14' | gmx mindist -f $TRAJNAME.xtc -s md.tpr -n index.ndx -on numcont_MCMC.xvg -od mindist_MCMC.xvg

printf '15 15' | gmx mindist -f $TRAJNAME.xtc -s md.tpr -n index.ndx -on numcont_SCSC.xvg -od mindist_SCSC.xvg

printf '14 15' | gmx mindist -f $TRAJNAME.xtc -s md.tpr -n index.ndx -on numcont_MCSC.xvg -od mindist_MCSC.xvg

printf '14 14' | gmx mindist -f md.xtc -s md.tpr -n index.ndx -on numcont_MCMC.xvg -od mindist_MCMC.xvg -e 25000

printf '15 15' | gmx mindist -f md.xtc -s md.tpr -n index.ndx -on numcont_SCSC.xvg -od mindist_SCSC.xvg -e 25000

printf '14 15' | gmx mindist -f md.xtc -s md.tpr -n index.ndx -on numcont_MCSC.xvg -od mindist_MCSC.xvg -e 25000

#***************************************     CONTACTS
#********************************************************************************
#********************************************************************************

#********************************************************************************
#********************************************************************************
#***************************************     CLUSTERING

export START=5
export END=25
export DT=1

export STARTTIME=$((1000*START))
export ENDTIME=$((1000*END))
#export DTTIME=$((1000*DT))
export DTTIME=1

export TRAJNAME=md # F2 -25 -32 -64 -128 F4-25
export TRAJNAME=traj_comp # F4

export PEPCT=64

for i in {0..14};
do
cd /home/mason/exdrive/oligo/F4/CG/F4_64-$i
printf '2' | gmx clustsize -f $TRAJNAME.xtc -s topol.tpr -n index.ndx -nc nclust-0-25.xvg -e $ENDTIME
mkdir cluster-0-25
mv nclust* cluster-0-25/
done


#***************************************     CLUSTERING
#********************************************************************************
#********************************************************************************


#********************************************************************************
#********************************************************************************
#***************************************     Plots

#Contacts and Clustering Figure for Bottom Up Models
plot 'numcont_MCMC.xvg' u 1:2 w l, 'numcont_SCSC.xvg' u 1:2 w l, 'numcont_MCSC.xvg' u 1:2 w l, 'numcont_AMDAMD.xvg' u 1:2 w l, 'numcont_NH3COO.xvg' u 1:2 w l

#Contacts and Clustering Figure for Martini Models
plot 'numcont_MCMC.xvg' u 1:2 w l, 'numcont_SCSC.xvg' u 1:2 w l, 'numcont_MCSC.xvg' u 1:2 w l

#***************************************     Plots
#********************************************************************************
#********************************************************************************


