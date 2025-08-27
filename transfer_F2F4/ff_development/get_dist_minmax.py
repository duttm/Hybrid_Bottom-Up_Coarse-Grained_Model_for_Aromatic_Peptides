import os
import numpy as np
import re
from pprint import pprint

ROOTDIR = os.getcwd()

distre = re.compile('.*\.dist\.new$')

allfiles = os.listdir()
distfiles = [ i for i in allfiles if re.match(distre,i) ]

bonds=re.compile('([A-Z0-9]{3,4}-){1}[A-Z0-9]{3,4}\.dist\.new')
angles=re.compile('[A-Z0-9]{3,4}-[A-Z0-9]{3,4}-[A-Z0-9]{3,4}\.dist\.new')
dihedrals=re.compile('[A-Z0-9]{3,4}-[A-Z0-9]{3,4}-[A-Z0-9]{3,4}-[A-Z0-9]{3,4}\.dist\.new')

bondfiles = [ i for i in distfiles if re.match(bonds,i) ]
anglefiles = [ i for i in distfiles if re.match(angles,i) ]
dihedralfiles = [ i for i in distfiles if re.match(dihedrals,i) ]
#fileslist= sorted([ i for i in allfiles if re.match(p,i) ])

paramnames = [ re.split(r'\.',i)[0] for i in dihedralfiles ]

print(f'# running get_dist_minmax.py in {ROOTDIR} ')

# run bonds/angles/dihedrals separately to impose different thresholds etc
# angles are this way TODO turn this into a function

for my_file in bondfiles:
    filedata = np.loadtxt(my_file, comments=('#'), usecols=(0,1), skiprows=0)
    nonzero = filedata[ filedata[:,1] != 0 ]
    if nonzero.size!=0:
        mymin = np.min(nonzero[:,0])
        mymax = np.max(nonzero[:,0])
        print(f'{my_file:<40} {mymin:< 4.3f}\t{mymax:< 4.3f}\t{(mymax-mymin)*1000+2:.0f}')
#    else: print(f'{my_file} has no nonzero values')

for my_file in anglefiles:
    filedata = np.loadtxt(my_file, comments=('#'), usecols=(0,1), skiprows=0)
    nonzero = filedata[ filedata[:,1] != 0 ]
    onemil = nonzero[ nonzero[:,1] > 0.001 ]
    if onemil.size!=0:
        mymin = np.min(onemil[:,0])
        mymax = np.max(onemil[:,0])
        print(f'{my_file:<40} {mymin:< 4.3f}\t{mymax:< 4.3f}\t{(mymax-mymin)*100+2:.0f}')
    else:
        mymin = np.min(nonzero[:,0])
        mymax = np.max(nonzero[:,0])
        print(f'{my_file:<40} {mymin:< 4.3f}\t{mymax:< 4.3f}\t{(mymax-mymin)*100+2:.0f}')

for my_file in dihedralfiles:
    filedata = np.loadtxt(my_file, comments=('#'), usecols=(0,1), skiprows=0)
    nonzero = filedata[ filedata[:,1] != 0 ]
    if nonzero.size!=0:
        mymin = np.min(nonzero[:,0])
        mymax = np.max(nonzero[:,0])
        print(f'{my_file:<40} {mymin:< 4.3f}\t{mymax:< 4.3f}\t{90:.0f}')


