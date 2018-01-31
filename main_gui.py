# -*- coding: utf-8 -*-
"""
Alchromy main executable

Richard Hickey


TODO: Documentation
TODO: Icon
TODO: Error handling
TODO: Capture output from deconv and send to GUI
TODO: Input multiple waves from one file
TODO: Figure out when deconv is done running
TODO: Send files one at a time to deconv and make progress bar
TODO: Operator

"""

# Python 3
import tkinter as T
from tkinter import ttk
from tkinter import filedialog
import pandas as pd
import glob
import os
import deconv
import time

#%% Title, initialization and menubar
root = T.Tk()
root.title('Alchromy - Spectral Deconvolution')

# make the top right close button close the main window
root.protocol("WM_DELETE_WINDOW", root.destroy)

# make Esc exit the program
root.bind('<Escape>', lambda e: root.destroy())

# create a menu bar with an Exit command
menubar = T.Menu(root)
filemenu = T.Menu(menubar, tearoff=0)
filemenu.add_command(label="Exit", command=root.destroy)
menubar.add_cascade(label="File", menu=filemenu)

aboutmenu = T.Menu(menubar, tearoff=0)
aboutmenu.add_command(label="About")
menubar.add_cascade(label="About", menu=aboutmenu)
root.config(menu=menubar)

#%% File and directory browsing

fileVsDir = T.IntVar(value=1) # 1=file, 2=dir
allFiles = []
filePath = T.StringVar()
filePath.set("")

dirPath = T.StringVar()
dirPath.set("")

def useFile():
    e1.configure(state="normal")
    e2.configure(state="disabled")
    browse1.configure(state="normal")
    browse2.configure(state="disabled")
    e1.update()
    e2.update()

def useDir():
    e1.configure(state="disabled")
    e2.configure(state="normal")
    browse1.configure(state="disabled")
    browse2.configure(state="normal")
    e1.update()
    e2.update()

def browseForFile():
    newPath = filedialog.askopenfilename()
    if newPath:
        filePath.set(newPath)
        statusUpdate("Using file "+os.path.basename(filePath.get()))
        statusUpdate("Found ### waveforms.")
    e1.update()
    e1.xview_moveto(1)
    
def browseForDir():
    global allFiles
    newPath = filedialog.askdirectory()
    if newPath:
        dirPath.set(newPath)        
        statusUpdate("Using dir /"+os.path.split(dirPath.get())[1]+"/")
        allFiles = glob.glob(dirPath.get()+"/*.dat")
        
        statusBox.insert(T.END,"Found "+str(len(allFiles))+" files.\n")
    e2.update()
    e2.xview_moveto(1)

T.Label(root, text="Input file(s)").grid(row=0, column=0,columnspan=2)

r1 = T.Radiobutton(root,text="Select File",variable=fileVsDir, value=1,command=useFile)
r1.grid(row=1, column=0, sticky='w')
e1 = T.Entry(root, textvariable=filePath)
e1.grid(row=1, column=1, sticky="w")
browse1 = T.Button(root,text="Browse",command=browseForFile)
browse1.grid(row=1,column=2)

r2 = T.Radiobutton(root,text="Select Directory",variable=fileVsDir, value=2,command=useDir)
r2.grid(row=2, column=0, sticky='w')
e2 = T.Entry(root, textvariable=dirPath)
e2.grid(row=2, column=1, sticky="w")
browse2 = T.Button(root,text="Browse",command=browseForDir)
browse2.grid(row=2,column=2)

#%% Output options
outGraph = T.BooleanVar(root,value=True)
outTxt = T.BooleanVar(root,value=True)
outSpectra = T.BooleanVar(root,value=True)

T.Label(root, text="Output options").grid(row=0, column=3,columnspan=2)

T.Label(root, text="Graph (.png)").grid(row=1, column=3, sticky='w')
r_graph_y = T.Radiobutton(root,text="Yes",variable=outGraph,value=True).grid(row=1, column=4, sticky='w')
r_graph_n = T.Radiobutton(root,text="No",variable=outGraph,value=False).grid(row=1, column=5, sticky='w')

T.Label(root, text="Report (.txt)").grid(row=2, column=3, sticky='w')
r_txt_y = T.Radiobutton(root,text="Yes",variable=outTxt,value=True).grid(row=2, column=4, sticky='w')
r_txt_n = T.Radiobutton(root,text="No",variable=outTxt,value=False).grid(row=2, column=5, sticky='w')

T.Label(root, text="Spectra (.xslx)").grid(row=3, column=3, sticky='w')
r_spectra_y = T.Radiobutton(root,text="Yes",variable=outSpectra,value=True)
r_spectra_y.grid(row=3, column=4, sticky='w')
r_spectra_n = T.Radiobutton(root,text="No",variable=outSpectra,value=False)
r_spectra_n.grid(row=3, column=5, sticky='w')

#%% Wavelength select

nmMin = T.StringVar(value="450") 
nmMax = T.StringVar(value="700") 
T.Label(root, text="Wavelength min-max").grid(row=4, column=3, sticky='w')
#T.Label(root, text="Min").grid(row=4, column=3, sticky='w')
e_nmMin = T.Entry(root, textvariable=nmMin, width=6).grid(row=4, column=4, sticky='w')
e_nmMax = T.Entry(root, textvariable=nmMax, width=6).grid(row=4, column=5, sticky='w')


#%% Specify reference spectra

def getRefCols(filePath='refspec.dat'):
    try:
        ref = pd.read_csv(filePath,'\t')
        species = list(ref.drop('nm',axis=1))
    except:
        statusUpdate("Error reading file!")
        return
    # clear lists
    l_cols_unused.delete(0, T.END)
    l_cols_used.delete(0, T.END)

     # update used list
    for item in species:
        l_cols_used.insert(T.END,item)

    statusUpdate("Using reference "+os.path.basename(filePath))        
    statusUpdate("Found " + str(len(species)) + " waves.") 
    
def useCustomRef():
    e_ref.configure(state="normal")
    b_ref.configure(state="normal")

def useDefaultRef():
    getRefCols()
    e_ref.configure(state="disabled")
    b_ref.configure(state="disabled")

def browseForRef():
    newPath = filedialog.askopenfilename()
    if newPath:
        refPath.set(newPath)
    getRefCols(newPath)
    e_ref.update()
    e_ref.xview_moveto(1)

refDefault = T.BooleanVar(root, value=True)
T.Label(root, text="Reference spectra").grid(row=4, column=0, columnspan=2)
refPath = T.StringVar(root, value="refspec.dat")
r_ref_default = T.Radiobutton(root,text="Default ",variable=refDefault,value=True,command=useDefaultRef).grid(row=5, column=0, sticky='w')
r_ref_custom = T.Radiobutton(root,text="Custom ",variable=refDefault,value=False,command=useCustomRef).grid(row=6, column=0, sticky='w')
e_ref = T.Entry(root, textvariable=refPath)
e_ref.grid(row=6, column=1, sticky="w")
b_ref = T.Button(root,text="Browse", command=browseForRef)
b_ref.grid(row=6,column=2)

#%% Choose columns to use
def useCol():
    mover = l_cols_unused.get(T.ACTIVE)
    l_cols_used.insert(0, mover)
    l_cols_unused.delete(T.ACTIVE)

def unuseCol():
    mover = l_cols_used.get(T.ACTIVE)
    l_cols_unused.insert(0, mover)
    l_cols_used.delete(T.ACTIVE)

colBrowser = T.Frame(root)
T.Label(colBrowser, text="Used").grid(row=0, column=0)
T.Label(colBrowser, text="Ignored").grid(row=0, column=2)
l_cols_used = T.Listbox(colBrowser)

l_cols_unused = T.Listbox(colBrowser)
l_cols_used.grid(row=1,column=0,rowspan=4)
l_cols_unused.grid(row=1,column=2,rowspan=4)

b_useCol = T.Button(colBrowser,text="<", command=useCol).grid(row=1,column=1,sticky='s')
b_unuseCol = T.Button(colBrowser,text=">",command=unuseCol).grid(row=2,column=1,sticky='n')

colBrowser.grid(row=7,column=0,columnspan=3)

#%% Operator ID
labelOpID = T.Label(root,text="Operator ID")
labelOpID.grid(row=0,column=6)
opID = T.StringVar(root, value="John Doe")
enterOpID = T.Entry(root, textvariable=opID)
enterOpID.grid(row=1,column=6)


#%% Go button!
def launchDeconv():
    # clear progress bar
    global allFiles
    global nmMin
    global nmMax
    pBar['value'] = 0
    
    # Decide what file we're using
    if fileVsDir.get()==1:
        #dataFile = filePath.get()
        allFiles = [glob.glob(filePath.get())]
    #else:
        ##dataFile = dirPath.get()
        #dataFile = glob.glob(dirPath.get()+"/*.dat")
        
    # Check setting for ignored columns
    ignored_species = list(l_cols_unused.get(0,T.END))
    # Get and check 
    try:
        nmMinInt = int(nmMin.get())
        nmMaxInt = int(nmMax.get())
    except:
        #statusBox.insert(T.END, "Error in wavelengths\n")
        statusUpdate("Error in wavelengths")
        return
    
    if nmMinInt > nmMaxInt:
        #statusBox.insert(T.END, "Error, minimum too high\n")
        statusUpdate("Error, minimum too high\n")
        return
        
    # Print out to status box
    statusUpdate("Have files "+str(allFiles))
    statusUpdate("Ignoring: "+str(ignored_species))
    
    # Figure out status bar increments
    barStep = round(100/len(allFiles))
    # For each file we have
    for eachFile in allFiles:
        statusUpdate("Reading file: "+str(eachFile))
        deconv.deconv(eachFile,reffile=refPath.get(),except_species=ignored_species,nm_min=nmMinInt, nm_max=nmMaxInt)
        # Update progress bar
        pBar['value'] += barStep
        pBar.update()
        time.sleep(1)

    # When finished, announce it
    statusUpdate("Done")
    pBar['value'] = 100

bigGreenButton = T.Button(root, text="GO", bg="lightgreen", command=launchDeconv)
bigGreenButton.grid(row=1, column=7) #, padx=10, pady=10

# Progres bar
pBar = ttk.Progressbar(root,orient=T.HORIZONTAL,length=200,mode='determinate')
pBar.grid(row=6, column=5, columnspan=2, sticky='s')
#pBarCanvas = T.Canvas(root)
#pBarCanvas.create_text(0,0,"Bar label")
#pBarCanvas.grid(row=6, column=5, columnspan=2, sticky='s')
#pBarLabel = T.Label(root,text="Bar label")
#pBarLabel.grid(row=6, column=5, columnspan=2, sticky='s')

# status box
def statusUpdate(phrase):
    statusBox.insert(T.END,phrase+"\n")
    statusBox.yview_moveto(1)
    
statusBox = T.Text(root, height=10, width=40)
statusBox.grid(row=7,column=5,columnspan=3,rowspan=2)

#%% Make some defafult changes
# default dir off
useFile()
useDefaultRef()


#%% Execute loop
root.mainloop()

