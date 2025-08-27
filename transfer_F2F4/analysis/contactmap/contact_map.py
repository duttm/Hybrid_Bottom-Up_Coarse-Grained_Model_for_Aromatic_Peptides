#!/usr/bin/env python3

# accept a gro file with a single frame of a cg configuration,
# write a file with a 2d symmetrical contact matrix,
# which should be pretty easy to plot as a contour map.
# good luck!

import numpy as np
import sys
#np.set_printoptions(precision=3,suppress=True)

THRESHOLD = 0.6
#NUMMOL = 32
#NUMRESMOL = 10
user_input_file = sys.argv[1]
NUMMOL = int(sys.argv[2])
NUMRESMOL = int(sys.argv[3])
NUMATOMRES = 1
FRAMES = 1

numatoms = NUMMOL*NUMRESMOL*NUMATOMRES
numres = NUMMOL*NUMRESMOL

#RESNAME_DICT = {
#    1: 'NH3', 2:'CAB1', 3:'PHE1', 4:'AMD1', 5:'CAB2',
#    6:'PHE2', 7:'AMD2', 8:'CAB3', 9:'PHE3', 10:'COO',
#}

def calculate_contacts(periodic_config):
    contacts = []
    extended_count = len(periodic_config)
    for i in range(extended_count):
        for j in range(i+1, extended_count):
            mol_i = int(periodic_config[i,0])
            mol_j = int(periodic_config[j,0])
            i_iscentral = int(periodic_config[i,5])
            j_iscentral = int(periodic_config[j,5])
            if (not(mol_i==mol_j)) and ((i_iscentral==1 or j_iscentral==1)):
#            if ((i_iscentral==1 or j_iscentral==1)):
                dist = distance(periodic_config[i,2:5], periodic_config[j,2:5])
                if dist < THRESHOLD:
                    contact = np.r_[
                        periodic_config[i,0], 
                        periodic_config[j,0],
                        periodic_config[i,1], 
                        periodic_config[j,1], 
                        periodic_config[i,5], 
                        periodic_config[j,5],
                        dist]
                    contacts.append(contact)
                else: pass
            else: pass
    with open('contacts.txt','w') as contactfile:
        np.savetxt(contactfile, contacts, encoding='utf8',fmt='%d %d \t %d %d \t %d %d \t %f')

    return contacts

def distance(a,b):
    """accept 2 numpy arrays of x,y,z coords, return distance"""
    return np.sqrt(np.sum((a-b)**2))

def make_map(contacts):
    contact_map = np.zeros((NUMRESMOL,NUMRESMOL))
    tryafew=0
    for contact in contacts:
        # i,j are residue numbers, like sequence numbers in a molecule
        i = int(contact[2] - 1)
        j = int(contact[3] - 1)
        
        contact_map[i][j] = contact_map[i][j] + 1 
        if i!=j: contact_map[j][i] = contact_map[j][i] + 1
        with open('contactmap.txt','w') as cmapfile:
            np.savetxt(cmapfile, contact_map, encoding='utf8', fmt='%d',delimiter='\t')
    return contact_map    

def organize_config(config):
    """in: [x,y,z], out: [molnum, resnum, x,y,z]"""
    residues = np.zeros((numres,5))
    resnum = 1
    molnum = 1
    while len(config) > 0:
        coords = config[0]      ## pop
        config = config[1:]     ## pop
        residue = np.r_[molnum, resnum, coords]                      #####
        residues[NUMRESMOL*(molnum-1)+(resnum-1)] = residue
        if resnum == NUMRESMOL: 
            resnum = 1
            molnum = molnum+1
        else: resnum = resnum+1
    return residues

def periodize_config(molres_config, box_length):
    """in: [molnum,resnum,x,y,z]*1, out: [ ... , central_volume_indicator]*27"""
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

def main(config_file):
    with open(config_file) as f:
        xyz_config = np.loadtxt(f, usecols=(3,4,5), skiprows=2, max_rows=numatoms)
        rest_of_file = f.readlines()
        boxlength = float(rest_of_file[-1].split()[0])

    # label my xyz config with the respective molecule number in sim (e.g. 1-32)
    # and residue number within a peptide (e.g. 1-10).
    # looks like: 'molnum, resnum, x,y,z'
    molres_config = organize_config(xyz_config)

    # periodically extend config and label central volume atoms
    # looks like: 'molnum, resnum, x,y,z, indicator'
    periodic_config = periodize_config(molres_config, boxlength)
    print(periodic_config)
    
    # make a list of contacts involving central image atoms.
    # looks like: 'res[i], res[j], mol[i], mol[j], distance'
    contacts = calculate_contacts(periodic_config)
    
    # make a symmetrical 2d matrix of these contacts and print that to file
    contact_map = make_map(contacts)
    
if __name__ == '__main__':
    main(user_input_file)
