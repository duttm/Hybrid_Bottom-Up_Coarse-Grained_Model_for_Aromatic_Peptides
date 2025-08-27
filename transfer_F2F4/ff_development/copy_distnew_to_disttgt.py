import os
import numpy as np
import re
from pprint import pprint

ROOTDIR = os.getcwd()

distre = re.compile('(.*)\.dist\.new')

allfiles=os.listdir()
distfiles = [ i for i in allfiles if 'dist.new' in i ]

for my_filename in distfiles:
    print(my_filename)
    basename_match = re.match(distre,my_filename)
    basename = basename_match.group(1)
    os.system(f'cp -a {basename}.dist.new {basename}.dist.tgt')


