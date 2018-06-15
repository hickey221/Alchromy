# -*- coding: utf-8 -*-
"""
Created on Thu Jun 14 16:17:29 2018

@author: hickey.221
"""
import pickle
#import alchClass

def load_alch(fname):
    with open(fname, 'rb') as pickle_file:
        A = pickle.load(pickle_file)
    return A

A = load_alch('output/A.alch')

A.plot_results()
