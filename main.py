# -*- coding: utf-8 -*-
'''
Created on Mon Jun 18 09:11:28 2018

@author: hickey.221
'''
# Standard imports
import tkinter as T
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
from warnings import warn
# Custom imports
from themes import * # For dict solarized
import alchClass

global versionNumber
versionNumber = '1.5.0'
global selectedTheme


def set_theme(frame, mode):
    if mode=='light':
        frame.tk_setPalette(background=solarized['lightbg1'], foreground=solarized['lighttext1'],
               activeBackground=solarized['lightbg2'], activeForeground=solarized['lighttext2'])
        selectedTheme = 'light'
    elif mode == 'dark':
        frame.tk_setPalette(background=solarized['darkbg1'], foreground=solarized['darktext1'],
               activeBackground=solarized['darkbg2'], activeForeground=solarized['darktext2'])
        selectedTheme = 'dark'
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
    def __init__(self,master):
        self.master = master # Expect this to be main_gui instance
        self.frame = T.Frame(self.master) # This frame, where widgets will live
        self.fileWindow = a_load_file_dialog(self) # Initialize but do not open
        self.refWindow = a_load_file_dialog(self) # Initialize but do not open

        self.Alch = alchClass.Alch() # Initialize an Alch instance

        self.lab_selectFile = T.Label(self.frame, text='Input file(s)')
        self.str_dataLoaded = T.StringVar(self.frame)
        self.lab_dataLoaded = T.Label(self.frame, textvariable=self.str_dataLoaded, width=20)
        self.but_selectFile = T.Button(self.frame, text='Load/Edit', command=self.get_data)  
        
        # TODO: Need a way of determining whether we're getting exp or ref data
        self.str_refLoaded = T.StringVar(self.frame)
        self.lab_refLoaded = T.Label(self.frame, textvariable=self.str_refLoaded, width=20)
        self.but_selectRef = T.Button(self.frame, text='Load/Edit', command=self.get_ref)  

        self.status_update()
        self.arrange()

    def get_data(self):
        # Pop up window and allow for file loading
        self.fileWindow.Focus() 
        # Assign local variable to whatever ended up in the file browse window
        # TODO: Figure out where to save this
        # TODO: Save actual columns to the Alch, not just the file path
        filePath = self.fileWindow.filePath.get()
        #self.status_update() # moved to Save()
         
    def get_ref(self):
        # Pop up window and allow for file loading
        self.refWindow.Focus() 
        # Assign local variable to whatever ended up in the file browse window
        # TODO: Figure out where to save this
        # TODO: Save actual columns to the Alch, not just the file path
        refPath = self.refWindow.filePath.get()
        #self.status_update() # moved to Save()

    
    def status_update(self):
        print('Updating status')
        # Check if data file has been locked in
        if self.fileWindow.filePath.get():
            self.str_dataLoaded.set('Data file loaded')
            self.lab_dataLoaded.config(bg='green')
        else:
            self.str_dataLoaded.set('Data not loaded')
            self.lab_dataLoaded.config(bg='red')
        # Check for reference
        if self.fileWindow.refPath.get():
            self.str_refLoaded.set('Reference file loaded')
            self.lab_refLoaded.config(bg='green')
        else:
            self.str_refLoaded.set('Reference not loaded')
            self.lab_refLoaded.config(bg='red')
        #self.lab_dataLoaded.update()
    
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
class a_load_file_dialog:
    def __init__(self,master):
        # Initialize bare minimum, wait for Open() to be called to do the rest
        self.master = master
        self.filePath = T.StringVar(value='')
        self.refPath = T.StringVar(value='')
        self.tempPath = T.StringVar() # Goes into filePath when using Save()
        self.windowOpen = None # Object starts without a window

    def Open(self):
        # The rest of the initialization procedure, opening the window
        self.window = T.Toplevel(self.master.master) # All the way up to root
        self.window.geometry('300x300')
        self.make_frames() # Gives topFrame, midFrame, botFrame

        self.topInfo = T.Label(self.topFrame, text='Upload your data file here')
        self.ent_file = T.Entry(self.topFrame, textvariable=self.tempPath)
        self.but_file = T.Button(self.topFrame, text='Browse',command=self.Browse)

        self.listItems = T.Listbox(self.midFrame,selectmode='multiple')

        self.but_reset = T.Button(self.botFrame, text='Reset', command=self.Reset)
        self.but_cancel = T.Button(self.botFrame, text='Cancel', command=self.Cancel)
        self.but_save = T.Button(self.botFrame, text='Save', command=self.Save)
        self.arrange()

        # Set window status and close procedure
        self.window.protocol('WM_DELETE_WINDOW', self.Cancel) # X = Cancel()
        self.windowOpen = True # Window officially exists now

    def Browse(self):
        # Open file browse dialog
        newPath = filedialog.askopenfilename(parent = self.window,filetypes=[('Data file','*.xls *.csv *.dat'),('All files','*.*')])
        if not newPath:
            print('Nothing chosen, nothing saved')
            return None
        # If we have a new file...
        try:
            ## Read in data file using existing Alch instance
            self.master.Alch.load_exp(newPath)
            # TODO: What if we don't want to keep this one and cancel later? 
            self.tempPath.set(newPath)
            self.ent_file.xview_moveto(1)
        except:
            warn('Error between Browse()-load_exp()')
        print('Received '+str(len(self.master.Alch.dataCols))+' cols from Browse()')
        try:
            # Clear listbox if not empty
            if self.listItems.size() > 0:
                print('Clearing listbox')
                self.listItems.delete(0,T.END)
            # Repopulate with data col names from Alch
            for l in self.master.Alch.dataCols:
                self.listItems.insert(T.END, l) # Grab all colnames
                self.listItems.select_set(0, T.END) # Select all by default
        except:
            warn('Something went wrong populating column list')

    def Cancel(self):
        print('Cancelling ' + self.tempPath.get())
        print('Revering back to ' + self.filePath.get())
        # Discard our changes
        self.tempPath.set(self.filePath.get())
        # Hide window but preserve the object
        self.window.withdraw()
        #self.windowOpen = None

    def Reset(self):
        # Pretend this object never existed
        print('Throwing it all away')
        self.filePath.set('')
        self.tempPath.set('')
        self.windowOpen = None
        self.master.status_update()
        self.window.destroy()

    def Save(self):
        # Commit changes back to the master
        # TODO: Need a way of determining whether we're getting exp or ref data
        # Maybe return data, instead of modifying master?
        print('Saving ' + self.tempPath.get())
        self.filePath.set(self.tempPath.get())
        self.master.status_update() 
        self.window.withdraw()
        return self.tempPath.get()

    def Focus(self):
        if self.windowOpen:
            # If we already have one open, raise it
            try:
                self.window.deiconify()
                print('Used deiconify()')
            except:
                self.window.lift()    
                print('Used lift()')
        else:
            # Else, create a new one
            print('Making a new window!')
            self.Open()
        self.ent_file.xview_moveto(1)

    def make_frames(self):
        self.topFrame = T.Frame(self.window)
        self.midFrame = T.Frame(self.window)
        self.botFrame = T.Frame(self.window)

        self.topFrame.pack(side=T.TOP, fill=T.X)
        self.midFrame.pack(side=T.TOP, fill=T.BOTH)
        self.botFrame.pack(side=T.BOTTOM, fill=T.X)

    def arrange(self):
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

#%% Execute loop
root = T.Tk()

root.iconbitmap('lib/alch_flask_icon.ico')
app = A_main(root)
root.mainloop()