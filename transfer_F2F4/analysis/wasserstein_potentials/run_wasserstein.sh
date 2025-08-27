#!/bin/bash

#REFDIR=/home/mason/oligo/distributions/F4_1/AA/dist_0-500ns
REFDIR=/home/mason/oligo/distributions/F2_1/AA/dist_0-500ns
SCRIPTDIR=/home/mason/oligo/codes
ROOTDIR=$PWD

for i in {1..5}
##for i in {1..2}
do
cd $ROOTDIR/step_00$i/dist
find . -name "*dist.new" -exec python3 $SCRIPTDIR/calc_wasserstein.py {} $REFDIR/{} >> wassersteinvals.txt \;
done


