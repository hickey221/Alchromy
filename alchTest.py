# -*- coding: utf-8 -*-
"""
Created on Wed Jun 13 16:00:24 2018

@author: hickey.221
"""

import pandas as pd
import numpy as np
import deconv_multi




flags={'Image':True,  # Output flags
               'Text':True,
               'Excel':True,
               'Mode':'Simple',
               'Note':'',
               'Normalize':False,
               'Verbose':False,
               'Cutoff':(450,700)}

deconv_multi.multiColDeconv(refPath='refspec.dat',
                              filePath='data/test.xls',
                              ignored=[],
                              flags=flags)