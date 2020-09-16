# -*- coding: utf-8 -*-
"""
Created on Tue Jun 12 17:41:47 2018

@author: hickey.221

AlchClass.py

Describes the Alch object class. An Alch instance contains a set of data,
references, and results objects from an Alchromy analysis.


"""
# External packages
import datetime
import numpy as np
from lib.globals import *


class Alch:
    """
    An Alchromy analysis object. Linked to a single data file. Contains objects
    for each result produced.
    """
    def __init__(self):
        # Miscellaneous data about the alch object
        self.metadata = {
            'date': datetime.datetime.now().isoformat(),  # datetime string
            'version': VERSION,
            'name': 'new',
            'data_file_path': '',
            'reference_file_path': ''
        }
        # Options that are relevant to the deconvolution function
        self.options = {
            'normalize': False,
            'endpoints': [-np.inf, np.inf],
            'mode': 'single'
        }
        # Initialize placeholders for pandas data frames
        self.data = None
        self.references = None
        self.result_df = None

        self.common_idx = None
        self.r2 = None
        self.results = {}

