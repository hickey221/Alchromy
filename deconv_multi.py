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
#import glob
import os

#%% New functions
def readFile(filePath):
    """
    Reads in a csv or spreadsheet file. Returns a dataframe with data, and
    a dict with file information
    """
    print('Looking at ',filePath)
    # Analyze the file path and save important parts
    fileDict = {'fullPath': filePath} # Initialize dict with given path
    fileDict['name.ext'] = os.path.basename(filePath) # yields 'filename.ext'
    fileDict['name'],fileDict['ext'] = os.path.splitext(fileDict['name.ext']) # yields 'filename', '.ext'
    fileDict['dir'] = os.path.dirname(filePath) # yields 'data/somebatch/'
    fileDict['outDir'] = fileDict['dir'] + '/' + 'output' # yields data/somebatch/output

    # Read in the file
    if fileDict['ext'] in ['.dat','.txt','.csv']:
        df = pd.read_csv(filePath,'\t')
    elif fileDict['ext'] in ['.xls','.xlsx']:
        df = pd.read_excel(filePath)
    else:
        raise Exception("Error: Unknown input file type (must be .dat, .txt, .csv, .xls, .xlsx)")

    df.rename(columns={df.columns[0]:'nm'}, inplace=True)
    if df.columns[1] == '0.1':
        # Bug fix for mangled 0 in first two col names
        # '0,0' -> '0,0.1' -> 'nm, 0'
        df.rename(columns={df.columns[1]:'0'}, inplace=True)

    return df, fileDict

# Define curve_fit function
def func(X, *params):
    return np.stack(params).dot(X)

def cleanData(df, cutoff):
    """
    Inputs a dataframe of reference spectra as well as wavelength cutoffs.
    Trims all data to be within the limits, and removes data points that don't match (odds)
    """
    # Treat 1st col as wavelengths
    #df.rename(columns={df.columns[0]: 'nm'}, inplace=True) # done in readFile() now
    # Take only evens between wavelength limits
    df = df[df['nm'] >= cutoff[0]]
    df = df[df['nm'] <= cutoff[1]]
    df = df[df['nm'] % 2 == 0]

    return df

def multiColDeconv(refPath='refspec.dat',
                   filePath='test_kinetic.dat',
                   ignored=[],
                   flags={'Image':True,  # Output flags
                          'Text':True,
                          'Excel':True,
                          'Kinetic':False,
                          'Operator':'',
                          'Normalize':False,
                          'Cutoff':(450,700)}):
    """
    Handle multiple columns of experimental data by treating it as
    1) Replicates of the same data points
    2) Kinetic data over time
    """
    def kineticAnalysis():
        kdf = pd.DataFrame(timePoints, columns=['Time']) # kinetic data frame
        kdf = pd.concat([kdf,pd.DataFrame(columns=species)])
        kdf = kdf.set_index('Time') # do we need this?
        # make error columns
        species_err = [sp + '_err' for sp in species]
        species_perc = [sp + ' (%)' for sp in species] # % of total
        kdf = pd.concat([kdf,pd.DataFrame(columns=species_err)])
        for timePoint in timePoints:
            # Make call to curve_fit
            coeffs, perr = doFitting(ref.drop('nm',axis=1), exp[timePoint])
            # Extract error and coefficients from results
            for sp,sp_e,coeff,sd,sp_perc in zip(species,species_err,coeffs,perr, species_perc):
                kdf.loc[timePoint,sp] = coeff # Actual coefficient
                kdf.loc[timePoint,sp_e] = sd # Standard error
                kdf.loc[timePoint,sp_perc] = coeff/sum(coeffs) # Percent of total composition
        #kdf.sort_index(inplace=True) # Sort by time index
        ax = kdf.drop(species_err+species,axis=1).plot.area(lw=0)
        ax.set_xlabel('Time')
        ax.set_ylabel('Fractional composition')
        plt.show()
        return kdf

    # Input reference file
    ref, _ = readFile(refPath)
    ref = cleanData(ref,flags['Cutoff'])
    ref = ref.drop(ignored, axis=1)
    species = list(ref.drop('nm',axis=1)) # each non 'nm' header is a species

    # Input experimental file
    exp, fileDict = readFile(filePath)
    exp = cleanData(exp,flags['Cutoff'])
    timePoints = list(exp.drop('nm',axis=1))
    print(timePoints)

    # Check number of data cols
    nCols = len(list(exp.drop('nm',axis=1)))

    if nCols < 1: # If none, we have a problem
        raise Exception("Error: Can't find any data")
    elif nCols == 1: # If 1, run simple deconvolution
        print("Running simple deconv")
        exp.rename(columns={exp.columns[1]: 'data'}, inplace=True) # call 2nd column data
        coeffs, perr = doFitting(ref.drop('nm',axis=1),exp['data'])
        # Create a line of best fit using our results
        exp['fit'] = func(ref.drop('nm',axis=1).T, *coeffs)
        #print(coeffs)
        plotStandard(exp,fileDict,flags)
    else:# If more than two, check if we are kinetic or replicate
        if flags['Kinetic']: # Do kinetic function
            print("Running kinetic deconv")
            kdf = kineticAnalysis()
            print("Done")
            #return kdf
        else: # Assume replicates
            # Average all non-wavelength spectra into one
            print("Running average of replicates deconv")
            exp['data'] = exp[timePoints].mean(axis=1)
            # Then perform deconvolution
            coeffs, perr = doFitting(ref.drop('nm',axis=1), exp['data'])
            # Create a line of best fit using our results
            exp['fit'] = func(ref.drop('nm',axis=1).T, *coeffs)
            #print(coeffs)
            plotReplicates(exp,fileDict,flags)
            
    # Report status of completed run
    # TODO: Add more options for error codes
    statusReport = {'Code': 0, 'Message': 'Finished without incident'} # No problems
    
    return statusReport

    # Perform deconvolution against all relevant specrta
    # Make dataframe of time, error, species composition
    # create one column for each species

        # Save numeric data (no file output yet)
    # Afterwards, graph composition over time (from header) as scatter with error bars

def doFitting(refCols,expCol):
    k_init = np.ones_like(list(refCols)) # All initial guesses = 1
    myBounds = (0,np.inf) # Coefficients between 0 and +infinity
    coeffs, pcov = curve_fit(func, refCols.T, expCol, p0=k_init, bounds=myBounds)
    # Extract error and coefficients from results
    perr = np.sqrt(np.diag(pcov))
    return coeffs, perr

def plotStandard(exp,fileDict,flags):
    fig, ax = plt.subplots(1,1)
    ax.plot(exp['nm'], exp['data'], 'b.-', label='data')
    ax.plot(exp['nm'], exp['fit'], 'r-', label='fit')

    ax.set_title(fileDict['name'])
    ax.set_xlabel('Wavelength (nm)')
    ax.set_ylabel('Absorbance')
    ax.legend(loc=1)

    # Print fit data and coefficients
    ss_r = np.sum((exp['data'] - exp['fit'])**2)
    ss_t = np.sum((exp['data'] - np.mean(exp['data']))**2)
    r2 = 1-(ss_r/ss_t)
    tbox = r"$R^2$ fit: {:.5f}".format(r2)
    anchored_text = AnchoredText(tbox, loc=5,prop=dict(color='black', size=9))
    anchored_text.patch.set(boxstyle="round,pad=0.,rounding_size=0.2",alpha=0.2)
    ax.add_artist(anchored_text)

    ax.set_title(fileDict['name'])
    ax.set_xlabel('Wavelength (nm)')
    ax.set_ylabel('Absorbance')
    if flags['Image']:
        if not os.path.exists(fileDict['outDir']):
            os.makedirs(fileDict['outDir'])
        plt.savefig(fileDict['outDir']+'/'+fileDict['name']+'_output.png', bbox_inches='tight',facecolor='white', dpi=300)
    plt.show()

def plotReplicates(exp, fileDict, flags):
    fig, ax = plt.subplots(1,1)
    exp['min'] = exp.drop(['nm','fit'],axis=1).min(axis=1)
    exp['max'] = exp.drop(['nm','fit','min'],axis=1).max(axis=1)

    ss_r = np.sum((exp['data'] - exp['fit'])**2)
    ss_t = np.sum((exp['data'] - np.mean(exp['data']))**2)
    r2 = 1-(ss_r/ss_t)

    # Print fit data and coefficients
    tbox = r"$R^2$ fit: {:.5f}".format(r2)
    anchored_text = AnchoredText(tbox, loc=5,prop=dict(color='black', size=9))
    anchored_text.patch.set(boxstyle="round,pad=0.,rounding_size=0.2",alpha=0.2)
    ax.add_artist(anchored_text)

    # Fill between x, y1, y2
    ax.fill_between(exp['nm'], exp['min'], exp['max'])
    ax.plot(exp['nm'], exp['data'], 'b.-', label='data')
    ax.plot(exp['nm'], exp['fit'], 'r-', label='fit')

    ax.set_title(fileDict['name'])
    ax.set_xlabel('Wavelength (nm)')
    ax.set_ylabel('Absorbance')
    ax.legend(loc=1)
    if flags['Image']:
        if not os.path.exists(fileDict['outDir']):
            os.makedirs(fileDict['outDir'])
        plt.savefig(fileDict['outDir']+'/'+fileDict['name']+'_output.png', bbox_inches='tight',facecolor='white', dpi=300)
    plt.show()

def plotKinetic(kdf):

    pass

def printResultsExcel(df, fileDict):
    if not os.path.exists(fileDict['outDir']):
            os.makedirs(fileDict['outDir'])
    writer = pd.ExcelWriter(fileDict['outDir']+'/'+fileDict['name']+'_output.xlsx')
    df.to_excel(writer, index=False)
    writer.save()
    
def printResultsText(fileDict,flags):
    if not os.path.exists(fileDict['outDir']):
            os.makedirs(fileDict['outDir'])
    tbody = ["Curve fitting report",
             "Using scipy.optimize.curve_fit (non-linear least squares regression)",
             "Version 1.1.0 \t Richard Hickey \t Ohio State University",
             ""]
    tbody += ["Sample: \t"+fileDict['name'],
              "Filename: \t"+fileDict['name.ext'],
              "Reference: \t"+reffile,
              "Wavelengths: \t"+str(flags['Cutoff'][0])+"-"+str(flags['Cutoff'][1]),
              "Operator: \t"+flags['Operator']]
    if flags['Normalize']:
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
    f = open(fileDict['outDir']+'/'+fileDict['name']+'_output.txt','w')
    f.write('\n'.join(tbody))
    f.close()

#%%
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



    # Do the following for each file we are given:
    for thisfile in datafile:
        # Figure out where in the world we are working
        myPath = os.path.basename(thisfile) # yields 'filename.ext'
        myTitle, myExt = os.path.splitext(myPath) # yields 'filename', '.ext'
        myDir = os.path.dirname(thisfile) # yields 'data/somebatch/'
        # Decide where output will go
        out_dir = myDir + '/' + 'output'

        # Read the file
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
        #exp.columns = ['Wavelength (nm)','Original wave','Best fit'] # (This messes up column names for plotting)
        writer = pd.ExcelWriter(out_dir+'/'+myTitle+'_output.xlsx')
        exp.to_excel(writer, index=False)
        writer.save()
        #exp.to_csv(out_dir+'/'+myTitle+'_output.dat',sep='\t',index=False)
        plt.show()
