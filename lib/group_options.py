from PySide2.QtWidgets import *


class OptGroup(QGroupBox):
    def __init__(self, parent):
        QGroupBox.__init__(self, "Options")
        self.parent = parent  # Refers to the Qt MainWindow
        opt_layout = QVBoxLayout()
        norm_box = QCheckBox('Normalize')
        norm_box.setStatusTip('Set minimum absorbance of spectra to 0 by subtraction.')
        wave_box = QCheckBox('Manual wavelength')
        wave_box.setStatusTip('Specify custom wavelengths for measurement.')
        opt_layout.addWidget(norm_box)
        opt_layout.addWidget(wave_box)
        opt_layout.addWidget(QCheckBox('Etc'))
        self.setLayout(opt_layout)
