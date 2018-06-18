# -*- coding: utf-8 -*-
"""
Created on Mon Jun 18 09:11:28 2018

@author: hickey.221
"""

import tkinter as T
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk

#%% Title, initialization and menubar
root = T.Tk()
root.title('Alchromy - Spectral Deconvolution')
topFrame = T.Frame(root)
mainFrame = T.Frame(root)

versionNumber = "1.3.0"
#%% "About" dialog box
def aboutBox():
    messagebox.showinfo("Alchromy","Alchromy Spectral Deconvolution\nwww.Alchromy.com\nVersion "+versionNumber+"\nRichard Hickey\nOhio State University\n2018")

# Logo in top right
_imagefile = Image.open("lib/logo_378x100.png")
_imagefile = _imagefile.resize((189, 50), Image.ANTIALIAS)
_photo = ImageTk.PhotoImage(_imagefile)
logo = T.Label(topFrame, image=_photo)
logo.image = _photo # keep a reference!


# make the top right close button close the main window
root.protocol("WM_DELETE_WINDOW", root.destroy)

# create a menu bar with an Exit command
menubar = T.Menu(root)
filemenu = T.Menu(menubar, tearoff=0)
filemenu.add_command(label="Exit", command=root.destroy)
menubar.add_cascade(label="File", menu=filemenu)

aboutmenu = T.Menu(menubar, tearoff=0)
aboutmenu.add_command(label="About",command=aboutBox)
menubar.add_cascade(label="Help", menu=aboutmenu)
root.config(menu=menubar)

#%% Input file area
lab_selectFile = T.Label(mainFrame, text="Input file(s)")
but_selectFile = T.Button(mainFrame,text="Browse")
rad_selectFileile = T.Radiobutton(mainFrame,text="Select File",value=1)

#enterFile = T.Entry(f1, textvariable=filePath)
#enterFile.grid(row=1, column=1, sticky="w")
#buttonBrowseFile = T.Button(f1,text="Browse",command=browseForFile)
#buttonBrowseFile.grid(row=1,column=2)

##################################################
#                     PACKING                    #
##################################################
#%% Pack FRAMES
topFrame.pack(side=T.TOP, fill=T.X)
mainFrame.pack(side=T.BOTTOM,fill=T.BOTH)


#%% Pack CONTENTS of top frame
logo.pack(side=T.RIGHT)



#%% Pack CONTENTS of main frame
lab_selectFile.pack(side=T.LEFT)
but_selectFile.pack()



#%% Execute loop
root.mainloop()