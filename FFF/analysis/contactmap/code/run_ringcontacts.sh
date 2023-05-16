#!/bin/bash

# accept a gro file with some fff peptides,
# pare it down to atom triplets representing the side chain rings,
# measure ring contacts with rings.py,
# plot a little histogram

INPUT_FILE=$1
PEP_CT=$2
MODELTYPE=$3

# for AA files, get 3 carbons from each ring
grep -e 'PH*.*C[GE]' -e '^[ ]*[0-9]\.[0-9]\+[ ]*[0-9].*' $INPUT_FILE > ringatoms.txt

# for CG files, get the 3 side chain beads
#grep -e 'PH*' $INPUT_FILE > ringatoms.txt

# even better, get the 3 beads and the box vector
#grep -e 'PH*' -e '^[ ]*[0-9]\.[0-9]\+[ ]*[0-9].*' $INPUT_FILE > ringatoms.txt

python3 /home/mason/fff/contactmap/code/ring_contacts.py ringatoms.txt $PEP_CT

python3 /home/mason/fff/contactmap/code/plot_ringangle_hist.py ringcontacts.txt

#mv ringcontacts.txt ringcontacts-${MODELNO}${MODELTYPE}${PEPCT}.txt
#mv ringhist.png ringhist-${MODELNO}${MODELTYPE}${PEPCT}.png
