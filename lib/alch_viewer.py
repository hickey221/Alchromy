from PySide2.QtWidgets import *
from PySide2.QtGui import QIcon
import pickle


class ViewerWindow(QWidget):
    """
    TODO: How to dynamically change contents of right side?
    """
    def __init__(self):
        # Establish some window stuff
        QWidget.__init__(self)
        self.resize(800, 400)
        self.setWindowIcon(QIcon("assets/alch_flask_icon.ico"))
        # Container for loaded alch files

        # Layout definitions
        self.final_layout = QHBoxLayout()
        self.button_bar = QHBoxLayout()
        self.side_left = QVBoxLayout()
        self.size_left = QSizePolicy()
        self.side_right = QVBoxLayout()
        self.size_right = QSizePolicy()

        # Layout: Left
        self.group_left = QGroupBox('Files')
        self.side_left.addWidget(QListWidget())
        self.side_left.addLayout(self.button_bar)
        self.group_left.setLayout(self.side_left)
        self.size_left.setHorizontalStretch(0)
        self.group_left.setSizePolicy(self.size_left)
        # Layout: Right
        self.group_right = QGroupBox('Results')
        self.side_right.addWidget(QLabel('Graph'))
        self.side_right.addWidget(QLabel('Options used'))
        self.group_right.setLayout(self.side_right)
        self.size_right.setHorizontalStretch(1)
        self.group_right.setSizePolicy(self.size_right)

        # Layout: Buttons
        self.button_bar.addWidget(QPushButton('Export'))
        self.button_bar.addWidget(QPushButton('Re-run'))
        self.button_bar.addWidget(QPushButton('Remove'))

        # Add widgets
        self.split_area = QSplitter()
        self.split_area.addWidget(self.group_left)
        self.split_area.addWidget(self.group_right)
        self.split_area.setCollapsible(0, False)
        self.split_area.setCollapsible(1, False)

        # Finalize layout
        self.final_layout.addWidget(self.split_area)
        self.setLayout(self.final_layout)

    def splashScreen(self):
        """
        A placeholder for the preview pane
        :return:
        """
        pass

    def loadAlch(self):
        """
        Take in a .alch pickle file and load it into the viewer GUI
        :return:
        """
        pass

    def focusAlch(self):
        """
        Select a file from the menu and load its contents into the preview pane
        :return:
        """
        pass
