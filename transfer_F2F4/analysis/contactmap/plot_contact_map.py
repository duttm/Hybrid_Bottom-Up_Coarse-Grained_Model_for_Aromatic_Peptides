#!/usr/bin/env python3

import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import sys
mpl.use('svg')
import seaborn as sns

model_id = int(sys.argv[2])

if model_id == 1:
    user_labels = [
        'NH3', 'CAB1', 'PHE1', 'AMD1', 'CAB2',
        'PHE2', 'AMD2', 'CAB3', 'PHE3', 'COO',
    ]

if model_id == 2:
    user_labels = [
        'NH3', 'CA1', 'PHA1', 'PHB1', 'PHC1', 'AMD1', 
        'CA2', 'PHA2', 'PHB2', 'PHC2', 'AMD2',
        'CA3', 'PHA3', 'PHB3', 'PHC3', 'COO',
    ]

if model_id == 3:
    user_labels = [
        'NH3', 'CA1', 'PHA1', 'PHB1', 'PHC1', 'AMD1', 
        'CA2', 'PHA2', 'PHB2', 'PHC2', 'COO',
    ]

if model_id == 4:
    user_labels = [
        'NH3', 'CA1', 'PHA1', 'PHB1', 'PHC1', 'AMD1', 
        'CA2', 'PHA2', 'PHB2', 'PHC2', 'AMD2',
        'CA3', 'PHA3', 'PHB3', 'PHC3', 'AMD3',
        'CA4', 'PHA4', 'PHB4', 'PHC4', 'COO',
    ]

    
print(user_labels)
data = []
with open(sys.argv[1]) as f:
    contactmap = np.loadtxt(f,dtype='<i4')

print(contactmap)
restype_count = len(contactmap)

myvmin = np.min(np.clip(contactmap,1,None))
myvmax = np.max(contactmap)
#myvmax = 149

#mycmap = sns.color_palette("mako_r",as_cmap=True)
mycmap = sns.color_palette("plasma_r",as_cmap=True)
mycmap.set_under('w')

plt.imshow(contactmap, origin="lower",cmap=mycmap,vmin=myvmin,vmax=myvmax)
plt.xticks(np.arange(restype_count), user_labels, rotation=90)
plt.yticks(np.arange(restype_count), user_labels)

bounds = range(myvmin,myvmax+2)
tics = range(myvmin,myvmax+2,2)
cbar = plt.colorbar(ticks=tics, boundaries=bounds)
cbar.ax.get_yaxis().labelpad = 15
cbar.ax.set_ylabel('# of contacts', rotation=270)

plt.title("Contact Map")
plt.tight_layout()
plt.savefig('contactmap.png',dpi=300)


