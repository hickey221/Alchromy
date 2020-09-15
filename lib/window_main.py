# PyQt5==5.9.2
"""
Main window containing all other widgets.
Contains groups for 'mode', 'data', 'options', and 'reference'
As well as bars for menu and status

"""
from PySide2.QtWidgets import *
from PySide2.QtGui import QIcon

# Internal imports
from lib import group_mode, group_data, group_options, bar_top_menu, alch_class, group_ref, window_viewer, bar_bottom_status, alch_engine


class MainWindow(QMainWindow):
    # Main window class from https://github.com/pyqt/examples/blob/_/src/09%20Qt%20dark%20theme/main.py
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowIcon(QIcon("assets/alch_flask_icon.ico"))
        # Create a new log file
        self.statusLog = QLabel("")
        self.alch = alch_class.Alch()
        self.logMsg("New alch created")
        self.window_viewer = window_viewer.ViewerWindow()  # Why must this exist already?

        # Get a menu bar at top of window
        self.menu_bar = bar_top_menu.MenuBar(parent=self)
        self.setMenuBar(self.menu_bar)
        # Get a status bar at bottom of window
        self.status_bar = bar_bottom_status.StatusBar(parent=self, log=self.statusLog)
        self.setStatusBar(self.status_bar)
        # self.populateStatusBar()

        # Begin main content assembly
        self.content = QWidget()
        self.setCentralWidget(self.content)
        self.group_mode = group_mode.ModeGroup(parent=self)
        self.group_data = group_data.DataGroup(parent=self)
        self.group_ref = group_ref.RefGroup(parent=self)
        self.group_opt = group_options.OptGroup(parent=self)

        run_button = QPushButton('Run')
        # run_button.setStatusTip('Begin analysis with selected settings.')
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

    def run_action(self):
        #
        if self.group_data.window_load.df is None:
            self.showMsg('No data loaded!')
            return
        self.showMsg('Running!')
        # Grab temp data from the loading window
        self.alch.data = self.group_data.window_load.df
        try:
            print(f'trying to set name {self.group_data.window_load.name}')
            # TODO: Clean up path  to file name
            #self.alch.metadata['name'] = self.group_data.window_load.name
        except:
            print('could not set name')
        self.alch.references = self.group_ref.get_df()
        self.alch.options['mode'] = 'replicate'

        # Perform ready check
        self.alch.ready = alch_engine.readyCheck(self.alch)
        self.logMsg("Ready check: "+str(self.alch.ready))
        if not self.alch.ready:
            self.logMsg("Not ready!")
            return
        self.logMsg("Running...")
        # Send it for processing
        alch_engine.generate_result(self.alch)

        # Send the result over to the viewer
        self.logMsg("Loading results")
        self.window_viewer.load_alch(self.alch)
        self.window_viewer.show()

    def showMsg(self, msg):
        self.status_bar.showMessage(msg, 2000)

    def logMsg(self, msg):
        # Display on output
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
        return

    def closeEvent(self, e):
        """
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
        """
        return
