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
    A560 = spec.loc[560][0]
    A630 = spec.loc[630][0]
    oxyHb = (-89*A560 + 119*A577 - 39*A630)*D/1000
    metHb = (-55*A560 + 28*A577 + 307*A630)*D/1000
    hemiHb = (233*A560 - 133*A577 - 114*A630)*D/1000
    totalHb = oxyHb+metHb+hemiHb
    return {'oxyHb':oxyHb,
            'metHb':metHb,
            'hemiHb':hemiHb,
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
        oxyHb = (-350.52*A541 + 388.95*A576 + 150.02*A630)*D/1000
        metHb = (-185.77*A541 + 171.88*A576 + 387.58*A630)*D/1000
        ferrylHb = (702.23*A541 - 657.43*A576 - 455.64*A630)*D/1000
        totalHb =( oxyHb+metHb+ferrylHb)
    else:
        oxyHb = (-75.78*A560 + 103.16*A576 - 38.39*A630)*D/1000
        metHb = (-26.09*A560 + 12.48*A576 + 280.7*A630)*D/1000
        deoxyHb = (132.6*A560 - 74.1*A576 - 68.33*A630)*D/1000
        totalHb = (oxyHb+metHb+deoxyHb)
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
result_wb = Winterbourn(df,D=20)
result_al = Alayash(df,D=20)
result_iso = Isosbestic(df,D=20)
print("Results of total hb calculation:")
print("Winterbourn:",result_wb['totalHb']*16.125)
print("Alayash:",result_al['totalHb']*16.125)
print("Isosbestic:",result_iso['totalHb']*16.125)