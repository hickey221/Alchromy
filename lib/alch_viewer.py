from PySide2.QtWidgets import *
from PySide2.QtCore import Qt
from PySide2.QtGui import QIcon

from lib import alch_import
from lib import alch_graph


class ViewerWindow(QWidget):
    def __init__(self):
        # Establish some window stuff
        QWidget.__init__(self)
        self.resize(800, 400)
        self.setWindowIcon(QIcon("assets/alch_flask_icon.ico"))

        # Construct layout
        self.final_layout = QHBoxLayout()
        self.side_left = QVBoxLayout()
        self.side_right = QVBoxLayout()
        self.bottom_button_bar = QHBoxLayout()

        # Add widgets
        self.side_left.addWidget(QListWidget(), 0)
        self.side_right.addWidget(QLabel('Graph'))
        self.side_right.addWidget(QLabel('Options'))

        # Finalize layout
        self.final_layout.addLayout(self.side_left)
        self.final_layout.addLayout(self.side_right)
        self.setLayout(self.final_layout)