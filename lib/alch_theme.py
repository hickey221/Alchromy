from PySide2.QtGui import QPalette, QColor
from PySide2.QtCore import Qt


class Darkmode(QPalette):
    def __init__(self):
        QPalette.__init__(self)
        self.setColor(QPalette.Window, QColor(53, 53, 53))
        self.setColor(QPalette.WindowText, Qt.white)
        self.setColor(QPalette.Base, QColor(25, 25, 25))
        self.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        self.setColor(QPalette.ToolTipBase, Qt.white)
        self.setColor(QPalette.ToolTipText, Qt.white)
        self.setColor(QPalette.Text, Qt.white)
        self.setColor(QPalette.Button, QColor(53, 53, 53))
        self.setColor(QPalette.ButtonText, Qt.white)
        self.setColor(QPalette.BrightText, Qt.red)
        self.setColor(QPalette.Link, QColor(42, 130, 218))
        self.setColor(QPalette.Highlight, QColor(42, 130, 218))
        self.setColor(QPalette.HighlightedText, Qt.black)

        self.setColor(QPalette.Disabled, QPalette.ButtonText, QColor(100, 100, 100))
        self.setColor(QPalette.Disabled, QPalette.WindowText, QColor(100, 100, 100))
