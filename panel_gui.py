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

versionNumber = "1.3.0"
#%% "About" dialog box
def aboutBox():
    messagebox.showinfo("Alchromy","Alchromy Spectral Deconvolution\nwww.Alchromy.com\nVersion "+versionNumber+"\nRichard Hickey\nOhio State University\n2018")


#%% Title, initialization and menubar
root = T.Tk()
root.title('Alchromy - Spectral Deconvolution')

n = ttk.Notebook(root)
f1 = ttk.Frame(n)   # first page, which would get widgets gridded into it
f2 = ttk.Frame(n)   # second page
f3 = ttk.Frame(n)   # third page
n.add(f1, text='Control panel')
n.add(f2, text='Output')
n.add(f3, text='Assays')
n.grid()

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

T.Label(f1, text="Input file(s)").grid(row=0, column=0,columnspan=3)

radioFile = T.Radiobutton(f1,text="Select File",variable=fileVsDir, value=1,command=useFile)
radioFile.grid(row=1, column=0, sticky='w')
enterFile = T.Entry(f1, textvariable=filePath)
enterFile.grid(row=1, column=1, sticky="w")
buttonBrowseFile = T.Button(f1,text="Browse",command=browseForFile)
buttonBrowseFile.grid(row=1,column=2)

radioDir = T.Radiobutton(f1,text="Select Directory",variable=fileVsDir, value=2,command=useDir)
radioDir.grid(row=2, column=0, sticky='w')
enterDir = T.Entry(f1, textvariable=dirPath)
enterDir.grid(row=2, column=1, sticky="w")
buttonBrowseDir = T.Button(f1,text="Browse",command=browseForDir)
buttonBrowseDir.grid(row=2,column=2)

#%% Kinetic vs replicate
multiMode = T.StringVar(f1,value="Replicate")
T.Label(f1, text="Treat multiple columns as").grid(row=5, column=3, sticky='w')
radioReplicate = T.Radiobutton(f1,text="Replicate",variable=multiMode, value="Replicate")
radioReplicate.grid(row=5, column=4, sticky='w')
radioKinetic = T.Radiobutton(f1,text="Kinetic",variable=multiMode, value="Kinetic")
radioKinetic.grid(row=5, column=5, columnspan=2, sticky='w')

#%% Normalize
normalize = T.BooleanVar(f1,value=False)
T.Label(f1, text="Normalize data to 0").grid(row=6, column=3, sticky='w')
radioNormYes = T.Radiobutton(f1,text="Yes",variable=normalize, value=True)
radioNormYes.grid(row=6, column=4, sticky='w')
#radioNormYes.configure(state="disabled")
radioNormNo = T.Radiobutton(f1,text="No",variable=normalize, value=False)
radioNormNo.grid(row=6, column=5, columnspan=2, sticky='w')
#radioNormNo.configure(state="disabled")

#%% Verbose output
verbose = T.BooleanVar(f1,value=False)
T.Label(f1, text="Verbose debug output").grid(row=7, column=3, sticky='nw')
radioVerboseYes = T.Radiobutton(f1,text="Yes",variable=verbose, value=True)
radioVerboseYes.grid(row=7, column=4, sticky='nw')
radioVerboseNo = T.Radiobutton(f1,text="No",variable=verbose, value=False)
radioVerboseNo.grid(row=7, column=5, columnspan=2, sticky='nw')

#%% Output options
outGraph = T.BooleanVar(f1,value=True)
outTxt = T.BooleanVar(f1,value=True)
outSpectra = T.BooleanVar(f1,value=True)

T.Label(f1, text="Output options").grid(row=0, column=3,columnspan=3)

T.Label(f1, text="Graph (.png)").grid(row=1, column=3, sticky='w')
r_graph_y = T.Radiobutton(f1,text="Yes",variable=outGraph,value=True).grid(row=1, column=4, sticky='w')
r_graph_n = T.Radiobutton(f1,text="No",variable=outGraph,value=False).grid(row=1, column=5, sticky='w')

T.Label(f1, text="Report (.txt)").grid(row=2, column=3, sticky='w')
r_txt_y = T.Radiobutton(f1,text="Yes",variable=outTxt,value=True).grid(row=2, column=4, sticky='w')
r_txt_n = T.Radiobutton(f1,text="No",variable=outTxt,value=False).grid(row=2, column=5, sticky='w')

T.Label(f1, text="Spectra (.xslx)").grid(row=3, column=3, sticky='w')
r_spectra_y = T.Radiobutton(f1,text="Yes",variable=outSpectra,value=True)
r_spectra_y.grid(row=3, column=4, sticky='w')
r_spectra_n = T.Radiobutton(f1,text="No",variable=outSpectra,value=False)
r_spectra_n.grid(row=3, column=5, sticky='w')

#%% Wavelength select
nmMin = T.StringVar(value="450")
nmMax = T.StringVar(value="700")
T.Label(f1, text="Wavelength min-max").grid(row=4, column=3, sticky='w')
e_nmMin = T.Entry(f1, textvariable=nmMin, width=8).grid(row=4, column=4, sticky='w')
e_nmMax = T.Entry(f1, textvariable=nmMax, width=8).grid(row=4, column=5, sticky='w')

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

refDefault = T.BooleanVar(f1, value=True)
T.Label(f1, text="Reference spectra").grid(row=4, column=0, columnspan=2)
refPath = T.StringVar(f1, value="refspec.dat")
r_ref_default = T.Radiobutton(f1,text="Default ",variable=refDefault,value=True,command=useDefaultRef).grid(row=5, column=0, sticky='w')
T.Label(f1, text="refspec.dat").grid(row=5, column=1, sticky="w")
r_ref_custom = T.Radiobutton(f1,text="Custom ",variable=refDefault,value=False,command=useCustomRef).grid(row=6, column=0, sticky='w')
e_ref = T.Entry(f1, textvariable=refPath)
e_ref.grid(row=6, column=1, sticky="w")
b_ref = T.Button(f1,text="Browse", command=browseForRef)
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

colBrowser = T.Frame(f1)
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
labelNote = T.Label(f1,text="File note (appended to filename)")
labelNote.grid(row=0,column=6)
note = T.StringVar(f1, value="")
enterNote = T.Entry(f1, textvariable=note)
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
               'Mode':multiMode.get(),
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

bigGreenButton = T.Button(f1, text="GO", bg="lightgreen", command=launchDeconv)
bigGreenButton.grid(row=1, column=7) #, padx=10, pady=10

#%% Progres bar
pBar = ttk.Progressbar(f1,orient=T.HORIZONTAL,length=300,mode='determinate')
pBar.grid(row=6, column=6, columnspan=3)

#%% status box
def statusUpdate(phrase):
    statusBox.insert(T.END,phrase+"\n")
    statusBox.yview_moveto(1)

statusBox = T.Text(f1, height=10, width=40)
statusBox.grid(row=7,column=6,columnspan=3,rowspan=2)

############################################################
#%% RESULTS PANEL
############################################################
resultsPath = T.StringVar()
resultsPath.set("")
def browseForResults():
    newPath = filedialog.askopenfilename(filetypes=[('Alchromy file','*.alch'),('All files','*.*')])
    if newPath:
        resultsPath.set(newPath)
        #currentResultsFile.update()
        currentResultsFile.xview_moveto(1)

T.Label(f2, text="Results of run:").grid(row=0, column=0)
currentResultsFile = T.Entry(f2, textvariable=resultsPath)
currentResultsFile.grid(row=0, column=1)
T.Label(f2, text="Browse for .alch file:").grid(row=1, column=0)

buttonBrowseResults = T.Button(f2,text="Browse",command=browseForResults)
buttonBrowseResults.grid(row=1,column=1)

#%% Results plot
# Create a canvas
w, h = 300, 200
canvas = T.Canvas(f2, width=w, height=h)
canvas.grid(row=2,column=2, rowspan=3, columnspan=3)
############################################################
#%%  ASSAYS PANEL                                          #
############################################################
T.Label(f3, text="Concentration calculator").grid(row=0, column=0)
T.Label(f3, text="Winterbourn:").grid(row=2, column=3)
T.Label(f3, text="Alayash:").grid(row=3, column=3)

# High vs low met level
highMet = T.BooleanVar()
highMet.set(False)
T.Label(f3, text="MetHb level:").grid(row=1, column=0)
radioLowMet = T.Radiobutton(f3,text="Low",variable=highMet, value=False)
radioLowMet.grid(row=1, column=1, sticky='w')
radioHighMet = T.Radiobutton(f3,text="High",variable=highMet, value=True)
radioHighMet.grid(row=1, column=2, sticky='w')

# Dilution factor
dilution = T.IntVar(value=1)
T.Label(f3, text="Dilution factor:").grid(row=2, column=0)
enterDilution = T.Entry(f3, textvariable=dilution,width=4)
enterDilution.grid(row=2,column=1)

############################################################
#%% EXECUTION                                              #
############################################################
#%% Make some defafult changes
# default dir off
useFile()
useDefaultRef()

#%% Execute loop
root.mainloop()
