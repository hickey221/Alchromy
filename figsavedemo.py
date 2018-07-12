# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt

plt.ioff()

def show_figure(fig):
    #fig.canvas.draw()
    #plt.show()
    fig.show()

def create_figure(xdata,ydata):
    fig, ax = plt.subplots(1,1)
    ax.plot(xdata,ydata)
    plt.close(fig)
    return fig

xdata = np.arange(20)
ydata = xdata * 2

myFig = create_figure(xdata, ydata)
show_figure(myFig)
#graphs(myFig)

