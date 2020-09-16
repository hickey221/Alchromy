from PySide2.QtWidgets import *
from PySide2.QtGui import Qt
from lib import read_data_file
from lib.globals import *
import os


class RefGroup(QGroupBox):
    def __init__(self, parent):
        QGroupBox.__init__(self, "Reference")
        self.parent = parent  # Refers to the Qt MainWindow
        self.df = None
        self.name = None
        self.file_path = None

        self.list_waves = QListWidget()
        self.final_layout = QVBoxLayout()

        self.radio_default = QRadioButton('Default', checked=True)
        self.radio_default.setStatusTip('Use built-in reference spectra.')
        self.radio_default.clicked.connect(self.disable_custom)

        self.radio_custom = QRadioButton('Custom', checked=False)
        self.radio_custom.setStatusTip('Load custom reference spectra.')
        self.radio_custom.clicked.connect(self.enable_custom)

        self.button_custom = QPushButton('Load', enabled=False)
        self.button_custom.clicked.connect(self.browse_button_action)

        self.line_custom = QHBoxLayout()
        self.line_custom.addWidget(self.radio_default)
        self.line_custom.addWidget(self.radio_custom)
        self.line_custom.addWidget(self.button_custom)
        self.line_custom.addWidget(QLabel(''), 1)

        self.final_layout.addLayout(self.line_custom)
        self.final_layout.addWidget(self.list_waves, 1)
        self.setLayout(self.final_layout)

        self.load_default()

    def enable_custom(self):
        self.button_custom.setEnabled(True)
        self.radio_custom.setChecked(True)
        self.radio_default.setChecked(False)
        self.clear_all()

    def disable_custom(self):
        self.button_custom.setDisabled(True)
        self.radio_default.setChecked(True)
        self.radio_custom.setChecked(False)
        # Reload defaults
        self.load_default()

    def load_default(self):
        self.load_ref_file(DEFAULT_REFERENCE_PATH)
        if self.df is None:
            print("Unable to load defaults")
            self.enable_custom()
            self.radio_default.setDisabled(True)
            self.radio_default.setStatusTip('Built-in reference spectra \''+DEFAULT_REFERENCE_PATH+'\' not found.')
            return
        #self.populate_list()

    def browse_button_action(self):
        get_file_path = QFileDialog.getOpenFileName(self, 'Open Reference File', '.', '(*.*)')
        file_path = get_file_path[0]  # /home/users/.../hHb_default.dat
        basename = os.path.basename(file_path)  # hHb_default.dat
        if not file_path:
            return
        # Send to the loading method
        self.load_ref_file(file_path)

        # Keep track of the path & name
        self.name = os.path.splitext(basename)[0]  # hHb_default
        self.file_path = file_path

    def load_ref_file(self, path):
        try:
            self.df = read_data_file.load(path)
        except:
            print("Couldn't import reference at", path)
        self.populate_list()

    def clear_all(self):
        self.list_waves.clear()
        self.df = None

    def populate_list(self):
        if self.df is None:
            print("Can't fill list, no df loaded")
            return
        # Empty list to rewrite
        self.list_waves.clear()
        for col in self.df.columns[1:]:
            # Populate the list widget, each should have a checkbox
            newitem = QListWidgetItem(col, self.list_waves)
            # If indicated, enable by default
            newitem.setCheckState(Qt.CheckState.Checked)

    def get_checked_items(self, list_widget):
        """
        Return an index of selected reference species
        :param list_widget:
        :return:
        """
        checked_index = []
        for i in range(list_widget.count()):
            if list_widget.item(i).checkState() == Qt.CheckState.Checked:
                checked_index.append(i)
        return checked_index

    def get_df(self):
        if self.df is None:
            print("Can't get df, none loaded")
            return False
        # See what waves are checked
        idx = self.get_checked_items(self.list_waves)
        # Add the index column back then build the df index
        df_index = [0]
        df_index += [x+1 for x in idx]
        new_df = self.df.iloc[:, df_index]
        if len(idx) < 1:
            print("No waves selected")
            new_df = None
        return new_df