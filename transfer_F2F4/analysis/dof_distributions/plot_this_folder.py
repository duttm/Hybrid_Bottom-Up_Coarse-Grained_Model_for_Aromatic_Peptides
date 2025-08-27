#!/usr/bin/env python3

import sys
import re
import os
from matplotlib import pyplot as plt
import numpy as np
import re
from pprint import pprint

def plot_these_files(suffix):
    allfiles=os.listdir()
#    myfiles = [ i for i in allfiles if 'dist.new' in i ]
    distre = re.compile('(.*)'+suffix+'$')
    for myfile in allfiles:
        basename_match = re.match(distre,myfile)
        if basename_match:
            print(basename_match)
            basename = basename_match.group(1)
#            if basename:
            print(basename)
            mydata = np.loadtxt(myfile,comments=('#','@'),usecols=(0,1))
            fig,ax = plt.subplots(1,1,figsize=(3,3))
            ax.plot(mydata[:,0],mydata[:,1])
            ax.set_title(basename)
            ax.set_xlabel('r')
            ax.set_ylabel('df')
#            ax.set_ylim([-.1,.5])
            ax.axhline(0)
            plt.tight_layout()
            fig.savefig(myfile+'.png')
            plt.close()
    

if __name__ == '__main__':
    suffix = sys.argv[1]
    plot_these_files(suffix)


