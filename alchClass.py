# -*- coding: utf-8 -*-
"""
Created on Tue Jun 12 17:41:47 2018

@author: hickey.221
"""
# External packages
import os
import pandas as pd
import numpy as np
from warnings import warn
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.offsetbox import AnchoredText

import pickle
import datetime
# Internal scripts
import deconv

#plt.ioff()
#%%
class Alch():
    """
    An Alchromy analysis object. Linked to a single data file. Contains objects
    for each result produced.
    """
    def __init__(self,dataPath,refPath,name=None):
        # Initialize parameters
        self.dataPath = dataPath
        self.exp = None
        #self.outputPath = outputPath
        self.refPath = refPath
        self.result_list = []
        # Initialize methods
        self.identify(name)
        #self.exp, self.dataCols = self.read_file()
        self.settings = {'Normalize':False,
                    'Cutoff':(450,700)}
        
    def identify(self,name):
        """
        Establish information about file name and location
        """
        self.dirName = os.path.dirname(self.dataPath)
        self.fullName = os.path.basename(self.dataPath)
        self.simpleName, self.ext = os.path.splitext(self.fullName)
        if name:
            self.nickName = name
            
    def generate_result(self,ignored=[]):
        """
        Given settings about a run, generate a result object
        """
        workingRef = self.ref.drop(ignored, axis=1)
        settings = {'Normalize':False,
                    'Cutoff':(450,700) }
        # Select which reference cols are being used
        #ref = self.ref.drop(ignored, axis=1)
        # Generate a new object instance from result()
        new_result = Result(self,workingRef)
        # Add to results_list
        self.result_list.append(new_result)
        
    def read_file(self,filePath):
        _, ext = os.path.splitext(filePath)
        allowedFiles = ['.dat','.txt','.csv','.xls','.xlsx']
            # Read in the file
        print("My extension is",ext)
        if ext in allowedFiles:
            if ext in ['.xls','.xlsx']:
                print("Reading as excel")
                df = pd.read_excel(filePath)
            else:
                print("Reading as csv")
                df = pd.read_csv(filePath,'\t')
            # Rename first column as 'nm' for wavelengths
            df.rename(columns={df.columns[0]:'nm'}, inplace=True)
            # Bug fix for duplicate 2nd column name in some Olis-produced files
            if df.columns[1] == '0.1':
                df.rename(columns={df.columns[1]:'0'}, inplace=True)
         
            dataCols = list(df.drop('nm',axis=1)) # List of col names besides nm
            
            return df, dataCols 
        else:
            print("Error: File must be of type:",allowedFiles)
            
    def load_exp(self):
        if self.exp:
            warn("Exp data already exists")
        try:
            self.exp, self.dataCols = self.read_file(self.dataPath)
            self.exp = self.clean_data(self.exp)
        except:
                print("Error in reading files, aborting!")
        
    def load_ref(self):
        print("Refpath is",self.refPath)
        self.ref, self.species = self.read_file(self.refPath)
        self.ref = self.clean_data(self.ref)
        #ref = ref.drop(ignored, axis=1)
            
    def save_pdf(self,fname, fig):
        doc = PdfPages(fname)
        fig.savefig(doc, format='pdf')
        doc.close()
        
    def plot_results(self):
        for r in self.result_list:
            fig = r.export()
            print("Exporting",r.ts)
            #fig.figure
            #fig.canvas.draw()
            fig.show()
            #ax_list = fig.axes
            #print(ax_list)
            self.save_pdf('output/'+str(r.ts)+'.pdf',fig)
            
    def list_results(self):
        print("Results list:")
        for r in self.result_list:
            print(r.ts)
    
    def clean_data(self,df):
        """
        Trims all data to be within the limits, and removes data points that
        don't match (odds)
        """
        df = df[df['nm'] >= self.settings['Cutoff'][0]]
        df = df[df['nm'] <= self.settings['Cutoff'][1]]
        df = df[df['nm'] % 2 == 0]
        return df
    
#%%    
class Result():
    """
    A result object containing fit data, run parameters, and statistics
    """
    def __init__(self,owner,ref):
        self.owner = owner # The Alch instance we belong to
        self.mode = 'S' # (S)imple, (R)eplicate, (K)inetic
        self.ts = datetime.datetime.now().timestamp() # Epoch timestamp
        self.ref = ref # Reference data frame
        self.refData = self.owner.ref.drop('nm',axis=1) # Remove nm column
        self.expData = self.owner.exp # Grab data from owner
        self.run_deconv()
        self.do_stats()
        
    def run_deconv(self):
        """
        Run the deconvolution algorithm given a certain set of data and 
        reference spectra. Called automaticaly on object creation.
        """
        if self.mode=='S':
            # In simple case, rename single data column to 'data'
            self.expData.rename(columns={self.expData.columns[1]: 'data'}, inplace=True)
        if self.mode=='R':
            # In replicate case, make an average of all data
            self.expData = self.owner.exp[self.owner.dataCols].mean(axis=1)

        # Make a call to deconvolution algo, store the results
        self.coeffs, self.perr = deconv.doFitting(self.refData,self.expData['data'])
        
        # Get fit data column now that deconvolution is complete
        self.fit = deconv.func(self.refData.T, *self.coeffs)
        
    def do_stats(self):
        """
        Get some summary data about the results.
        """
        ss_r = np.sum((self.expData['data'] - self.fit)**2)
        ss_t = np.sum((self.expData['data'] - np.mean(self.expData['data']))**2)
        self.r2 = 1-(ss_r/ss_t)
    
    def export(self):
        """
        Method for saving spreadsheet and plot data from an individual .alch
        result
        """
        # Set up figure
        fig, ax = plt.subplots(1,1)
        ax.set_title(self.ts)
        ax.set_xlabel('Wavelength (nm)')
        ax.set_ylabel('Absorbance')

        # Plot data
        if self.mode =='R':
            _min= self.expData.min(axis=1)
            _max = self.expData.max(axis=1)
            ax.fill_between(self.expData['nm'], _min, _max)
        ax.plot(self.expData['nm'], self.expData['data'], 'b.-', label='data')
        ax.plot(self.expData['nm'], self.fit, 'r-', label='fit')
    
        # Print fit data and coefficients
        tbox = r"$R^2$ fit: {:.5f}".format(self.r2)
        anchored_text = AnchoredText(tbox, loc=5,prop=dict(color='black', size=9))
        anchored_text.patch.set(boxstyle="round,pad=0.,rounding_size=0.2",alpha=0.2)
        ax.add_artist(anchored_text)
        ax.legend(loc=1)
        plt.close(fig)
        #print(type(fig))
        #plt.show()
        return fig

if __name__=='__main__':
    from alchClass import Alch # Prevent object from belonging to __main__
    fname = 'output/A.alch'
    A = Alch(dataPath='data/test.xls',refPath='refspec.dat')
    
    A.load_exp()
    
    A.load_ref()
    
    A.generate_result()
    A.generate_result()
    
    A.plot_results()
    with open(fname, 'wb') as pickle_file:
        pickle.dump(A, pickle_file)
    
    with open(fname, 'rb') as pickle_file:
        B = pickle.load(pickle_file)
    