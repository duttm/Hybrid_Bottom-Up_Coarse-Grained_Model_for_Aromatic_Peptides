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

shift=2

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
data = {
    'FF':{32:{'AA-CG':25.13,'CG-BA':25.69,'AA-BA':3.79},
        64:{'AA-CG':23.39,'CG-BA':22.92,'AA-BA':2.90},
        'AA-AA':2.61,'CG-CG':16.41,'BA-BA':3.56,'shift':-shift
    },
    'FFFF':{32:{'AA-CG':17.17,'CG-BA':18.21,'AA-BA':6.40},
        64:{'AA-CG':16.63,'CG-BA':16.72,'AA-BA':6.40},
        'AA-AA':9.60,'CG-CG':12.71,'BA-BA':5.30,'shift':+shift
    }
}

# max EMD calculated between sampled contact maps
#EMDmax=146.13
# max EMD between FES
EMDmax=25.69


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

fig, axs = plt.subplots(nrows=1, ncols=2, sharey=True)

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
axs[0].set_title('(a) Compare simulation types')
axs[0].set_xlim([25,71])
axs[0].set_xticks([32,64])
axs[0].legend(handles=artists[0:3]+artists[6:9],ncol=1)

artists2=[]
for i in ['FF','FFFF']:
    for k in ['AA-AA','CG-CG','BA-BA']:
        artists2.append(
            axs[1].scatter(data[i]['shift'],data[i][k]/EMDmax,marker=markers[i][k],label=f'{k}')
        )
axs[1].set_title('(b) Compare systems 32 vs 64')
axs[1].set_xlim([-2*shift,2*shift])
axs[1].set_xticks([-shift,shift],['FF','FFFF'])
axs[1].legend(handles=artists2[0:3])

plt.tight_layout()
plt.show()

