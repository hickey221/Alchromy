from PySide2.QtWidgets import *


class ModeGroup(QGroupBox):
    def __init__(self, parent):
        QGroupBox.__init__(self, "Mode")
        self.parent = parent  # Refers to the Qt MainWindow
        self.mode_list = ("Simple",
                          "Replicate",
                          "Kinetic")
        self.mode_desc = ("Analyze one spectrum at a time, or a batch of several spectra separately.",
                          "Average multiple spectra and analyze as one.",
                          "Treat multiple spectra as time course data.")
        self.label_mode = QLabel(self.mode_desc[0])
        self.mode_box = QComboBox()
        self.mode_box.addItems(self.mode_list)
        self.mode_box.setStatusTip("Change the operation mode.")
        self.mode_box.currentIndexChanged.connect(self.mode_change)
        self.mode_layout = QHBoxLayout()
        self.mode_layout.addWidget(self.mode_box)
        self.mode_layout.addWidget(self.label_mode, 1)
        self.setLayout(self.mode_layout)

    def mode_change(self):
        # Get the appropriate description of the selected mode
        self.label_mode.setText(self.mode_desc[self.mode_box.currentIndex()])






