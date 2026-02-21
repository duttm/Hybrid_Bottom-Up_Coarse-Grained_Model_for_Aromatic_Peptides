#!/usr/bin/env python3
"""
Average backmapped ensemble contactmaps for each (peptide, count) combination
and invoke plot_contact_map.py to produce a 4x3 grid:

  rows (slow): F2x32, F2x64, F4x32, F4x64
  cols (fast): AA, CG, BA (ensemble-averaged backmapped)

BA is the element-wise mean of four independent backmapped trajectories,
rounded to the nearest integer.  Named intermediate files are written to
the same directory as this script so that subplot titles are informative.
"""

import numpy as np
import subprocess
import sys
import os

ROOT = '/home/mason/exdrive/oligo'
HERE = os.path.dirname(os.path.abspath(__file__))


def load(path):
    with open(path) as f:
        return np.loadtxt(f, dtype='<i4')


def save_txt(arr, name):
    path = os.path.join(HERE, name)
    np.savetxt(path, arr, fmt='%d', delimiter='\t')
    return path


combos = [
    {
        'label': 'F2x32',
        'AA': f'{ROOT}/F2/AA/F2_32/cmap/contactmap.txt',
        'CG': f'{ROOT}/F2/CG/F2a6d2_32/cmap/contactmap.txt',
        'BA': [
            f'{ROOT}/F2/CG/F2a6d2_32/backmap/cmap/contactmap.txt',
            f'{ROOT}/F2/CG/F2a6d2_32/backmap-1/cmap/contactmap.txt',
            f'{ROOT}/F2/CG/F2a6d2_32/backmap-2/cmap/contactmap.txt',
            f'{ROOT}/F2/CG/F2a6d2_32/backmap-3/cmap/contactmap.txt',
        ],
    },
    {
        'label': 'F2x64',
        'AA': f'{ROOT}/F2/AA/F2_64/cmap/contactmap.txt',
        'CG': f'{ROOT}/F2/CG/F2_64/cmap/contactmap.txt',
        'BA': [
            f'{ROOT}/F2/CG/F2_64/backmap/cmap/contactmap.txt',
            f'{ROOT}/F2/CG/F2_64/backmap-1/cmap/contactmap.txt',
            f'{ROOT}/F2/CG/F2_64/backmap-2/cmap/contactmap.txt',
            f'{ROOT}/F2/CG/F2_64/backmap-3/cmap/contactmap.txt',
        ],
    },
    {
        'label': 'F4x32',
        'AA': f'{ROOT}/F4/AA/F4_32/cmap/contactmap.txt',
        'CG': f'{ROOT}/F4/CG/F4_32-1/cmap/contactmap.txt',
        'BA': [
            f'{ROOT}/F4/CG/F4_32-1/backmap/cmap/contactmap.txt',
            f'{ROOT}/F4/CG/F4_32-1/backmap-1/cmap/contactmap.txt',
            f'{ROOT}/F4/CG/F4_32-1/backmap-2/cmap/contactmap.txt',
            f'{ROOT}/F4/CG/F4_32-1/backmap-3/cmap/contactmap.txt',
        ],
    },
    {
        'label': 'F4x64',
        'AA': f'{ROOT}/F4/AA/F4_64/cmap/contactmap.txt',
        'CG': f'{ROOT}/F4/CG/F4_64-8/cmap/contactmap.txt',
        'BA': [
            f'{ROOT}/F4/CG/F4_64-8/backmap/cmap/contactmap.txt',
            f'{ROOT}/F4/CG/F4_64-8/backmap-1/cmap/contactmap.txt',
            f'{ROOT}/F4/CG/F4_64-8/backmap-2/cmap/contactmap.txt',
            f'{ROOT}/F4/CG/F4_64-8/backmap-3/cmap/contactmap.txt',
        ],
    },
]

file_list = []
for combo in combos:
    label = combo['label']

    aa_path = save_txt(load(combo['AA']), f'{label}_AA.txt')
    cg_path = save_txt(load(combo['CG']), f'{label}_CG.txt')

    ba_mean = np.round(np.mean([load(p) for p in combo['BA']], axis=0)).astype('<i4')
    ba_path = save_txt(ba_mean, f'{label}_BA.txt')

    file_list += [aa_path, cg_path, ba_path]

plot_script = os.path.join(HERE, 'plot_contact_map.py')
cmd = [sys.executable, plot_script] + file_list
print('Running:', ' '.join(cmd))
subprocess.run(cmd, check=True)
