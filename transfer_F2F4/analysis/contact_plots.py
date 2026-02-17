import marimo

__generated_with = "0.19.11"
app = marimo.App(width="medium")


@app.cell
def _():
    import matplotlib.pyplot as plt
    import matplotlib as mpl
    import numpy as np
    import sys
    # mpl.use('pdf')
    import seaborn as sns
    import sys
    import re
    import os

    np.set_printoptions(threshold=sys.maxsize)
    np.seterr(divide = 'ignore') 

    mycmap = sns.color_palette("plasma_r",as_cmap=True)
    mycmap.set_under('w')
    plt.set_cmap(mycmap)

    mpl.rcParams["lines.linewidth"]=1.8

    def normalize_data(data_1col, min_est, max_est):
        return (data_1col - min_est) / (max_est - min_est)

    def moving_average(x, w):
        return np.convolve(x, np.ones(w), 'valid') / w

    def makeplotfromdatadir(DATADIR,PEPCT,TMAX_ns,NUM_RES,ax,interaction=None):
        p = re.compile(r".*(F[24](a[0-9]d[0-9])?_[0-9]+-?[0-9]+).*")
        SYSNAME = p.match(DATADIR).group(1)
        # print(f'sysname is {SYSNAME}')

        PEPCT=int(PEPCT) # 64
        tmax = int(TMAX_ns* 1000)
        NUM_RES = int(NUM_RES)

        CONTACTSUBDIR="contacts-0-100"
        CLUSTERSUBDIR="cluster-0-100"

        CONTACTFILE1="numcont_MCMC.xvg"
        CONTACTFILE2="numcont_SCSC.xvg"
        CONTACTFILE3="numcont_MCSC.xvg"
        CONTACTFILE4="numcont_AMDAMD.xvg"
        CONTACTFILE5="numcont_NH3COO.xvg"
        CLUSTERFILE="nclust.xvg"

        with open(f"{DATADIR}/{CONTACTSUBDIR}/{CONTACTFILE1}") as f1:
            data1 = np.loadtxt(f1,skiprows=0,usecols=(0,1),comments=["@","#"])
        with open(f"{DATADIR}/{CONTACTSUBDIR}/{CONTACTFILE2}") as f2:
            data2 = np.loadtxt(f2,skiprows=0,usecols=(0,1),comments=["@","#"])
        with open(f"{DATADIR}/{CONTACTSUBDIR}/{CONTACTFILE3}") as f3:
            data3 = np.loadtxt(f3,skiprows=0,usecols=(0,1),comments=["@","#"])
        with open(f"{DATADIR}/{CONTACTSUBDIR}/{CONTACTFILE4}") as f4:
            data4 = np.loadtxt(f4,skiprows=0,usecols=(0,1),comments=["@","#"])
        with open(f"{DATADIR}/{CONTACTSUBDIR}/{CONTACTFILE5}") as f5:
            data5 = np.loadtxt(f5,skiprows=0,usecols=(0,1),comments=["@","#"])
        with open(f"{DATADIR}/{CLUSTERSUBDIR}/{CLUSTERFILE}") as f6:
            data6 = np.loadtxt(f6,skiprows=0,usecols=(0,1),comments=["@","#"])

        mawindow = 20
        data6ma = moving_average(data6[:,1],mawindow)

        NUM_CA  = NUM_RES
        NUM_AMD = NUM_RES - 1

        AMDmin=0
        NH3min=0
        COOmin=0
        NH3COOmin=0
        MCmin=0
        SCmin=0
        MCSCmin=0

        # max number is if somehow they are all in contact which of course can't happen
        MCmax = PEPCT*NUM_CA * (PEPCT*NUM_CA-1) / 2 
        SCmax = PEPCT*3*NUM_RES * (PEPCT*3*NUM_RES-1) / 2
        MCSCmax = PEPCT*NUM_CA * PEPCT*3*NUM_RES / 2
        AMDmax = PEPCT*NUM_AMD * (PEPCT*NUM_AMD-1) / 2
        NH3max = PEPCT * (PEPCT-1) / 2
        COOmax = PEPCT * (PEPCT-1) / 2
        NH3COOmax = PEPCT * PEPCT / 2

        data1[:,1] = normalize_data(data1[:,1], MCmin, MCmax)
        data2[:,1] = normalize_data(data2[:,1], SCmin, SCmax)
        data3[:,1] = normalize_data(data3[:,1], MCSCmin, MCSCmax)
        data4[:,1] = normalize_data(data4[:,1], AMDmin, AMDmax)
        data5[:,1] = normalize_data(data5[:,1], NH3COOmin, NH3COOmax)

        plotstep=1

        linealpha = 0.4
        line1, = ax.plot(data1[:tmax:plotstep,0],data1[:tmax:plotstep,1],label='MC-MC',alpha=linealpha)
        line2, = ax.plot(data2[:tmax:plotstep,0],data2[:tmax:plotstep,1],label='SC-SC',alpha=linealpha)
        line3, = ax.plot(data3[:tmax:plotstep,0],data3[:tmax:plotstep,1],label='MC-SC',alpha=linealpha)
        line4, = ax.plot(data4[:tmax:plotstep,0],data4[:tmax:plotstep,1],label='AMD-AMD',alpha=linealpha)
        line5, = ax.plot(data5[:tmax:plotstep,0],data5[:tmax:plotstep,1],label='NH3-COO',alpha=linealpha)

        ax.set_xlim([0,tmax])

        # axsecond = ax.twinx()
        ### line6, = axsecond.plot(data6ma[:tmax],'k--',label='clusters')
        # line6, = axsecond.plot(data6[:tmax:plotstep,0],data6[:tmax:plotstep,1],'k--',label='clusters')
        # if interaction=='cluster':
        #     ax.legend(
        #         handles=[line1,line2,line3,line4,line5],
        #         loc='center',bbox_to_anchor=(0.8,.31)
        #     )
        # # ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        # return axsecond
    return makeplotfromdatadir, normalize_data, np, plt, re


@app.cell
def _(makeplotfromdatadir, plt):
    # ORIGINAL MANUSCRIPT PLOT
    fig, ((ax1,ax2),(ax3,ax4)) = plt.subplots(nrows=2,ncols=2,figsize=(10,7.5))

    ax12 = makeplotfromdatadir("/home/mason/exdrive/oligo/F2/CG/F2_32-0",32, 2.5,  2,ax1)
    ax22 = makeplotfromdatadir("/home/mason/exdrive/oligo/F4/CG/F4_32-1/",32, .5,  4,ax2)
    ax32 = makeplotfromdatadir("/home/mason/exdrive/oligo/F2/CG/F2_64",    64, 2.5,  2,ax3)
    ax42 = makeplotfromdatadir("/home/mason/exdrive/oligo/F4/CG/F4_64-10", 64, .5,  4,ax4,'cluster')

    ax1.annotate("micelles",(.2,.9),xycoords='axes fraction',fontsize="large")
    ax2.annotate("rod",     (.2,.9),xycoords='axes fraction',fontsize="large")
    ax3.annotate("micelles",(.2,.9),xycoords='axes fraction',fontsize="large")
    ax4.annotate("network", (.2,.9),xycoords='axes fraction',fontsize="large")

    fig.text(.1,.5,"Normalized contact counts", ha='center', va='center',rotation=90,fontsize="large")
    fig.text(.53,.03,"Simulated time [ps]", ha='center', va='center',rotation=0,fontsize="large")

    fig.text(.07,.7,"32 peptides", ha='center', va='center',rotation=90,fontsize="xx-large")
    fig.text(.07,.3,"64 peptides", ha='center', va='center',rotation=90,fontsize="xx-large")

    fig.text(.32,.95,"F2 systems", ha='center', va='center',rotation=0,fontsize="xx-large")
    fig.text(.75,.95,"F4 systems", ha='center', va='center',rotation=0,fontsize="xx-large")

    plt.subplots_adjust(left=.15,top=.9,bottom=0.1,right=.9,wspace=.3,hspace=.18)

    plt.show()
    return


@app.cell
def _(itertools, makeplotfromdatadir, plt, rcParams):
    # ENSEMBLE PLOT

    END_TIME_ns = 2.5
    figa, ((axa,axb),(axc,axd)) = plt.subplots(nrows=2,ncols=2,figsize=(10,7.5))
    # figa, (axa,axb)= plt.subplots(nrows=2,ncols=1,figsize=(10,7.5))

    def set_color_cycle(self, clist=None):
        if clist is None:
            clist = rcParams['axes.color_cycle']
        self.color_cycle = itertools.cycle(clist)

    def set_color_cycle(self, clist):
        """
        Set the color cycle for any future plot commands on this Axes.

        *clist* is a list of mpl color specifiers.
        """
        self._get_lines.set_color_cycle(clist)
        self._get_patches_for_fill.set_color_cycle(clist)

    for i in range(1,10):
        # plt.gca().set_prop_cycle(None)
        ax12a = makeplotfromdatadir(f"/home/mason/exdrive/oligo/F2/CG/F2_32-{i}",32, END_TIME_ns,  2,axa)
        ax22a = makeplotfromdatadir(f"/home/mason/exdrive/oligo/F4/CG/F4_32-{i}",32, END_TIME_ns,  4,axb)
        ax32a = makeplotfromdatadir(f"/home/mason/exdrive/oligo/F2/CG/F2_64-{i}", 64, END_TIME_ns,  2,axc)
        ax42a = makeplotfromdatadir(f"/home/mason/exdrive/oligo/F4/CG/F4_64-{i}", 64, END_TIME_ns,  4,axd)
        axa.set_prop_cycle(None)
        axb.set_prop_cycle(None)
        axc.set_prop_cycle(None)
        axd.set_prop_cycle(None)

    figa.text(.1,.5,"Normalized contact counts", ha='center', va='center',rotation=90,fontsize="large")
    figa.text(.53,.03,"Simulation steps / 1000", ha='center', va='center',rotation=0,fontsize="large")

    figa.text(.07,.7,"32 peptides", ha='center', va='center',rotation=90,fontsize="xx-large")
    figa.text(.07,.3,"64 peptides", ha='center', va='center',rotation=90,fontsize="xx-large")

    figa.text(.32,.95,"F2 systems", ha='center', va='center',rotation=0,fontsize="xx-large")
    figa.text(.75,.95,"F4 systems", ha='center', va='center',rotation=0,fontsize="xx-large")

    leg = axd.legend(
        labels=['MC-MC','SC-SC','MC-SC','AMD-AMD','NH3-COO'],
        loc='center',bbox_to_anchor=(0.8,.26),

    )
    for lh in leg.legendHandles: 
        lh.set_alpha(1)

    plt.subplots_adjust(left=.15,top=.9,bottom=0.1,right=.9,wspace=.2,hspace=.18)
    #plt.tight_layout()
    plt.savefig(f"fig-SI-clustercontacts-{END_TIME_ns}.png")

    plt.show()
    return


@app.cell
def _(normalize_data, np, re):
    # REWORKED PLOTTING FUNCTION FOR SI FIG
    def makeplotfromdatadir2(DATADIR,PEPCT,TMAX_ns,NUM_RES,ax,interaction):
        p = re.compile(r".*(F[24](a[0-9]d[0-9])?_[0-9]+-?[0-9]+).*")
        SYSNAME = p.match(DATADIR).group(1)
        # print(f'sysname is {SYSNAME}')

        PEPCT=int(PEPCT) # 64
        tmax = int(TMAX_ns* 1000)
        NUM_RES = int(NUM_RES)

        if interaction == "cluster": 
            DATAFILE="nclust.xvg"
            DATASUBDIR="cluster-0-100"

        elif interaction == "clustsize": 
            DATAFILE="avclust.xvg"
            DATASUBDIR="."

        else: 
            DATAFILE=f"numcont_{interaction}.xvg"
            DATASUBDIR="contacts-0-100"

        with open(f"{DATADIR}/{DATASUBDIR}/{DATAFILE}") as f1:
            data1 = np.loadtxt(f1,skiprows=0,usecols=(0,1),comments=["@","#"])

        NUM_CA  = NUM_RES
        NUM_AMD = NUM_RES - 1
        AMDmin=0
        NH3min=0
        COOmin=0
        NH3COOmin=0
        MCmin=0
        SCmin=0
        MCSCmin=0
        clustermin=0

        # max number is if somehow they are all in contact which of course can't happen
        MCmax = PEPCT*NUM_CA * (PEPCT*NUM_CA-1) / 2 
        SCmax = PEPCT*3*NUM_RES * (PEPCT*3*NUM_RES-1) / 2
        MCSCmax = PEPCT*NUM_CA * PEPCT*3*NUM_RES / 2
        AMDmax = PEPCT*NUM_AMD * (PEPCT*NUM_AMD-1) / 2
        NH3max = PEPCT * (PEPCT-1) / 2
        COOmax = PEPCT * (PEPCT-1) / 2
        NH3COOmax = PEPCT * PEPCT / 2
        clustermax=70

        clustsizemin = 0

        clustsizemax = PEPCT

        ranges = {
            'MCMC':[MCmin,MCmax],
            'SCSC':[SCmin,SCmax],
            'MCSC':[MCSCmin,MCSCmax],
            'AMDAMD':[AMDmin,AMDmax],
            'NH3COO':[NH3COOmin,NH3COOmax],
            'cluster':[clustermin,clustermax],
            'clustsize':[clustsizemin,clustsizemax]
        }


        if interaction != "cluster": 
            data1[:,1] = normalize_data(data1[:,1], ranges[interaction][0], ranges[interaction][1])

        plotstep=1

        ax.plot(data1[:tmax:plotstep,0],data1[:tmax:plotstep,1],label=interaction)

        ax.set_xlim([0,tmax])

        # ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    return (makeplotfromdatadir2,)


@app.cell
def _(makeplotfromdatadir2, plt):
    # SI CONTACTS FIG
    figb, ((axa1,axa2,axa3),(axa4,axa5,axa6),(axa7,axa8,axa9),(axa10,axa11,axa12)) = \
        plt.subplots(nrows=4,ncols=3,figsize=(10,6),sharex='col')

    tmax = 2.5
    for j in range(1,10):
        makeplotfromdatadir2(f"/home/mason/exdrive/oligo/F2/CG/F2_32-{j}",32, tmax,  2,axa1,'MCMC')
        makeplotfromdatadir2(f"/home/mason/exdrive/oligo/F2/CG/F2_32-{j}",32, tmax,  2,axa2,'SCSC')
        makeplotfromdatadir2(f"/home/mason/exdrive/oligo/F2/CG/F2_32-{j}",32, tmax,  2,axa3,'MCSC')
        makeplotfromdatadir2(f"/home/mason/exdrive/oligo/F2/CG/F2_32-{j}",32, tmax,  2,axa4,'AMDAMD')
        makeplotfromdatadir2(f"/home/mason/exdrive/oligo/F2/CG/F2_32-{j}",32, tmax,  2,axa5,'NH3COO')
        makeplotfromdatadir2(f"/home/mason/exdrive/oligo/F2/CG/F2_32-{j}",32, tmax,  2,axa6,'cluster')

        makeplotfromdatadir2(f"/home/mason/exdrive/oligo/F2/CG/F2_64-{j}",64, tmax,  2,axa1,'MCMC')
        makeplotfromdatadir2(f"/home/mason/exdrive/oligo/F2/CG/F2_64-{j}",64, tmax,  2,axa2,'SCSC')
        makeplotfromdatadir2(f"/home/mason/exdrive/oligo/F2/CG/F2_64-{j}",64, tmax,  2,axa3,'MCSC')
        makeplotfromdatadir2(f"/home/mason/exdrive/oligo/F2/CG/F2_64-{j}",64, tmax,  2,axa4,'AMDAMD')
        makeplotfromdatadir2(f"/home/mason/exdrive/oligo/F2/CG/F2_64-{j}",64, tmax,  2,axa5,'NH3COO')
        makeplotfromdatadir2(f"/home/mason/exdrive/oligo/F2/CG/F2_64-{j}",64, tmax,  2,axa6,'cluster')

        makeplotfromdatadir2(f"/home/mason/exdrive/oligo/F4/CG/F4_32-{j}",32, tmax,  4,axa7,'MCMC')
        makeplotfromdatadir2(f"/home/mason/exdrive/oligo/F4/CG/F4_32-{j}",32, tmax,  4,axa8,'SCSC')
        makeplotfromdatadir2(f"/home/mason/exdrive/oligo/F4/CG/F4_32-{j}",32, tmax,  4,axa9,'MCSC')
        makeplotfromdatadir2(f"/home/mason/exdrive/oligo/F4/CG/F4_32-{j}",32, tmax,  4,axa10,'AMDAMD')
        makeplotfromdatadir2(f"/home/mason/exdrive/oligo/F4/CG/F4_32-{j}",32, tmax,  4,axa11,'NH3COO')
        makeplotfromdatadir2(f"/home/mason/exdrive/oligo/F4/CG/F4_32-{j}",32, tmax,  4,axa12,'cluster')

        makeplotfromdatadir2(f"/home/mason/exdrive/oligo/F4/CG/F4_64-{j}",64, tmax,  4,axa7,'MCMC')
        makeplotfromdatadir2(f"/home/mason/exdrive/oligo/F4/CG/F4_64-{j}",64, tmax,  4,axa8,'SCSC')
        makeplotfromdatadir2(f"/home/mason/exdrive/oligo/F4/CG/F4_64-{j}",64, tmax,  4,axa9,'MCSC')
        makeplotfromdatadir2(f"/home/mason/exdrive/oligo/F4/CG/F4_64-{j}",64, tmax,  4,axa10,'AMDAMD')
        makeplotfromdatadir2(f"/home/mason/exdrive/oligo/F4/CG/F4_64-{j}",64, tmax,  4,axa11,'NH3COO')
        makeplotfromdatadir2(f"/home/mason/exdrive/oligo/F4/CG/F4_64-{j}",64, tmax,  4,axa12,'cluster')


    ylims = {
        'MCMC':[0,.07],
        'SCSC':[0,.15],
        'MCSC':[0,.07],
        'AMDAMD':[0,.1],
        'NH3COO':[0,.07],
        'cluster':[0,20]
    }
    axa1.set_ylim([0,ylims['MCMC'][1]])
    axa2.set_ylim([0,ylims['SCSC'][1]])
    axa3.set_ylim([0,ylims['MCSC'][1]])
    axa4.set_ylim([0,ylims['AMDAMD'][1]])
    axa5.set_ylim([0,ylims['NH3COO'][1]])
    axa6.set_ylim([0,ylims['cluster'][1]])
    axa7.set_ylim([0,ylims['MCMC'][1]])
    axa8.set_ylim([0,ylims['SCSC'][1]])
    axa9.set_ylim([0,ylims['MCSC'][1]])
    axa10.set_ylim([0,ylims['AMDAMD'][1]])
    axa11.set_ylim([0,ylims['NH3COO'][1]])
    axa12.set_ylim([0,ylims['cluster'][1]])

    fracx, fracy = 0.02, 0.85
    axa1.annotate("MCMC contacts",(fracx,fracy),xycoords='axes fraction',fontsize="large")
    axa2.annotate("SCSC contacts",(fracx,fracy),xycoords='axes fraction',fontsize="large")
    axa3.annotate("MCSC contacts",(fracx,fracy),xycoords='axes fraction',fontsize="large")
    axa4.annotate("AMDAMD contacts",(fracx,fracy),xycoords='axes fraction',fontsize="large")
    axa5.annotate("NH3COO contacts",(fracx,fracy),xycoords='axes fraction',fontsize="large")
    axa6.annotate("cluster counts",(.4,fracy),xycoords='axes fraction',fontsize="large")
    axa7.annotate("MCMC contacts",(fracx,fracy),xycoords='axes fraction',fontsize="large")
    axa8.annotate("SCSC contacts",(fracx,fracy),xycoords='axes fraction',fontsize="large")
    axa9.annotate("MCSC contacts",(fracx,fracy),xycoords='axes fraction',fontsize="large")
    axa10.annotate("AMDAMD contacts",(fracx,fracy),xycoords='axes fraction',fontsize="large")
    axa11.annotate("NH3COO contacts",(fracx,fracy),xycoords='axes fraction',fontsize="large")
    axa12.annotate("cluster counts",(.4,fracy),xycoords='axes fraction',fontsize="large")



    figb.text(.1,.5,"Normalized contact counts", ha='center', va='center',rotation=90,fontsize="large")
    # figb.text(.92,.5,"Moving average cluster counts", ha='center', va='center',rotation=90,fontsize="large")
    figb.text(.53,.03,"Simulation steps / 1000", ha='center', va='center',rotation=0,fontsize="large")

    figb.text(.07,.7,"F2 systems", ha='center', va='center',rotation=90,fontsize="xx-large")
    figb.text(.07,.3,"F4 systems", ha='center', va='center',rotation=90,fontsize="xx-large")

    # figb.text(.32,.95,"F2 systems", ha='center', va='center',rotation=0,fontsize="xx-large")
    # figb.text(.75,.95,"F4 systems", ha='center', va='center',rotation=0,fontsize="xx-large")

    plt.subplots_adjust(left=.18,top=.9,bottom=0.1,right=.9,wspace=.24,hspace=.18)
    #plt.tight_layout()
    plt.savefig(f"fig-clustercontacts-{tmax}.png")

    plt.show()
    return


@app.cell
def _(makeplotfromdatadir2, plt):
    # SI CLUSTERING FIG
    figc, ((axb1,axb2),(axb3,axb4)) = \
        plt.subplots(nrows=2,ncols=2,figsize=(10,6),sharex='col')

    MY_T_MAX=2.5

    for k in range(1,10):
        makeplotfromdatadir2(f"/home/mason/exdrive/oligo/F2/CG/F2_32-{k}",32, MY_T_MAX,  2,axb1,'cluster')
        makeplotfromdatadir2(f"/home/mason/exdrive/oligo/F2/CG/F2_64-{k}",64, MY_T_MAX,  2,axb2,'cluster')

        makeplotfromdatadir2(f"/home/mason/exdrive/oligo/F4/CG/F4_32-{k}",32, MY_T_MAX,  4,axb3,'cluster')
        makeplotfromdatadir2(f"/home/mason/exdrive/oligo/F4/CG/F4_64-{k}",64, MY_T_MAX,  4,axb4,'cluster')

    figc.text(.1,.5,"Cluster counts", ha='center', va='center',rotation=90,fontsize="large")
    figc.text(.92,.5,"Average peptides per cluster", ha='center', va='center',rotation=90,fontsize="large")
    figc.text(.53,.03,"Simulation steps / 1000", ha='center', va='center',rotation=0,fontsize="large")

    figc.text(.07,.7,"F2 systems", ha='center', va='center',rotation=90,fontsize="xx-large")
    figc.text(.07,.3,"F4 systems", ha='center', va='center',rotation=90,fontsize="xx-large")

    plt.subplots_adjust(left=.15,top=.9,bottom=0.1,right=.9,wspace=.20,hspace=.18)
    #plt.tight_layout()
    plt.savefig(f"fig-clustercontacts-{MY_T_MAX}ns.png")

    plt.show()
    return


@app.cell
def _(np):
    # AVG CLUSTERING FIG
    # read in an ensemble of average cluster counts e.g. F4-32 x 9
    def make_file_lists(pep,pepct):
        return (
            [f"/home/mason/exdrive/oligo/{pep}/CG/{pep}_{str(pepct)}-{str(i)}/"
             f"cluster-0-100/avclust.xvg" for i in range(1,10)],
             # f"avclust.xvg" for i in range(1,10)],
            [f"/home/mason/exdrive/oligo/{pep}/CG/{pep}_{str(pepct)}-{str(i)}/"
             f"cluster-0-100/avclust.xvg" for i in range(1,10)]
             # f"avclust.xvg" for i in range(1,10)]
             )

    def read_ensemble(data_files:list):
        ensemble_data = None
        for data_file in data_files:
            file_data = np.loadtxt(data_file,skiprows=0,max_rows=579,usecols=(0,1),comments=["@","#"])
            # print(file_data)
            if type(ensemble_data) == type(None):
                ensemble_data = file_data
                # print(ensemble_data[:5,:])
            else: 
                file_data = file_data[:,1]
                file_data = file_data[:,np.newaxis]
                ensemble_data = np.hstack((ensemble_data, file_data))
        return ensemble_data

    def calc_ensemble_avg(ensemble_data, pepct, CG_ATOM_COUNT, countadjust=None):
        # divide by the # of CG atoms: 11 for FF, 21 for FFFF (ref nclust.xvg and avclust.xvg)
        molcounts = ensemble_data[:,1:] / CG_ATOM_COUNT
        # adjust by the count of peptides in system
        if countadjust=='otherthing':
            molcounts = molcounts / pepct # gives the size of the average aggregate relative to system size 
        if countadjust=='invert':
            molcounts = pepct / molcounts # invert type. counts how many aggregates exist in the system, on average
        ensemble_avg = np.average(molcounts,axis=1)
        ensemble_se = np.std(molcounts,axis=1)
        ensemble_avg_withtime = np.column_stack((ensemble_data[:,0],ensemble_avg))
        ensemble_se_withtime = np.column_stack((ensemble_data[:,0],ensemble_se))
        return ensemble_avg_withtime, ensemble_se_withtime

    

    return calc_ensemble_avg, make_file_lists, read_ensemble


@app.cell
def _(calc_ensemble_avg, make_file_lists, plt, read_ensemble):
    # COUNT_ADJUST=None
    # COUNT_ADJUST='otherthing'
    COUNT_ADJUST='invert'

    f232nclust, f232avclust = make_file_lists('F2',32)
    f264nclust, f264avclust = make_file_lists('F2',64)
    f432nclust, f432avclust = make_file_lists('F4',32)
    f464nclust, f464avclust = make_file_lists('F4',64)

    f232data_nclust = read_ensemble(f232nclust)
    f264data_nclust = read_ensemble(f264nclust)
    f432data_nclust = read_ensemble(f432nclust)
    f464data_nclust = read_ensemble(f464nclust)

    f232avg_nclust,f232se_nclust = calc_ensemble_avg(f232data_nclust,32,11,COUNT_ADJUST)
    f264avg_nclust,f264se_nclust = calc_ensemble_avg(f264data_nclust,64,11,COUNT_ADJUST)
    f432avg_nclust,f432se_nclust = calc_ensemble_avg(f432data_nclust,32,21,COUNT_ADJUST)
    f464avg_nclust,f464se_nclust = calc_ensemble_avg(f464data_nclust,64,21,COUNT_ADJUST)

    f232data_avclust = read_ensemble(f232avclust)
    f264data_avclust = read_ensemble(f264avclust)
    f432data_avclust = read_ensemble(f432avclust)
    f464data_avclust = read_ensemble(f464avclust)

    f232avg_avclust,f232se_avclust = calc_ensemble_avg(f232data_avclust,32,11,COUNT_ADJUST)
    f264avg_avclust,f264se_avclust = calc_ensemble_avg(f264data_avclust,64,11,COUNT_ADJUST)
    f432avg_avclust,f432se_avclust = calc_ensemble_avg(f432data_avclust,32,21,COUNT_ADJUST)
    f464avg_avclust,f464se_avclust = calc_ensemble_avg(f464data_avclust,64,21,COUNT_ADJUST)

    # fige, axe = plt.subplots(nrows=1,ncols=1,figsize=(10,6))
    fige, axe = plt.subplots(nrows=1,ncols=1,figsize=(8,6))

    alphalevel=.5

    axe.plot(f232avg_avclust[:,0],f232avg_avclust[:,1],label='F2-32')
    axe.fill_between(f232avg_avclust[:,0], f232avg_avclust[:,1]-f232se_avclust[:,1], f232avg_avclust[:,1]+f232se_avclust[:,1], alpha=alphalevel)

    axe.plot(f264avg_avclust[:,0],f264avg_avclust[:,1],label='F2-64')
    axe.fill_between(f264avg_avclust[:,0], f264avg_avclust[:,1]-f264se_avclust[:,1], f264avg_avclust[:,1]+f264se_avclust[:,1], alpha=alphalevel)

    axe.plot(f432avg_avclust[:,0],f432avg_avclust[:,1],label='F4-32')
    axe.fill_between(f432avg_avclust[:,0], f432avg_avclust[:,1]-f432se_avclust[:,1], f432avg_avclust[:,1]+f432se_avclust[:,1], alpha=alphalevel)

    axe.plot(f464avg_avclust[:,0],f464avg_avclust[:,1],label='F4-64')
    axe.fill_between(f464avg_avclust[:,0], f464avg_avclust[:,1]-f464se_avclust[:,1], f464avg_avclust[:,1]+f464se_avclust[:,1], alpha=alphalevel)

    # axe.set_title('average size of aggregates [#molecules]')
    # axe.set_title('average aggregate size in proportion to system size [peptides/peptides]') # otherthing
    axe.set_title('dispersion -- average number of aggregates in system [#aggregates]') # invert

    lege = axe.legend(
        # loc='center',bbox_to_anchor=(0.58,.29), #
        # loc='center',bbox_to_anchor=(0.68,.38), # otherthing
        loc='center',bbox_to_anchor=(0.2,.8), # inverted
    )
    for lhe in lege.legendHandles: 
        lhe.set_alpha(1)

    # axe.set_ylim([0,71])
    # axe.set_ylim([0,1.2])
    axe.set_ylim([0,10])

    axe.set_xlim([0,59000])

    plt.savefig(f"fig-aggregatesize{COUNT_ADJUST}.png")
    plt.show()
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
