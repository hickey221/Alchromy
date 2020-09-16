# PyQt5==5.9.2
"""
Main window containing all other widgets.
Contains groups for 'mode', 'data', 'options', and 'reference'
As well as bars for menu and status

"""
from PySide2.QtWidgets import *
from PySide2.QtGui import QIcon

# Internal imports
from lib import group_mode, group_data, group_options, bar_top_menu, \
    alch_class, group_ref, window_viewer, bar_bottom_status, alch_engine


class MainWindow(QMainWindow):
    # Main window class from https://github.com/pyqt/examples/blob/_/src/09%20Qt%20dark%20theme/main.py
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowIcon(QIcon("assets/alch_flask_icon.ico"))
        # Create a new log file
        self.statusLog = QLabel("")
        self.alch = alch_class.Alch()
        self.logMsg("New alch created")
        self.window_viewer = window_viewer.ViewerWindow()

        # Get a menu bar at top of window
        self.menu_bar = bar_top_menu.MenuBar(parent=self)
        self.setMenuBar(self.menu_bar)
        # Get a status bar at bottom of window
        self.status_bar = bar_bottom_status.StatusBar(parent=self, log=self.statusLog)
        self.setStatusBar(self.status_bar)

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
        """
        Grab dataframes from the reference and data groups,
        pack it into our current alch, and send it out to
        be fitted using alch_engine.
        :return:
        """
        # Todo: Check if we're using loaded or pasted data
        if self.group_data.window_load.df is None:
            self.showMsg("No data loaded!")
            return
        elif self.group_ref.get_df() is None:
            self.showMsg("No reference loaded!")
            return

        # Grab temp data from the loading window
        self.logMsg("Migrating dataframes from load window")
        self.alch.data = self.group_data.window_load.df
        self.alch.references = self.group_ref.get_df()
        self.logMsg("Performing ready check: ")

        self.alch.options['mode'] = self.group_mode.get_current_mode()
        # Todo: If mode is single but multiple data columns exist, run them individually
        # Todo: Popup confirm dialog if running potentially too many individuals at once

        self.logMsg("Cleaning data")
        alch_engine.clean_data(self.alch)

        self.logMsg("Loading metadata into alch")
        self.alch.metadata['name'] = self.group_data.window_load.name
        self.alch.metadata['data_file_path'] = self.group_data.window_load.file_path
        self.alch.metadata['reference_file_path'] = self.group_ref.file_path

        # Send it out for processing
        self.logMsg("Running...")
        alch_engine.generate_result(self.alch)

        # Make a backup of the run so far
        self.logMsg("Saving temp file")
        alch_engine.save_temp_file(self.alch)

        # Send the result over to the viewer
        self.logMsg("Loading results")
        self.window_viewer.load_alch(self.alch)
        self.window_viewer.show()

    def showMsg(self, msg):
        # Display a message in the status bar for 2 seconds
        self.status_bar.showMessage(msg, 2000)

    def logMsg(self, msg):
        # Display on output
        print(msg)
        self.statusLog.setText(msg)
        # Record the message in the log file

    def closeEvent(self, e):
        """
        Safely shut down the program
        :param e:
        :return:
        """
        # Todo: Write current settings to a config file to reload later
        self.logMsg("Shutting down nicely")
        self.close()
