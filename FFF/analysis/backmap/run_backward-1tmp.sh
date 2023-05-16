#!/bin/sh

#INPUT_FILE=1cgfff32_5ns-end_dt5ns99.gro
INPUT_FILE=table.gro
NUM_BEADS=2195
BEADS_PER_MOL=10
NUM_MOL=32
VROUTPUT=${NUM_MOL}_CG_rewrite.gro

BACKWARD_DIR=/home/mason/fff/backmap/backward-v5

##Some pre-processing: Use python votca_reader.py cg8_aa10.gro <number of frames> <number of beads> <number of beads in 1 molecule> <tital number of peptides> <number of beads in 1 molecule>
cp -a ${BACKWARD_DIR}/votca_reader-1.py ./votca_reader.py
python3 votca_reader.py ${INPUT_FILE} 1 ${NUM_BEADS} ${BEADS_PER_MOL} ${NUM_MOL} ${BEADS_PER_MOL} 0

# copy Backward files
cp -ra ${BACKWARD_DIR}/Mapping ./
cp -a ${BACKWARD_DIR}/backward.py ./
cp -a ${BACKWARD_DIR}/initram-v5.sh ./

## MANUAL STEP - MODIFY TOPOLOGY
# Delete or comment out ions and solvent. These are handled automatically.

# run Backward
./initram-v5.sh -f ${VROUTPUT} -o fg_em.gro -to amber -p topol.top -em 5000 -np 8
