# -*- coding: utf-8 -*-
"""
Created on Mon Apr 16 14:57:45 2018

@author: hickey.221
"""
from scipy.optimize import curve_fit
import numpy as np


def func(X, *params):
    """
    The curve fit function:
    Vector of coefficients multiplied by vector of data points
    """
    return np.stack(params).dot(X)


def doFitting(refCols, expCol):
    k_init = np.ones_like(list(refCols))  # All initial guesses = 1
    myBounds = (0, np.inf)  # Coefficients between 0 and +infinity
    coeffs, pcov = curve_fit(func, refCols.T, expCol, p0=k_init, bounds=myBounds)
    # Extract error and coefficients from results
    perr = np.sqrt(np.diag(pcov))
    return coeffs, perr
