from PySide2.QtWidgets import *
from PySide2.QtGui import QKeySequence, QDesktopServices
from PySide2.QtCore import QUrl


class MenuBar(QMenuBar):
    def __init__(self, parent):
        QMenuBar.__init__(self)
        self.parent = parent  # Refers to the Qt MainWindow
        # Populate QMenuBar with QMenu items
        self.menu_file = self.addMenu("&File")
        self.menu_file.addAction(QAction("test"))
        self.menu_tools = self.addMenu("&Tools")
        self.menu_help = self.addMenu("&Help")
        self.populateMenuBar()

    def populateMenuBar(self):
        # About dialog
        self.action_about = QAction("&About")
        self.action_about.triggered.connect(self.show_about_dialog)
        # Save function
        self.action_save = QAction("&Save")
        self.action_save.triggered.connect(self.parent.save)
        self.action_save.setShortcut(QKeySequence.Save)
        # Close function
        self.action_close = QAction("&Close")
        self.action_close.triggered.connect(self.parent.close)
        # Preferences
        self.action_pref = QAction("&Preferences")
        # Theme switching (to be moved to preferences)
        self.action_theme = QAction(text='&Theme', checkable=True, checked=False)
        self.action_theme.triggered.connect(self.changeTheme)
        # Debug setting
        self.action_debug = QAction(text='&Debug mode', checkable=True, checked=False)
        self.action_faq = QAction("&FAQ")
        self.action_faq.triggered.connect(self.launchFAQ)
        # Viewer shortcut
        self.action_viewer = QAction('&Viewer')
        self.action_viewer.triggered.connect(self.parent.window_viewer.show)

        # Attach actions to QMenu items
        self.menu_file.addAction(self.action_save)
        self.menu_file.addAction(self.action_close)

        self.menu_tools.addAction(self.action_pref)
        self.menu_tools.addAction(self.action_debug)
        self.menu_tools.addAction(self.action_viewer)
        #menu_tools.addAction(action_theme)
        self.menu_help.addAction(self.action_faq)
        self.menu_help.addAction(self.action_about)

    def changeTheme(self):
        return
        app.setPalette(lightmode)
        self.repaint()

    def launchFAQ(self):
        QDesktopServices.openUrl(QUrl("http://www.alchromy.com/"))

    def show_about_dialog(self):
        text = '<center>' \
               '<h1>Alchromy</h1>' \
               '&#8291;' \
               '</center>' \
               '<p>Version x.xx<br/>' \
               'Copyright &copy; 2016-2019 Rich Hickey</p>'
        QMessageBox.about(self, "Alchromy v. x.xx", text)