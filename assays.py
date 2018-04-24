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
#import pandas as pd

def Winterbourn(df, D=1):
    spec = df.set_index('nm') # Use int values of wavelength as index
    try:
        A577 = spec.loc[577][0]
    except:
        A577 = (spec.loc[576][0]+spec.loc[578][0])/2
    A630 = spec.loc[630][0]
    oxyHb = (66*A577 - 80*A630) / D
    metHb = (-3*A577 + 279*A630) / D
    return {'oxyHb':oxyHb,
            'metHb':metHb}

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
        oxyHb = (-350.52*A541 + 388.95*A576 + 150.02*A630) / D
        metHb = (-185.77*A541 + 171.88*A576 + 387.58*A630) / D
        ferrylHb = (702.23*A541 - 657.43*A576 - 455.64*A630) / D
    else:
        oxyHb = (-75.78*A560 + 103.16*A576 - 38.39*A630) / D
        metHb = (-26.09*A560 + 12.48*A576 - 280.7*A630) / D
        deoxyHb = (132.6*A560 - 74.1*A576 - 68.33*A630) / D
    return {'oxyHb':oxyHb,
            'metHb':metHb}   
