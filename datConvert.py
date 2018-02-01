# -*- coding: utf-8 -*-
"""
Utility for conversion of UV-Vis excel files to tab-delimited .dat files

Created on Thu Feb  1 12:04:32 2018

@author: hickey.221
"""
import pandas as pd

def datConvert(thisFile):
    df = pd.read_excel(thisFile,header=1) # Read in Excel file
    df.columns = ['nm','A'] # Rename headers
    df.to_csv('datOutput.dat',sep='\t',index=False) #save as .dat file 
