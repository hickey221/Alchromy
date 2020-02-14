# -*- coding: utf-8 -*-
"""
Created on Tue Jun 12 17:41:47 2018

@author: hickey.221

AlchClass.py

Describes the Alch object class. An Alch instance contains a set of data,
references, and results objects from an Alchromy analysis.

TODO: Change result_list to only be a single result per alch

"""
# External packages
import os
import pandas as pd
import numpy as np
from warnings import warn
# import matplotlib.pyplot as plt
# from matplotlib.backends.backend_pdf import PdfPages
# from matplotlib.offsetbox import AnchoredText

import pickle
import datetime
# Internal scripts
from lib import alch_deconv


class Alch:
    """
    An Alchromy analysis object. Linked to a single data file. Contains objects
    for each result produced.
    """
    def __init__(self):
        # Initialize placeholders for pandas data frames
        self.data = None
        self.ref = None
        self.common_idx = None
        self.mode = None  # 'S'imple, 'R'eplicate, 'K'inetic
        self.result = None
        self.name = "new"
        # self.outputPath = outputPath
        # self.refPath = refPath
        self.normalize = False
        self.endpoints = (-np.inf, np.inf)
        self.result_list = []
        self.ready = self.readyCheck()
        self.r2 = None

    def readyCheck(self):
        # Weird 'is not None' calls because of df truth ambiguity
        if self.data is not None and self.ref is not None:
            try:
                self.clean_data()
            except ValueError as e:
                warn("Couldn't clean data"+str(e))
                return False
        else:
            # warn("Do not have both data and reference loaded")
            return False
        # Passed all tests
        return True

    def clean_data(self):
        """
        Trims all data to be within the limits, and removes data points that
        don't match (odds)
        """
        if self.ref is None or self.data is None:
            warn("Don't have all df loaded to clean")
            return
        # Find the index from the ref df
        ref_idx = self.ref.index.values
        # Find the index from the data df
        data_idx = self.data.index.values
        # Find common points and save this as the new index
        self.common_idx = np.intersect1d(ref_idx, data_idx)
        # Cut anything outside our specified cutoffs
        self.common_idx = np.array([x for x in self.common_idx if self.endpoints[0] < x < self.endpoints[1]])
        # Throw error if no overlap
        if len(self.common_idx) == 0:
            warn("No overlap in indices!")
            return
        elif len(self.common_idx) < 20:
            warn("Fewer than 20 index points remaining")
        # Slim down each df by the new index
        self.data = self.data.loc[self.common_idx]
        self.ref = self.ref.loc[self.common_idx]
        # Drop indices from data now that it's in common_idx
        self.data = self.data.drop('idx', axis=1)
        self.ref = self.ref.drop('idx', axis=1)
        print("Cleaned successfully with", len(self.common_idx), "fitting points.")

    def generate_result(self):
        """
        Given settings about a run, generate a result object
        """
        if not self.ready:
            warn("Not ready to run")
            return

        # Get out of pandas format
        expData = self.data.values

        if self.mode == 'S':
            pass
        elif self.mode == 'R':
            # In replicate case, make an average of all data
            expData = expData.mean(axis=1)
        else:
            print("Don't recognize mode", self.mode)
            return

        # Make a call to deconvolution algo, store the results
        coeffs, perr = alch_deconv.doFitting(self.ref, expData)

        # Get fit data column now that deconvolution is complete
        self.result = pd.DataFrame(self.common_idx)
        self.result.columns = ['idx']
        self.result['data'] = expData
        # print(self.result['data'])
        self.result['fit'] = alch_deconv.func(self.ref.T, *coeffs)
        # print(refCols)
        # print(coeffs/sum(coeffs))

        ss_r = np.sum((self.result['data'] - self.result['fit']) ** 2)
        # print(f"ss_r={ss_r} ({type(ss_r)})")
        # print(type(self.result))
        ss_t = np.sum((self.result['data'] - np.mean(self.result['data'])) ** 2)
        # print(f"ss_r={ss_t} ({type(ss_t)})")
        # print(ss_t)
        self.r2 = 1 - (ss_r / ss_t)
        print(f"R^2: {self.r2}")

    def Reset(self):
        """
        Erases all exp and ref data
        """
        self.data = None
        self.ref = None

    def save_pdf(self, fname, fig):
        # doc = PdfPages(fname)
        # fig.savefig(doc, format='pdf')
        # doc.close()
        pass
