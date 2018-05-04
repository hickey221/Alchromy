"""
plotband.py 
Hill Research Group
Theoretical Chemistry, University of Sheffield


PlotBand A Python script for simulating UV/Vis spectra.

There are a number of tools for simulating UV/Vis spectra (such as GaussSum), 
but sometimes you might want to use a quantum chemistry code that isn't 
supported (or something else exotic). PlotBand is a simple Python3 script that 
uses matplotlib (and numpy) to generate a UV/Vis spectrum using only excitation 
energies and oscillator strengths. Using matplotlib means the script is easily 
hackable for producing publication-ready graphics. If you find the script useful, 
or find any problems, then please let us know.
"""
import sys
import numpy as np
import matplotlib.pyplot as plt

# Adjust the following three variables to change which area of the spectrum is plotted and number of points used
# in plotting the curves
start=200
finish=700
points=500

# A sqrt(2) * standard deviation of 0.4 eV is 3099.6 nm. 0.1 eV is 12398.4 nm. 0.2 eV is 6199.2 nm.
#stdev = 12398.4
stdev = [6e3,1e4,1.8e4,1.8e4,1.1e4]
# For Lorentzians, gamma is half bandwidth at half peak height (nm)
gamma = 12.5
# Excitation energies in nm
bands = [415, 505, 542, 576, 630]
# Oscillator strengths (dimensionless)
f = [.129,.00045, .00141,.00149,.00055]

# Basic check that we have the same number of bands and oscillator strengths
if len(bands) != len(f):
    print('Number of bands does not match the number of oscillator strengths.')
    sys.exit()

# Information on producing spectral curves (Gaussian and Lorentzian) is adapted from:
# P. J. Stephens, N. Harada, Chirality 22, 229 (2010).
# Gaussian curves are often a better fit for UV/Vis.
def gaussBand(x, band, strength, stdev):
    "Produces a Gaussian curve"
    bandshape = 1.3062974e8 * (strength / (1e7/stdev))  * np.exp(-(((1.0/x)-(1.0/band))/(1.0/stdev))**2)
    return bandshape

def lorentzBand(x, band, strength, stdev, gamma):
    "Produces a Lorentzian curve"
    bandshape = 1.3062974e8 * (strength / (1e7/stdev)) * ((gamma**2)/((x - band)**2 + gamma**2))
    return bandshape

x = np.linspace(start,finish,points)

composite = 0
for count,peak in enumerate(bands):
    thispeak = gaussBand(x, peak, f[count], stdev[count])
#    thispeak = lorentzBand(x, peak, f[count], stdev, gamma)
    composite += thispeak

fig, ax = plt.subplots()
ax.plot(x,composite)
plt.xlabel('$\lambda$ / nm')
plt.ylabel('$\epsilon$ / L mol$^{-1}$ cm$^{-1}$')

plt.show()