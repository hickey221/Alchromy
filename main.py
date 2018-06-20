# -*- coding: utf-8 -*-
'''
Created on Mon Jun 18 09:11:28 2018

@author: hickey.221
'''

import tkinter as T
from themes import * # For dict solarized
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk

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
        #self.master.overrideredirect(True) # removes titlebar
        
        # Make frames and pack them
        #self.menuFrame = A_Menu(self.master)
        self.leftFrame = A_L_frame(self.master)
        self.rightFrame = A_R_frame(self.master)
        
        self.arrange()

    def arrange(self):
        #self.menuFrame.pack(side=T.TOP)
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

"""
class A_Menu:
    def __init__(self, master):
        self.master = master
        self.frame = T.Frame(self.master)
        self.m_File = T.Label(self.frame, text='File')
        self.m_View = T.Label(self.frame, text='View')
        
        self.m_Min = T.Button(self.frame, text='Min',command=self.Min)
        self.m_Close = T.Button(self.frame, text='X',command=self.Close)
        
        self.arrange()
        
    def Min(self):
        self.master.iconify()
        
    def Max(self):
        self.master.destroy()
        
    def Close(self):
        self.master.destroy()
        
    def arrange(self):
        # Pack everything together
        self.m_File.pack(side=T.LEFT)
        self.m_View.pack(side=T.LEFT)
        
        self.m_Close.pack(side=T.RIGHT)
        self.m_Min.pack(side=T.RIGHT)

    def pack(self,*args,**kwargs):
        # To be called by master window
        self.frame.pack(*args,**kwargs)
        self.configure(background='yellow')
"""     
#%% LEFT FRAME - MAIN CONFIG PANEL
class A_L_frame:
    def __init__(self,master):
        self.master = master # Expect this to be main_gui instance
        self.frame = T.Frame(self.master) # This frame, where widgets will live
        self.fileWindow = a_load_file_dialog(self) # Initialize but do not open

        self.lab_selectFile = T.Label(self.frame, text='Input file(s)')
        self.lab_status = T.Label(self.frame, textvariable=self.fileWindow.filePath)
        self.but_selectFile = T.Button(self.frame, text='Load data file', command=self.fileWindow.Focus)  
        self.arrange()
        
    def pack(self,*args,**kwargs):
        # To be called by master window
        self.frame.pack(*args,**kwargs)
    
    def arrange(self):
        # Pack everything together
        self.lab_selectFile.pack()
        self.but_selectFile.pack()
        self.lab_status.pack()

#%% RIGHT FRAME - LOGO, RESULTS
class A_R_frame:
    def __init__(self,master):
        self.master = master # Expect this to be main_gui instance
        self.frame = T.Frame(self.master) # This frame, where widgets will live
        self.make_logo()
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
        # Pack everything together
        self.logo.pack(side=T.TOP)

#%% NEW WINDOW FOR LOADING DATA
class a_load_file_dialog:
    def __init__(self,master):
        self.master = master.master
        self.filePath = T.StringVar(value='')
        self.tempPath = T.StringVar() # Goes into filePath when using Save()
        self.windowOpen = None # Object starts without a window
    
    def Open(self):
        # The rest of the initialization procedure, opening the window
        self.window = T.Toplevel(self.master)
        self.make_frames() # Gives topFrame, midFrame, botFrame
        
        self.topInfo = T.Label(self.topFrame, text='Upload your data file here')
        self.ent_file = T.Entry(self.topFrame, textvariable=self.tempPath)
        self.but_file = T.Button(self.topFrame, text='Browse',command=self.Browse)
        
        self.listItems = T.Listbox(self.midFrame)
        
        self.but_reset = T.Button(self.botFrame, text='Reset', command=self.Reset)
        self.but_cancel = T.Button(self.botFrame, text='Cancel', command=self.Cancel)
        self.but_save = T.Button(self.botFrame, text='Save', command=self.Save)
        self.arrange()
        
        # Set window status and close procedure
        self.window.protocol('WM_DELETE_WINDOW', self.Cancel) # Hit X = cancel
        self.windowOpen = True # Window officially exists now
    
    def Browse(self):
        newPath = filedialog.askopenfilename(parent = self.window,filetypes=[('Data file','*.xls *.csv *.dat'),('All files','*.*')])
        if newPath:
            self.tempPath.set(newPath)
        else:
            print('Nothing chosen, nothing saved')
        self.ent_file.xview_moveto(1)
    
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
        self.window.destroy()
        
    def Save(self):
        print('Saving ' + self.tempPath.get())
        self.filePath.set(self.tempPath.get())
        self.window.withdraw()
        
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
app = A_main(root)
root.mainloop()