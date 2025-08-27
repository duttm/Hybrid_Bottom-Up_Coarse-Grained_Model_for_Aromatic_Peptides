#!/usr/bin/env python3

import numpy as np
from scipy.stats import wasserstein_distance_nd
import sys

inp1 = sys.argv[1]
inp2 = sys.argv[2]

def make_fes(dat):
    kBT = 2.49435 # <!-- 300*0.00831451 gromacs units -->
    prob = dat/np.sum(dat)
    fes = -kBT * np.log(prob)
#    print(fes)
    fes[fes==np.inf] = 0
#    print(fes)
    return fes

dat1 = np.loadtxt(inp1,comments=['@','#'])
dat2 = np.loadtxt(inp2,comments=['@','#'])

fes1 = make_fes(dat1)
fes2 = make_fes(dat2)

dist = wasserstein_distance_nd(dat1,dat2)
fesdist = wasserstein_distance_nd(fes1,fes2)

print(f'contact map 2d wasserstein: {dist}')
print(f'FES 2d wasserstein:         {fesdist}')


