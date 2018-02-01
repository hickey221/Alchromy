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

def datConvert(thisFile):
    myPath = os.path.basename(thisFile) # yields 'filename.ext'
    myTitle, myExt = os.path.splitext(myPath) # yields 'filename', '.ext'
    df = pd.read_excel(thisFile,header=1) # Read in Excel file
    df.columns = ['nm','A'] # Rename headers
    df.to_csv(myTitle+'.dat',sep='\t',index=False) #save as .dat file 
