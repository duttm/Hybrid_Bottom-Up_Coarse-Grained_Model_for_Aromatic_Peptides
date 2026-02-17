#!/bin/bash
# calculate contact maps

# get a sample of the full system (with solvent) to match sample to the baked tpr file
echo 0 | gmx trjconv -f md.xtc -s md.tpr -o traj.xtc -b 90000 -e 100000 -dt 1000
# or
echo 0 | gmx trjconv -f md.xtc -s md.tpr -o traj.xtc -b 10000 -e 20000 -dt 1000

mkdir cmap; cd cmap
# cg map aa systems.
# NOTE: alternative mappings for other configs.
~/code/containers/votca1.6.4.sif csg_map --trj ../traj.xtc --cg "/home/mason/exdrive/oligo/mappings/mapping_F2.xml;/home/mason/exdrive/oligo/mappings/mapping_water.xml" --top ../md.tpr --out traj-cg.gro

# remove water
grep -v 'SOL' traj-cg.gro > traj-cg-nowater.gro

# calculate the contact map -- change per model and system size.
# NOTE: example below shows (32) peptides and the F2 model (11 beads per mol)
# cmap alg scales O(N^2), executes in a few minutes for ten frames of CG peptides 
time python /home/mason/exdrive/oligo/Hybrid_Bottom-Up_Coarse-Grained_Model_for_Aromatic_Peptides/transfer_F2F4/analysis/contactmap/contact_map.py traj-cg-nowater.gro 32 11 > log.log 2>&1

# plot the contact map -- change per model.
# NOTE: example below shows the F2 model (model id 3, 11 beads per mol)
python /home/mason/exdrive/oligo/Hybrid_Bottom-Up_Coarse-Grained_Model_for_Aromatic_Peptides/transfer_F2F4/analysis/contactmap/plot_contact_map.py contactmap.txt 3 11


