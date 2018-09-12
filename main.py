# -*- coding: utf-8 -*-
'''
Created on Mon Jun 18 09:11:28 2018

@author: hickey.221

TODO: Add icon to TopLevel windows
'''
# Standard imports
import tkinter as T
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
from warnings import warn
import pandas as pd
import os
from numpy import arange, sin, pi #TEMP for embedded plot test
# For result GUI
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
# Custom imports
#from themes import * # For dict solarized
import alchClass

global versionNumber
versionNumber = '1.5.0'
global selectedTheme
global verbose
verbose = True
#def set_theme(frame, mode):
#    if mode=='light':
#        frame.tk_setPalette(background=solarized['lightbg1'], foreground=solarized['lighttext1'],
#               activeBackground=solarized['lightbg2'], activeForeground=solarized['lighttext2'])
#        selectedTheme = 'light'
#    elif mode == 'dark':
#        frame.tk_setPalette(background=solarized['darkbg1'], foreground=solarized['darktext1'],
#               activeBackground=solarized['darkbg2'], activeForeground=solarized['darktext2'])
#        selectedTheme = 'dark'
#    else:
#        pass

def Vprint(*msg):
    """
    Print a string iff the verbose setting is True.
    """
    if verbose:
        print(*msg)
    else:
        pass

class A_main:
    def __init__(self, root):
        self.root = root # Expect this to be root
        # General main window stuff
        self.root.title('Alchromy - Spectral Deconvolution')
        self.root.geometry('800x600')
        self.root.iconbitmap('lib/alch_flask_icon.ico')
        self.selectedTheme = T.StringVar(value='light')
        #self.theme_light()
        self.nb = ttk.Notebook(self.root)
        
        # Moved Alch init to main
        self.Alch = alchClass.Alch()
        # Menubar
        self.make_menu()
        
        # Not in use
        #self.custom_menu = A_Menu(self.master)
        #self.master.overrideredirect(True) # removes titlebar

        # Make frames and pack them
        #self.menuFrame = A_Menu(self.master)
        self.leftFrame = A_L_frame(self)
        self.rightFrame = A_R_frame(self)
        
        try:
            self.resultFrame = A_ResultTab(self)
            Vprint('Able to create resultFrame')
        except Exception as e:
            Vprint('Not able to create resultFrame:',e)
        
        self.nb.add(self.leftFrame.frame, text='Input')
        self.nb.add(self.resultFrame.frame, text='Results')
        self.nb.pack(expand=1, fill='both')
        
    def Update(self):
        Vprint('Updating Main')
        try:
            self.resultFrame.Update()
        except:
            Vprint('Could not find self.resultFrame')

        #self.resultFrame.Update()

    def arrange(self):
        #self.custom_menu.pack(side=T.TOP,fill=T.X)
        self.leftFrame.pack(side=T.LEFT, fill=T.BOTH)
        self.rightFrame.pack(side=T.RIGHT,fill=T.Y)
        
    def _quit(self):
        Vprint('Quitting...')
        self.root.quit()
        self.root.destroy() 

    def make_menu(self):
        self.root.protocol('WM_DELETE_WINDOW', self._quit)

        # create a menu bar with an Exit command
        self.menubar = T.Menu(self.root)
        filemenu = T.Menu(self.menubar, tearoff=0, bd=0,relief=T.FLAT)
        filemenu['borderwidth'] = 0
        filemenu.add_command(label='Exit', command=self._quit)
        self.menubar.add_cascade(label='File', menu=filemenu)

        viewmenu = T.Menu(self.menubar, tearoff=0, bd=0,relief=T.FLAT)
        viewmenu.add_checkbutton(label='Light mode', onvalue='light', offvalue='dark', variable=self.selectedTheme)
        viewmenu.add_checkbutton(label='Dark mode', onvalue='dark', offvalue='light', variable=self.selectedTheme)
        self.menubar.add_cascade(label='View', menu=viewmenu)

        aboutmenu = T.Menu(self.menubar, tearoff=0, bd=0,relief=T.FLAT)
        aboutmenu.add_command(label='About',command=self.about_Box)
        self.menubar.add_cascade(label='Help', menu=aboutmenu)
        #self.menubar['highlightthickness']=0
        self.root.config(menu=self.menubar)

    def about_Box(self):
        messagebox.showinfo('Alchromy','Alchromy Spectral Deconvolution\nwww.Alchromy.com\nVersion '+versionNumber+'\nRichard Hickey\nOhio State University\n2018')

#%% LEFT FRAME - MAIN CONFIG PANEL
class A_L_frame:
    """
    Panel in main window for controlling file loading and other operations
    """
    def __init__(self,master):
        self.master = master # Expect this to be main_gui instance
        self.root = self.master.root
        self.frame = ttk.Frame(self.master.nb) # This frame, where widgets will live

        # Now refer to other Alch
        self.Alch = self.master.Alch

        # Initialize, but do not open, browse windows
        self.dataWindow = A_LoadWindow(self,colType='exp')
        self.refWindow = A_LoadWindow(self,colType='ref')
        #self.resultWindow = A_ResultWindow(self)
        
        # Create all the stuff
        self.make_widgets()
        # Preload reference from file
        self.preload_ref()
        # Finish init and arrange widget
        self.status_update()
        self.arrange()
        
    def make_widgets(self):
        # Make data browse buttons
        self.combo_data = T.Frame(self.frame)
        #self.lab_selectFile = T.Label(self.frame, text='Input file(s)')
        self.str_dataLoaded = T.StringVar(self.frame)
        self.lab_dataLoaded = T.Label(self.combo_data, textvariable=self.str_dataLoaded, width=20)
        self.but_selectFile = T.Button(self.combo_data, text='Load/Edit', command=self.dataWindow.Focus)

        # Reference browse button
        self.combo_ref = T.Frame(self.frame)
        self.str_refLoaded = T.StringVar(self.frame)
        self.lab_refLoaded = T.Label(self.combo_ref, textvariable=self.str_refLoaded, width=20)
        self.but_selectRef = T.Button(self.combo_ref, text='Load/Edit', command=self.refWindow.Focus)

        # Analyze button!
        self.but_analyze = T.Button(self.frame, text='Begin analysis', command=self.analyze)
        # Results test button
        #self.but_results = T.Button(self.frame, text='Result window', command=self.resultWindow.Focus)
        #self.but_plot = T.Button(self.frame, text='Plot test',command=self.resultWindow.plot_frame)
 
    def preload_ref(self):
        """
        Load in a hardcoded default reference path
        """
        ref = 'ref/default.dat'
        Vprint("Loading default reference file",)
        self.refWindow.Focus()
        self.refWindow.filePath.set(ref)
        self.refWindow.oldPath.set(ref)
        self.refWindow.Read_Columns()
        self.refWindow.List()
        self.refWindow.Save()
    
    def analyze(self):
        # Check to see if we're ready
        self.status_update()
        if not self.str_dataLoaded.get():
            warn("Don't have data files loaded")
            return
        elif not self.str_refLoaded.get():
            warn("Don't have reference files loaded")
            return
        else:
            # If it all looks good, tell Alch to get to make a new result
            Vprint('Calling for a result to be generated')
            self.Alch.generate_result()
            
            
            #self.Alch.plot_results()

    def status_update(self):
        """
        Check if the Alch object has loaded data yet
        """
        Vprint('Updating status')
        # Check if data file has been locked in
        if self.Alch.expPath:
            self.str_dataLoaded.set('Data file loaded')
            self.lab_dataLoaded.config(bg='green')
        else:
            self.str_dataLoaded.set('Data not loaded')
            self.lab_dataLoaded.config(bg='red')
        # Check for reference
        if self.Alch.refPath:
            self.str_refLoaded.set('Reference file loaded')
            self.lab_refLoaded.config(bg='green')
        else:
            self.str_refLoaded.set('Reference not loaded')
            self.lab_refLoaded.config(bg='red')
        self.master.Update()

    def pack(self,*args,**kwargs):
        # To be called by master window
        self.frame.pack(*args,**kwargs)

    def arrange(self):
        # Pack everything together
        #self.lab_selectFile.pack(side=T.TOP)
        self.lab_dataLoaded.pack(side=T.LEFT, anchor=T.W)
        self.but_selectFile.pack(side=T.LEFT)
        self.combo_data.pack(side=T.TOP)

        self.lab_refLoaded.pack(side=T.LEFT,anchor=T.W)
        self.but_selectRef.pack(side=T.LEFT,anchor=T.E)
        self.combo_ref.pack(side=T.TOP)

        self.but_analyze.pack(side=T.TOP)
        #self.but_results.pack()
        #self.but_plot.pack()

#%% RIGHT FRAME - LOGO, RESULTS
class A_R_frame:
    def __init__(self,master):
        self.master = master # Expect this to be main_gui instance
        self.frame = ttk.Frame(self.master.nb) # This frame, where widgets will live
        #self.make_logo()
        self.title = T.Label(self.frame,text='Alchromy v. '+str(versionNumber))
        self.arrange()

    def make_logo(self):
        # Logo in top right
        #_imagefile = Image.open('lib/logo_378x100.png')
        _imagefile = Image.open('lib/alch_flask_icon.gif')
        _imagefile = _imagefile.resize((90, 90))
        _photo = ImageTk.PhotoImage(_imagefile)
        self.logo = T.Label(self.frame, image=_photo)
        self.logo.image = _photo # keep a reference!

    def pack(self,*args,**kwargs):
        # To be called by master window
        self.frame.pack(*args,**kwargs)

    def arrange(self):
        # Pack everything together
        #self.logo.pack(side=T.TOP)
        self.title.pack(side=T.TOP)

#%% NEW WINDOW FOR LOADING DATA
class A_LoadWindow:
    """
    An object that manages the loading of a file, either of experimental or
    reference data.
    Methods:
        __init__(): Initialize the object, but doesn't create a window
        Open(): Create the window
        Browse(): Call the file open dialog to read a file
        Cancel(): Reset to previous (temp) data and close
        Reset(): Clears the temp data
        Save(): Convert temp data to saved data
        List(): Refresh items in listbox
        Focus(): If window exists, focus it, otherwise call Open()
        Frames(): Create frames for filling with widgets
        Arrange(): Pack frames and widgets into the window
    """
    def __init__(self,master,colType):
        # Initialize bare minimum, wait for Open() to be called to do the rest
        self.master = master # A_main
        self.root = self.master.root
        self.colType = colType # 'exp' or 'ref'
        self.filePath = T.StringVar(value='')
        self.oldPath = T.StringVar(value='')
        self.windowOpen = None # Object starts without a window

        # Establish old path if applicable
        if colType=='exp':
            if self.master.Alch.expPath:
                self.oldPath = self.master.Alch.expPath
        elif colType=='ref':
            if self.master.Alch.refPath:
                self.oldPath = self.master.Alch.refPath

    def Open(self):
        # The rest of the initialization procedure, opening the window
        self.window = T.Toplevel(self.root) # All the way up to root
        self.window.geometry('300x300')
        self.window.iconbitmap('lib/alch_flask_icon.ico')
        self.Frames() # Gives topFrame, midFrame, botFrame

        self.topInfo = T.Label(self.topFrame, text='Upload your data file here')
        self.ent_file = T.Entry(self.topFrame, textvariable=self.filePath)
        self.but_file = T.Button(self.topFrame, text='Browse',command=self.Browse)

        self.listItems = T.Listbox(self.midFrame,selectmode='multiple')

        self.but_reset = T.Button(self.botFrame, text='Reset', command=self.Reset)
        self.but_cancel = T.Button(self.botFrame, text='Cancel', command=self.Cancel)
        self.but_save = T.Button(self.botFrame, text='Save', command=self.Save)
        self.Arrange()

        # Set window status and close procedure
        self.window.protocol('WM_DELETE_WINDOW', self.Cancel) # X = Cancel()
        self.windowOpen = True # Window officially exists now

    def Browse(self):
        # Open file browse dialog
        newPath = filedialog.askopenfilename(parent = self.window,filetypes=[('Data file','*.csv *.dat *.txt *.xls *.xlsx'),('All files','*.*')])
        if not newPath:
            Vprint('Nothing chosen, nothing saved')
            return None
        else:
            Vprint("From dialog got",newPath)
        # If we have a new file...
        try:
            ## Read in data file using existing Alch instance
            # TODO: What if we don't want to keep this one and cancel later?
            #self.master.Alch.load_exp(newPath)
            self.filePath.set(newPath)
            Vprint('Calling Read_Columns')
            self.Read_Columns()

            self.ent_file.xview_moveto(1)
        except:
            warn('Error between Browse()-load_exp()')
            self.Cancel()
        #Vprint('Received '+str(len(self.master.Alch.exp))+' cols from Browse()')
        self.List()

    def Read_Columns(self):
        """
        Read in the data from a spreadsheet file. Assumes a header row, and
        the first column must contain the x-axis (wavelengths).
        """
        Vprint('Check 1')
        _, ext = os.path.splitext(self.filePath.get())
        Vprint('Check 2')
        allowedFiles = ['.csv','.dat','.txt','.xls','.xlsx']
            # Read in the file
        Vprint("My extension is",ext)
        if ext in allowedFiles:
            if ext in ['.xls','.xlsx']:
                Vprint("Reading as excel")
                self.df = pd.read_excel(self.filePath.get())
            else:
                Vprint("Reading as plaintext (tab delim)")
                self.df = pd.read_csv(self.filePath.get(),'\t')
            Vprint('Check 3')
            # Clean up the dataframe
            # Rename first column as 'nm' for wavelengths
            self.df.rename(columns={self.df.columns[0]:'nm'}, inplace=True)
            # Bug fix for duplicate 2nd column name in some Olis-produced files
            if self.df.columns[1] == '0.1':
                self.df.rename(columns={self.df.columns[1]:'0'}, inplace=True)

            # Add stuff to the listBox
            self.cols = list(self.df.drop('nm',axis=1)) # Data col names
            Vprint('Sending',self.cols,'to List()')
            #self.List() # done in Browse()

        else:
            Vprint("Error: File must be of type:", allowedFiles)

    def List(self):
        # Received columns, now populate listbox
        try:
            # Clear listbox if not empty
            if self.listItems.size() > 0:
                Vprint('Clearing listbox')
                self.listItems.delete(0,T.END)
            # Repopulate with data col names from Alch
            for l in self.cols:
                self.listItems.insert(T.END, l) # Grab all colnames
                self.listItems.select_set(0, T.END) # Select all by default
        except:
            warn('Something went wrong populating column list')

    def Cancel(self):
        """
        Discard changes since window has been open
        """
        Vprint('Cancelling ' + self.filePath.get())
        Vprint('Revering back to ' + self.oldPath.get())
        
        self.filePath.set(self.oldPath.get())
        #TODO: Re-select correct listbox items
        # for item in cols
            # 
            #self.listItems.select_set(0)
        # Hide window but preserve the object
        self.window.withdraw()
        #self.windowOpen = None

    def Reset(self):
        # Pretend this object never existed
        Vprint('Throwing it all away')
        self.filePath.set('')
        self.oldPath.set('')
        # Erase data saved to the Alch
        self.windowOpen = None
        self.master.status_update()
        self.window.destroy()

    def Save(self):
        """
        Commit changes back to the associated Alch object
        TODO: Should any of this be moved to the Alch method?
        """
        # Get the desired columns from the listbox
        selectedCols = [self.listItems.get(i) for i in self.listItems.curselection()]
        selectedCols.insert(0,'nm') # Don't forget the 1st col!
        Vprint('Saving', selectedCols, 'from', self.filePath.get())

        # Save selected list cols to the Alch df
        self.master.Alch.load_cols(self.df,self.colType,self.filePath.get())

        # Update status of the master status window
        self.master.status_update()

        # Close window, our job is done
        self.window.withdraw()

    def Focus(self):
        """
        Open a single file browse window, or focus an already opened one.
        """
        if self.windowOpen:
            # If we already have one open, raise it
            try:
                self.window.deiconify()
                Vprint('Used deiconify()')
            except:
                self.window.lift()
                Vprint('Used lift()')
        else:
            # Else, create a new one
            Vprint('Making a new window!')
            self.Open()
        # Move cursor to the end
        self.ent_file.xview_moveto(1)

    def Frames(self):
        self.topFrame = T.Frame(self.window)
        self.midFrame = T.Frame(self.window)
        self.botFrame = T.Frame(self.window)

        self.topFrame.pack(side=T.TOP, fill=T.X)
        self.midFrame.pack(side=T.TOP, fill=T.BOTH)
        self.botFrame.pack(side=T.BOTTOM, fill=T.X)

    def Arrange(self):
        # Pack top frame
        self.topInfo.pack(side=T.TOP)
        self.ent_file.pack(side=T.LEFT,fill=T.X,expand=True)
        self.but_file.pack(side=T.RIGHT)
        # Pack middle frame
        self.listItems.pack()
        # Pack bottom frame
        self.but_reset.pack(side=T.RIGHT)
        self.but_cancel.pack(side=T.RIGHT)
        self.but_save.pack(side=T.RIGHT)
#%%
class A_ResultTab:
    """
    An object that manages the loading of a file, either of experimental or
    reference data.
    Methods:

    """
    def __init__(self, master):
        self.master = master
        self.root = self.master.root
        self.Alch = self.master.Alch
        
        self.frame = ttk.Frame(self.master.nb) # Main frame called by master
        
        self.LFrame = A_ResultFrame(self)
        self.RFrame = A_GUIFrame(self)
        
        self.LFrame.pack(side=T.LEFT, fill=T.BOTH)
        self.RFrame.pack(side=T.RIGHT, fill=T.BOTH)
        #self.RFrame.pack(side=T.RIGHT, fill=T.BOTH)
        
    def Update(self):
        self.LFrame.Update()
        self.RFrame.Update()
        
#%%
class A_GUIFrame:
    def __init__(self,master):
        Vprint('Starting GUIFrame')
        self.master = master
        self.Alch = self.master.Alch
        self.root = self.master.root
        self.refreshButton = T.Button(master=self.master.frame, text='Refresh', command=self.master.Update)

        self.setup_plot()
        self.Arrange()
        self.Update()
        # TODO: Store some info here that can be shared between the results 
        # frames eg. the chosen result itself.
        
    def setup_plot(self):
        self.fig = Figure(figsize=(3, 2), dpi=100)
        self.a = self.fig.add_subplot(111)
        
    def Update(self):
        """
        Check to see if there is a new figure to plot
        """
        Vprint('Updating result plot')
        
        self.a.clear()
        try:
            l = len(self.Alch.result_list)
        except:
            l = 0    
        if l==1:
            # Temp solution if there's 1 result
            Vprint('Using actual solution')
            #result = self.master.result
            result = self.Alch.result_list[0]
            self.fig = Figure(figsize=(3, 2), dpi=100)
            #a = self.f.add_subplot(111)
            x = result.expData['nm']
            y = result.expData['data']
            yy = result.fit
            self.a.clear()
            self.a.plot(x,y,x,yy)
            #self.f = self.Alch.result_list[0].export()
        else:
            Vprint('Using dummy data')
            #self.f = Figure(figsize=(3, 2), dpi=100)
            #a = self.f.add_subplot(111)
            t = arange(0.0, 3.0, 0.01)
            s = sin(2*pi*t)
            self.a.clear()
            self.a.plot(t, s)
        self.canvas.draw()

    def Arrange(self):

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master.frame)
        self.canvas.show()
        self.canvas.get_tk_widget().pack(side=T.TOP, fill=T.BOTH, expand=1)
        
        toolbar = NavigationToolbar2TkAgg(self.canvas, self.master.frame)
        toolbar.update()
        self.canvas._tkcanvas.pack(side=T.TOP, fill=T.BOTH, expand=1)
        self.refreshButton.pack()

        def on_key_event(event):
            Vprint('you pressed %s' % event.key)
            key_press_handler(event, self.canvas, toolbar)
        self.canvas.mpl_connect('key_press_event', on_key_event)

    def pack(self,*args,**kwargs):
        # To be called by master window
        pass
        #self.frame.pack(*args,**kwargs)
#%%
class A_ResultFrame:
    def __init__(self,master):
        self.master = master # Frame containing loadWindow, Alch, etc.
        self.root = self.master.root # All the way up to root
        self.windowOpen = None # Object starts without a window
        self.frame = self.master.frame
        
        # Establish widgets
        self.resultChoices = ['Choose a result']
        self.resultName = T.StringVar(self.frame)
        self.resultName.set('Choose a result')
        self.resultMenu = T.OptionMenu(self.frame,self.resultName,*self.resultChoices, command=self.read_result)
        self.dummyText = T.StringVar(self.frame,value='none')
        self.dummyLabel = T.Label(self.frame,textvariable=self.dummyText)
        
        # Check for initial data
        self.Update()
        
        # Pack the widgets
        self.Arrange()
        
    def Update(self):
        self.results = self.master.Alch.result_list # List of result objects
        # Result list dropdown items
        self.resultChoices = ['Choose a result']
        self.resultName.set('Choose a result')
        for r in self.results:
            Vprint(r)
            # Get a string of the epoch timestamp of each result
            self.resultChoices.append(str(r.ts.timestamp()))

    def read_result(self,*args):
        """
        Get data about the chosen result
        """
        Vprint('Looking inside resultChoices menu')
        theChoice = self.resultName.get()
        for i in self.resultChoices:
            print(i)
        if theChoice=='Choose a result':
            # Break if nothing selected yet
            Vprint('Default option selected, aborting read_result')
            return
        resultLoc = self.resultChoices.index(theChoice)-1
        #self.master.result = self.results[resultLoc]
        result = self.results[resultLoc]
        # Change the display text shown
        #self.dummyText.set(str(result.ts))
        self.dummyText.set(result.ts.strftime("%c"))

    def addItem(self,item):
        """
        Accept an indivudal species and number combination and make a widget
        """
        # Generate label based on species
        # Add
        pass

    # Method for producing wigdets to reside in this frame
            # Widget containing data from the results
            # Image
            # Settings used
            # Numeric data (percent composition)

    def Arrange(self):
        self.resultMenu.pack()
        self.dummyLabel.pack()
        # Place widgets into the window and pack()

    def pack(self,*args,**kwargs):
        # To be called by master window
        self.frame.pack(*args,**kwargs)

#%% Execute loop
root = T.Tk()

app = A_main(root)
root.mainloop()
