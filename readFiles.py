# -*- coding: utf-8 -*-
"""
Created on Mon Apr 16 15:04:05 2018

@author: hickey.221
"""
import pandas as pd
import os
import shutil

def readFile(filePath):
    """
    Reads in a csv or spreadsheet file. Returns a dataframe with data, and
    a dict with file information
    """
    # Analyze the file path and save important parts
    fileDict = {'fullPath': filePath} # Initialize dict with given path
    fileDict['name.ext'] = os.path.basename(fileDict['fullPath']) # yields 'filename.ext'
    fileDict['name'],fileDict['ext'] = os.path.splitext(fileDict['name.ext']) # yields 'filename', '.ext'
    fileDict['dir'] = os.path.dirname(filePath) # yields 'data/somebatch/'
    fileDict['outDir'] = fileDict['dir'] + '/' + 'output' # yields data/somebatch/output
    fileDict['tempDir'] = 'temp' # Alchromy/temp/
    
    # Make sure the desired paths are writable
    if not os.path.exists(fileDict['outDir']):
        os.makedirs(fileDict['outDir'])
    if os.path.exists(fileDict['tempDir']):
        shutil.rmtree(fileDict['tempDir'])
    else:
        os.makedirs(fileDict['tempDir'])

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