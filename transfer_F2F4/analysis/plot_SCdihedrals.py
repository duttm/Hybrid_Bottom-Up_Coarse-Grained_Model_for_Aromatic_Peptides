#!/usr/bin/env python3

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

mpl.rcParams["lines.linewidth"]=1.8

DATADIR="/home/mason/exdrive/oligo/F4"
#SINGLE PEPTIDE
data11 = [
    'AA/F4_1/dist_SCdihedral/PHA1-CA1-CA2-PHA2.dist.new',
    'CG/F4_1/dist_SCdihedral/PHA1-CA1-CA2-PHA2.dist.new',
    'CG/M2_F4_1/dist_SCdihedral/SC11-BB1-BB2-SC12.dist.new',
    'CG/M3_F4_1/dist_SCdihedral/SC11-BB1-BB2-SC12.dist.new'
    ]
    
data12 = [
    'AA/F4_1/dist_SCdihedral/PHA2-CA2-CA3-PHA3.dist.new',
    'CG/F4_1/dist_SCdihedral/PHA2-CA2-CA3-PHA3.dist.new',
    'CG/M2_F4_1/dist_SCdihedral/SC12-BB2-BB3-SC13.dist.new',
    'CG/M3_F4_1/dist_SCdihedral/SC12-BB2-BB3-SC13.dist.new'
    ]

data13 = [
    'AA/F4_1/dist_SCdihedral/PHA3-CA3-CA4-PHA4.dist.new',
    'CG/F4_1/dist_SCdihedral/PHA3-CA3-CA4-PHA4.dist.new',
    'CG/M2_F4_1/dist_SCdihedral/SC13-BB3-BB4-SC14.dist.new',
    'CG/M3_F4_1/dist_SCdihedral/SC13-BB3-BB4-SC14.dist.new'
    ]
    
#MULTIPLE PEPTIDES
data21 = [
    'AA/F4_25/dist_SCdihedral/PHA1-CA1-CA2-PHA2.dist.new',
    'CG/F4a7d2_25/dist_SCdihedral/PHA1-CA1-CA2-PHA2.dist.new',
    'CG/M2_F4_32/dist_SCdihedral/SC11-BB1-BB2-SC12.dist.new',
    'CG/M3_F4_32/dist_SCdihedral/SC11-BB1-BB2-SC12.dist.new',
    ]

data22 = [
    'AA/F4_25/dist_SCdihedral/PHA2-CA2-CA3-PHA3.dist.new',
    'CG/F4a7d2_25/dist_SCdihedral/PHA2-CA2-CA3-PHA3.dist.new',
    'CG/M2_F4_32/dist_SCdihedral/SC12-BB2-BB3-SC13.dist.new',
    'CG/M3_F4_32/dist_SCdihedral/SC12-BB2-BB3-SC13.dist.new'
    ]

data23 = [
    'AA/F4_25/dist_SCdihedral/PHA3-CA3-CA4-PHA4.dist.new',
    'CG/F4a7d2_25/dist_SCdihedral/PHA3-CA3-CA4-PHA4.dist.new',
    'CG/M2_F4_32/dist_SCdihedral/SC13-BB3-BB4-SC14.dist.new',
    'CG/M3_F4_32/dist_SCdihedral/SC13-BB3-BB4-SC14.dist.new'
    ]

def readfromfile(thisfile):
    return np.loadtxt(thisfile, usecols=(0,1), comments=["@","#"])

def plotthisdatatothisaxis(thisdata,thisaxis):
    thisaxis.plot(thisdata[:,0],thisdata[:,1])

fig, ((ax1,ax2,ax3),(ax4,ax5,ax6)) = plt.subplots(nrows=2,ncols=3,figsize=(12,5), sharex=True)

for i in data11:
    mydata=readfromfile(f"{DATADIR}/{i}")
    plotthisdatatothisaxis(mydata,ax1)
for i in data12:
    mydata=readfromfile(f"{DATADIR}/{i}")
    plotthisdatatothisaxis(mydata,ax2)
for i in data13:
    mydata=readfromfile(f"{DATADIR}/{i}")
    plotthisdatatothisaxis(mydata,ax3)
for i in data21:
    mydata=readfromfile(f"{DATADIR}/{i}")
    plotthisdatatothisaxis(mydata,ax4)
for i in data22:
    mydata=readfromfile(f"{DATADIR}/{i}")
    plotthisdatatothisaxis(mydata,ax5)
for i in data23:
    mydata=readfromfile(f"{DATADIR}/{i}")
    plotthisdatatothisaxis(mydata,ax6)

ax1.legend(['AA','CG','M2','M3'])

for idx,ax in enumerate([ax1,ax2,ax3,ax4,ax5,ax6]):
    if idx in [1,2,4,5]:
        ax.tick_params(
            axis='y',          # changes apply to the x-axis
            which='both',      # both major and minor ticks are affected
            left=False,      # ticks along the bottom edge are off
            right=False,         # ticks along the top edge are off
            labelleft=False) # labels along the bottom edge are off
    ax.margins(x=0,y=0.05)

ax1.set_yticks([0])
ax4.set_yticks([0])

for idx,ax in enumerate([ax4,ax5,ax6]):
    ax.set_xticks([-3,-2,-1,0,1,2,3])

ax1.set_title("SC1-SC2",fontsize='xx-large',pad=10)
ax2.set_title("SC2-SC3",fontsize='xx-large',pad=10)
ax3.set_title("SC3-SC4",fontsize='xx-large',pad=10)

#ax1.set_ylabel(
#    "Frequency",rotation=90,fontsize='large',
#    horizontalalignment='right',verticalalignment='center',
#    labelpad=5)
#ax4.set_ylabel(
#    "Multiple\nPeptides",rotation=90,fontsize='large',
#    horizontalalignment='right',verticalalignment='center',
#    labelpad=5)

fig.text(.12,.5,"Frequency", ha='right', va='center',rotation=90,fontsize="large")

fig.text(.09,.705,"Single\nPeptide", ha='right', va='center',rotation=0,fontsize="xx-large")
fig.text(.09,.275,"Multiple\nPeptides", ha='right', va='center',rotation=0,fontsize="xx-large")

fig.text(.55,.03,"Dihedral angle [radians]", ha='center', va='center',rotation=0,fontsize="large")

plt.subplots_adjust(left=.14,top=.9,bottom=0.1,right=.99,wspace=.04,hspace=.09)

#plt.tight_layout()
#plt.show()
plt.savefig("fig-SCdihedrals.png",dpi=300)

