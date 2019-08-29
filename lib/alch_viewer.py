from PySide2.QtWidgets import *
from PySide2.QtGui import QIcon
import pickle, copy


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
        self.alchs = []
        self.list_alch = QListWidget()
        self.list_alch.clicked.connect(self.focusAlch)
        self.idx = 0

        # Layout definitions
        self.final_layout = QHBoxLayout()
        self.button_bar = QHBoxLayout()
        self.side_left = QVBoxLayout()
        self.size_left = QSizePolicy()
        self.side_right = QVBoxLayout()
        self.size_right = QSizePolicy()
        self.side_splash = QVBoxLayout()

        # Layout: Left
        self.group_left = QGroupBox('Files')
        self.side_left.addWidget(self.list_alch)
        self.side_left.addLayout(self.button_bar)
        self.group_left.setLayout(self.side_left)
        self.size_left.setHorizontalStretch(0)
        self.group_left.setSizePolicy(self.size_left)
        # Layout: Right
        self.r2value = QLabel('R squared goes here')
        self.group_right = QGroupBox('Results')
        self.side_right.addWidget(QLabel('Graph'))
        self.side_right.addWidget(QLabel('Options used'))
        self.side_right.addWidget(self.r2value)
        self.group_right.setLayout(self.side_right)
        self.size_right.setHorizontalStretch(1)
        self.group_right.setSizePolicy(self.size_right)

        # Layout: Buttons
        self.button_bar.addWidget(QPushButton('Export'))
        self.button_bar.addWidget(QPushButton('Re-run'))
        self.button_bar.addWidget(QPushButton('Remove'))

        # Splash screen
        self.group_splash = QGroupBox('Splash')
        self.side_splash.addWidget(QLabel('Alchromy'))
        self.group_splash.setLayout(self.side_splash)

        # Add widgets
        self.split_area = QSplitter()
        self.split_area.addWidget(self.group_left)
        self.split_area.addWidget(self.group_right)
        self.split_area.setCollapsible(0, False)
        self.split_area.setCollapsible(1, False)
        # Finalize layout
        self.final_layout.addWidget(self.split_area)
        self.setLayout(self.final_layout)
        # Start empty
        self.showSplashScreen()

    def showSplashScreen(self):
        """
        A placeholder for the preview pane
        :return:
        """
        self.split_area.replaceWidget(1, self.group_splash)

    def loadAlch(self, alch):
        """
        Take in a .alch pickle file and load it into the viewer GUI
        :return:
        """
        # Use deep copy because this one may be changed
        self.alchs.append(copy.deepcopy(alch))
        self.updateList()
        # Focus on latest addition to list
        new_idx = self.list_alch.count()-1
        print("Want to select", new_idx)
        self.list_alch.setCurrentRow(new_idx)
        self.focusAlch()
        print("At index:", self.list_alch.item(new_idx))
        print("Current:", self.list_alch.currentItem())
        self.list_alch.item(new_idx).setSelected(True)
        self.list_alch.setFocus()
        #self.focusAlch(self.list_alch.count())

    def updateList(self):
        self.list_alch.clear()
        for a in self.alchs:
            self.list_alch.addItem(a.name)

    def focusAlch(self, i=None):
        """
        Select a file from the menu and load its contents into the preview pane
        :return:
        """
        # Change labels to reflect current alch's results
        i = self.list_alch.currentRow()
        #if i is None:
        #    i = self.list_alch.currentRow()
        print("Focusing on item", i)
        self.r2value.setText(str(self.alchs[i].r2))
        self.split_area.replaceWidget(1, self.group_right)
