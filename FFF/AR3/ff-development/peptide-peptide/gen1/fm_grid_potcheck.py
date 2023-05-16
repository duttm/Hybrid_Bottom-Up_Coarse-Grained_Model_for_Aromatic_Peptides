#!/usr/bin/env python3
# potcheck.py

"""Read a given potential table file, check for 'compliance', print the results."""

import sys
import numpy as np

input_file = sys.argv[1]

def main(potential_table) -> int:
    checks=[0 for i in range(3)]
    with open(potential_table) as f:
        table_data = np.loadtxt(f, comments=("#","@"))
        if table_data[0,5] > 10:         checks[0]+=1
        if table_data[:,5].min() < 0:   checks[1]+=1
        if table_data[0,5] > 100:       checks[2]+=1
        
    print(' '.join(list(str(i) for i in checks)))
    return checks

if __name__ == '__main__':
    main(input_file)
