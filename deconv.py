# -*- coding: utf-8 -*-
"""
Created on Mon Apr 16 14:57:45 2018

@author: hickey.221
"""
from scipy.optimize import curve_fit
import numpy as np

# Define curve_fit function
def func(X, *params):
    return np.stack(params).dot(X)

def doFitting(refCols,expCol):
    k_init = np.ones_like(list(refCols)) # All initial guesses = 1
    myBounds = (0,np.inf) # Coefficients between 0 and +infinity
    coeffs, pcov = curve_fit(func, refCols.T, expCol, p0=k_init, bounds=myBounds)
    # Extract error and coefficients from results
    perr = np.sqrt(np.diag(pcov))
    return coeffs, perr