#!/usr/bin/env python3

import matplotlib.pyplot as plt
#import matplotlib as mpl
import numpy as np
import sys
import os
#mpl.use('svg') # svg backend for output to svg
#mpl.use('GTK4Agg') # gui backend for debugging
import seaborn as sns
np.set_printoptions(threshold=sys.maxsize)
from cycler import cycler


#ROOTDIR = os.getcwd()
DATADIR=''
MYFILE=sys.argv[1]

dtypes=(str,str)
pairs = np.loadtxt(MYFILE,dtype=dtypes)
#print(pairs[1,:])

with open(MYFILE) as f:
    lines=[]
    for idx,line in enumerate(f):
        linedata = line.split()
#        print(linedata[1])
#        print(linedata[0]+'.dist.new ../table_'+linedata[1]+'.xvg '+linedata[0])
        command = str(f'python3 /home/mason/code/Mason_Hooten_Research_Codes/plotting/plot_two_normalized_lines.py {linedata[0]}.dist.new ../table_{linedata[1]}.xvg {linedata[0]}')
#        if idx==0: 
#            print(command)
        os.system(command)

#with open(MYFILE) as f:
#    mystuff = f.read()
#print([i for i in mystuff])

#    
#def load_and_norm(filename):
#    mydata = np.loadtxt(filename, comments=('@','#'))
#    bounds = (mydata[mydata[:,1]!=0][0][0], mydata[mydata[:,1]!=0][-1][0])
#    simdatanorm = mydata[:,1] / np.max(mydata[:,1])
##    print(mydata)
##    print(mydata[:,0])
##    print(mydata[:,1])
#    normdata = np.column_stack((mydata[:,0],simdatanorm))
#    maxloc = mydata[mydata.argmax(axis=0)[1]][0]
#    return normdata, bounds, maxloc

##rePaired = sns.color_palette('Paired')[0:2]+sns.color_palette('Paired')[4:6]
#custom_cycler = (cycler(ls=['dotted', 'dotted']*2) + cycler(color=['red','blue']*2))
##cycler(color=rePaired) +
#                 

#fig,ax = plt.subplots(1,1,figsize=(6,4))
#ax.set_prop_cycle(custom_cycler)
#xlim = [None,None]
#for file in data:
#    filepath = DATADIR + file
#    normdata, bounds, maxloc = load_and_norm(filepath)
#    print(maxloc)
#    if xlim[0]:
#        if bounds[0] < xlim[0]: xlim[0] = bounds[0]
#    if xlim[1]: 
#        if bounds[1] < xlim[1]: xlim[1] = bounds[1]
#    ax.plot(normdata[:,0],normdata[:,1],alpha=0.5)

#ax.set_xlim(xlim)
##ax.set_xlim([10,30])
##ax.set_xlim([0,.75])
##ax.set_ylim([None,.4])
#plt.legend(['first line','second line'])
#plt.xlabel('$r$ [Angstroms]')
#plt.ylabel('$P(r)/P_{max}(r)$')
#plt.title(f'just two lines\npretty simple')
#plt.tight_layout()
##plt.show()
#plt.savefig(sys.argv[3]+'two_lines.png')


