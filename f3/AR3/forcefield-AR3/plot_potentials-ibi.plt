#!/usr/bin/gnuplot
# looks ok with gnuplot 5.2

# clear all plot settings.
# this does not clear the current figure, i don't know how to do that yet.
reset

# sets a terminal suitable for plotting a 3x7 array of plots
# set terminal wxt size 800,400 enhanced font 'Verdana,6' persist
set terminal pngcairo size 1600,800 enhanced font 'Verdana,10'


# borders make the multiplot look too busy
unset border

# extra tics do too. this makes it so they only appear on the axes
set tics nomirror
#set xtics 0.2
#set ytics 5

# if tics don't do it for you then you can comment above and uncomment this one
# unset tics

# no labels
unset xlabel
unset ylabel

# but hey, options!
#set xlabel 'x'
#set ylabel 'y'

# yes x axis, yes line at x=1.2, no title
set xzeroaxis linetype -1 linewidth 1
#set arrow from 1.2, graph 0 to 1.2, graph 1 nohead dashtype 2
set key noautotitle

# bonds
set output 'bonds.png'
set multiplot layout 3,3
set xrange [0:1.2]
set yrange [-10:10]

set label 1 'F1B1' at graph 0.0,0.9
plot 'table_b1.xvg' using 1:2 with lines

set label 1 'NB1' at graph 0.0,0.9
plot 'table_b2.xvg' using 1:2 with lines

set label 1 'B1A1' at graph 0.0,0.9
plot 'table_b3.xvg' using 1:2 with lines

set label 1 'A1B2' at graph 0.0,0.9
plot 'table_b4.xvg' using 1:2 with lines

set label 1 'B2F2' at graph 0.0,0.9
plot 'table_b5.xvg' using 1:2 with lines

set label 1 'B2A2' at graph 0.0,0.9
plot 'table_b6.xvg' using 1:2 with lines 

set label 1 'A2B3' at graph 0.0,0.9
plot 'table_b7.xvg' using 1:2 with lines 

set label 1 'B3F3' at graph 0.0,0.9
plot 'table_b8.xvg' using 1:2 with lines 

set label 1 'B3C' at graph 0.0,0.9
plot 'table_b9.xvg' using 1:2 with lines 

unset multiplot

# angles
set output 'angles.png'
set multiplot layout 3,4
set xrange [0:180]
set yrange [-2:30]

set label 1 'F1B1N' at graph 0.0,0.9
plot 'table_a21.xvg' using 1:2 with lines 
#
set label 1 'F1B1A1' at graph 0.0,0.9
plot 'table_a22.xvg' using 1:2 with lines 
#
set label 1 'NB1A1' at graph 0.0,0.9
plot 'table_a23.xvg' using 1:2 with lines 
#
set label 1 'B1A1B2' at graph 0.0,0.9
plot 'table_a24.xvg' using 1:2 with lines 
#
set label 1 'A1B2F2' at graph 0.0,0.9
plot 'table_a25.xvg' using 1:2 with lines 
#
set label 1 'A1B2A2' at graph 0.0,0.9
plot 'table_a26.xvg' using 1:2 with lines 
#
set label 1 'B2A2B3' at graph 0.0,0.9
plot 'table_a27.xvg' using 1:2 with lines 
#
set label 1 'F2B2A2' at graph 0.0,0.9
plot 'table_a28.xvg' using 1:2 with lines 
#
set label 1 'A2B3F3' at graph 0.0,0.9
plot 'table_a29.xvg' using 1:2 with lines 
#
set label 1 'A2B3C' at graph 0.0,0.9
plot 'table_a30.xvg' using 1:2 with lines 
#
set label 1 'F3B3C' at graph 0.0,0.9
plot 'table_a31.xvg' using 1:2 with lines 

unset multiplot

# dihedrals
set output 'dihedrals.png'
set multiplot layout 3,3
set xrange [-180:180]
set yrange [-2:25]

#
set label 1 'F1B1A1B2' at graph 0.0,0.9
plot 'table_d32.xvg' using 1:2 with lines 
#
set label 1 'NB1A1B2' at graph 0.0,0.9
plot 'table_d33.xvg' using 1:2 with lines 
#
set label 1 'B1A1B2F2' at graph 0.0,0.9
plot 'table_d34.xvg' using 1:2 with lines 
#
set label 1 'B1A1B2A2' at graph 0.0,0.9
plot 'table_d35.xvg' using 1:2 with lines 
#
set label 1 'A1B2A2B3' at graph 0.0,0.9
plot 'table_d36.xvg' using 1:2 with lines 
#
set label 1 'F2B2A2B3' at graph 0.0,0.9
plot 'table_d37.xvg' using 1:2 with lines 
#
set label 1 'B2A2B3F3' at graph 0.0,0.9
plot 'table_d38.xvg' using 1:2 with lines 
#
set label 1 'B2A2B3C' at graph 0.0,0.9
plot 'table_d39.xvg' using 1:2 with lines 

unset multiplot

# nonbonds
set output 'nonbonds.png'
set multiplot layout 3,5
set xrange [0.:1.2]
set yrange [-30:10]

set label 1 'AMD-AMD' at graph 0.0,0.9
plot 'table_AMD_AMD.xvg' using 1:6 with lines
#
set label 1 'CAB-AMD' at graph 0.0,0.9
plot 'table_CAB_AMD.xvg' using 1:6 with lines
#
set label 1 'CAB-CAB' at graph 0.0,0.9
plot 'table_CAB_CAB.xvg' using 1:6 with lines
#
set label 1 'CAB-COO' at graph 0.0,0.9
plot 'table_CAB_COO.xvg' using 1:6 with lines
#
set label 1 'CAB-NH3' at graph 0.0,0.9
plot 'table_CAB_NH3.xvg' using 1:6 with lines
#
set label 1 'COO-AMD' at graph 0.0,0.9
plot 'table_COO_AMD.xvg' using 1:6 with lines

set label 1 'COO-COO' at graph 0.0,0.9
plot 'table_COO_COO.xvg' using 1:6 with lines
#
set label 1 'NH3-AMD' at graph 0.0,0.9
plot 'table_NH3_AMD.xvg' using 1:6 with lines
#
set label 1 'NH3-COO' at graph 0.0,0.9
plot 'table_NH3_COO.xvg' using 1:6 with lines
#
set label 1 'NH3-NH3' at graph 0.0,0.9
plot 'table_NH3_NH3.xvg' using 1:6 with lines
#
set label 1 'PHE-AMD' at graph 0.0,0.9
plot 'table_PHE_AMD.xvg' using 1:6 with lines
#
set label 1 'PHE-CAB' at graph 0.0,0.9
plot 'table_PHE_CAB.xvg' using 1:6 with lines

set label 1 'PHE-COO' at graph 0.0,0.9
plot 'table_PHE_COO.xvg' using 1:6 with lines
#
set label 1 'PHE-NH3' at graph 0.0,0.9
plot 'table_PHE_NH3.xvg' using 1:6 with lines
#
set label 1 'PHE-PHE' at graph 0.0,0.9
plot 'table_PHE_PHE.xvg' using 1:6 with lines

# apparently this is a gnuplot convention, always unset multiplot
unset multiplot

# waters
set output 'waters.png'
set multiplot layout 2,3
set xrange [0.:1.2]
set yrange [-150:100]

set label 1 'AMD-SOL' at graph 0.0,0.9
plot 'table_AMD_SOL.xvg' using 1:6 with lines
#
set label 1 'CAB-SOL' at graph 0.0,0.9
plot 'table_CAB_SOL.xvg' using 1:6 with lines
#
set label 1 'COO-SOL' at graph 0.0,0.9
plot 'table_COO_SOL.xvg' using 1:6 with lines
#
set label 1 'NH3-SOL' at graph 0.0,0.9
plot 'table_NH3_SOL.xvg' using 1:6 with lines
#
set label 1 'PHE-SOL' at graph 0.0,0.9
plot 'table_PHE_SOL.xvg' using 1:6 with lines
#
set label 1 'SOL-SOL' at graph 0.0,0.9
plot 'table_SOL_SOL.xvg' using 1:6 with lines

# apparently this is a gnuplot convention, always unset multiplot
unset multiplot
