# -*- coding: utf-8 -*-
"""
Created on Tue Jun 12 17:41:47 2018

@author: hickey.221

AlchClass.py

Describes the Alch object class. An Alch instance contains a set of data,
references, and results objects from an Alchromy analysis.

TODO: Change result_list to only be a single result per alch
TODO: Move methods out of this class

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
        self.metadata = {
            'date': datetime.datetime.now().isoformat(),  # datetime string
            'version': VERSION,
            'name': 'new'
        }
        self.options = {
            'normalize': False,
            'endpoints': [-np.inf, np.inf],
            'mode': 'single'
        }
        # Initialize placeholders for pandas data frames
        self.data = None
        self.references = None
        self.common_idx = None
        self.result = None
        self.ready = False
        self.r2 = None
        # self.name = "new"
        # self.outputPath = outputPath
        # self.refPath = refPath
        # self.normalize = False
        # self.endpoints = (-np.inf, np.inf)
        # self.result_list = []
        # self.mode = None  # 'S'ingle, 'R'eplicate, 'K'inetic
