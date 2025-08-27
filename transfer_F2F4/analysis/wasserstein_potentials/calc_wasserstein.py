#!/usr/bin/env python3

from scipy.stats import wasserstein_distance
import numpy as np
import sys
from pprint import pprint

#dist1file='/home/mason/oligo/distributions/F2_1/AA/dist_0-500ns/NH3-CA1-PHA1-PHC1.dist.new'
#dist2file='/home/mason/oligo/F4/ff-development/bonded/gen2/dihedrals/step_003/dist/NH3-CA1-PHA1-PHC1.dist.new'

def print_wasserstein_distance(dist1,dist2):
#    print(f"{dist1file.split('/')[-1]:<30} {np.log(wasserstein_distance(dist1, dist2)):>10.3f}")
    print(f"{dist1file.split('/')[-1]:<30} {wasserstein_distance(dist1, dist2):>10.3f}")
#    print('\n')

if __name__ == '__main__':
    dist1file = sys.argv[1]
    dist2file = sys.argv[2]
    
    dist1 = np.loadtxt(dist1file, usecols=(0,1), comments=['@','#'])
    dist2 = np.loadtxt(dist2file, usecols=(0,1), comments=['@','#'])
    
    dist2r = dist2[np.isin(dist2[:,0],dist1[:,0])]
    
    print_wasserstein_distance(dist1[:,1],dist2r[:,1])
#    pprint(np.concatenate(dist1,dist2r[:,1].T), axis=1)


