#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Spectral deconvolution of hemoglobin solutions

@author: Richard Hickey
"""
# Import packages:
import numpy as np
# Import local files:
import packageResults
import deconv
import readFiles
import kineticAnalysis
import os

def multiColDeconv(refPath='refspec.dat',
                   filePath='',
                   ignored=[],
                   flags={'Image':True,  # Output flags
                          'Text':True,
                          'Excel':True,
                          'Mode':'Replicate',
                          'Note':'',
                          'Normalize':False,
                          'Verbose':False,
                          'Cutoff':(450,700)}):
    """
    Main backend for deconvolution. Considers 3 cases: Simple (one data column),
    replicate (multiple columns will be averaged), and kinetic (multiple columns
    will be treated as changes over time).
    """
    # Dict of eventual results (figure, Excel, text)
    results={}
    
    # Container for string passed back to GUI status box
    statusReport = {'Code': -1, 'Message': 'Initialized but not finished'}
    
    # Make temporary folder
    if not os.path.exists('temp'):
        os.makedirs('temp') 

    # Basic error handling:
    if len(filePath)==0:
        return {'Code': 1, 'Message': 'No file specified'}
    
    # Input reference file
    ref, _ = readFiles.readFile(refPath)
    ref = readFiles.cleanData(ref,flags['Cutoff'])
    ref = ref.drop(ignored, axis=1)
    species = list(ref.drop('nm',axis=1)) # each non 'nm' header is a species

    # Input experimental file
    exp, fileDict = readFiles.readFile(filePath)
    exp = readFiles.cleanData(exp,flags['Cutoff'])
    timePoints = list(exp.drop('nm',axis=1))
    fileDict['Reference'] = refPath

    # Check number of data cols
    nCols = len(list(exp.drop('nm',axis=1)))

    if flags['Verbose']:
        print("Found species",species)
        print("Found",nCols,"columns of data")
        print("Have data column headers",timePoints)
        
    if nCols < 1: # If none, we have a problem
        return {'Code': 1, 'Message': "Couldn't find any data columns."}
    elif nCols == 1:
        #%%%%%% CASE 1: SIMPLE DECONVOLUTION %%%%%%
        # If there's only 1 data column, name it 'data'
        exp.rename(columns={exp.columns[1]: 'data'}, inplace=True)
        if flags['Normalize']:
            print("Normalizing data")
            exp['data'] = exp['data']-np.min(exp['data'])
        # Call curve fitting function
        coeffs, perr = deconv.doFitting(ref.drop('nm',axis=1),exp['data'])
        # Create a line of best fit using our results
        exp['fit'] = deconv.func(ref.drop('nm',axis=1).T, *coeffs)
        if flags['Verbose']:
            print("Finished with coefficients",coeffs)
        results['Image'] = packageResults.genImage(exp,fileDict,flags)
        if flags['Text']:
            packageResults.printResultsText(species, coeffs, perr, fileDict, flags)
        if flags['Excel']:
            packageResults.printResultsExcel(exp,fileDict,flags)
    elif flags['Mode']=='Kinetic':
        #%%%%%% CASE 2: MULTIPLE COLUMNS, KINETIC DATA %%%%%% # Do kinetic function
        kdf, results = kineticAnalysis.kineticAnalysis(fileDict,timePoints,species,exp,ref,flags)
        if flags['Excel']:
            packageResults.printResultsExcel(kdf,fileDict, flags,idx=True)
    elif flags['Mode']=='Replicate':
        #%%%%%% CASE 3: MULTIPLE COLUMNS, REPLICATE DATA %%%%%%
        if flags['Verbose']:
            print("Running average of replicates deconv")
        # Average all non-wavelength spectra into one
        exp['data'] = exp[timePoints].mean(axis=1)
        # Then perform deconvolution
        coeffs, perr = deconv.doFitting(ref.drop('nm',axis=1), exp['data'])
        # Create a line of best fit using our results
        exp['fit'] = deconv.func(ref.drop('nm',axis=1).T, *coeffs)
        if flags['Verbose']:
            print("Finished with coefficients",coeffs)
        results['Image'] = packageResults.genImage(exp,fileDict,flags)
        if flags['Text']:
            packageResults.printResultsText(species, coeffs, perr, fileDict, flags)
        if flags['Excel']:
            packageResults.printResultsExcel(exp,fileDict,flags)
    else:
        return {'Code': 1, 'Message': "Couldn't determine run mode."}
    #%% Send out to generate results file
    packageResults.Pack(fileDict,results,flags)
    
    statusReport = {'Code': 0, 'Message': 'Finished without incident.'} # No problems

    return statusReport

