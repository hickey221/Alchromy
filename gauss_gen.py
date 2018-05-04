# -*- coding: utf-8 -*-
"""
Created on Fri May  4 10:14:29 2018

@author: hickey.221
"""

from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Read spectra to analyze
df = pd.read_csv('test.dat','\t')
nm = df["nm"]
ydata = df["A"]

xrange = np.arange(300,700,2) # wavelength axis

def single_gauss(x, center, height, sigma, offset=0):
    return height*np.exp(-(x - center)**2/(2*sigma**2)) + offset
    
# Define initial guesses [height, center, sigma, (offset)]
_N =  [345,1.5,10]
_B =  [415,3,20]
_IV = [505,0.3,15]
_Qv = [540,0.5,10]
_Q0 = [576,0.5,10]
_I =  [630,0.05,20]

# Set bounds for each wave
_Nb = [330,360]
_Bb = [390,430]
_IVb = [490,510]
_Qvb = [530,565]
_Q0b = [565,590]
_Ib = [610,650]
bnd = ([_Nb[0],0,0,
       _Bb[0],0,0,
       _IVb[0],0,0,
       _Qvb[0],0,0,
       _Q0b[0],0,0,
       _Ib[0],0,0],
        [_Nb[1],3,50,
       _Bb[1],40,100,
       _IVb[1],3,50,
       _Qvb[1],3,50,
       _Q0b[1],3,50,
       _Ib[1],3,50])

def Hb_gaussian(x, *args):
    """
    x is an array of wavelengths to plot
    args are a list of curves to generate (each itself a list of gauss params)
    """
    return sum((single_gauss(x,*arg) for arg in args))

def Hb_6band(x, *args):
    """ 
    Takes x data along with exactly 6x3=18 args for initial conditions
    """
    # Split into sets of 3 args
    band1 = args[0:3]
    band2 = args[3:6]
    band3 = args[6:9]
    band4 = args[9:12]
    band5 = args[12:15]
    band6 = args[15:18]
    return sum(((single_gauss(x,*band1)),(single_gauss(x,*band2)),(single_gauss(x,*band3)), (single_gauss(x,*band4)), (single_gauss(x,*band5)), (single_gauss(x,*band6)) ))

#Call Hb_gauss with as many bands as we want


bands = [_N,_B,_IV,_Qv,_Q0,_I]
p0 = np.array([list(t) for t in bands]).flatten()
#A = Hb_gaussian(x,_B,_Qv,_Q0,_I)
#curve_fit(f, xdata, ydata, p0=None, sigma=None, absolute_sigma=False, check_finite=True, bounds=(-inf, inf), method=None, jac=None, **kwargs)

# Arbitrary number of bands (doesn't work)
#popt, pcov = curve_fit(Hb_gaussian,nm,ydata,bands)

# 1 band at a time (works)
#popt, pcov = curve_fit(single_gauss,nm,ydata,_B)
#fit = single_gauss(nm,*popt)

# Exactly 4 bands with flattened initial conditions
popt, pcov = curve_fit(Hb_6band,nm,ydata,p0,bounds=bnd)
fit = Hb_6band(nm,*popt)

print(popt[0],popt[3],popt[6],popt[9],popt[12],popt[15])
#plt.plot(xrange,Hb_6band(xrange,*popt))
plt.plot(nm,ydata,nm,fit)

plt.savefig('tempout.png',dpi=150)

