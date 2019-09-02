from PySide2.QtGui import QPalette, QColor, QBrush, QPen, QFont
from PySide2.QtCore import Qt
from PySide2.QtCharts import QtCharts


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


class DarkChart(QtCharts.QChart):
    """
    Dark themed QChart object
    """
    def __init__(self):
        QtCharts.QChart.__init__(self)
        self.setBackgroundBrush(QBrush(color=Qt.transparent))


class DarkAxis(QtCharts.QValueAxis):
    def __init__(self):
        QtCharts.QValueAxis.__init__(self)
        self.lightpen = QPen(color=Qt.green)
        self.lightbrush = QBrush(color=Qt.white)

        self.setGridLinePen(self.lightpen)
        self.setLinePen(self.lightpen)
        self.setLabelsBrush(self.lightbrush)
