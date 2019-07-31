# PtQt5=5.9.2

from PyQt5.QtWidgets import *
from PyQt5.QtGui import QKeySequence, QPalette, QColor, QDesktopServices
from PyQt5.QtCore import Qt, QUrl

app = QApplication([])
app.setApplicationName("Alchromy")


#############
### THEME ###
#############

# Force the style to be the same on all OSs:
app.setStyle("Fusion")

# Now use a palette to switch to dark colors:
palette = QPalette()
palette.setColor(QPalette.Window, QColor(53, 53, 53))
palette.setColor(QPalette.WindowText, Qt.white)
palette.setColor(QPalette.Base, QColor(25, 25, 25))
palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
palette.setColor(QPalette.ToolTipBase, Qt.white)
palette.setColor(QPalette.ToolTipText, Qt.white)
palette.setColor(QPalette.Text, Qt.white)
palette.setColor(QPalette.Button, QColor(53, 53, 53))
palette.setColor(QPalette.ButtonText, Qt.white)
palette.setColor(QPalette.BrightText, Qt.red)
palette.setColor(QPalette.Link, QColor(42, 130, 218))
palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
palette.setColor(QPalette.HighlightedText, Qt.black)
app.setPalette(palette)

# Main window class from https://github.com/pyqt/examples/blob/_/src/09%20Qt%20dark%20theme/main.py
class MainWindow(QMainWindow):
    def closeEvent(self, e):
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

# Create a main window to house everything
window = MainWindow()

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

# About pane
def show_about_dialog():
    text = '<center>' \
           '<h1>Alchromy</h1>' \
           '&#8291;' \
           '<img src="alch.png", width="50">' \
           '</center>' \
           '<p>Version x.xx<br/>' \
           'Copyright &copy;2016-2019 Rich Hickey</p>'
    QMessageBox.about(window, "Alchromy v. x.xx", text)
about_action = QAction("&About")
about_action.triggered.connect(show_about_dialog)

# FAQ action
def launch_FAQ():
    QDesktopServices.openUrl(QUrl("http://www.alchromy.com/"))
FAQ_action = QAction("&FAQ")
FAQ_action.triggered.connect(launch_FAQ)

# Populate Menubars
file_menu.addAction(save_action)
file_menu.addAction(close)

tools_menu.addAction(pref_action)

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
mode_layout = QHBoxLayout()
mode_layout.addWidget(mode_box)
mode_layout.addWidget(mode_label, 1)
mode_group.setLayout(mode_layout)

#self.connect(self.command,QtCore.SIGNAL('activated(QString)'),self.optionopen)
mode_box.currentIndexChanged.connect(mode_change)

# DATA group
data_group = QGroupBox('Data')
data_layout = QHBoxLayout()
load_button = QPushButton('Load')
def load_action():
    perm_status.setText("Loading file")
    #status_bar.showMessage("Running!", 2000)
load_button.clicked.connect(load_action)
#load_button.underMouse.connect(load_action)
load_button.setToolTip("tool tip?")

data_layout.addWidget(QLabel('From file'))
data_layout.addWidget(load_button)
data_group.setLayout(data_layout)

# OPTIONS group
opt_group = QGroupBox('Options')
opt_layout = QVBoxLayout()
opt_layout.addWidget(QCheckBox('Normalize'))
opt_layout.addWidget(QCheckBox('Wavelength'))
opt_layout.addWidget(QCheckBox('Etc'))
opt_group.setLayout(opt_layout)

# Define a working button
run_button = QPushButton('Run')
def run_action():
    #temp_status.setText("Running!")
    status_bar.showMessage("Running!", 2000)
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
