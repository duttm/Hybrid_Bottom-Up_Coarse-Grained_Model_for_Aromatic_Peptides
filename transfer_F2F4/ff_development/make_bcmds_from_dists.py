import os
import numpy as np
import re
from pprint import pprint

ROOTDIR = os.getcwd()

distre = re.compile('.*\.dist\.new$')

allfiles = os.listdir()
distfiles = [ i for i in allfiles if re.match(distre,i) ]

bodyct_params = {
    2: {
        'nmult':1000,
        'paramtype':'bond'
    },
    3: {
        'nmult':100,
        'paramtype':'angle'
    },
    4: {
        'nmult':None,
        'paramtype':'dihedral'
    },
}

#distfiles = ['NH3-CA1.dist.new']
for my_filename in distfiles:
    print(my_filename)
    bodies = re.findall(r'[A-Z0-9]{2,4}',my_filename)
    bodyct = len(bodies)
    if bodyct == 0: continue
    paramname = re.split('\.',my_filename)[0]
    paramtype = bodyct_params[bodyct]['paramtype']
    filedata = np.loadtxt(my_filename, comments=('#'), usecols=(0,1), skiprows=0)
    nonzero = filedata[ filedata[:,1] != 0 ]
    print(nonzero)
    if nonzero.size!=0:
        min = np.min(nonzero[:,0])
        max = np.max(nonzero[:,0])
        if not bodyct_params[bodyct]['nmult']: setn = 90
        else: setn = (max-min)*bodyct_params[bodyct]['nmult'] + 2
        with open('bcmds/bcmds_'+paramname,'w') as f:    
            f.write(f'tab set T 300\ntab set scale {paramtype}\ntab set auto 0\n'+
                f'tab set min {min:.3f}\ntab set max {max:.3f}\ntab set n {setn:.0f}\n'+
                f'tab {paramname}.pot.ib *{paramname}*\nq\n\n')


