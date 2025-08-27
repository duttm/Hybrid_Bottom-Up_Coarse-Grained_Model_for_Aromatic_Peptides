#!/usr/bin/env python3

import numpy as np
import os

AA=0

# AA
if AA==1:
    distgroups='15\n16\n17\n'
    mdfile='md.xtc'
    tprfile='md.tpr'
    pairtype='CB'
    starttime=300000
# CG
else:
    distgroups='17\n20\n22\n'
    mdfile='traj_comp.xtc'
    tprfile='topol.tpr'
    pairtype='PHA'
    starttime=0

gmxdist = f'echo "{distgroups}" | gmx distance -f {mdfile} -s {tprfile} -n index.ndx -oh {pairtype}-disthist.xvg -len .6 -tol .5 -b {starttime}'
os.system(gmxdist)

dat = np.loadtxt(f'{pairtype}-disthist.xvg',comments=['@','#'])
datmax = np.column_stack((dat[:,0], dat[:,1:].max(axis=1)))
datsum = np.column_stack((dat[:,0], dat[:,1:].sum(axis=1)))
with open(f'max-{pairtype}-hist.xvg','w') as f: np.savetxt(f,datmax)
with open(f'sum-{pairtype}-hist.xvg','w') as f: np.savetxt(f,datsum)


