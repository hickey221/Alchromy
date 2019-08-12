from PySide2.QtWidgets import *
from PySide2.QtCore import Qt
from PySide2.QtGui import QIcon

import alch_import
import alch_graph


class LoadWindow(QWidget):
    def __init__(self):
        # Establish some window stuff
        QWidget.__init__(self)
        self.resize(800, 400)
        self.setWindowIcon(QIcon("lib/alch_flask_icon.ico"))

        # Make some widgets
        self.graph = alch_graph.Graph()
        self.waves_list = QListWidget()
        self.waves_list.itemChanged.connect(self.update_wave_list)
        # self.load_label = QLabel('Load window screen')

        # Browse button & action
        self.browse_button = QPushButton('Select file')
        self.browse_button.clicked.connect(self.browse_button_action)

        # Browse button & action
        self.check_button = QPushButton('Check/uncheck all')
        self.check_button.clicked.connect(self.check_button_action)

        # Construct layout
        self.layout = QVBoxLayout()
        top_button_bar = QHBoxLayout()
        graph_bar = QHBoxLayout()
        bottom_button_bar = QHBoxLayout()

        # First row: Load buttons
        #top_button_bar.addWidget(self.load_label, stretch=0)
        top_button_bar.addWidget(self.browse_button, stretch=0)
        top_button_bar.addWidget(QLabel(''), 1)  # Spacer
        # Second row: wave list and graph plot
        graph_bar.addWidget(self.waves_list)
        # self.waves_list.clicked.connect(self.make_wave_list)
        graph_bar.addWidget(self.graph, stretch=1)
        # Third row: Save button
        bottom_button_bar.addWidget(self.check_button, stretch=0)
        bottom_button_bar.addWidget(QLabel(''), 1)  # Spacer
        bottom_button_bar.addWidget(QPushButton('Save'))

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
        file_name = QFileDialog.getOpenFileName(self, 'Open File', '.', '(*.*)')
        if file_name[0]:
            self.df = alch_import.load(file_name[0])
            self.graph.setModel(self.df)
            self.make_wave_list(self.df)

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
