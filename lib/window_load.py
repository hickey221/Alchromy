from PySide2.QtWidgets import *
from PySide2.QtCore import Qt
from PySide2.QtGui import QIcon

from lib import read_data_file
from lib import group_graph
import os


class LoadWindow(QWidget):
    # Todo: Allow for name specification, with default being filename
    def __init__(self):
        # Establish some window stuff
        QWidget.__init__(self)
        self.resize(800, 400)
        self.df = None
        self.name = None
        self.file_path = None
        self.setWindowIcon(QIcon("assets/alch_flask_icon.ico"))
        # Modal setting = this window has focus over MainWindow when shown
        self.setWindowModality(Qt.ApplicationModal)
        # Make some widgets
        self.graph = group_graph.Graph()
        self.waves_list = QListWidget()
        self.waves_list.itemChanged.connect(self.update_wave_list)
        # self.load_label = QLabel('Load window screen')

        # Browse button & action
        self.browse_button = QPushButton('Select file')
        self.browse_button.clicked.connect(self.browse_button_action)

        # Browse button & action
        self.check_button = QPushButton('Check/uncheck all')
        self.check_button.clicked.connect(self.check_button_action)

        self.box_name = QLineEdit('')
        self.box_name.setFixedWidth(200)

        self.button_save = QPushButton('Save')
        self.button_save.clicked.connect(self.button_save_action)

        # Construct layout
        self.layout = QVBoxLayout()
        top_button_bar = QHBoxLayout()
        graph_bar = QHBoxLayout()
        bottom_button_bar = QHBoxLayout()

        # First row: Load buttons
        # top_button_bar.addWidget(self.load_label, stretch=0)
        top_button_bar.addWidget(self.browse_button, stretch=0)
        top_button_bar.addWidget(QLabel(''), 1)  # Spacer
        # Second row: wave list and graph plot
        graph_bar.addWidget(self.waves_list)
        # self.waves_list.clicked.connect(self.make_wave_list)
        graph_bar.addWidget(self.graph, stretch=1)
        # Third row: Save button
        bottom_button_bar.addWidget(self.check_button, stretch=0)
        bottom_button_bar.addWidget(QLabel(''), 1)  # Spacer
        bottom_button_bar.addWidget(QLabel('Run name:'))
        bottom_button_bar.addWidget(self.box_name)
        bottom_button_bar.addWidget(self.button_save)

        # Assemble the layout and apply it
        self.layout.addLayout(top_button_bar)
        self.layout.addLayout(graph_bar)
        self.layout.addLayout(bottom_button_bar)
        self.setLayout(self.layout)

    def make_wave_list(self, df):
        # Make a list of cols from the df loaded
        self.waves_list.clear()
        for col in df.columns[1:]:
            # Populate the list widget, each should have a checkbox
            newitem = QListWidgetItem(col, self.waves_list)
            newitem.setCheckState(Qt.CheckState.Checked)

    def get_checked_items(self, list_widget):
        checked_index = []
        for i in range(list_widget.count()):
            if list_widget.item(i).checkState() == Qt.CheckState.Checked:
                checked_index.append(i)
        return checked_index

    def button_save_action(self):
        # Send the chosen df back to the Alch
        self.close()

    def update_wave_list(self):
        # Check to see which list items are checked
        checked_index = self.get_checked_items(self.waves_list)
        # print("Adding", self.waves_list.item(i))
        # Pass those items back to Graph and update the plot
        # Adjusting index by 1 to account for skipped nm column
        df_index = [0]  # Add the nm col back
        df_index += [x+1 for x in checked_index]
        new_df = self.df.iloc[:, df_index]
        if len(checked_index) < 1:
            new_df = None
        # print("Sending", new_df)
        self.graph.setModel(new_df)

    def browse_button_action(self):
        # Todo: Allow for multiple file / directory loading
        get_file_path = QFileDialog.getOpenFileName(self, 'Open File', '.', '(*.*)')
        file_path = get_file_path[0]  # /home/users/.../data.txt
        basename = os.path.basename(file_path)  # data.txt
        if not file_path:
            return
        self.df = read_data_file.load(file_path)
        if self.df is None:
            print('No df generated, aborting file browse')
            return
        self.graph.setModel(self.df)
        self.make_wave_list(self.df)

        # Keep track of the path & name
        self.name = os.path.splitext(basename)[0]  # data
        self.file_path = file_path
        self.box_name.setText(self.name)

    def check_button_action(self):
        checked_index = self.get_checked_items(self.waves_list)
        if len(checked_index) == self.waves_list.count():
            # uncheck all
            new_state = Qt.CheckState.Unchecked
        else:
            # check all
            new_state = Qt.CheckState.Checked
        # Apply to all
        for i in range(self.waves_list.count()):
            self.waves_list.item(i).setCheckState(new_state)
        # Call an update
        self.update_wave_list()
