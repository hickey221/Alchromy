from PySide2.QtWidgets import *


class StatusBar(QStatusBar):
    def __init__(self, parent, log):
        QStatusBar.__init__(self)
        self.parent = parent
        self.statusLog = log
        temp_status = QLabel("")
        bar_space = QLabel("")
        self.addWidget(temp_status)
        self.addWidget(bar_space, 1)
        self.addPermanentWidget(self.statusLog)

