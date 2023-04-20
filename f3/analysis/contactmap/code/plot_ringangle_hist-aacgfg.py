#!/usr/bin/env python3

import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import sys
mpl.use('svg')
import seaborn as sns

np.set_printoptions(threshold=sys.maxsize)

MODELNO=sys.argv[1]
PEPCT=sys.argv[2]

with open("ringcontacts-"+MODELNO+"aa"+str(PEPCT)+".txt") as f:
    angledata_aa = np.loadtxt(f,skiprows=1)
with open("ringcontacts-"+MODELNO+"cg"+str(PEPCT)+".txt") as g:
    angledata_cg = np.loadtxt(g,skiprows=1)
with open("ringcontacts-"+MODELNO+"fg"+str(PEPCT)+".txt") as h:
    angledata_fg = np.loadtxt(h,skiprows=1)

plt.hist(angledata_aa[:,5], bins="auto", histtype="step", density=False)
plt.hist(angledata_cg[:,5], bins="auto", histtype="step", density=False)
plt.hist(angledata_fg[:,5], bins="auto", histtype="step", density=False)
plt.xlim(0,180)
plt.title("Distribution of Ring Contact Angles")
plt.legend(["aa","cg","fg"])
plt.tight_layout()
plt.savefig('ringhist-aacgfg.png')
