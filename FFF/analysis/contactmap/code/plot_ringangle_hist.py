#!/usr/bin/env python3

import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import sys
mpl.use('svg')
import seaborn as sns

np.set_printoptions(threshold=sys.maxsize)

data = []
with open(sys.argv[1]) as f:
    angledata = np.loadtxt(f,skiprows=1)

plt.hist(angledata[:,5], bins="auto", histtype="step", density=False)
plt.xlim(0,180)
plt.title("Distribution of Ring Contact Angles")
plt.tight_layout()
plt.savefig('ringhist.png')
