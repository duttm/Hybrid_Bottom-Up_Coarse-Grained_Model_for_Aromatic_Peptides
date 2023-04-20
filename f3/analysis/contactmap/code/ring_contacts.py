#!/usr/bin/env python3

# WARNING this code will not cope with incorrect gro inputs
# WARNING this code does not actually take gro inputs
# this code accepts a file with gro formatted atoms, 
# but just 3 atoms per ring,
# and no headers or anything like that.
# it outputs a file with a list of ring contacts with angles,
# which should be pretty easy to plot into a histogram.
# good luck!

import numpy as np
import sys

THRESHOLD = 0.6
#NUMMOL = 32
NUMRESMOL = 3
NUMMOL = int(sys.argv[2])
NUMATOMRES = 3
FRAMES = 1

user_input_file = sys.argv[1]
numatoms = NUMMOL*NUMRESMOL*NUMATOMRES # 32 pep, 96 res, 288 atoms, e.g.
numres = NUMMOL*NUMRESMOL
    
def angle(u,v):
    """accept 2 numpy arrays of i,j,k unit vectors, return angle"""
    return np.arccos(np.dot(u,v))*180/np.pi

def calculate_contacts(periodic_config):
    ring_contacts = []
    extended_count = len(periodic_config)
    for i in range(extended_count):
        for j in range(i+1, extended_count):
            mol_i = int(periodic_config[i,0])
            mol_j = int(periodic_config[j,0])
            i_iscentral = int(periodic_config[i,8])
            j_iscentral = int(periodic_config[j,8])
            if (not(mol_i==mol_j)) and ((i_iscentral==1 or j_iscentral==1)):
                ringdist = distance(periodic_config[i][2:5], periodic_config[j][2:5])
                if ringdist < THRESHOLD:
                    ringangle = angle(periodic_config[i][5:8], periodic_config[j][5:8])
                    ring_contact = np.r_[periodic_config[i][1], periodic_config[j][1], i+1, j+1, ringdist, ringangle]
                    ring_contacts.append(ring_contact)
    print(ring_contacts)
    head = '# mol1 mol2 mol1res mol2res distance angle'
    with open('ringcontacts.txt','w') as g:
        np.savetxt(g, ring_contacts, header=head, encoding='utf8')
    return ring_contacts

def centroid(a,b,c):
    """accept 3 numpy arrays of x,y,z coords, return centroid"""
    return (a+b+c)/3

def distance(a,b):
    """accept 2 numpy arrays of x,y,z coords, return distance"""
    return np.sqrt(np.sum((a-b)**2))

def make_rings(config):
    rings = np.zeros((numres,8))
    res = 1
    mol = 1
    while len(config) > 0:
        p1,p2,p3 = config[0:3]
        config = config[3:]
        cent = centroid(p1,p2,p3)
        unorm = unitnormal(p1,p2,p3)
        ring = np.r_[mol, res, cent, unorm]                      #####
        rings[3*(mol-1)+(res-1)] = ring
        if res == 3: 
            res = 1
            mol = mol+1
        else: res = res+1
    return rings

def periodize_config(molres_config, box_length):
    """in: [mol,res,cent,unorm]*1, out: [ ... , central_volume_indicator]*27"""
    # force true atoms into the central box
    molres_config[:,2:5] = np.mod(molres_config[:,2:5],box_length)

    # the number of central volume atoms
    central_count = len(molres_config)
    
    # make a bunch of shifting vectors, starting with the 0-shift vector,
    # finishing with [boxlength,boxlength,boxlength].
    box_deltas = np.multiply(
                [(i,j,k) for i in [0,-1,1] for j in [0,-1,1] for k in [0,-1,1]],
                box_length
                )

    # make new object to copy in all the shifted atoms
    periodic = np.copy(molres_config)
    for delta in box_deltas[1:]:
        molres_delta = np.copy(molres_config)
        molres_delta[:,2:5] = molres_delta[:,2:5] + delta
        periodic = np.r_[periodic, molres_delta]

    # the number of total periodic atoms
    extended_count = len(periodic)
    
    central_volume_indicator = np.r_[
                                np.ones(central_count),
                                np.zeros(extended_count-central_count)
                                ]
    print(sum(central_volume_indicator)) 
    # indicator=1 for the 0-shifted atoms only, indictor=0 for periodic images
    periodic = np.c_[periodic, central_volume_indicator]
    print(periodic)
#    with open('periodic.txt','w') as periofile:
#        np.savetxt(periofile, periodic, encoding='utf8')

    return periodic    

def unitnormal(a,b,c):
    """accept 3 numpy arrays of x,y,z coords, return unit normal"""
    normal = np.cross(b-a,c-a)
    return (normal / (normal**2).sum()**0.5)

def main(config_file):
    with open(config_file) as f:
        triplet_config = np.loadtxt(f, usecols=(3,4,5), max_rows=numatoms)
        boxvector = f.readline()
        boxlength = float(boxvector.split()[0])
    
    # transform 3-bead config into ring centroids and normal vectors
    rings = make_rings(triplet_config)
    
    # periodically extend config and label central volume centroids
    periodic_rings = periodize_config(rings, boxlength)
        
    # calculate contacts and interring angles and print all that to file
    ring_contacts = calculate_contacts(periodic_rings)

if __name__ == '__main__':
    main(user_input_file)
