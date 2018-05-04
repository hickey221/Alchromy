# -*- coding: utf-8 -*-
"""
Created on Fri May  4 10:14:29 2018

@author: hickey.221
"""

from scipy import signal
import matplotlib.pyplot as plt


Qv = signal.gaussian(540, std=7)
Q0 = signal.gaussian(576, std=7)


plt.plot(Qv)