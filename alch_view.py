from PySide2.QtWidgets import *
from PySide2.QtCore import QAbstractTableModel, Qt, QModelIndex, SLOT
from PySide2 import QtGui
from PySide2.QtWidgets import (QAction, QApplication, QHBoxLayout, QHeaderView,
                               QMainWindow, QSizePolicy, QTableView, QWidget)
from PySide2.QtCharts import QtCharts

import pd_to_model
import alch_load

class Graph(QWidget):
    def __init__(self):
        """
        Container widget for all elements of a waveform graph plot
        """
        QWidget.__init__(self)
        self.series = None
        self.model = None
        # Create table
        # self.table_view = QTableView()
        # self.table_view.setModel(self.model)

        # Table Headers
        # resize = QHeaderView.ResizeToContents
        # self.horizontal_header = self.table_view.horizontalHeader()
        # self.vertical_header = self.table_view.verticalHeader()
        # self.horizontal_header.setSectionResizeMode(resize)
        # self.vertical_header.setSectionResizeMode(resize)
        # self.horizontal_header.setStretchLastSection(True)

        # Create chart
        self.chart = QtCharts.QChart()
        self.chart_view = QtCharts.QChartView(self.chart)
        self.chart_view.setRenderHint(QtGui.QPainter.Antialiasing)

        # Left layout
        self.main_layout = QHBoxLayout()
        size = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        size.setHorizontalStretch(1)
        # self.table_view.setSizePolicy(size)
        # Right Layout
        size.setHorizontalStretch(4)
        self.chart_view.setSizePolicy(size)

        ################################################################
        # Setting X-axis
        self.axis_x = QtCharts.QValueAxis()
        self.axis_x.setTickCount(6)
        self.axis_x.setLabelFormat("%.0f")
        #self.axis_x.setTitleText("Wavelength")
        self.chart.addAxis(self.axis_x, Qt.AlignBottom)

        # Setting Y-axis
        self.axis_y = QtCharts.QValueAxis()
        #self.axis_y.setTickCount(10)
        self.axis_y.setLabelFormat("%.2f")
        #self.axis_y.setTitleText("Absorbance")
        self.chart.addAxis(self.axis_y, Qt.AlignLeft)
        self.chart.legend().hide()
        ################################################################

        # Set the layout
        # self.main_layout.addWidget(self.table_view)
        self.main_layout.addWidget(self.chart_view)
        self.setLayout(self.main_layout)

    def setModel(self, df):
        """
        Accept a new pandas df and set as the model. Clear and re-populate line series
        :param df:
        :return:
        """
        # Empty the line series if it's already in use
        if self.series:
            self.series.clear()
        self.model = pd_to_model.PandasModel(df)
        self.add_series()
        self.series.attachAxis(self.axis_x)
        self.series.attachAxis(self.axis_y)

    def add_series(self):
        self.series = QtCharts.QLineSeries()
        #self.series.setName(name)
        for i in range(1, self.model.rowCount()):
            x = float(self.model.index(i, 0).data())
            y = float(self.model.index(i, 1).data())
            # print(i, x, y)
            self.series.append(x, y) # issue with x being type str
            if x > 0 and y > 0:
                self.series.append(x, y)

        self.chart.addSeries(self.series)


class LoadWindow(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.graph = Graph()
        self.waves_list = QListWidget()

        self.load_label = QLabel('Load window screen')

        # Browse button & action
        self.browse_button = QPushButton('Browse')
        self.browse_button.clicked.connect(self.browse_button_action)

        # Set layout
        self.layout = QVBoxLayout()

        self.layout.addWidget(self.load_label, stretch=0)
        self.layout.addWidget(self.browse_button, stretch=0)
        # self.layout.addWidget(self.waves_list)
        self.layout.addWidget(self.graph, stretch=1)
        self.setLayout(self.layout)

    def browse_button_action(self):
        file_name = QFileDialog.getOpenFileName(self, 'Open File', '.', '(*.*)')
        if file_name[0]:
            # print("file_name looks like: ", file_name)
            df = alch_load.load(file_name[0])
            self.graph.setModel(df)
