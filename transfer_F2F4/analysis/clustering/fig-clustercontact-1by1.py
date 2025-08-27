#!/usr/bin/env python3

import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import sys
mpl.use('svg')
import seaborn as sns
import sys
import re
import os

np.set_printoptions(threshold=sys.maxsize)
np.seterr(divide = 'ignore') 

mycmap = sns.color_palette("plasma_r",as_cmap=True)
mycmap.set_under('w')
plt.set_cmap(mycmap)

DATA1DIR=sys.argv[1] # ~/exdrive/oligo/F2/CG/F2_64-1
if DATA1DIR=='.': DATA1DIR=os.getcwd()

p = re.compile(r".*(F[24](a[0-9]d[0-9])?_[0-9]+-?[0-9]+?).*")
SYSNAME = p.match(DATA1DIR).group(1)
print(f'sysname is {SYSNAME}')

PEPCT=int(sys.argv[2]) # 64
TMAX_ns = int(sys.argv[3])
tmax = TMAX_ns* 1000
NUM_RES = int(sys.argv[4])

CONTACTSUBDIR="contacts-0-25"
CLUSTERSUBDIR="cluster-0-25"

CONTACTFILE1="numcont_MCMC.xvg"
CONTACTFILE2="numcont_SCSC.xvg"
CONTACTFILE3="numcont_MCSC.xvg"
CONTACTFILE4="numcont_AMDAMD.xvg"
CONTACTFILE5="numcont_NH3COO.xvg"
CLUSTERFILE="nclust-0-25.xvg"

with open(f"{DATA1DIR}/{CONTACTSUBDIR}/{CONTACTFILE1}") as f11:
    data11 = np.loadtxt(f11,skiprows=0,usecols=(0,1),comments=["@","#"])
with open(f"{DATA1DIR}/{CONTACTSUBDIR}/{CONTACTFILE2}") as f12:
    data12 = np.loadtxt(f12,skiprows=0,usecols=(0,1),comments=["@","#"])
with open(f"{DATA1DIR}/{CONTACTSUBDIR}/{CONTACTFILE3}") as f13:
    data13 = np.loadtxt(f13,skiprows=0,usecols=(0,1),comments=["@","#"])
with open(f"{DATA1DIR}/{CONTACTSUBDIR}/{CONTACTFILE4}") as f14:
    data14 = np.loadtxt(f14,skiprows=0,usecols=(0,1),comments=["@","#"])
with open(f"{DATA1DIR}/{CONTACTSUBDIR}/{CONTACTFILE5}") as f15:
    data15 = np.loadtxt(f15,skiprows=0,usecols=(0,1),comments=["@","#"])
with open(f"{DATA1DIR}/{CLUSTERSUBDIR}/{CLUSTERFILE}") as f16:
    data16 = np.loadtxt(f16,skiprows=0,usecols=(0,1),comments=["@","#"])

def moving_average(x, w):
    return np.convolve(x, np.ones(w), 'valid') / w

mawindow = 100
data11ma = moving_average(data11[:,1],mawindow)
data12ma = moving_average(data12[:,1],mawindow)
data13ma = moving_average(data13[:,1],mawindow)
data14ma = moving_average(data14[:,1],mawindow)
data15ma = moving_average(data15[:,1],mawindow)
data16ma = moving_average(data16[:,1],mawindow)

#fig, ax = plt.subplots(nrows=1, ncols=1, sharex=True, figsize=(6.4,4.8))
fig, ax = plt.subplots(nrows=1, ncols=1, sharex=True, figsize=(4,4))

plotalpha=0.7

#NUM_RES = 4
NUM_CA  = NUM_RES
NUM_AMD = NUM_RES - 1

# minimum contact count will be the expected number of intrapeptide contacts
# should check single peptide case to see what we get here
#AMDmin=3*PEPCT
AMDmin=0
NH3min=0
COOmin=0
NH3COOmin=0
#MCmin=2*PEPCT
#SCmin=32*PEPCT
#MCSCmin=11*PEPCT
MCmin=0
SCmin=0
MCSCmin=0

# max number is if somehow they are all in contact which of course can't happen
MCmax = PEPCT*NUM_CA * (PEPCT*NUM_CA-1) / 2 
SCmax = PEPCT*3*NUM_RES * (PEPCT*3*NUM_RES-1) / 2
MCSCmax = PEPCT*NUM_CA * PEPCT*3*NUM_RES / 2
AMDmax = PEPCT*NUM_AMD * (PEPCT*NUM_AMD-1) / 2
NH3max = PEPCT * (PEPCT-1) / 2
COOmax = PEPCT * (PEPCT-1) / 2
NH3COOmax = PEPCT * PEPCT / 2

def normalize_data(data_1col, min_est, max_est):
    return (data_1col - min_est) / (max_est - min_est)

data11[:,1] = normalize_data(data11[:,1], MCmin, MCmax)
data12[:,1] = normalize_data(data12[:,1], SCmin, SCmax)
data13[:,1] = normalize_data(data13[:,1], MCSCmin, MCSCmax)
data14[:,1] = normalize_data(data14[:,1], AMDmin, AMDmax)
data15[:,1] = normalize_data(data15[:,1], NH3COOmin, NH3COOmax)

plotargs={
    'alpha':plotalpha,
#    'ls':'--',
    'lw':5
}

ax.plot(data11[:tmax,0],data11[:tmax,1],':',label='MC-MC',**plotargs)
ax.plot(data12[:tmax,0],data12[:tmax,1],':',label='SC-SC',alpha=plotalpha)
ax.plot(data13[:tmax,0],data13[:tmax,1],':',label='MC-SC',alpha=plotalpha)
ax.plot(data14[:tmax,0],data14[:tmax,1],':',label='AMD-AMD',alpha=plotalpha)
ax.plot(data15[:tmax,0],data15[:tmax,1],':',label='NH3-COO',alpha=plotalpha)

ax.set_xlim([0,tmax])
axmaxy = np.max(np.concatenate((data11[:tmax,1],data12[:tmax,1],data14[:tmax,1],data15[:tmax,1],data15[:tmax,1])))
print(f'axmaxy is {axmaxy}')
ax.set_ylim([0,np.round(axmaxy+.01,2)])

ax2 = ax.twinx()
ax2.plot(data16ma[:tmax],'k-',label='clusters')
ax2.set_ylim([0,80])

#ax2.annotate(f"F4_{PEPCT}-{DATA1DIR.split('-')[-1]}",(50,28),bbox=dict(boxstyle="square,pad=0.3",
#                      fc="lemonchiffon", ec="maroon", lw=1))

#fig.text(0.04,0.5, "Normalized Contact Count", ha="center", va="center", rotation=90)
ax.set_ylabel("Normalized Contact Count")
#fig.text(0.95,0.5, "Cluster Count, 100-sample moving average", ha="center", va="center", rotation=90)
ax2.set_ylabel("Cluster Count, 100-sample moving average")

h1, l1 = ax.get_legend_handles_labels()
h2, l2 = ax2.get_legend_handles_labels()
ax.legend(h1+h2, l1+l2, loc='upper center', bbox_to_anchor=(0.5,1.125), 
    ncols=6, columnspacing=1, handletextpad=0.5)
ax.set_title(f"Cluster and Contact Counts in {PEPCT} peptide systems", pad=40)

#plt.tight_layout()
plt.savefig(f"clustercontacts-{SYSNAME}-{str(tmax)}steps.png")


