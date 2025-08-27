#!/usr/bin/python3
# developed as a notebook, not guaranteed to run nicely standalone
# %%
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
#import tkinter
import os
#mpl.use('tkagg')
import sys

mpl.rcParams["font.size"] = 18

MODEL = str(sys.argv[1]) # F2 or F4
PEPCT = str(sys.argv[2]) # 1 or 25

REF_FILE_EXT = '.dist.new'
DAT_FILE_EXT = '.dist.new'

DAT_DIR = f'/home/mason/exdrive/oligo/{MODEL}/CG/{MODEL}_{PEPCT}/dist-0-end'
REF_DIR = f'/home/mason/exdrive/oligo/{MODEL}/AA/{MODEL}_{PEPCT}/dist-300-500'

waters = ['NH3-SOL','CA-SOL','AMD-SOL','PHA-SOL','PHB-SOL','PHC-SOL',
        'COO-SOL','SOL-SOL']

nonbonds = ['NH3-NH3','NH3-CA','NH3-AMD','NH3-PHA','NH3-PHB',
        'NH3-PHC','NH3-COO','CA-CA','CA-AMD','CA-PHA','CA-PHB',
        'CA-PHC','CA-COO','AMD-AMD','AMD-PHA','AMD-PHB','AMD-PHC',
        'AMD-COO','PHA-PHA','PHA-PHB','PHA-PHC','PHA-COO','PHB-PHB',
        'PHB-PHC','PHB-COO','PHC-PHC','PHC-COO','COO-COO',]
nonbonds1 = nonbonds[0:9]
nonbonds2 = nonbonds[9:18]
nonbonds3 = nonbonds[18:27]
nonbonds4 = nonbonds[27:]

conform = ["term-end-end-dist", "bb-end-end-dist"]

if MODEL == 'F2':
    bonds = ["NH3-CA1", "CA1-PHA1", "PHA1-PHB1", "PHB1-PHC1", "PHC1-PHA1", 
        "CA1-AMD1", "AMD1-CA2", "CA2-PHA2", "PHA2-PHB2", "PHB2-PHC2", 
        "PHC2-PHA2", "CA2-COO"]
    bonds1 = bonds[0:9]
    bonds2 = bonds[9:]

    angles = ["NH3-CA1-AMD1", "CA1-AMD1-CA2", "NH3-CA1-PHA1", "CA1-PHA1-PHB1", 
        "CA1-PHA1-PHC1", "PHA1-PHB1-PHC1", "PHB1-PHC1-PHA1", "PHC1-PHA1-PHB1", 
        "AMD1-CA1-PHA1", "AMD1-CA2-PHA2", "CA2-PHA2-PHB2", "CA2-PHA2-PHC2", 
        "PHA2-PHB2-PHC2", "PHB2-PHC2-PHA2", "PHC2-PHA2-PHB2", "AMD1-CA2-COO", 
        "COO-CA2-PHA2"]
    angles1 = angles[0:9]
    angles2 = angles[9:]

    dihedrals = ["NH3-CA1-AMD1-CA2", "NH3-CA1-PHA1-PHB1", "NH3-CA1-PHA1-PHC1", 
        "CA1-PHA1-PHB1-PHC1", "CA1-PHA1-PHC1-PHB1", "AMD1-CA1-PHA1-PHB1", 
        "AMD1-CA1-PHA1-PHC1", "AMD1-CA2-PHA2-PHB2", "AMD1-CA2-PHA2-PHC2", 
        "CA2-AMD1-CA1-PHA1", "CA2-PHA2-PHB2-PHC2", "CA2-PHA2-PHC2-PHB2", 
        "CA1-AMD1-CA2-COO", "COO-CA2-PHA2-PHB2", "COO-CA2-PHA2-PHC2", 
        "CA1-AMD1-CA2-PHA2"]
    dihedrals1 = dihedrals[0:9]
    dihedrals2 = dihedrals[9:]

if MODEL == 'F4':
    bonds = ["NH3-CA1", "CA1-PHA1", "PHA1-PHB1", "PHB1-PHC1", "PHC1-PHA1", 
        "CA1-AMD1", "AMD1-CA2", "CA2-PHA2", "PHA2-PHB2", "PHB2-PHC2", 
        "PHC2-PHA2", "CA2-AMD2", "AMD2-CA3", "CA3-PHA3", "PHA3-PHB3", 
        "PHB3-PHC3", "PHC3-PHA3", "CA3-AMD3", "AMD3-CA4", "CA4-PHA4", 
        "PHA4-PHB4", "PHB4-PHC4", "PHC4-PHA4", "CA4-COO"]
    bonds1 = bonds[0:9]
    bonds2 = bonds[9:18]
    bonds3 = bonds[18:]

    angles = ["NH3-CA1-AMD1", "CA1-AMD1-CA2", "AMD1-CA2-AMD2", "CA2-AMD2-CA3", 
        "NH3-CA1-PHA1", "CA1-PHA1-PHB1", "CA1-PHA1-PHC1", "PHA1-PHB1-PHC1", 
        "PHB1-PHC1-PHA1", "PHC1-PHA1-PHB1", "AMD1-CA1-PHA1", "AMD1-CA2-PHA2", 
        "CA2-PHA2-PHB2", "CA2-PHA2-PHC2", "PHA2-PHB2-PHC2", "PHB2-PHC2-PHA2", 
        "PHC2-PHA2-PHB2", "AMD2-CA2-PHA2", "AMD2-CA3-PHA3", "CA3-PHA3-PHB3", 
        "CA3-PHA3-PHC3", "PHA3-PHB3-PHC3", "PHB3-PHC3-PHA3", "PHC3-PHA3-PHB3", 
        "AMD2-CA3-AMD3", "CA3-AMD3-CA4", "AMD3-CA4-COO", "AMD3-CA3-PHA3", 
        "AMD3-CA4-PHA4", "CA4-PHA4-PHB4", "CA4-PHA4-PHC4", "PHA4-PHB4-PHC4", 
        "PHB4-PHC4-PHA4", "PHC4-PHA4-PHB4", "COO-CA4-PHA4"]
    angles1 = angles[0:9]
    angles2 = angles[9:18]
    angles3 = angles[18:27]
    angles4 = angles[27:]

    dihedrals = ["NH3-CA1-AMD1-CA2", "CA1-AMD1-CA2-AMD2", "AMD1-CA2-AMD2-CA3", 
        "NH3-CA1-PHA1-PHB1", "NH3-CA1-PHA1-PHC1", "CA1-PHA1-PHB1-PHC1", 
        "CA1-PHA1-PHC1-PHB1", "AMD1-CA1-PHA1-PHB1", "AMD1-CA1-PHA1-PHC1", 
        "AMD1-CA2-PHA2-PHB2", "AMD1-CA2-PHA2-PHC2", "CA2-AMD1-CA1-PHA1", 
        "CA2-AMD2-CA3-PHA3", "CA2-PHA2-PHB2-PHC2", "CA2-PHA2-PHC2-PHB2", 
        "AMD2-CA2-PHA2-PHB2", "AMD2-CA2-PHA2-PHC2", "AMD2-CA3-PHA3-PHB3", 
        "AMD2-CA3-PHA3-PHC3", "CA3-AMD2-CA2-PHA2", "CA3-PHA3-PHB3-PHC3", 
        "CA3-PHA3-PHC3-PHB3", "CA1-AMD1-CA2-PHA2", "CA2-AMD2-CA3-AMD3", 
        "AMD2-CA3-AMD3-CA4", "CA3-AMD3-CA4-COO", "CA3-AMD3-CA4-PHA4", 
        "AMD3-CA3-PHA3-PHB3", "AMD3-CA3-PHA3-PHC3", "AMD3-CA4-PHA4-PHB4", 
        "AMD3-CA4-PHA4-PHC4", "CA4-AMD3-CA3-PHA3", "CA4-PHA4-PHB4-PHC4", 
        "CA4-PHA4-PHC4-PHB4", "COO-CA4-PHA4-PHB4", "COO-CA4-PHA4-PHC4"]
    dihedrals1 = dihedrals[0:9]
    dihedrals2 = dihedrals[9:18]
    dihedrals3 = dihedrals[18:27]
    dihedrals4 = dihedrals[27:]

def normdata(myarray):
    mydata = myarray
    if (mydata[:,1].max() == 0):
        print('skipping norm due to divisor error')
        return mydata
    bounds = (mydata[mydata[:,1]!=0][0][0], mydata[mydata[:,1]!=0][-1][0])
    print(f'BOUNDS IS {str(bounds)}')
    print(f'DIVISOR IS {np.max(mydata[:,1])}')
#    print(mydata[:,0])
    simdatanorm = mydata[:,1] / np.max(mydata[:,1])
#    print(mydata)
#    print(mydata[:,0])
#    print(mydata[:,1])
    normdata = np.column_stack((mydata[:,0],simdatanorm))
#    maxloc = mydata[mydata.argmax(axis=0)[1]][0]
    return normdata#, bounds, maxloc

def plotdist(interaction_type, interaction_list, figrows, figcols):
    refs=[]
    dats=[]

    for idx, interaction in enumerate(interaction_list):
        print(f'PROCESSING INTERACTION: {interaction}')
        ref_file = os.path.join(REF_DIR, interaction + REF_FILE_EXT)
        dat_file = os.path.join(DAT_DIR, interaction + DAT_FILE_EXT)
        ref = np.loadtxt(ref_file,skiprows=0,usecols=[0,1])
        dat = np.loadtxt(dat_file,skiprows=0,usecols=[0,1])
        refnorm = normdata(ref)
        datnorm = normdata(dat)
        refs.append(refnorm)
        dats.append(datnorm)

    plt.close('all')

    fig, axes = plt.subplots(figrows, figcols, figsize=(20,10))
    fig.suptitle(interaction_type+' -- CG'+MODEL+' -- '+PEPCT+' peptides')

    for idx,ax in enumerate(axes.flatten()):
        if(idx == len(interaction_list)):
            break
        ax.plot(dats[idx][:,0], dats[idx][:,1],'-',refs[idx][:,0], refs[idx][:,1],'--', lw=5)
        ax.set_title(interaction_list[idx])

    for idx,ax in enumerate(fig.get_axes()):
        if(idx == len(interaction_list)):
            break
        # ax.label_outer()
        ax.grid()
        ax.legend(['CG','AA'])

    plt.tight_layout()
    plt.savefig(f'./{interaction_type}_{MODEL}_{PEPCT}.png')


# %%
if MODEL == 'F2':
    plotdist("bonds-1",bonds1,3,3)
    plotdist("bonds-2",bonds2,3,3)
    plotdist("angles-1",angles1,3,3)
    plotdist("angles-2",angles2,3,3)
    plotdist("waters",waters,3,3)
    plotdist("nonbonds-1",nonbonds1,3,3)
    plotdist("nonbonds-2",nonbonds2,3,3)
    plotdist("nonbonds-3",nonbonds3,3,3)
    plotdist("nonbonds-4",nonbonds4,3,3)
    plotdist("dihedrals-1",dihedrals1,3,3)
    plotdist("dihedrals-2",dihedrals2,3,3)
    plotdist("conform",conform,1,2)

if MODEL == 'F4':
    plotdist("bonds-1",bonds1,3,3)
    plotdist("bonds-2",bonds2,3,3)
    plotdist("bonds-3",bonds3,3,3)
    plotdist("angles-1",angles1,3,3)
    plotdist("angles-2",angles2,3,3)
    plotdist("angles-3",angles3,3,3)
    plotdist("angles-4",angles4,3,3)
    plotdist("waters",waters,3,3)
    plotdist("nonbonds-1",nonbonds1,3,3)
    plotdist("nonbonds-2",nonbonds2,3,3)
    plotdist("nonbonds-3",nonbonds3,3,3)
    plotdist("nonbonds-4",nonbonds4,3,3)
    plotdist("dihedrals-1",dihedrals1,3,3)
    plotdist("dihedrals-2",dihedrals2,3,3)
    plotdist("dihedrals-3",dihedrals3,3,3)
    plotdist("dihedrals-4",dihedrals4,3,3)
    plotdist("conform",conform,1,2)
    

