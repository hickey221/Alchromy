# PyQt5==5.9.2

import sys
from PyQt5.QtWidgets import *
#QWidget,QCheckBox,QComboBox,QCommandLinkButton,QDateEdit,QDateTimeEdit,QTimeEdit,QDial,QFocusFrame,QFontComboBox,QLabel,QLCDNumber,QLineEdit,QMenu,QProgressBar,QPushButton,QRadioButton,QScrollArea,QScrollBar,QSizeGrip,QSlider,QDoubleSpinBox,QSpinBox
from PyQt5.QtGui import QKeySequence, QPalette, QColor, QDesktopServices, QWindow, QIcon
#from PyQt5.QtChart import *
from PyQt5.QtCore import Qt, QUrl, QCoreApplication
# For plot test
import pandas as pd

filePath = "test_3.dat"
#app = QApplication([])
app = QCoreApplication.instance()
if app is None:
    app = QApplication(sys.argv)
app.setApplicationName("Alchromy")


#############
### THEME ###
#############

# Force the style to be the same on all OSs:
app.setStyle("Fusion")

# Now use a palette to switch to dark colors:

lightmode = QPalette()
darkmode = QPalette()

darkmode.setColor(QPalette.Window, QColor(53, 53, 53))
darkmode.setColor(QPalette.WindowText, Qt.white)
darkmode.setColor(QPalette.Base, QColor(25, 25, 25))
darkmode.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
darkmode.setColor(QPalette.ToolTipBase, Qt.white)
darkmode.setColor(QPalette.ToolTipText, Qt.white)
darkmode.setColor(QPalette.Text, Qt.white)
darkmode.setColor(QPalette.Button, QColor(53, 53, 53))
darkmode.setColor(QPalette.ButtonText, Qt.white)
darkmode.setColor(QPalette.BrightText, Qt.red)
darkmode.setColor(QPalette.Link, QColor(42, 130, 218))
darkmode.setColor(QPalette.Highlight, QColor(42, 130, 218))
darkmode.setColor(QPalette.HighlightedText, Qt.black)

darkmode.setColor(QPalette.Disabled, QPalette.ButtonText, QColor(100, 100, 100))

app.setPalette(darkmode)

# Main window class from https://github.com/pyqt/examples/blob/_/src/09%20Qt%20dark%20theme/main.py
class MainWindow(QMainWindow):
    def closeEvent(self, e):
        return
        if not text.document().isModified():
            return
        answer = QMessageBox.question(
            window, None,
            "You have unsaved changes. Save before closing?",
            QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel
        )
        if answer & QMessageBox.Save:
            save()
        elif answer & QMessageBox.Cancel:
            e.ignore()

#class LoadWindow(QWindow):
    #def __init__(self):
        #self.raise()
        
    

# Create a main window to house everything
window = QMainWindow()
window.setWindowIcon(QIcon("lib/alch_flask_icon.ico"))

###############
### MENUBAR ###
###############

# Declare menubars
file_menu = window.menuBar().addMenu("&File")
tools_menu = window.menuBar().addMenu("&Tools")
help_menu = window.menuBar().addMenu("&Help")

# Declare status bar
status_bar = QStatusBar()
temp_status = QLabel("")
bar_space = QLabel("")
perm_status = QLabel("Initialized")

status_bar.addWidget(temp_status)
status_bar.addWidget(bar_space, 1)
status_bar.addPermanentWidget(perm_status)

# Save function
file_path = None
save_action = QAction("&Save")

def save():
    pass
    """
    if file_path is None:
        save_as()
    else:
        with open(file_path, "w") as f:
            f.write(text.toPlainText())
        text.document().setModified(False)
    """
save_action.triggered.connect(save)
save_action.setShortcut(QKeySequence.Save)

# Close function

close = QAction("&Close")
close.triggered.connect(window.close)

# Preferences
pref_action = QAction("&Preferences")

# Debug setting
debug_action = QAction(text='&Debug mode', checkable=True, checked=False)

def changetheme():
    app.setPalette(lightmode)
    window.repaint()
    
theme_action = QAction(text='&Theme', checkable=True, checked=False)
theme_action.triggered.connect(changetheme)

# About pane
def show_about_dialog():
    text = '<center>' \
           '<h1>Alchromy</h1>' \
           '&#8291;' \
           '</center>' \
           '<p>Version x.xx<br/>' \
           'Copyright &copy; 2016-2019 Rich Hickey</p>'
    QMessageBox.about(window, "Alchromy v. x.xx", text)
about_action = QAction("&About")
about_action.triggered.connect(show_about_dialog)

           #'<img src="lib/alch_flask_icon.gif", width="50">' \
           
# FAQ action
def launch_FAQ():
    QDesktopServices.openUrl(QUrl("http://www.alchromy.com/"))
FAQ_action = QAction("&FAQ")
FAQ_action.triggered.connect(launch_FAQ)


# Populate Menubars
file_menu.addAction(save_action)
file_menu.addAction(close)

tools_menu.addAction(pref_action)
tools_menu.addAction(debug_action)
#tools_menu.addAction(theme_action)

help_menu.addAction(FAQ_action)
help_menu.addAction(about_action)


####################
### MAIN CONTENT ###
####################

def sendMsg():
    status_bar.showMessage("Msg")

# Most stuff goes in our content area (central widget)
content = QWidget()
window.setCentralWidget(content)
window.setStatusBar(status_bar)

# MODE group
mode_group = QGroupBox('Mode')

mode_list = ("Simple",
             "Replicate",
             "Kinetic")
mode_desc = ("Analyze one spectrum at a time, or a batch of several spectra separately.",
             "Average multiple spectra and analyze as one.",
             "Treat multiple spectra as time course data.")
mode_box = QComboBox()
mode_label = QLabel(mode_desc[0])
def mode_change():
    # Get the appropriate description of the selected mode
    mode_label.setText(mode_desc[mode_box.currentIndex()])

mode_box.addItems(mode_list)
mode_box.setStatusTip("Change the operation mode.")
mode_layout = QHBoxLayout()
mode_layout.addWidget(mode_box)
mode_layout.addWidget(mode_label, 1)
mode_group.setLayout(mode_layout)

#self.connect(self.command,QtCore.SIGNAL('activated(QString)'),self.optionopen)
mode_box.currentIndexChanged.connect(mode_change)

##### Load window #####

load_window = QWidget()
load_layout = QVBoxLayout()
load_layout.addWidget(QLabel('Load window screen'))
load_layout.addWidget(QListWidget())
#prev_chart = QChartView()
load_window.setLayout(load_layout)

#######################



# DATA group
data_group = QGroupBox('Data')
data_layout = QVBoxLayout()
load_line_layout = QHBoxLayout()
paste_line_layout = QHBoxLayout()

def load_action():
    perm_status.setText("Loading file")
    # TEMPORARY LOAD & PLOT TEST
    df = pd.read_csv(filePath,'\t')
    df.rename(columns={df.columns[0]:'nm'}, inplace=True)
    dataCols = list(df.drop('nm',axis=1))
    load_window.show()
    
load_button = QPushButton('Load')
load_button.clicked.connect(load_action)


def switchToLoad():
    load_button.setEnabled(True)
    paste_button.setDisabled(True)
    
def switchToPaste():
    paste_button.setEnabled(True)
    load_button.setDisabled(True)
    #load_button.setPalette(QPalette.Text, Qt.red)
    

load_file_radio = QRadioButton('From file', checked=True)
load_file_radio.clicked.connect(switchToLoad)
load_file_radio.setStatusTip("Load spectra from a data file.")

load_line_layout.addWidget(load_file_radio)
load_line_layout.addWidget(load_button)

##### Paste window #####

paste_window = QWidget()
paste_layout = QVBoxLayout()
paste_layout.addWidget(QLabel("Must be whitespace delimited"))
paste_layout.addWidget(QTextEdit())
paste_window.setLayout(paste_layout)

def paste_action():
    perm_status.setText("Paste in data")
    paste_window.show()
#######################

paste_button = QPushButton('Input', enabled=False)
paste_button.clicked.connect(paste_action)

paste_data_radio = QRadioButton('Paste data')
paste_data_radio.setStatusTip("Load spectra from copy/pasted data.")
paste_data_radio.clicked.connect(switchToPaste)

paste_line_layout.addWidget(paste_data_radio)
paste_line_layout.addWidget(paste_button)

data_layout.addLayout(load_line_layout)
data_layout.addLayout(paste_line_layout)

data_group.setLayout(data_layout)



# OPTIONS group
opt_group = QGroupBox('Options')
opt_layout = QVBoxLayout()
norm_box = QCheckBox('Normalize')
norm_box.setStatusTip('Force minimum absorbance of spectra to 0 by subtraction.')
wave_box = QCheckBox('Manual wavelength')
wave_box.setStatusTip('Specify custom wavelengths for measurement.')
opt_layout.addWidget(norm_box)
opt_layout.addWidget(wave_box)
opt_layout.addWidget(QCheckBox('Etc'))
opt_group.setLayout(opt_layout)

# Define a working button
run_button = QPushButton('Run')
run_button.setStatusTip('Begin analysis with selected settings.')
def run_action():
    perm_status.setText("Running!")
    #status_bar.showMessage("Running!", 2000)
run_button.clicked.connect(run_action)


#######################
### LAYOUT ASSEMBLY ###
#######################

# Assemble layout
V_layout = QVBoxLayout()
V_layout.addWidget(mode_group)
V_layout.addWidget(data_group)
V_layout.addWidget(opt_group)
V_layout.addWidget(run_button)
content.setLayout(V_layout)

# Execute Qt
window.show()
app.exec_()

# Alchromy to-do
# Change forced "evens only" to find only common wavelength index points and use those
# Make main dashboard more minimal
# Allow for pasted simple data
