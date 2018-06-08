# -*- coding: utf-8 -*-
"""
Created on Mon Apr 16 15:19:44 2018

@author: hickey.221
"""
import pandas as pd
import numpy as np
import deconv
import matplotlib.pyplot as plt
import packageResults

def kineticAnalysis(fileDict,timePoints,species,exp,ref,flags):
    results = {}
    if flags['Verbose']:
        print("Running kinetic analysis")
    kdf = pd.DataFrame(timePoints, columns=['Time']) # kinetic data frame
    kdf = pd.concat([kdf,pd.DataFrame(columns=species)])
    kdf = kdf.set_index('Time') # do we need this?
    # make error columns
    species_err = [sp + '_err' for sp in species]
    species_perc = [sp + ' (%)' for sp in species] # % of total
    kdf = pd.concat([kdf,pd.DataFrame(columns=species_err)])
    for timePoint in timePoints:
        #print(timePoint)
        # Make call to curve_fit
        coeffs, perr = deconv.doFitting(ref.drop('nm',axis=1), exp[timePoint])
        # Extract error and coefficients from results
        for sp,sp_e,coeff,sd,sp_perc in zip(species,species_err,coeffs,perr, species_perc):
            kdf.loc[timePoint,sp] = coeff # Actual coefficient
            kdf.loc[timePoint,sp_e] = sd # Standard error
            kdf.loc[timePoint,sp_perc] = coeff/sum(coeffs) # Percent of total composition
    #kdf.sort_index(inplace=True) # Sort by time index
    
    # Set up figure
    fig, ax = plt.subplots(1,1)    
    # Area plot between lines
    ax = kdf.drop(species_err+species,axis=1).plot.area(lw=0)
    ax.set_xlabel('Time')
    timeLabels = [round(float(t),2) for t in timePoints]
    if flags['Verbose']:
        print("Timepoints",timeLabels) 
        
    # Find what x labels were automatically chosen
    label_texts = [label.get_text() for label in ax.xaxis.get_ticklabels()]
    # Convert to float, round, then back to string (dumb.)
    label_nums = [str(round(float(t),2)) for t in label_texts[:-1]]
    # Set those as new labels
    ax.set_xticklabels(label_nums)

    ax.set_ylabel('Fractional composition')
    results['Image'] = fig
    plt.savefig(packageResults.genFileName(fileDict,'png',flags), bbox_inches='tight',facecolor='white', dpi=300)
    
    #TODO: More specific text output for kinetic data
    c_init = kdf[species].iloc[0]
    c_init_perc = 100 * c_init / np.sum(c_init)
    c_final = kdf[species].iloc[-1]
    c_final_perc = 100 * c_final / np.sum(c_final)
    c_init_final_perc = pd.concat([c_init_perc,c_final_perc],axis=1)

    tbody = ["Kinetic data report",
             "Using scipy.optimize.curve_fit (non-linear least squares regression)",
             "Version 1.2.1 \t Richard Hickey \t Ohio State University",
             ""]
    tbody += ["Filename: \t"+fileDict['name.ext'],
              "Reference: \t"+fileDict['Reference'],
              "Wavelengths: \t"+str(flags['Cutoff'][0])+"-"+str(flags['Cutoff'][1]),
              "File note: \t"+flags['Note']]
    if flags['Normalize']:
        tbody += ["Normalized to lowest value = 0"]
    tbody += [""]
    tbody += ["Start and ending composition (percent)"]
    tbody += [c_init_final_perc.to_string(header=['initial','final'])]
    tbody += ["Component maximum and mimimums:"]
    
    results['Text'] = tbody

    return kdf, results