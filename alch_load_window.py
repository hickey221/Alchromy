from PySide2.QtWidgets import *
from PySide2.QtCore import  Qt

import alch_import
import alch_graph


class LoadWindow(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.graph = alch_graph.Graph()
        self.waves_list = QListWidget()
        self.waves_list.itemClicked.connect(self.update_wave_list)

        self.load_label = QLabel('Load window screen')

        # Browse button & action
        self.browse_button = QPushButton('Select file')
        self.browse_button.clicked.connect(self.browse_button_action)

        # Browse button & action
        self.check_button = QPushButton('Check')
        self.check_button.clicked.connect(self.update_wave_list)

        # Construct layout
        self.layout = QVBoxLayout()
        top_button_bar = QHBoxLayout()
        graph_bar = QHBoxLayout()
        bottom_button_bar = QHBoxLayout()

        # First row: Load buttons
        top_button_bar.addWidget(self.load_label, stretch=0)
        top_button_bar.addWidget(self.browse_button, stretch=0)
        # Second row: wave list and graph plot
        graph_bar.addWidget(self.waves_list)
        # self.waves_list.clicked.connect(self.make_wave_list)
        graph_bar.addWidget(self.graph, stretch=1)
        # Third row: Save button
        bottom_button_bar.addWidget(self.check_button, stretch=0)
        bottom_button_bar.addWidget(QLabel(''), 1)
        bottom_button_bar.addWidget(QPushButton('Save'))

        # Assemble the layout and apply it
        self.layout.addLayout(top_button_bar)
        self.layout.addLayout(graph_bar)
        self.layout.addLayout(bottom_button_bar)
        self.setLayout(self.layout)

    def make_wave_list(self, df):
        # Make a list of cols from the df loaded
        # Make a list widget
        # Populate the list widget, each should have a checkbox
        self.waves_list.clear()
        for col in df.columns[1:]:
            newitem = QListWidgetItem(col, self.waves_list)
            newitem.setCheckState(Qt.CheckState.Checked)

    def update_wave_list(self):
        # Check to see which list items are checked
        checked_index = []
        for i in range(self.waves_list.count()):
            if self.waves_list.item(i).checkState() == Qt.CheckState.Checked:
                checked_index.append(i)
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
