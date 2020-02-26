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

def genFileName(fileDict,fileExt,flags):
    fileOut = fileDict['outDir']+'/'+fileDict['name']
    if flags['Kinetic']:
        fileOut += '_kinetic'
    if flags['Note']:
        fileOut += '_'+flags['Note']
    fileOut += '.'+fileExt
    return fileOut

def multiColDeconv(refPath='refspec.dat',
                   filePath='',
                   ignored=[],
                   flags={'Image':True,  # Output flags
                          'Text':True,
                          'Excel':True,
                          'Kinetic':False,
                          'Note':'',
                          'Normalize':False,
                          'Verbose':False,
                          'Cutoff':(450,700)}):
    """
    Handle multiple columns of experimental data by treating it as
    1) Replicates of the same data points
    2) Kinetic data over time
    """


    if flags['Verbose']:
        print("working on",filePath)
    if len(filePath)==0:
        return {'Code': 1, 'Message': 'No file found'}
    # Input reference file
    ref, _ = readFile(refPath)
    ref = cleanData(ref,flags['Cutoff'])
    ref = ref.drop(ignored, axis=1)
    species = list(ref.drop('nm',axis=1)) # each non 'nm' header is a species

    # Input experimental file
    exp, fileDict = readFile(filePath)
    exp = cleanData(exp,flags['Cutoff'])
    timePoints = list(exp.drop('nm',axis=1))
    fileDict['Reference'] = refPath
    
    # Check number of data cols
    nCols = len(list(exp.drop('nm',axis=1)))

    if flags['Verbose']:
        print("Found species",species)
        print("Found",nCols,"columns of data")
        print("Have data column headers",timePoints)

    #%% Nested function for kinetic analysis
    def kineticAnalysis(fileDict,flags):
        if flags['Verbose']:
            print("Running kinetic analysis")
        print(f"adding columns: {['Time']}")
        kdf = pd.DataFrame(timePoints, columns=['Time']) # kinetic data frame
        print(f"adding columns: {species}")
        kdf = pd.concat([kdf,pd.DataFrame(columns=species)], sort=False)
        kdf = kdf.set_index('Time') # do we need this?
        # make error columns
        species_err = [sp + '_err' for sp in species]
        species_perc = [sp + ' (%)' for sp in species] # % of total
        if flags['Verbose']:
            print(f"adding columns: {species_err}")
        kdf = pd.concat([kdf, pd.DataFrame(columns=species_err)], sort=False)
        for timePoint in timePoints:
            # Make call to curve_fit
            if flags['Verbose']:
                print(f"Fitting {exp[timePoint]}")
            if flags['Normalize']:
                print("Normalizing data")
                exp[timePoint] = exp[timePoint] - np.min(exp[timePoint])
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
        if flags['Image']:
            if not os.path.exists(fileDict['outDir']):
                os.makedirs(fileDict['outDir'])
            plt.savefig(genFileName(fileDict,'png',flags), 
                        bbox_inches='tight',facecolor='white', dpi=300)
        plt.show()
        if flags['Text']:
            #TODO: More specific text output for kinetic data
            c_init = kdf[species].iloc[0]
            c_init_perc = 100 * c_init / np.sum(c_init)
            c_final = kdf[species].iloc[-1]
            c_final_perc = 100 * c_final / np.sum(c_final)
            c_init_final_perc = pd.concat([c_init_perc,c_final_perc],axis=1)
            
            if not os.path.exists(fileDict['outDir']):
                os.makedirs(fileDict['outDir'])
            tbody = ["Kinetic data report",
                     "Using scipy.optimize.curve_fit (non-linear least squares regression)",
                     "Version 1.2.1 \t Richard Hickey \t Ohio State University",
                     ""]
            tbody += ["Filename: \t"+fileDict['name.ext'],
                      "Reference: \t"+fileDict['Reference'],
                      "Wavelengths: \t"+str(flags['Cutoff'][0])+"-"+str(flags['Cutoff'][1]),
                      "File note: \t"+flags['Note']]
            if flags['Normalize']:
                tbody += ["Normalized to lowest value = 0"]
            tbody += [""]
            tbody += ["Start and ending composition (percent)"]
            tbody += [c_init_final_perc.to_string(header=['initial','final'])]
            tbody += ["Component maximum and mimimums:"]
            
            if flags['Verbose']:
                # Print output report to console
                print('\n'.join(tbody))
            # Print output report to .txt file
            f = open(genFileName(fileDict,'txt',flags),'w')
            f.write('\n'.join(tbody))
            f.close()         
            
        return kdf

    if nCols < 1: # If none, we have a problem
        raise Exception("Error: Can't find any data")
    elif nCols == 1: 
        #%%%%%% CASE 1: SIMPLE DECONVOLUTION %%%%%%
        # If there's only 1 data column, name it 'data'
        exp.rename(columns={exp.columns[1]: 'data'}, inplace=True)
        if flags['Normalize']:
            print("Normalizing data")
            exp['data'] = exp['data']-np.min(exp['data'])
        # Call curve fitting function
        coeffs, perr = doFitting(ref.drop('nm',axis=1),exp['data'])
        if flags['Verbose']:
            print(f"coeffs {coeffs}")
        # Create a line of best fit using our results
        exp['fit'] = func(ref.drop('nm',axis=1).T, *coeffs)
        if flags['Verbose']:
            print("Finished with coefficients",coeffs)
        plotStandard(exp,fileDict,flags)
        if flags['Text']:
            printResultsText(species, coeffs, perr, fileDict, flags)
        if flags['Excel']:
            printResultsExcel(exp,fileDict,flags)
    else:
        #%%%%%% CASE 2: MULTIPLE COLUMNS, KINETIC DATA %%%%%%
        if flags['Kinetic']: # Do kinetic function
            kdf = kineticAnalysis(fileDict,flags)
            if flags['Excel']:
                printResultsExcel(kdf,fileDict, flags,idx=True)
            print("Done")

        else: 
            #%%%%%% CASE 3: MULTIPLE COLUMNS, REPLICATE DATA %%%%%%
            if flags['Verbose']:
                print("Running average of replicates deconv")
            # Average all non-wavelength spectra into one
            exp['data'] = exp[timePoints].mean(axis=1)
            # Then perform deconvolution
            coeffs, perr = doFitting(ref.drop('nm',axis=1), exp['data'])
            # Create a line of best fit using our results
            exp['fit'] = func(ref.drop('nm',axis=1).T, *coeffs)
            if flags['Verbose']:
                print("Finished with coefficients",coeffs)
            plotReplicates(exp,fileDict,flags)
            if flags['Text']:
                printResultsText(species, coeffs, perr, fileDict, flags)
            if flags['Excel']:
                printResultsExcel(exp,fileDict,flags)
    #%% End of cases cases
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

def plotStandard(exp, fileDict, flags):
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
        plt.savefig(genFileName(fileDict,'png',flags), 
                    bbox_inches='tight',facecolor='white', dpi=300)
    if flags['Verbose']:
        print("Finished fitting, plotting image")
        plt.show()
    if flags['Text']:
        pass

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
        plt.savefig(genFileName(fileDict,'png',flags), bbox_inches='tight',facecolor='white', dpi=300)
    if flags['Verbose']:
        print("Finished fitting, plotting image")
        plt.show()



def printResultsExcel(df, fileDict,flags, idx=False):
    if not os.path.exists(fileDict['outDir']):
            os.makedirs(fileDict['outDir'])
    writer = pd.ExcelWriter(genFileName(fileDict,'xlsx',flags))
    df.to_excel(writer, index=idx)
    writer.save()
#%%
def printResultsText(species, coeffs, perr, fileDict, flags):
    if not os.path.exists(fileDict['outDir']):
            os.makedirs(fileDict['outDir'])
    tbody = ["Curve fitting report",
             "Using scipy.optimize.curve_fit (non-linear least squares regression)",
             "Version 1.2.1 \t Richard Hickey \t Ohio State University",
             ""]
    tbody += ["Sample: \t"+fileDict['name'],
              "Filename: \t"+fileDict['name.ext'],
              "Reference: \t"+fileDict['Reference'],
              "Wavelengths: \t"+str(flags['Cutoff'][0])+"-"+str(flags['Cutoff'][1]),
              "File note: \t"+flags['Note']]
    if flags['Normalize']:
        tbody += ["Normalized to lowest value = 0"]
    tbody += [""]
    tbody += ["Species\tPercent\tCoefficients\tStandard error*"]
    for sp,coef,sd in zip(species,coeffs,perr):
        cpercent = 100*coef/sum(coeffs)
        if coef< 0.000001:
            sdpercent = 0
        else:
            sdpercent = 100 * sd / coef
        #tbox = tbox + "\n" + "{:.2f}% ".format(cpercent) + str(sp)
        tbody += [sp+"\t{:.2f}%".format(cpercent)+"\t{:.6f}".format(coef)+"\t{:.6f}".format(sd)]

    #tbody += ["",
    #          "Fit data:",
    #          "Sum of squares (residual) = "+str(ss_r),
    #          "Sum of squares (total) = "+str(ss_t),
    #          "R-squared = "+str(r2)]
    tbody += ["\nStandard error being defined as the diagonal of the square root of the coefficient covariance matrix."]
    if flags['Verbose']:
        # Print output report to console
        print('\n'.join(tbody))
    # Print output report to .txt file
    #f = open(out_dir+'/'+myTitle+'_output.txt','w')
    f = open(genFileName(fileDict,'txt',flags),'w')
    f.write('\n'.join(tbody))
    f.close()
