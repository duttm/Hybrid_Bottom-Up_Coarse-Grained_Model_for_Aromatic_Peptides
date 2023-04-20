#!/bin/sh

INPUT_FILE=1cg32_last-frame-200ns.gro
NUM_BEADS=2195
BEADS_PER_MOL=10
NUM_MOL=32
VRINPUT=${NUM_MOL}_RESFFF.gro
VROUTPUT=${NUM_MOL}_CG_rewrite.gro

BACKWARD_DIR=/home/mason/fff/backmap/backward-v5

sed -e 's/RES/FFF/g' $INPUT_FILE > $VRINPUT

##Some pre-processing: Use python votca_reader.py cg8_aa10.gro <number of frames> <number of beads> <number of beads in 1 molecule> <tital number of peptides> <number of beads in 1 molecule>
cp -a ${BACKWARD_DIR}/votca_reader-1.py ./votca_reader.py
python3 votca_reader.py ${VRINPUT} 1 ${NUM_BEADS} ${BEADS_PER_MOL} ${NUM_MOL} ${BEADS_PER_MOL} 0

# copy Backward files
cp -ra ${BACKWARD_DIR}/Mapping ./
cp -a ${BACKWARD_DIR}/backward.py ./
cp -a ${BACKWARD_DIR}/initram-v5.sh ./
cp -a ${BACKWARD_DIR}/posre.itp ./

## MANUAL STEP - MODIFY TOPOLOGY
# Delete or comment out ions and solvent. These are handled automatically.

# run Backward
./initram-v5.sh -f ${VROUTPUT} -o back-em.gro -to amber -p topol.top -em 500 -nb 500 -np 1
