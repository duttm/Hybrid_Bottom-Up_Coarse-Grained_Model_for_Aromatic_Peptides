#!/usr/bin/env python3

import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import sys
mpl.use('svg')
import seaborn as sns

np.set_printoptions(threshold=sys.maxsize)

#MODELNO=sys.argv[1]
PEPCT= str(sys.argv[1])

DOF1 = sys.argv[2]
DOF2 = sys.argv[3]

AA_1_DIST="/home/mason/fff/aa/fff"+PEPCT+"/dist_first-cg_300-500ns/"
CG_1_DIST="/home/mason/fff/first_cg/cg"+PEPCT+"_211111/dist-5-end/"

AA_2_DIST="/home/mason/fff/aa/fff"+PEPCT+"/dist_second-cg_300-500ns/"
CG_2_DIST="/home/mason/fff/second_cg/cg_simulation/cg"+PEPCT+"/dist-5-end/"

#DOF="bb-end-end-dist"

with open(AA_1_DIST+DOF1+".dist.new") as f1:
    data_aa1= np.loadtxt(f1,skiprows=0,usecols=(0,1))
with open(CG_1_DIST+DOF1+".dist.new") as g1:
    data_cg1= np.loadtxt(g1,skiprows=0,usecols=(0,1))

with open(AA_2_DIST+DOF2+".dist.new") as f2:
    data_aa2 = np.loadtxt(f2,skiprows=0,usecols=(0,1))
with open(CG_2_DIST+DOF2+".dist.new") as g2:
    data_cg2 = np.loadtxt(g2,skiprows=0,usecols=(0,1))

fig, (ax0, ax1, ax2) = plt.subplots(nrows=3, ncols=1, sharex=True, figsize=(6, 12))

##angles
#left=0
#right=3.14
#top=5
##lengths
left=0.3
right=1.0
top=20
bottom=-1

ax0.set_title("AR1 vs AA")
ax0.set_xlim(left,right)
ax0.set_ylim(bottom,top)
ax0.plot(data_aa1[:,0], data_aa1[:,1])
ax0.plot(data_cg1[:,0], data_cg1[:,1],"-.")
ax0.legend(['AA','CG'])

ax1.set_title("AR3 vs AA")
ax1.plot(data_aa2[:,0], data_aa2[:,1])
ax1.plot(data_cg2[:,0], data_cg2[:,1],"-.")
ax1.set_ylim(bottom,top)
ax1.legend(['AA','CG'])

ax2.set_title("CG Residuals vs AA")
ax2.plot(data_aa1[:,0], (data_cg1[:,1]-data_aa1[:,1]),"m--")
ax2.plot(data_aa2[:,0], (data_cg2[:,1]-data_aa2[:,1]),"k:")
ax2.set_ylim(-top,top)
ax2.legend(['AR1','AR3'])

fig.suptitle("Distribution Comparison - "+PEPCT+" Peptides\n"+DOF1+" vs "+DOF2+"\n")
plt.tight_layout()
plt.savefig('conformhist'+PEPCT+'.png')
