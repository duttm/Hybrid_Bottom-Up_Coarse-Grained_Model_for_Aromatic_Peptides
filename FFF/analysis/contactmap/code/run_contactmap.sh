#!/bin/bash

# accept a gro file with some fff peptides,
# calculate contacts,
# plot a little contour map

INPUT_FILE=$1
MODELNO=$2
PEPCT=$3
RES_PER_MOL=$4
MODELTYPE=$5

python3 /home/mason/fff/contactmap/code/contact_map.py $INPUT_FILE $PEPCT $RES_PER_MOL

#user_input_file = sys.argv[1]
#NUMMOL = int(sys.argv[2])
#NUMRESMOL = int(sys.argv[3])

python3 /home/mason/fff/contactmap/code/plot_contact_map.py contactmap.txt $MODELNO

mv contacts.txt contacts-${MODELNO}${MODELTYPE}${PEPCT}.txt
mv contactmap.txt contactmap-${MODELNO}${MODELTYPE}${PEPCT}.txt
mv contactmap.png contactmap-${MODELNO}${MODELTYPE}${PEPCT}.png
