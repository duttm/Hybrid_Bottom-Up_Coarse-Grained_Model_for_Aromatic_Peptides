#!/usr/bin/env python3

import numpy as np
from matplotlib import pyplot as plt
from matplotlib import rcParams
import sys
import seaborn as sns
import os

pt=sns.color_palette('colorblind')
col1=pt[1]
col2=pt[-1]

rcParams['font.family'] = 'sans-serif'
#rcParams['font.weight'] = 'bold'
rcParams['font.size'] = '18'
#font = {'family' : 'sans-serif',
#        'weight' : 'bold',
#        'size'   : 8}
#rc('font', **font)

#plt.style.use('ggplot')

# read a DOF name from command line,
# read in distributions matchin the supplied DOF name,
# scale the DOF distributions by their max values,
# label the locations of nonzero density for each distribution (i.e. support),
# plot scaled distributions with support identifiers above,
# labeled with distance or radians, plus degrees for angular DOFs

DOF=sys.argv[1]
MODEL='F4'

AA_DIR=f'/home/mason/exdrive/oligo/{MODEL}/AA/{MODEL}_1/dist-300-500'
CG_DIR=f'/home/mason/exdrive/oligo/{MODEL}/CG/{MODEL}_1/dist-0-end'

dat1=np.loadtxt(f'{AA_DIR}/{DOF}.dist.new',usecols=(0,1))
dat2=np.loadtxt(f'{CG_DIR}/{DOF}.dist.new',usecols=(0,1))
dat1[:,1]/=np.max(dat1[:,1])
dat2[:,1]/=np.max(dat2[:,1])

sup1mask=dat1[:,1]!=0
sup2mask=dat2[:,1]!=0
sup1 = dat1[sup1mask]
sup2 = dat2[sup2mask]
sup1[:,1]=1.1
sup2[:,1]=1.2

fig,ax=plt.subplots(1,1,figsize=(7,3))

ax.plot(dat1[:,0],dat1[:,1],lw=5,color=col1,label='AA',ls=(0, (1, 1)))
ax.plot(dat2[:,0],dat2[:,1],lw=5,color=col2,label='CG')

ax.plot(sup1[:,0],sup1[:,1],lw=0,color=col1,marker='o',alpha=0.5)
ax.plot(sup2[:,0],sup2[:,1],lw=0,color=col2,marker='o',alpha=0.5)

XVALS=np.concatenate((dat1[:,0],dat2[:,0]))
XLIM=[ np.min(XVALS), np.max(XVALS) ]
if XLIM[1]==3.14:
    xticklocs = [0, 1.05, 2.09, 3.14]
    xticklabels = [i for i in range(0,190,60)]
    if XLIM[0]==-3.14:
        xticklocs = [-i for i in xticklocs][1:] + xticklocs
        xticklabels = [-i for i in xticklabels][1:] + xticklabels
    xticklocstrs = [str(i) for i in xticklocs]
    xticklabelstrs = ['\n'+str(i) for i in xticklabels]
    xtickalllabels = [ ''.join(x) for x in zip(xticklocstrs,xticklabelstrs)]
    plt.xticks(xticklocs, xtickalllabels)

plt.xlim(XLIM)
plt.ylim([0,1.3])

ax.set(yticklabels=[])
ax.tick_params(left=False)

ax.legend(bbox_to_anchor=(1,1))
plt.title(f'{DOF}')

plt.tight_layout()
figname=f'supports-{MODEL}-{DOF}.png'
plt.savefig(figname, dpi=300)
os.system(f'rm supports.png; ln -s {figname} supports.png')


