# -*- coding: utf-8 -*-
"""
Created on Mon Apr 16 14:57:45 2018

@author: hickey.221
"""
from scipy.optimize import curve_fit
import numpy as np


def func(x, *params):
    """
    The curve fit function:
    Vector of coefficients multiplied by vector of data points
    """
    return np.stack(params).dot(x)


def doFitting(references, experimental_data):
    k_init = np.ones_like(list(references))  # All initial guesses = 1
    myBounds = (0, np.inf)  # Coefficients between 0 and +infinity
    coeffs, pcov = curve_fit(func, references.T, experimental_data, p0=k_init, bounds=myBounds)
    # Extract error and coefficients from results
    perr = np.sqrt(np.diag(pcov))
    return coeffs, perr
