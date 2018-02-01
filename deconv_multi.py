#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Spectral deconvolution of hemoglobin solutions

@author: Richard Hickey
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.offsetbox import AnchoredText
from scipy.optimize import curve_fit
import pandas as pd
import glob
import os

def deconv(datafile, # List of file path strings
           reffile='refspec.dat', # Reference spectra
           norm=False,  # Normalize minimum value to 0
           savePng=True, # Output image
           except_species = [], # Omit this list of species
           nm_min=450, # Minimum wavelength
           nm_max=700, # Maximum wavelength
           opID=''): # Operator ID
    """
    Performs spectral deconvolution of an experimental hemoglobin solution compared to standard references (reffile). datafile is a LIST of path strings. norm subtracts the lowest value (usually at 700 nm) from all entries.
    """
    # Turn a single filename into a 1-item list to be iterated
    if isinstance(datafile, str):
        datafile = [datafile]
    # Read reference spectra
    ref = pd.read_csv(reffile,'\t')
    # Remove unwanted reference species
    ref = ref.drop(except_species, axis=1)

    species = list(ref.drop('nm',axis=1))
    n = len(species) # number of species
    k_init = np.ones(n) # Initial guesses for coefficients (default 1)

    myBounds = (0,np.inf) # Limits for coefficients (non-neg)
    
    # Take only evens between wavelength limits
    ref = ref[ref['nm'] >= nm_min]
    ref = ref[ref['nm'] <= nm_max]
    ref = ref[ref['nm'] % 2 == 0]
    
    # Define curve_fit function    
    def func(X, *params):
        return np.stack(params).dot(X)

    def cleanData(df, nm_min, nm_max):
        """
        Inputs a dataframe of reference spectra as well as wavelength cutoffs.
        Trims all data to be within the limits, and removes data points that don't match (odds)
        """
        # Take only evens between wavelength limits
        df = df[df['nm'] >= nm_min]
        df = df[df['nm'] <= nm_max]
        df = df[df['nm'] % 2 == 0]
        
        return df
    
    def multiColDeconv(ref,exp):
        """
        Handle multiple columns of experimental data by treating it as 
        1) Replicates of the same data points
        2) Kinetic data over time
        """
        # Check how many columns we have
        # Treat the first as wavelengths
        exp.rename(columns={0:'nm'}, inplace=True)
        
        # If two, run deconvolution
        
        # If more than two, check if we are kinetic or replicate
        # If replicate, average all non-wavelength spectra into one
        timePoints = list(exp.drop('nm',axis=1))
        exp['average'] = exp[timePoints].mean(axis=1)
        
        # Then perform deconvolution
        
        # If kinetic:
        
        # For each exp column:
        # timePoints = list(exp.drop('nm',axis=1)) # list of all timepoints
        
        # Perform deconvolution against all relevant specrta
        # Make dataframe of time, error, species composition
        # create one column for each species
        kdf = pd.DataFrame(timePoints, columns=['Time']) # kinetic data frame
        kdf = pd.concat([kdf,pd.DataFrame(columns=species)])
        kdf.set_index('Time') # do we need this?
        # make error columns
        species_err = [sp + '_err' for sp in species]
        kdf = pd.concat([kdf,pd.DataFrame(columns=species_err)])
        for timePoint in exp:
            # Make call to curve_fit
            coeffs, perr = doFitting(ref.drop('nm',axis=1).T, exp[timePoint])
            # Extract error and coefficients from results
            for sp,sp_e,coeff,sd in zip(species,species_err,coeffs,perr):
                kdf[kdf['Time']==timePoint][sp] = coeff # each coefficient
                kdf[kdf['Time']==timePoint][sp_e] = sd # each coefficient error
        return kdf

            # Save numeric data (no file output yet)
        # Afterwards, graph composition over time (from header) as scatter with error bars

    def doFitting(refCols,expCol):
        coeffs, pcov = curve_fit(func, refCols, expCol, p0=k_init, bounds=myBounds)
        # Extract error and coefficients from results
        perr = np.sqrt(np.diag(pcov))
        return coeffs, perr
        
        
        
    # Do the following for each file we are given:
    for thisfile in datafile:
        # Figure out where in the world we are working
        myPath = os.path.basename(thisfile) # yields 'filename.ext'
        myTitle, myExt = os.path.splitext(myPath) # yields 'filename', '.ext'
        myDir = os.path.dirname(thisfile) # yields 'data/somebatch/'
        # Decide where output will go
        out_dir = myDir + '/' + 'output'
        
        # Read the file
        # TODO: Make this its own function
        if myExt == ".dat" or myExt == ".txt" or myExt==".csv":
            exp = pd.read_csv(thisfile,'\t')
        elif myExt == ".xls" or myExt == ".xlsx":
            exp = pd.read_excel(thisfile)
        else:
            raise Exception("Error: Unknown input file type (must be .dat, .txt, .csv, .xls, .xlsx)")

        print("Running "+thisfile) # Announce file in case we crash during it
        
        # Take only evens between wavelength limits
        exp = cleanData(exp)
        
        # If desired, normalize to 0 (usually at 700)
        if norm:
            exp['A'] = exp['A']-np.min(exp['A'])
        
        # Make call to curve_fit
        popt, pcov = curve_fit(func, ref.drop('nm',axis=1).T, exp['A'], p0=k_init, bounds=myBounds)

        # Extract error and coefficients from results
        perr = np.sqrt(np.diag(pcov)) # standard errors
        concs = popt

        # Create a line of best fit using our results
        exp['fit'] = func(ref.drop('nm',axis=1).T, *popt)
        ss_r = np.sum((exp['A'] - exp['fit'])**2)
        ss_t = np.sum((exp['A'] - np.mean(exp['A']))**2)
        r2 = 1-(ss_r/ss_t)
        
        # Print fit data and coefficients
        
        tbox = r"$R^2$ fit: {:.5f}".format(r2)
        #%% Output text report
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
        tbody = ["Curve fitting report",
                 "Using scipy.optimize.curve_fit (non-linear least squares regression)",
                 "Version 1.1.0 \t Richard Hickey \t Ohio State University",
                 ""]
        tbody += ["Sample: \t"+myTitle,
                  "Filename: \t"+thisfile,
                  "Reference: \t"+reffile,
                  "Wavelengths: \t"+str(nm_min)+"-"+str(nm_max),
                  "Operator: \t"+opID]
        if norm:
            tbody += ["Normalized to lowest value = 0"]
        tbody += [""]
        tbody += ["Species\tCoefficients (Percent)\tStandard error*"]
        for sp,conc,sd in zip(species,concs,perr):
            cpercent = 100*conc/sum(concs)
            if conc< 0.000001:
                sdpercent = 0
            else:
                sdpercent = 100 * sd / conc
            tbox = tbox + "\n" + "{:.2f}% ".format(cpercent) + str(sp)
            tbody += [sp+"\t{:.6f} ({:.2f}%)".format(conc,cpercent)+"\t{:.6f} ({:.2f}%)".format(sd,sdpercent)]
        tbody += ["",
                  "Fit data:",
                  "Sum of squares (residual) = "+str(ss_r),
                  "Sum of squares (total) = "+str(ss_t),
                  "R-squared = "+str(r2)]
        tbody += ["",
                  "* Standard error being defined as the diagonal of the square root of the coefficient covariance matrix. The covariance matrix appears below.",
                  str(pcov)]
        # Print output report to console
        print('\n'.join(tbody))
        # Print output report to .txt file
        #f = open(out_dir+'/'+myTitle+'_output.txt','w')    
        f = open(out_dir+'/'+myTitle+'_output.txt','w')      
        f.write('\n'.join(tbody))
        f.close()

        #%% Plot results
        
        fig, ax = plt.subplots(1,1)
        ax.plot(exp['nm'], exp['A'], 'b.-', label='data')
        ax.plot(exp['nm'], exp['fit'], 'r-', label='fit')

        ax.set_title(myTitle)
        ax.set_xlabel('Wavelength (nm)')
        ax.set_ylabel('Absorbance')
        ax.legend(loc=1)
        anchored_text = AnchoredText(tbox, loc=5,prop=dict(color='black', size=9))
        anchored_text.patch.set(boxstyle="round,pad=0.,rounding_size=0.2",alpha=0.2)
        ax.add_artist(anchored_text)    
        #%% Save figure 
        if savePng:
            plt.savefig(out_dir+'/'+myTitle+'_output.png', bbox_inches='tight',facecolor='white', dpi=300)
        
        #%% Output spectra file
        exp.columns = ['Wavelength (nm)','Original wave','Best fit'] # (This messes up column names for plotting)
        writer = pd.ExcelWriter(out_dir+'/'+myTitle+'_output.xlsx')
        exp.to_excel(writer, index=False)
        writer.save()
        #exp.to_csv(out_dir+'/'+myTitle+'_output.dat',sep='\t',index=False)
        plt.show()    


#%% If running file directly, do this
if __name__ == '__main__':
    pass
    # These commands read all of the .dat files in the specified folder

    #myData = glob.glob('data/ZIF_1-24-18/*.dat')
    #allData = glob.glob('data/test/**/*.dat', recursive=True)
    
    # This is a list of commands used to create the majority of output so far
    # I left them here just in case we want to re-run any
    #deconv(datafile=myData,reffile='refspec.dat',except_species=['DeoxyHb','HbCO'])
    
    #deconv(datafile=allData,reffile='ref_offset.dat',except_species=['HbCO'], norm=False)
    #deconv(datafile=myData,reffile='ref_offset.dat',except_species=['HbCO'], norm=False)
"""
Here is an example call to the function with a single file:
deconv(datafile=['myExperimentalSpectra.dat'],reffile='refspec.dat',except_species=['DeoxyHb'])
"""
