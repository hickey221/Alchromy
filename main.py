# -*- coding: utf-8 -*-
'''
Created on Mon Jun 18 09:11:28 2018

@author: hickey.221

TODO: Add icon to TopLevel windows
'''
# Standard imports
import tkinter as T
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from warnings import warn
import pandas as pd
import os
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
    def __init__(self, master):
        self.master = master # Expect this to be root
        # General main window stuff
        self.master.title('Alchromy - Spectral Deconvolution')
        self.master.geometry('500x300')
        self.selectedTheme = T.StringVar(value='light')
        #self.theme_light()

        # Menubar
        self.make_menu()
        #self.custom_menu = A_Menu(self.master)
        #self.master.overrideredirect(True) # removes titlebar

        # Make frames and pack them
        #self.menuFrame = A_Menu(self.master)
        self.leftFrame = A_L_frame(self.master)
        self.rightFrame = A_R_frame(self.master)

        self.arrange()

    def arrange(self):
        #self.custom_menu.pack(side=T.TOP,fill=T.X)
        self.leftFrame.pack(side=T.LEFT, fill=T.BOTH)
        self.rightFrame.pack(side=T.RIGHT,fill=T.Y)

    def make_menu(self):
        root.protocol('WM_DELETE_WINDOW', root.destroy)

        # create a menu bar with an Exit command
        self.menubar = T.Menu(self.master)
        filemenu = T.Menu(self.menubar, tearoff=0, bd=0,relief=T.FLAT)
        filemenu['borderwidth'] = 0
        filemenu.add_command(label='Exit', command=root.destroy)
        self.menubar.add_cascade(label='File', menu=filemenu)

        viewmenu = T.Menu(self.menubar, tearoff=0, bd=0,relief=T.FLAT)
        viewmenu.add_checkbutton(label='Light mode', onvalue='light', offvalue='dark', variable=self.selectedTheme)
        viewmenu.add_checkbutton(label='Dark mode', onvalue='dark', offvalue='light', variable=self.selectedTheme)
        self.menubar.add_cascade(label='View', menu=viewmenu)

        aboutmenu = T.Menu(self.menubar, tearoff=0, bd=0,relief=T.FLAT)
        aboutmenu.add_command(label='About',command=self.about_Box)
        self.menubar.add_cascade(label='Help', menu=aboutmenu)
        #self.menubar['highlightthickness']=0
        self.master.config(menu=self.menubar)

    def about_Box(self):
        messagebox.showinfo('Alchromy','Alchromy Spectral Deconvolution\nwww.Alchromy.com\nVersion '+versionNumber+'\nRichard Hickey\nOhio State University\n2018')


#%% CUSTOM MENU - NOT IN USE
#class A_Menu:
#    def __init__(self, master):
#        self.master = master
#        self.frame = T.Frame(self.master)
#        self.m_File = T.Label(self.frame, text='File')
#        self.m_View = T.Label(self.frame, text='View')
#
#        # Grabbable part in center of bar
#        self.m_grip = T.Label(self.frame, bg='black')
#
#        self.m_Min = T.Button(self.frame, text='__',command=self.Min)
#        self.m_Close = T.Button(self.frame, text='X',command=self.Close)
#
#        self.arrange()
#        # Click-n-drag stuff
#        self.m_grip.bind("<ButtonPress-1>", self.StartMove)
#        self.m_grip.bind("<ButtonRelease-1>", self.StopMove)
#        self.m_grip.bind("<B1-Motion>", self.OnMotion)
#
#        self.m_grip.bind("<Map>",self.frame_mapped)
#
#    def Min(self):
#        #self.master.iconify()
#        self.master.update_idletasks()
#        self.master.overrideredirect(False)
#        #root.state('withdrawn')
#        self.master.state('iconic')
#
#    def Max(self):
#        self.master.destroy()
#
#    def Close(self):
#        self.master.destroy()
#
#    def StartMove(self, event):
#        self.x = event.x
#        self.y = event.y
#
#    def StopMove(self, event):
#        self.x = None
#        self.y = None
#
#    def OnMotion(self, event):
#        deltax = event.x - self.x
#        deltay = event.y - self.y
#        x = self.master.winfo_x() + deltax
#        y = self.master.winfo_y() + deltay
#        self.master.geometry("+%s+%s" % (x, y))
#
#    def frame_mapped(self,e):
#        print(self,e)
#        self.master.update_idletasks()
#        self.master.overrideredirect(True)
#        self.master.state('normal')
#
#    def arrange(self):
#        # Pack everything together
#        self.m_File.pack(side=T.LEFT)
#        self.m_View.pack(side=T.LEFT)
#
#        self.m_grip.pack(side=T.LEFT, expand=1, fill=T.BOTH)
#
#        self.m_Close.pack(side=T.RIGHT)
#        self.m_Min.pack(side=T.RIGHT)
#
#    def pack(self,*args,**kwargs):
#        # To be called by master window
#        self.frame.pack(*args,**kwargs)

#%% LEFT FRAME - MAIN CONFIG PANEL
class A_L_frame:
    """
    Panel in main window for controlling file loading and other operations
    """
    def __init__(self,master):
        self.master = master # Expect this to be main_gui instance
        self.frame = T.Frame(self.master) # This frame, where widgets will live

        # Begin by initializing an Alch instance
        self.Alch = alchClass.Alch()

        # Initialize, but do not open, browse windows
        self.dataWindow = A_LoadWindow(self,colType='exp')
        self.refWindow = A_LoadWindow(self,colType='ref')


        # Make data browse buttons
        self.lab_selectFile = T.Label(self.frame, text='Input file(s)')
        self.str_dataLoaded = T.StringVar(self.frame)
        self.lab_dataLoaded = T.Label(self.frame, textvariable=self.str_dataLoaded, width=20)
        self.but_selectFile = T.Button(self.frame, text='Load/Edit', command=self.dataWindow.Focus)
        # Reference browse button
        self.str_refLoaded = T.StringVar(self.frame)
        self.lab_refLoaded = T.Label(self.frame, textvariable=self.str_refLoaded, width=20)
        self.but_selectRef = T.Button(self.frame, text='Load/Edit', command=self.refWindow.Focus)
        # Analyze button!
        self.but_analyze = T.Button(self.frame, text='Begin analysis', command=self.analyze)

        # Finish init and arrange widget
        self.status_update()
        self.arrange()

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

    def pack(self,*args,**kwargs):
        # To be called by master window
        self.frame.pack(*args,**kwargs)

    def arrange(self):
        # Pack everything together
        self.lab_selectFile.pack(side=T.TOP)
        self.lab_dataLoaded.pack(side=T.LEFT, anchor=T.W)
        self.but_selectFile.pack(side=T.LEFT)

        self.lab_refLoaded.pack(side=T.BOTTOM,anchor=T.W)
        self.but_selectRef.pack(side=T.BOTTOM,anchor=T.E)

        self.but_analyze.pack(side=T.BOTTOM,anchor=T.W)

#%% RIGHT FRAME - LOGO, RESULTS
class A_R_frame:
    def __init__(self,master):
        self.master = master # Expect this to be main_gui instance
        self.frame = T.Frame(self.master) # This frame, where widgets will live
        #self.make_logo()
        self.arrange()

    def make_logo(self):
        # Logo in top right
        _imagefile = Image.open('lib/logo_378x100.png')
        _imagefile = _imagefile.resize((189, 50), Image.ANTIALIAS)
        _photo = ImageTk.PhotoImage(_imagefile)
        self.logo = T.Label(self.frame, image=_photo)
        self.logo.image = _photo # keep a reference!

    def pack(self,*args,**kwargs):
        # To be called by master window
        self.frame.pack(*args,**kwargs)

    def arrange(self):
        pass
        # Pack everything together
        #self.logo.pack(side=T.TOP)

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
        self.master = master
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
        self.window = T.Toplevel(self.master.master) # All the way up to root
        self.window.geometry('300x300')
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
        Vprint('Cancelling ' + self.filePath.get())
        Vprint('Revering back to ' + self.oldPath.get())
        # Discard our changes
        #self.tempPath.set(self.filePath.get())
        self.filePath.set(self.oldPath.get())
        # Hide window but preserve the object
        self.window.withdraw()
        #self.windowOpen = None

    def Reset(self):
        # Pretend this object never existed
        Vprint('Throwing it all away')
        self.filePath.set('')
        self.oldPath.set('')
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
class A_ResultWindow:
    """
    An object that manages the loading of a file, either of experimental or
    reference data.
    Methods:

    """
    def __init__(self,master):
        self.master = master # Frame containing loadWindow, Alch, etc.
        self.results = master.Alch.result_list # List of result objects
        # List of results from that Alch (may be empty)

    def make_results(self):
        # For each item in a single result

        pass

    # Method to select result from list and place that data into the GUI
    # Frame containing list of numeric results
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

    def arrange(self):
        pass
        # Place widgets into the window and pack()

#%% Execute loop
root = T.Tk()

root.iconbitmap('lib/alch_flask_icon.ico')
app = A_main(root)
root.mainloop()
