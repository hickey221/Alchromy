# PyQt5==5.9.2

import sys
from PySide2.QtCore import QCoreApplication
from PySide2.QtWidgets import QApplication

# Internal imports
from lib import alch_main_window, alch_theme

app = QCoreApplication.instance()
if app is None:
    app = QApplication(sys.argv)
app.setApplicationName("Alchromy")
# Force the style to be the same on all OSs:
app.setStyle("Fusion")
# Now use a palette to switch to dark colors:
darkmode = alch_theme.Darkmode()
app.setPalette(darkmode)
# Force the style to be the same on all OSs:
app.setStyle("Fusion")
# Create a main window to house everything
window = alch_main_window.MainWindow()

# Execute Qt
window.show()
app.exec_()
