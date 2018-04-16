# -*- coding: utf-8 -*-
"""
Created on Mon Apr 16 14:33:09 2018

@author: hickey.221
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.offsetbox import AnchoredText
import os
import pandas as pd
import shutil
import zipfile


def genFileName(fileDict,fileExt,flags):
    """
    Generate an output file path based on run parameters
    """

    fileOut = fileDict['outDir']+'/'+fileDict['name']
    if flags['Mode']=='Kinetic':
        fileOut += '_kinetic'
    if flags['Note']:
        fileOut += '_'+flags['Note']
    fileOut += '.'+fileExt
    return fileOut

def genImage(exp, fileDict, flags):
    """
    Returns a plot of fitted data
    """
    # Set up figure
    fig, ax = plt.subplots(1,1)
    ax.set_title(fileDict['name'])
    ax.set_xlabel('Wavelength (nm)')
    ax.set_ylabel('Absorbance')

    ss_r = np.sum((exp['data'] - exp['fit'])**2)
    ss_t = np.sum((exp['data'] - np.mean(exp['data']))**2)
    r2 = 1-(ss_r/ss_t)

    # Plot data
    if flags['Mode']=='Replicate':
        exp['min'] = exp.drop(['nm','fit'],axis=1).min(axis=1)
        exp['max'] = exp.drop(['nm','fit','min'],axis=1).max(axis=1)
        # fill_between(x, y1, y2)
        ax.fill_between(exp['nm'], exp['min'], exp['max'])
    ax.plot(exp['nm'], exp['data'], 'b.-', label='data')
    ax.plot(exp['nm'], exp['fit'], 'r-', label='fit')

    # Print fit data and coefficients
    tbox = r"$R^2$ fit: {:.5f}".format(r2)
    anchored_text = AnchoredText(tbox, loc=5,prop=dict(color='black', size=9))
    anchored_text.patch.set(boxstyle="round,pad=0.,rounding_size=0.2",alpha=0.2)
    ax.add_artist(anchored_text)
    ax.legend(loc=1)
    
    plt.savefig(genFileName(fileDict,'png',flags), bbox_inches='tight',facecolor='white', dpi=300)
    if flags['Verbose']:
        print("Finished fitting, plotting image")
        plt.show()
    return fig

def printResultsExcel(df, fileDict,flags, idx=False):
    if not os.path.exists(fileDict['outDir']):
            os.makedirs(fileDict['outDir'])
    writer = pd.ExcelWriter(genFileName(fileDict,'xlsx',flags))
    df.to_excel(writer, index=idx)
    writer.save()
#%%
def printResultsText(species, coeffs, perr, fileDict, flags):
    if not os.path.exists(fileDict['outDir']):
            os.makedirs(fileDict['outDir'])
    tbody = ["Curve fitting report",
             "Using scipy.optimize.curve_fit (non-linear least squares regression)",
             "Version 1.2.1 \t Richard Hickey \t Ohio State University",
             ""]
    tbody += ["Sample: \t"+fileDict['name'],
              "Filename: \t"+fileDict['name.ext'],
              "Reference: \t"+fileDict['Reference'],
              "Wavelengths: \t"+str(flags['Cutoff'][0])+"-"+str(flags['Cutoff'][1]),
              "File note: \t"+flags['Note']]
    if flags['Normalize']:
        tbody += ["Normalized to lowest value = 0"]
    tbody += [""]
    tbody += ["Species\tCoefficients (Percent)\tStandard error*"]
    for sp,coef,sd in zip(species,coeffs,perr):
        cpercent = 100*coef/sum(coeffs)
        if coef< 0.000001:
            sdpercent = 0
        else:
            sdpercent = 100 * sd / coef
        #tbox = tbox + "\n" + "{:.2f}% ".format(cpercent) + str(sp)
        tbody += [sp+"\t{:.6f} ({:.2f}%)".format(coef,cpercent)+"\t{:.6f} ({:.2f}%)".format(sd,sdpercent)]

    #tbody += ["",
    #          "Fit data:",
    #          "Sum of squares (residual) = "+str(ss_r),
    #          "Sum of squares (total) = "+str(ss_t),
    #          "R-squared = "+str(r2)]
    tbody += ["\nStandard error being defined as the diagonal of the square root of the coefficient covariance matrix."]
    if flags['Verbose']:
        # Print output report to console
        print('\n'.join(tbody))
    # Print output report to .txt file
    #f = open(out_dir+'/'+myTitle+'_output.txt','w')
    f = open(genFileName(fileDict,'txt',flags),'w')
    f.write('\n'.join(tbody))
    f.close()

def Pack(fileDict,results,flags):
    """
    Zip results dict into a single archive (.alch)
    """
    # Check which files we want to keep, and copy to results folder
    if flags['Image']:
        shutil.copyfile(src, dst)
    if flags['Text']:
        shutil.copyfile(src, dst)
    if flags['Excel']:
        shutil.copyfile(src, dst)
        
    # Generate .alch file
    #z = zipfile.ZipFile('the_file.zip', 'w')
       
    with zipfile.ZipFile('the_file.zip', 'w') as z:
        z.write('first file.txt')
    
    with zipfile.ZipFile(genFileName(fileDict,'zip',flags), 'a'):
        #for  each file in temp directory
        z.write('additional files.txt')
    