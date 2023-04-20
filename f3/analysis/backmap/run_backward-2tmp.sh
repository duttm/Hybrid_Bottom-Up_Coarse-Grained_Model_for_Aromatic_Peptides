#!/bin/sh

INPUT_FILE=2cg32_5ns-end_dt5ns8.gro
#INPUT_FILE=table.gro
#INPUT_FILE=2cg32input-conf.gro
NUM_BEADS=512
BEADS_PER_MOL=16
NUM_MOL=32
VRINPUT=${NUM_MOL}_RESFFF.gro
VROUTPUT=${NUM_MOL}_CG_rewrite.gro

BACKWARD_DIR=/home/mason/fff/backmap/backward-v5

sed -e 's/RES/FFF/g' $INPUT_FILE > $VR_INPUT

##Some pre-processing: Use python votca_reader.py cg8_aa10.gro <number of frames> <number of beads> <number of beads in 1 molecule> <tital number of peptides> <number of beads in 1 molecule> <number of ions>
cp -a ${BACKWARD_DIR}/votca_reader-2.py ./votca_reader.py
python3 votca_reader.py ${INPUT_FILE} 1 ${NUM_BEADS} ${BEADS_PER_MOL} ${NUM_MOL} ${BEADS_PER_MOL} 0

# copy Backward files
cp -ra ${BACKWARD_DIR}/Mapping ./
cp -a ${BACKWARD_DIR}/backward.py ./
cp -a ${BACKWARD_DIR}/initram-v5.sh ./
cp -a ${BACKWARD_DIR}/fff-second.amber.map ./Mapping/fff.amber.map
cp -a ${BACKWARD_DIR}/topol-second.top ./topol.top
cp -a ${BACKWARD_DIR}/posre.itp ./

## MANUAL STEP - MODIFY TOPOLOGY
# Delete or comment out ions and solvent. These are handled automatically.

# run Backward (Wasenaar 2014)
./initram-v5.sh -f ${VROUTPUT} -o fg_em.gro -to amber -p topol.top -em 5000 -np 4
