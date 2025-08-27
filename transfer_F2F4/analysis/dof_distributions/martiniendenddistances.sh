#!/bin/bash
# calculate peptide end-to-end distances for a martini structure with gmx tools

# make index file to measure backbone end-to-end distance with gmx distance
# list the first and fourth BB bead as TARGETATOMS
# make a line to feed make_ndx like "a 1" for each of those
# then run make_ndx
TARGETATOMS=`grep -e "^\s\+[14]PHE.*BB" md.gro | awk '{print $3}' | tr '\n/' ' '`
ADDLINES=`printf "a %s %s \\n" $TARGETATOMS`
echo "$ADDLINES"
printf "%s \n" "$ADDLINES" "q" | gmx make_ndx -f md.tpr

# calculate distances with that new index file
PAIRCOUNT=`echo "$ADDLINES" | wc -l`
INDEXEND=$((`grep -e '\[' index.ndx | wc -l` - 1))
INDEXSTART=$((INDEXEND - PAIRCOUNT + 2))
for i in $(seq $INDEXSTART $INDEXEND)
do 
printf "%s \n" "$i" 
done | gmx distance -f md.xtc -s md.tpr -n index.ndx -oh disthist.xvg -len 0.7 -tol 1 -b 5000 > enddist.txt 2>&1
