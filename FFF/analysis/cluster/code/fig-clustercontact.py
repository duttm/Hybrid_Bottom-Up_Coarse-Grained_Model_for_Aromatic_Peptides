#!/usr/bin/env python3

import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import sys
mpl.use('svg')
import seaborn as sns

np.set_printoptions(threshold=sys.maxsize)
np.seterr(divide = 'ignore') 

mycmap = sns.color_palette("plasma_r",as_cmap=True)
mycmap.set_under('w')
plt.set_cmap(mycmap)

MODELNO=sys.argv[1]
PEPCT= int(sys.argv[2])

with open("numcont-"+MODELNO+"cg32-MC.xvg") as f1:
    data1 = np.loadtxt(f1,skiprows=0,usecols=(0,1),comments=["@","#"])
with open("numcont-"+MODELNO+"cg32-SC.xvg") as f2:
    data2 = np.loadtxt(f2,skiprows=0,usecols=(0,1),comments=["@","#"])
with open("numcont-"+MODELNO+"cg32-MCSC.xvg") as f3:
    data3 = np.loadtxt(f3,skiprows=0,usecols=(0,1),comments=["@","#"])
with open("nclust-"+MODELNO+"cg32.xvg") as f4:
    data4 = np.loadtxt(f4,skiprows=0,usecols=(0,1),comments=["@","#"])


with open("numcont-"+MODELNO+"cg32-AMD.xvg") as f5:
    data5 = np.loadtxt(f5,skiprows=0,usecols=(0,1),comments=["@","#"])
with open("numcont-"+MODELNO+"cg32-NH3.xvg") as f6:
    data6 = np.loadtxt(f6,skiprows=0,usecols=(0,1),comments=["@","#"])
with open("numcont-"+MODELNO+"cg32-COO.xvg") as f7:
    data7 = np.loadtxt(f7,skiprows=0,usecols=(0,1),comments=["@","#"])
with open("numcont-"+MODELNO+"cg32-COO-NH3.xvg") as f8:
    data8 = np.loadtxt(f8,skiprows=0,usecols=(0,1),comments=["@","#"])


def moving_average(x, w):
    return np.convolve(x, np.ones(w), 'valid') / w

data4ma = moving_average(data4[:,1],100)

fig, ax1 = plt.subplots()

tmax = 20000

## plot log counts
#ax1.plot(data1[:tmax,0],np.log(data1[:tmax,1]),':',label='MC')
#ax1.plot(data2[:tmax,0],np.log(data2[:tmax,1]),':',label='SC')
#ax1.plot(data3[:tmax,0],np.log(data3[:tmax,1]),':',label='MCSC')
#ax1.plot(data5[:tmax,0],np.log(data5[:tmax,1]),':',label='AMD')
#ax1.plot(data6[:tmax,0],np.log(data6[:tmax,1]),':',label='NH3')
#ax1.plot(data7[:tmax,0],np.log(data7[:tmax,1]),':',label='COO')
#ax1.plot(data8[:tmax,0],np.log(data8[:tmax,1]),':',label='NH3-COO')

# plot scaled counts
# 

AMDmin=2*PEPCT
NH3min=0
COOmin=0
NH3COOmin=0
plotalpha=0.7

MCmax = PEPCT*3 * (PEPCT*3-1)
if MODELNO=='1': 
    MCmin=6*PEPCT
    SCmax = PEPCT*3 * (PEPCT*3-1)
    MCSCmax = PEPCT*3 * PEPCT*3
    SCmin=0
    MCSCmin=3*PEPCT

if MODELNO=='2': 
    MCmin=2*PEPCT
    SCmax = PEPCT*9 * (PEPCT*9-1)
    MCSCmax = PEPCT*3 * PEPCT*9
    SCmin=18*PEPCT
    MCSCmin=11*PEPCT

AMDmax = PEPCT*2 * (PEPCT*2-1)
NH3max = PEPCT * (PEPCT-1)
COOmax = PEPCT * (PEPCT-1)
NH3COOmax = PEPCT * PEPCT

data1r = (data1[:tmax,1]-MCmin)/(MCmax-MCmin)
data2r = (data2[:tmax,1]-SCmin)/(SCmax-SCmin)
data3r = (data3[:tmax,1]-MCSCmin)/(MCSCmax-MCSCmin)
data5r = (data5[:tmax,1]-AMDmin)/(AMDmax-AMDmin)
data6r = (data6[:tmax,1]-NH3min)/(NH3max-NH3min)
data7r = (data7[:tmax,1]-COOmin)/(COOmax-COOmin)
data8r = (data8[:tmax,1]-NH3COOmin)/(NH3COOmax-NH3COOmin)

ax1.plot(data1[:tmax,0],data1r,':',label='MC',alpha=plotalpha)
ax1.plot(data2[:tmax,0],data2r,':',label='SC',alpha=plotalpha)
ax1.plot(data3[:tmax,0],data3r,':',label='MCSC',alpha=plotalpha)
ax1.plot(data5[:tmax,0],data5r,':',label='AMD',alpha=plotalpha)
#ax1.plot(data6[:tmax,0],data6r,':',label='NH3',alpha=plotalpha)
#ax1.plot(data7[:tmax,0],data7r,':',label='COO',alpha=plotalpha)
ax1.plot(data8[:tmax,0],data8r,':',label='NH3-COO',alpha=plotalpha)


#ax1.set_ylabel('log(#contacts)')
ax1.set_ylabel('#contacts / MAX(contacts)')
ax1.set_xlabel('sim frame / 1000')
#plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.05),
#          ncol=3, fancybox=True, shadow=True)
plt.legend(loc='upper left')
ax2 = ax1.twinx()
ax2.plot(data4[:tmax,0],data4ma[:tmax],'k-',label='clustercount')
ax2.set_ylim([-1,32])
ax2.set_ylabel('100-sample moving average(#clusters)')

#plt.legend()
fig.suptitle("Cluster and Contact Counts "+MODELNO+"cg32")

plt.tight_layout()
plt.savefig('clustercontacts-'+MODELNO+'cg32.png')


