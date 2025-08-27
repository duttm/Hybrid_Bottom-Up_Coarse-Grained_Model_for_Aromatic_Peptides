#!/bin/bash

$1

## get a frame or a trajectory
#gmx trjconv -o npt.gro

ROOTDIR=$PWD
mkdir cmap; cd cmap


# cg map it if needed
~/code/containers/votca1.6.4.sif csg_map --trj ../md.gro --cg "/home/mason/oligo/mappings/mapping_F2-RES.xml;/home/mason/oligo/mappings/mapping_water.xml" --top ../md.tpr --out BA32_20ns_CG.gro

grep -v 'SOL' mapped.gro > nowater.gro

# algorithm in the cmap code has poor scaling N^2 or something
# calculation takes 7 minutes for a frame with 64 F4 peptides 
# (64 peptides * 21 particles per peptide)
time python ~/oligo/Hybrid_Bottom-Up_Coarse-Grained_Model_for_Aromatic_Peptides/FFF/analysis/contactmap/code/contact_map.py BA32_20ns_CG.gro 32 11 > log.log 2>&1

# 
python ~/oligo/Hybrid_Bottom-Up_Coarse-Grained_Model_for_Aromatic_Peptides/FFF/analysis/contactmap/code/plot_contact_map.py contactmap.txt 3 11 > log.log 2>&1


