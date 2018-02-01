# -*- coding: utf-8 -*-
"""
Utility for conversion of UV-Vis excel files to tab-delimited .dat files

Created on Thu Feb  1 12:04:32 2018

@author: hickey.221
"""

"""
TO DO: Allow for multi column import
TO DO: Allow for either replicate or kinetic data output instead of file output
"""
import pandas as pd
import os

def datConvert(thisFile, saveToFile = False, Kinetic = False):
    myPath = os.path.basename(thisFile) # yields 'filename.ext'
    myTitle, myExt = os.path.splitext(myPath) # yields 'filename', '.ext'
    header = 0 if not Kinetic else 'None' 
    df = pd.read_excel(thisFile,header=header) # Read in Excel file 
    df.columns = ['nm'] + ['A']*(df.shape[1]-1) # Rename headers
    if not Kinetic and df.shape[1]>2: df = (df[['nm']] 
        + df.drop(['nm'], axis=1).mean())
    if saveToFile:
        df.to_csv(myTitle+'.dat',sep='\t',index=False) #save as .dat file 
    else:
        return df, myTitle
    #df.to_csv(myTitle+'.dat',sep='\t',index=False) if saveToFile else return df
