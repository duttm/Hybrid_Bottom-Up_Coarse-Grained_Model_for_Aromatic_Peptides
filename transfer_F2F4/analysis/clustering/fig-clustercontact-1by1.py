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

mpl.rcParams["lines.linewidth"]=1.8

def normalize_data(data_1col, min_est, max_est):
    return (data_1col - min_est) / (max_est - min_est)

def moving_average(x, w):
    return np.convolve(x, np.ones(w), 'valid') / w

def makeplotfromdatadir(DATADIR,PEPCT,TMAX_ns,NUM_RES,ax):
    p = re.compile(r".*(F[24](a[0-9]d[0-9])?_[0-9]+-?[0-9]+).*")
    SYSNAME = p.match(DATADIR).group(1)
    print(f'sysname is {SYSNAME}')

    PEPCT=int(PEPCT) # 64
    tmax = int(TMAX_ns* 1000)
    NUM_RES = int(NUM_RES)

    CONTACTSUBDIR="contacts-0-25"
    CLUSTERSUBDIR="cluster-0-25"

    CONTACTFILE1="numcont_MCMC.xvg"
    CONTACTFILE2="numcont_SCSC.xvg"
    CONTACTFILE3="numcont_MCSC.xvg"
    CONTACTFILE4="numcont_AMDAMD.xvg"
    CONTACTFILE5="numcont_NH3COO.xvg"
    CLUSTERFILE="nclust-0-25.xvg"

    with open(f"{DATADIR}/{CONTACTSUBDIR}/{CONTACTFILE1}") as f1:
        data1 = np.loadtxt(f1,skiprows=0,usecols=(0,1),comments=["@","#"])
    with open(f"{DATADIR}/{CONTACTSUBDIR}/{CONTACTFILE2}") as f2:
        data2 = np.loadtxt(f2,skiprows=0,usecols=(0,1),comments=["@","#"])
    with open(f"{DATADIR}/{CONTACTSUBDIR}/{CONTACTFILE3}") as f3:
        data3 = np.loadtxt(f3,skiprows=0,usecols=(0,1),comments=["@","#"])
    with open(f"{DATADIR}/{CONTACTSUBDIR}/{CONTACTFILE4}") as f4:
        data4 = np.loadtxt(f4,skiprows=0,usecols=(0,1),comments=["@","#"])
    with open(f"{DATADIR}/{CONTACTSUBDIR}/{CONTACTFILE5}") as f5:
        data5 = np.loadtxt(f5,skiprows=0,usecols=(0,1),comments=["@","#"])
    with open(f"{DATADIR}/{CLUSTERSUBDIR}/{CLUSTERFILE}") as f6:
        data6 = np.loadtxt(f6,skiprows=0,usecols=(0,1),comments=["@","#"])

    mawindow = 20
    data6ma = moving_average(data6[:,1],mawindow)

    NUM_CA  = NUM_RES
    NUM_AMD = NUM_RES - 1

    AMDmin=0
    NH3min=0
    COOmin=0
    NH3COOmin=0
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

    data1[:,1] = normalize_data(data1[:,1], MCmin, MCmax)
    data2[:,1] = normalize_data(data2[:,1], SCmin, SCmax)
    data3[:,1] = normalize_data(data3[:,1], MCSCmin, MCSCmax)
    data4[:,1] = normalize_data(data4[:,1], AMDmin, AMDmax)
    data5[:,1] = normalize_data(data5[:,1], NH3COOmin, NH3COOmax)
    
    line1, = ax.plot(data1[:tmax,0],data1[:tmax,1],label='MC-MC')
    line2, = ax.plot(data2[:tmax,0],data2[:tmax,1],label='SC-SC')
    line3, = ax.plot(data3[:tmax,0],data3[:tmax,1],label='MC-SC')
    line4, = ax.plot(data4[:tmax,0],data4[:tmax,1],label='AMD-AMD')
    line5, = ax.plot(data5[:tmax,0],data5[:tmax,1],label='NH3-COO')

    ax.set_xlim([0,tmax])

    axsecond = ax.twinx()
    line6, = axsecond.plot(data6ma[:tmax],'k--',label='clusters')
#    line6, = axsecond.plot(data6[:tmax,0],data6[:tmax,1],'k--',label='clusters')
    if ax==ax4:
        ax.legend(
        handles=[line1,line2,line3,line4,line5,line6],
        loc='center',bbox_to_anchor=(0.8,.31)
        )
    return axsecond

fig, ((ax1,ax2),(ax3,ax4)) = plt.subplots(nrows=2,ncols=2,figsize=(10,7.5))

#makeplotfromdatadir(DATADIR,PEPCT,TMAX_ns,NUM_RES,ax):
ax12 = makeplotfromdatadir("/home/mason/exdrive/oligo/F2/CG/F2a6d2_32",32, 2.5,  2,ax1)
ax22 = makeplotfromdatadir("/home/mason/exdrive/oligo/F4/CG/F4a7d2_32",32, .2,  4,ax2)
ax32 = makeplotfromdatadir("/home/mason/exdrive/oligo/F2/CG/F2_64",    64, 2.5,  2,ax3)
ax42 = makeplotfromdatadir("/home/mason/exdrive/oligo/F4/CG/F4_64-10", 64, .2,  4,ax4)

ax1.annotate("micelles",(.2,.9),xycoords='axes fraction',fontsize="large")
ax2.annotate("rod",     (.2,.9),xycoords='axes fraction',fontsize="large")
ax3.annotate("micelles",(.2,.9),xycoords='axes fraction',fontsize="large")
ax4.annotate("network", (.2,.9),xycoords='axes fraction',fontsize="large")

#ax1.set_title("F2",fontsize='xx-large',pad=20)
#ax2.set_title("F4",fontsize='xx-large',pad=20)
#ax1.set_title("F2",fontsize='large')
#ax2.set_title("F4",fontsize='large')

#ax1.set_ylabel(
#    "32 Peptides",rotation=0,fontsize='xx-large',
#    horizontalalignment='right',verticalalignment='center',
#    labelpad=10)
#ax3.set_ylabel(
#    "64 Peptides",rotation=0,fontsize='xx-large',
#    horizontalalignment='right',verticalalignment='center',
#    labelpad=10)

#ax1.set_ylabel(
#    "Normalized contact counts", fontsize="large")#,rotation=90,#fontsize='xx-large',
##    horizontalalignment='right',verticalalignment='center',)
##    labelpad=10)
#ax3.set_ylabel(
#    "Normalized contact counts", fontsize="large")#,rotation=90,#fontsize='xx-large',
##    horizontalalignment='right',verticalalignment='center',)
##    labelpad=10)
#ax22.set_ylabel("Moving average cluster counts", fontsize="large")
#ax42.set_ylabel("Moving average cluster counts", fontsize="large")

fig.text(.1,.5,"Normalized contact counts", ha='center', va='center',rotation=90,fontsize="large")
fig.text(.95,.5,"Moving average cluster counts", ha='center', va='center',rotation=90,fontsize="large")
fig.text(.53,.03,"Simulated time [ps]", ha='center', va='center',rotation=0,fontsize="large")

fig.text(.05,.75,"32 peptides", ha='center', va='center',rotation=90,fontsize="xx-large")
fig.text(.05,.25,"64 peptides", ha='center', va='center',rotation=90,fontsize="xx-large")

fig.text(.32,.95,"F2 systems", ha='center', va='center',rotation=0,fontsize="xx-large")
fig.text(.75,.95,"F4 systems", ha='center', va='center',rotation=0,fontsize="xx-large")

#plt.suptitle("Contacts and Cluster Counts",fontsize="xx-large")

plt.subplots_adjust(left=.15,top=.9,bottom=0.1,right=.9,wspace=.3,hspace=.18)
#plt.tight_layout()
plt.savefig(f"fig-clustercontacts.png")


