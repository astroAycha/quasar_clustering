

import numpy as np
from astropy.io import fits

from astropy.table import Table



def spec_look_up(cluster_array, k):

    """ read a list of sdss names, corss-match list with table with mjd, plate, fiber IDs to generate spectra file name with format mjd-plate-fiber_proc.fits e.g., spec-3587-55182-0691_proc.fits
    the processed spectra (i.e., corrected for Galactic extinction and de-redshifted and normalized. See spec_proc.py)
    
    cluster_array: a 2D numpy array with the results of a clustering trial.  Each sample (row) has the values for the features (parameters) used in the clustering and the sdss names of the objects in each cluster. and a clolumn withe clusters labels. e.g, 'c4_ew_hwhm_5clstrs_name.npy'
    k: the cluster label you want to look at: k=0 --> first cluster, k=1 --> second cluster...
    
        """

    all_clstrs= np.load(cluster_array)
    
    data= Table.read('dr10q.fits') #DR10 catalog
    
    ss = np.load("dr10qsample.npy") # subsample with conditions (see quasar_cluster.py)
    
    #corss-match the above two files
    
    clstr_k= ss[(ss['SDSS_NAME'] == all_clstrs[:,4]) & (all_clstrs[:, 3].astype(int) == k)] # only samples in cluster k

    print len(clstr_k)

    spec_files_list=[]
    sdss_names_list= []
    for s in range(len(clstr_k)):
        spectrum_name= "./proc_data/spec-"+str(clstr_k['PLATE'][s])+"-"+str(clstr_k['MJD'][s])+"-"+str(clstr_k['FIBERID'][s]).zfill(4)+"_proc.fits"
        spec_files_list.append(spectrum_name)
        sdss_names_list.append(clstr_k['SDSS_NAME'][s])
    
    
        ## plot the spectra
    fig= figure()
    ax=fig.add_subplot(111)
    
    for (file, name) in zip(spec_files_list, sdss_names_list):
        try:
            spec= fits.open(file)
            wavelen= spec[0].data[0]
            flx= spec[0].data[1]
           # plot(wavelen[c4], flx[c4])
            plot (wavelen, flx)
            xlim(1350, 1750)
            ylim(-1, 4.5)
            axvline(1549, ls= ':')
            text(1355, 3.5, "SDSS "+name)
            print str(file)
            
            resume = input("Press Enter to plot next spectrum on list.")
        
        except SyntaxError:
            pass
            clf()
    



def spec_display(spec_ls, n1, n2):

    """ read a list of spectra and display them. Read input and use as flag (for either low SNR or BAL quasar).
        
        spec_ls: numpy array with the quasar sample as selected in quasar_cluster.py
        flag= 0 keep
        flag= 1 reject
        
        n1: start at line number n1
        n2: stop at line number n2
        
    """

    data= np.load(spec_ls)
    
    sample= data[n1:n2+1]
    print "Looking at lines", n1, "to", n2
    
    flag_ls=[]
    names=[]
    
    wavelen= np.arange(1100, 4000, 0.1)  #wavelength array
    fig= figure(figsize(20,8))
    
    for i in range(len(sample)):
        print "Looking at spectrum number", i+1
        try:
            spectrum_name= "./proc_data/spec-"+str(sample['PLATE'][i])+"-"+str(sample['MJD'][i])+"-"+str(sample['FIBERID'][i]).zfill(4)+"_proc.fits"
            spec= fits.open(spectrum_name)
            flx= spec[0].data[1]
            
            plot(wavelen, flx, c= 'k')
            xlim(1200, 3100)
            ylim(-1,4)
            axvline(1397, ls=':')
            axvline(1549, ls=':')
            axvline(1908, ls=':')
            axvline(2800, ls=':')
            text(2500, 3, sample['SDSS_NAME'][i])
            print "Flags: 0= keep, 1= reject"
            flag= input()
            flag_ls.append(flag)
            names.append(sample['SDSS_NAME'][i])
            resume = input("Press Enter to plot next spectrum on list.")
        
        except SyntaxError:
            pass
            clf()

    new_array= np.column_stack((names, flag_ls))
    save("myflags_"+str(n1)+"_to_"+str(n2)+".npy", new_array)



