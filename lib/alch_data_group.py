from PySide2.QtWidgets import *
from PySide2.QtGui import Qt
from lib import alch_load_window


class DataGroup(QGroupBox):
    def __init__(self, parent):
        QGroupBox.__init__(self, "Data")
        self.parent = parent  # Refers to the Qt MainWindow
        self.window_load = alch_load_window.LoadWindow()
        self.final_layout = QVBoxLayout()
        # Load line items
        self.make_load_line()
        # Paste window and line items
        self.make_paste_window()
        self.make_paste_line()
        self.final_layout.addLayout(self.load_line_layout)
        self.final_layout.addLayout(self.paste_line_layout)
        self.setLayout(self.final_layout)

    def make_load_line(self):
        self.load_line_layout = QHBoxLayout()

        self.load_button = QPushButton('Load')
        self.load_button.clicked.connect(self.load_action)

        self.load_file_radio = QRadioButton('From file', checked=True)
        self.load_file_radio.clicked.connect(self.switchToLoad)
        self.load_file_radio.setStatusTip("Load spectra from a data file.")

        self.load_line_layout.addWidget(self.load_file_radio)
        self.load_line_layout.addWidget(self.load_button)

    def make_paste_window(self):
        self.paste_window = QWidget()
        self.paste_window.setWindowModality(Qt.ApplicationModal)
        self.paste_layout = QVBoxLayout()
        self.paste_layout.addWidget(QLabel("Must be whitespace delimited"))
        self.paste_layout.addWidget(QTextEdit())

        self.paste_window.setLayout(self.paste_layout)

    def make_paste_line(self):
        self.paste_line_layout = QHBoxLayout()

        self.paste_button = QPushButton('Input', enabled=False)
        self.paste_button.clicked.connect(self.paste_action)

        self.paste_data_radio = QRadioButton('Paste data')
        self.paste_data_radio.setStatusTip("Load spectra from copy/pasted data.")
        self.paste_data_radio.clicked.connect(self.switchToPaste)

        self.paste_line_layout.addWidget(self.paste_data_radio)
        self.paste_line_layout.addWidget(self.paste_button)

    def load_action(self):
        self.window_load.show()
        # If nothing previously loaded, jump to file browse
        if self.window_load.df is None:
            self.window_load.browse_button_action()

    def paste_action(self):
        self.parent.showMsg("Opening paste window")
        self.paste_window.show()

    def switchToLoad(self):
        self.load_button.setEnabled(True)
        self.paste_button.setDisabled(True)

    def switchToPaste(self):
        self.paste_button.setEnabled(True)
        self.load_button.setDisabled(True)
