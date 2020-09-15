# PyQt5==5.9.2
"""
Todo list:
GENERAL:
[ ] Handle .alch as an input
[ ] Re-add kinetic run
[ ] Track results as a dict of { species: (amt, err) }
[ ] Allow choice of folder to save results
[ ] Save run as pickle/JSON
[ ] Load saved results (.alch file)

VIEWER:
[ ] Fix colors
[ ] Print results from dict (above)
[ ] ALlow for turning on/off original data vs fit
[ ] Export image as seen in app
"""
import sys
from PySide2.QtCore import QCoreApplication
from PySide2.QtWidgets import QApplication

# Internal imports
from lib import window_main, alch_theme

app = QCoreApplication.instance()
if app is None:
    app = QApplication(sys.argv)
app.setApplicationName("Alchromy")
# Force the style to be the same on all OSs:
app.setStyle("Fusion")
# Now use a palette to switch to dark colors:
darkmode = alch_theme.Darkmode()
#app.setPalette(darkmode)
# Force the style to be the same on all OSs:
app.setStyle("Fusion")
# Create a main window to house everything
window = window_main.MainWindow()

# Execute Qt
window.show()
app.exec_()
