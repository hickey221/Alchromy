from PySide2.QtWidgets import *
from PySide2.QtGui import QIcon
import copy
from lib import group_graph, alch_engine


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
        self.side_right = QVBoxLayout()
        self.side_splash = QVBoxLayout()

        # Widget creation
        self.graph = group_graph.Graph()

        # Layout: Left
        self.size_policy_left = QSizePolicy()
        self.group_left = QGroupBox('Files')
        self.side_left.addWidget(self.list_alch)
        self.side_left.addLayout(self.button_bar)
        self.group_left.setLayout(self.side_left)
        #self.size_policy_left.setHorizontalStretch(0)
        self.size_policy_left.setHorizontalPolicy(QSizePolicy.Maximum)
        #self.group_left.setSizePolicy(self.size_policy_left)

        # Layout: Right (functional)
        self.size_policy_right = QSizePolicy()
        self.stacked_right = QStackedWidget()
        self.r2value = QLabel('R squared goes here')
        self.group_right = QGroupBox('Results')
        self.side_right.addWidget(QLabel('Graph'), 0)
        self.side_right.addWidget(self.graph, 1)
        self.side_right.addWidget(QLabel('Options used'), 0)
        self.side_right.addWidget(self.r2value, 0)
        self.group_right.setLayout(self.side_right)
        #self.size_policy_right.setHorizontalStretch(1)
        #self.size_policy_right.setHorizontalPolicy(QSizePolicy.Maximum)
        #self.group_right.setSizePolicy(self.size_policy_right)

        # Layout: Right (Splash screen)
        self.group_splash = QGroupBox('Results')
        self.side_splash.addWidget(QLabel('Select a result from the list to view'))
        self.group_splash.setLayout(self.side_splash)
        #self.group_splash.setSizePolicy(self.size_policy_right)

        # Layout: Buttons
        self.button_import = QPushButton('Import')
        self.button_import.clicked.connect(self.import_alch)

        self.button_remove = QPushButton('Remove')
        self.button_remove.clicked.connect(self.remove)

        self.button_export = QPushButton('Export')
        self.button_export.clicked.connect(self.export)

        # self.button_bar.addWidget(QPushButton('Re-run'))
        self.button_bar.addWidget(self.button_import)
        self.button_bar.addWidget(self.button_export)
        self.button_bar.addWidget(self.button_remove)

        # Add widgets
        self.stacked_right.addWidget(self.group_splash)
        self.stacked_right.addWidget(self.group_right)
        self.split_area = QSplitter()
        self.split_area.addWidget(self.group_left)
        self.split_area.addWidget(self.stacked_right)

        # Set size policies now that widgets are placed
        self.split_area.setCollapsible(0, True)
        self.split_area.setCollapsible(1, False)
        self.split_area.setSizes([100, 400])
        self.split_area.setStretchFactor(0, 0)
        self.split_area.setStretchFactor(1, 1)
        self.group_left.setSizePolicy(self.size_policy_left)
        self.group_right.setSizePolicy(self.size_policy_right)
        self.group_splash.setSizePolicy(self.size_policy_right)

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
        self.stacked_right.setCurrentWidget(self.group_splash)

    def load_alch(self, alch):
        """
        Take in an alch OBJECT and import it to the list of active objects
        """
        # Use deep copy because this one may be changed
        # print(f"Making a (deep) copy of {type(alch)}")
        self.alchs.append(copy.deepcopy(alch))
        self.updateList()

        # Focus on latest addition to list
        new_idx = self.list_alch.count()-1
        self.list_alch.setCurrentRow(new_idx)
        self.focusAlch()
        self.list_alch.item(new_idx).setSelected(True)
        self.list_alch.setFocus()

    def updateList(self):
        self.list_alch.clear()
        for a in self.alchs:
            self.list_alch.addItem(a.metadata['name'])
        # Temp: Also call the graph save function

    def remove(self):
        """
        Get rid of the currently selected alch
        :return:
        """
        # Remove from list of alchs
        self.alchs.pop(self.idx)
        # Remove from list widget
        self.list_alch.takeItem(self.idx)

        # Adjust index if we were in the last position
        if self.idx >= self.list_alch.count():
            self.idx = self.list_alch.count() - 1
        if self.idx < 0:
            # Must have deleted last item
            self.showSplashScreen()
            return
        # Change focus
        self.focusAlch()

    def import_alch(self):
        """
        Browse for a .alch file and load it into the current workflow
        TODO: How to handle duplicate names?
        :return:
        """
        file_name = QFileDialog.getOpenFileName(self, 'Open File', '.', '(*.alch)')
        if not file_name[0]:
            # Abort if user cancelled the dialog
            return
        # Create alch object from file
        new_alch = alch_engine.import_from_json(file_name[0])
        # Add it to the viewer through the traditional method
        self.load_alch(new_alch)

    def export(self):
        """
        Grab the currently selected alch and send it to be turned into a file
        :return:
        """
        print(f"Taking name of index position {self.idx}: {self.alchs[self.idx].metadata['name']}")
        default_name = self.alchs[self.idx].metadata['name']
        file_name = QFileDialog.getSaveFileName(self, 'Export File', default_name, '(*.alch)')
        if not file_name[0]:
            # Abort if user cancelled the dialog
            return
        alch_engine.export_to_json(self.alchs[self.idx], file_name[0])

    def focusAlch(self, i=None):
        """
        Select a file from the menu and load its contents into the preview pane
        TODO: Add filename (if imported), all options selected,
        :return:
        """
        if type(i) is not int:
            # Convert index 'event' to an integer
            i = self.list_alch.currentRow()

        # Track index for navigating other lists
        self.idx = i

        # Load up results from the selected alch
        self.r2value.setText(str(self.alchs[i].r2))
        self.stacked_right.setCurrentWidget(self.group_right)

        # Load alch result into the RHS
        self.graph.setModel(self.alchs[i].result_df)
