# -*- coding: utf-8 -*-
"""
Created on Fri Jun 15 09:34:48 2018

@author: hickey.221
"""

#%%
if __name__=='__main__':
    from alchClass import Alch
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
    