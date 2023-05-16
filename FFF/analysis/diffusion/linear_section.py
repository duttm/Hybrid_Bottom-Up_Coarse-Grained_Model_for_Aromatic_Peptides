#!/usr/bin/env python3
# plot_histts.py

# Plot data and a fitted line

import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import scipy
import sys
mpl.use('svg')
#np.set_printoptions(threshold=sys.maxsize)
mpl.rcParams["font.size"] = 18

#TRAJFRACTION=sys.argv[2]


def make_figure(data_file_path):
    with open(data_file_path) as f:
        time_series_input = np.loadtxt(f, comments=("#","@"))
        
    TRAJMAXSTEP=int(float(sys.argv[2]) * len(time_series_input[:,0]))

    
#    time_series_data=time_series_input
    time_series_data=time_series_input[:TRAJMAXSTEP,:]
    
    plt.plot(time_series_data[:,0],time_series_data[:,1])

    slope, intercept, r_value, p_value, std_err = \
        scipy.stats.linregress( \
        time_series_data[:,0], \
        time_series_data[:,1] \
        )
    x = time_series_data[:,0]
    y = intercept + slope * time_series_data[:,0]
    print('r^2 = '+str(r_value**2))

    plt.plot(x, y, '--')
    
    plt.title("linear fit to msd -- "+data_file_path+ \
        "\n"+str(TRAJMAXSTEP)+" steps"+ \
        "\nR^2 = "+str(r_value**2))

    plt.tight_layout()
    plt.savefig('fitplot.png')

if __name__ == '__main__':
    data_file_path = sys.argv[1]
    myfig = make_figure(data_file_path)
#    print(myfig)
    
    
