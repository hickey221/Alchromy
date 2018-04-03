# -*- coding: utf-8 -*-
"""
Alchromy main executable

Richard Hickey

Alchromy is a tool for spectral deconvolution of data from UV-Vis analysis
machines. Compares an experimental spectrum to a set of spectra from known,
pure samples. Designed to seperate 

TODO: Documentation
TODO: Icon
TODO: Error handling
TODO: Add deconvolution description to the readme
TODO: Capture output from deconv and send to GUI
"""

# Requires Python 3.x
import tkinter as T
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import glob
import os
import deconv_multi
import time

versionNumber = "1.2.1"
#%% "About" dialog box
def aboutBox():
    messagebox.showinfo("Alchromy","Alchromy Spectral Deconvolution\nwww.Alchromy.com\nVersion "+versionNumber+"\nRichard Hickey\nOhio State University\n2018")


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
aboutmenu.add_command(label="About",command=aboutBox)
menubar.add_cascade(label="Help", menu=aboutmenu)
root.config(menu=menubar)

# Disable window resize
root.resizable(0,0)

#%% File and directory browsing

fileVsDir = T.IntVar(value=1) # 1=file, 2=dir
allFiles = []
filePath = T.StringVar()
filePath.set("")

dirPath = T.StringVar()
dirPath.set("")

def useFile():
    enterFile.configure(state="normal")
    enterDir.configure(state="disabled")
    buttonBrowseFile.configure(state="normal")
    buttonBrowseDir.configure(state="disabled")
    enterFile.update()
    enterDir.update()

def useDir():
    enterFile.configure(state="disabled")
    enterDir.configure(state="normal")
    buttonBrowseFile.configure(state="disabled")
    buttonBrowseDir.configure(state="normal")
    enterFile.update()
    enterDir.update()

def browseForFile():
    newPath = filedialog.askopenfilename()
    if newPath:
        filePath.set(newPath)
        statusUpdate("Using file "+os.path.basename(filePath.get()))
        #statusUpdate("Found ### waveforms.")
    enterFile.update()
    enterFile.xview_moveto(1)

def browseForDir():
    global allFiles
    newPath = filedialog.askdirectory()
    if newPath:
        dirPath.set(newPath)
        statusUpdate("Using dir /"+os.path.split(dirPath.get())[1]+"/")
        allFiles = glob.glob(dirPath.get()+"/*.*")
        approvedFiles = ['.dat','.txt','.csv','.xls','.xlsx']
        allFiles = [f for f in allFiles if os.path.splitext(os.path.basename(f))[1] in approvedFiles ]

        statusBox.insert(T.END,"Found "+str(len(allFiles))+" files.\n")
    enterDir.update()
    enterDir.xview_moveto(1)

T.Label(root, text="Input file(s)").grid(row=0, column=0,columnspan=3)

radioFile = T.Radiobutton(root,text="Select File",variable=fileVsDir, value=1,command=useFile)
radioFile.grid(row=1, column=0, sticky='w')
enterFile = T.Entry(root, textvariable=filePath)
enterFile.grid(row=1, column=1, sticky="w")
buttonBrowseFile = T.Button(root,text="Browse",command=browseForFile)
buttonBrowseFile.grid(row=1,column=2)

radioDir = T.Radiobutton(root,text="Select Directory",variable=fileVsDir, value=2,command=useDir)
radioDir.grid(row=2, column=0, sticky='w')
enterDir = T.Entry(root, textvariable=dirPath)
enterDir.grid(row=2, column=1, sticky="w")
buttonBrowseDir = T.Button(root,text="Browse",command=browseForDir)
buttonBrowseDir.grid(row=2,column=2)

#%% Kinetic vs replicate
kinetic = T.BooleanVar(root,value=False)
T.Label(root, text="Treat multiple columns as").grid(row=5, column=3, sticky='w')
radioReplicate = T.Radiobutton(root,text="Replicate",variable=kinetic, value=False)
radioReplicate.grid(row=5, column=4, sticky='w')
radioKinetic = T.Radiobutton(root,text="Kinetic",variable=kinetic, value=True)
radioKinetic.grid(row=5, column=5, columnspan=2, sticky='w')

#%% Normalize
normalize = T.BooleanVar(root,value=False)
T.Label(root, text="Normalize data to 0").grid(row=6, column=3, sticky='w')
radioNormYes = T.Radiobutton(root,text="Yes",variable=normalize, value=True)
radioNormYes.grid(row=6, column=4, sticky='w')
#radioNormYes.configure(state="disabled")
radioNormNo = T.Radiobutton(root,text="No",variable=normalize, value=False)
radioNormNo.grid(row=6, column=5, columnspan=2, sticky='w')
#radioNormNo.configure(state="disabled")

#%% Verbose output
verbose = T.BooleanVar(root,value=False)
T.Label(root, text="Verbose debug output").grid(row=7, column=3, sticky='nw')
radioVerboseYes = T.Radiobutton(root,text="Yes",variable=verbose, value=True)
radioVerboseYes.grid(row=7, column=4, sticky='nw')
radioVerboseNo = T.Radiobutton(root,text="No",variable=verbose, value=False)
radioVerboseNo.grid(row=7, column=5, columnspan=2, sticky='nw')

#%% Output options
outGraph = T.BooleanVar(root,value=True)
outTxt = T.BooleanVar(root,value=True)
outSpectra = T.BooleanVar(root,value=True)

T.Label(root, text="Output options").grid(row=0, column=3,columnspan=3)

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
e_nmMin = T.Entry(root, textvariable=nmMin, width=8).grid(row=4, column=4, sticky='w')
e_nmMax = T.Entry(root, textvariable=nmMax, width=8).grid(row=4, column=5, sticky='w')

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
T.Label(root, text="refspec.dat").grid(row=5, column=1, sticky="w")
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
labelNote = T.Label(root,text="File note (appended to filename)")
labelNote.grid(row=0,column=6)
note = T.StringVar(root, value="")
enterNote = T.Entry(root, textvariable=note)
enterNote.grid(row=1,column=6)

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
        allFiles = glob.glob(filePath.get())

    # Check setting for ignored columns
    ignored = list(l_cols_unused.get(0,T.END))
    # Get and check wavelengths
    try:
        nmMinInt = int(nmMin.get())
        nmMaxInt = int(nmMax.get())
    except:
        statusUpdate("Error in wavelengths")
        return

    if nmMinInt > nmMaxInt:
        statusUpdate("Error, minimum too high\n")
        return

    # Print out to status box
    statusUpdate("Running "+str(len(allFiles))+" files.")
    statusUpdate("Ignoring: "+str(ignored))

    # Figure out status bar increments
    if len(allFiles)>0:
        barStep = round(100/len(allFiles))
    else:
        barStep=0
        statusUpdate("No files found, aborting...")
        return
    flags={'Image':outGraph.get(),  # Output flags
               'Text':outTxt.get(),
               'Excel':outSpectra.get(),
               'Kinetic':kinetic.get(),
               'Note':note.get(),
               'Normalize':normalize.get(),
               'Verbose':verbose.get(),
               'Cutoff':(nmMinInt,nmMaxInt)}
    # For each file we have
    for eachFile in allFiles:
        statusUpdate("Reading file: "+os.path.basename(str(eachFile)))
        #######################################################################
        statusReport= deconv_multi.multiColDeconv(refPath=refPath.get(),
                                                  filePath=eachFile,
                                                  ignored=ignored,
                                                  flags=flags)
        #######################################################################
        # Update progress bar
        pBar['value'] += barStep
        pBar.update()
        time.sleep(1)
        if statusReport['Code'] == 0:
            statusUpdate(statusReport['Message'])
        else:
            statusUpdate('Quit with error code: '+statusReport['Code']+': '+statusReport['Message'])

    # When finished, announce it
    statusUpdate("Done!")
    pBar['value'] = 100

bigGreenButton = T.Button(root, text="GO", bg="lightgreen", command=launchDeconv)
bigGreenButton.grid(row=1, column=7) #, padx=10, pady=10

#%% Progres bar
pBar = ttk.Progressbar(root,orient=T.HORIZONTAL,length=300,mode='determinate')
pBar.grid(row=6, column=6, columnspan=3)

#%% status box
def statusUpdate(phrase):
    statusBox.insert(T.END,phrase+"\n")
    statusBox.yview_moveto(1)

statusBox = T.Text(root, height=10, width=40)
statusBox.grid(row=7,column=6,columnspan=3,rowspan=2)

#%% Make some defafult changes
# default dir off
useFile()
useDefaultRef()

#%% Execute loop
root.mainloop()
