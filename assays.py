# -*- coding: utf-8 -*-
"""
Assays for spectrophotometric quantification of hemoglobin species based on
various extinction coefficients

Expects waves to be in Pandas dataframe format with an index column of 
wavelengths
eg.

Created on Tue Apr 24 10:52:17 2018

@author: hickey.221
"""
import pandas as pd
import numpy as np

# Read spectra to analyze
#df = pd.read_csv('examples\\test_met.dat','\t')
df = pd.read_csv('examples\\test.dat','\t')
#nm = df["nm"]
#ydata = df["A"]

xrange = np.arange(300,700,2) # wavelength axis

def Winterbourn(df, D=1):
    spec = df.set_index('nm') # Use int values of wavelength as index
    try:
        A577 = spec.loc[577][0]
    except:
        A577 = (spec.loc[576][0]+spec.loc[578][0])/2
    A630 = spec.loc[630][0]
    oxyHb = (66*A577 - 80*A630) * D
    metHb = (-3*A577 + 279*A630) * D
    totalHb = oxyHb+metHb
    return {'oxyHb':oxyHb,
            'metHb':metHb,
            'totalHb':totalHb}

def Alayash(df, D=1, highMet=False):
    spec = df.set_index('nm') # Use int values of wavelength as index
    try:
        A541 = spec.loc[541][0]
    except:
        A541 = (spec.loc[540][0]+spec.loc[542][0])/2
    A560 = spec.loc[560][0]
    A576 = spec.loc[576][0]
    A630 = spec.loc[630][0]
    if highMet:
        oxyHb = (-350.52*A541 + 388.95*A576 + 150.02*A630) * D
        metHb = (-185.77*A541 + 171.88*A576 + 387.58*A630) * D
        ferrylHb = (702.23*A541 - 657.43*A576 - 455.64*A630) * D
        totalHb = oxyHb+metHb+ferrylHb
    else:
        oxyHb = (-75.78*A560 + 103.16*A576 - 38.39*A630) * D
        metHb = (-26.09*A560 + 12.48*A576 - 280.7*A630) * D
        deoxyHb = (132.6*A560 - 74.1*A576 - 68.33*A630) * D
        totalHb = oxyHb+metHb+deoxyHb
    return {'oxyHb':oxyHb,
            'metHb':metHb,
            'deoxyHb':deoxyHb,
            'totalHb':totalHb}   

def Isosbestic(df, D=1):
    spec = df.set_index('nm')
    try:
        A523 = spec.loc[523][0]
    except:
        A523 = (spec.loc[522][0]+spec.loc[524][0])/2    
    totalHb = (A523 * D) / 7.12
    return {'totalHb':totalHb}

print("Winterbourn:",Winterbourn(df))
print("Alayash:",Alayash(df))
print("Isosbestic:",Isosbestic(df))