# PyQt5==5.9.2

from PySide2.QtWidgets import *
from PySide2.QtGui import QIcon

# Internal imports
from lib import alch_mode_group, alch_data_group, alch_options_group, alch_menu_bar, alch_class, alch_ref_group, alch_viewer


class MainWindow(QMainWindow):
    # Main window class from https://github.com/pyqt/examples/blob/_/src/09%20Qt%20dark%20theme/main.py
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowIcon(QIcon("assets/alch_flask_icon.ico"))
        # Create a new log file
        self.statusLog = QLabel("")
        self.alch = alch_class.Alch()
        self.logMsg("Alch loaded")
        self.window_viewer = alch_viewer.ViewerWindow()
        # Get a menu bar at top of window
        self.menu_bar = alch_menu_bar.MenuBar(self)
        self.setMenuBar(self.menu_bar)
        # Get a status bar at bottom of window
        self.status_bar = QStatusBar()
        self.populateStatusBar()
        # Begin main content assembly
        self.content = QWidget()
        self.setCentralWidget(self.content)
        self.group_mode = alch_mode_group.ModeGroup(self)
        self.group_data = alch_data_group.DataGroup(self)
        self.group_ref = alch_ref_group.RefGroup(self)
        self.group_opt = alch_options_group.OptGroup(self)

        run_button = QPushButton('Run')
        run_button.setStatusTip('Begin analysis with selected settings.')
        run_button.clicked.connect(self.run_action)

        # Assemble layout
        layout_final = QVBoxLayout()

        layout_center = QHBoxLayout()
        layout_left = QVBoxLayout()
        layout_right = QVBoxLayout()

        layout_left.addWidget(self.group_data)
        layout_left.addWidget(self.group_opt)
        layout_left.addWidget(QLabel(''), 1)
        layout_right.addWidget(self.group_ref)

        layout_center.addLayout(layout_left)
        layout_center.addLayout(layout_right)

        layout_final.addWidget(self.group_mode)
        layout_final.addLayout(layout_center)
        layout_final.addWidget(run_button)

        self.content.setLayout(layout_final)

    def populateStatusBar(self):
        # Declare status bar
        temp_status = QLabel("")
        bar_space = QLabel("")
        self.status_bar.addWidget(temp_status)
        self.status_bar.addWidget(bar_space, 1)
        self.status_bar.addPermanentWidget(self.statusLog)
        self.setStatusBar(self.status_bar)

    def run_action(self):
        self.showMsg('Running!')
        self.alch.data = self.group_data.window_load.df
        self.alch.ref = self.group_ref.get_df()
        self.alch.mode = 'R'
        self.alch.ready = self.alch.readyCheck()
        print("Ready check:", self.alch.ready)
        if self.alch.ready:
            self.alch.generate_result()
            self.window_viewer.loadAlch(self.alch)
            self.window_viewer.show()

    def showMsg(self, msg):
        self.status_bar.showMessage(msg, 1000)

    def logMsg(self, msg):
        self.statusLog.setText(msg)
        # Record the message in the log file

    def save(self):
        """
        if file_path is None:
            save_as()
        else:
            with open(save_file_path, "w") as f:
                f.write(text.toPlainText())
            text.document().setModified(False)
        """
        pass

    def closeEvent(self, e):
        return
        if not text.document().isModified():
            return
        answer = QMessageBox.question(
            window, None,
            "You have unsaved changes. Save before closing?",
            QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel
        )
        if answer & QMessageBox.Save:
            save()
        elif answer & QMessageBox.Cancel:
            e.ignore()

