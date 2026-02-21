#!/usr/bin/env python3

import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import sys
#mpl.use('svg')
import seaborn as sns
import sys
mycmap = sns.color_palette("colorblind",as_cmap=True)

np.set_printoptions(threshold=sys.maxsize)
np.seterr(divide = 'ignore') 

shift=5

# EMD from raw contact map data
#data = {
#    'FF':{32:{'AA-CG':68.41,'CG-BA':57.73,'AA-BA':22.70},
#        64:{'AA-CG':128.44,'CG-BA':115.92,'AA-BA':39.25},
#        'AA-AA':88.23,'CG-CG':56.25,'BA-BA':69.89,'shift':-shift
#    },
#    'FFFF':{32:{'AA-CG':91.73,'CG-BA':86.35,'AA-BA':23.73},
#        64:{'AA-CG':146.13,'CG-BA':137.89,'AA-BA':42.94},
#        'AA-AA':66.28,'CG-CG':94.29,'BA-BA':53.94,'shift':+shift
#    }
#}

# EMD from FES inverted from contact maps
#data = {
#    'FF':{32:{'AA-CG':23.40,'CG-BA':23.56,'AA-BA':4.14},
#        64:{'AA-CG':24.99,'CG-BA':25.16,'AA-BA':2.58},
#        'AA-AA':2.51,'CG-CG':16.61,'BA-BA':2.39,'shift':-shift
#    },
#    'FFFF':{32:{'AA-CG':21.06,'CG-BA':22.17,'AA-BA':13.00},
#        64:{'AA-CG':15.90,'CG-BA':15.91,'AA-BA':7.30},
#        'AA-AA':11.86,'CG-CG':19.64,'BA-BA':11.30,'shift':+shift
#    }
#}

# EMD from FES inverted from contact maps, with BA ensembles
data = {
    'FF':{32:{'AA-CG':23.40,'CG-BA':23.30,'AA-BA':3.56},
        64:{'AA-CG':24.99,'CG-BA':24.97,'AA-BA':2.55},
        'AA-AA':2.51,'CG-CG':16.61,'BA-BA':1.59,'shift':-shift
    },
    'FFFF':{32:{'AA-CG':21.06,'CG-BA':22.17,'AA-BA':13.00},
        64:{'AA-CG':15.90,'CG-BA':15.69,'AA-BA':6.73},
        'AA-AA':11.86,'CG-CG':19.64,'BA-BA':3.77,'shift':+shift
    }
}

# max EMD calculated between sampled contact maps
#EMDmax=146.13
# max EMD between FES
#EMDmax=25.xx

EMDmax=1 # no scaling

markers = {
    'FF':{'AA-CG':'X',
    'CG-BA':'P',
    'AA-BA':'o',
    'AA-AA':'<',
    'CG-CG':'s',
    'BA-BA':'>',},

    'FFFF':{'AA-CG':'v',
    'CG-BA':'^',
    'AA-BA':'d',
    'AA-AA':'<',
    'CG-CG':'s',
    'BA-BA':'>',}
}

fig, axs = plt.subplots(nrows=1, ncols=2, sharey=True, figsize=(6.75,3.37))

artists=[]
colororder=0
for i in ['FF','FFFF']:
    for j in [32, 64]:
        for k in ['AA-CG','CG-BA','AA-BA']:
            artists.append(
                axs[0].scatter(
                    j+data[i]['shift'], data[i][j][k]/EMDmax,
                    marker=markers[i][k], label=f'{i} {k}', 
                    c=mycmap[int(colororder//6+colororder%3)]))
            colororder=colororder+1
axs[0].set_title('(a) Compare scales: AA, CG, BA')
#axs[0].set_xlim([25,71])
axs[0].set_xlim([20,150])
axs[0].set_xticks([32,64])
#axs[0].legend(handles=artists[0:3]+artists[6:9],ncol=1,handletextpad=0.02,loc='center')
axs[0].set_ylim([0,30])
axs[0].set_yticks([0,5,10,15,20,25])
axs[0].legend(handles=artists[0:3]+artists[6:9],ncol=1,handletextpad=0.02,loc='right',fontsize='large')

artists2=[]
for i in ['FF','FFFF']:
    for k in ['AA-AA','CG-CG','BA-BA']:
        artists2.append(
            axs[1].scatter(data[i]['shift'],data[i][k]/EMDmax,marker=markers[i][k],label=f'{k}')
        )
axs[1].set_title('(b) Compare sizes: 32 vs 64')
#axs[1].set_xlim([-2*shift,2*shift])
axs[1].set_xlim([-2*shift,4*shift])
axs[1].set_xticks([-shift,shift],['FF','FFFF'])
#axs[1].legend(handles=artists2[0:3],handletextpad=0.02,loc='center')
axs[1].legend(handles=artists2[0:3],handletextpad=0.02,loc='right',fontsize='large')

axs[0].tick_params(axis='both', which='major', labelsize='x-large')
axs[1].tick_params(axis='both', which='major', labelsize='x-large')

axs[0].set_ylabel("EMD between FES",fontsize='large')
axs[0].set_xlabel("Peptide count",fontsize='large')
axs[1].set_xlabel("Peptide type",fontsize='large')

fig.suptitle('FES disparity between scales ')

plt.tight_layout()
#plt.show()
plt.savefig(f"fig-cmapEMD.png")


