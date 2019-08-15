from PySide2.QtWidgets import *
from PySide2.QtCore import Qt
from PySide2 import QtGui
from PySide2.QtCharts import QtCharts

from lib import alch_pandas_model


class Graph(QWidget):
    def __init__(self):
        """
        Container widget for all elements of a waveform graph plot
        """
        QWidget.__init__(self)
        self.series = None
        self.model = None

        # Create chart
        self.chart = QtCharts.QChart()
        self.chart_view = QtCharts.QChartView(self.chart)
        self.chart_view.setRenderHint(QtGui.QPainter.Antialiasing)

        # Placeholder axes
        self.axis_x = QtCharts.QValueAxis()
        self.axis_y = QtCharts.QValueAxis()

        # Left layout
        self.main_layout = QHBoxLayout()
        size = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        size.setHorizontalStretch(1)
        # Right Layout
        size.setHorizontalStretch(4)
        self.chart_view.setSizePolicy(size)

        self.update_axes()
        self.chart.legend().hide()
        # Set the layout
        self.main_layout.addWidget(self.chart_view)
        self.setLayout(self.main_layout)

    def update_axes(self):
        # Remove old junk
        self.chart.removeAxis(self.axis_x)
        self.chart.removeAxis(self.axis_y)
        # Set X-axis
        self.axis_x = QtCharts.QValueAxis()
        self.axis_x.setTickCount(6)
        self.axis_x.setLabelFormat("%.0f")
        # self.axis_x.setTitleText("Wavelength")
        self.chart.addAxis(self.axis_x, Qt.AlignBottom)

        # Setting Y-axis
        self.axis_y = QtCharts.QValueAxis()
        # self.axis_y.setTickCount(10)
        self.axis_y.setLabelFormat("%.2f")
        # self.axis_y.setTitleText("Absorbance")
        self.chart.addAxis(self.axis_y, Qt.AlignLeft)

    def setModel(self, df):
        """
        Accept a new pandas df and set as the model. Clear and re-populate line series
        :param df:
        :return:
        """
        # Empty the line series if it's already in use
        self.chart.removeAllSeries()
        if df is None or df.empty:
            print("no df found, aborting")
            self.model = None
            return
        self.model = alch_pandas_model.PandasModel(df)
        # for each column
        for i in range(1, self.model.columnCount()):
            self.add_series(i)
        self.series.attachAxis(self.axis_x)
        self.series.attachAxis(self.axis_y)

    def add_series(self, c_index):
        self.series = QtCharts.QLineSeries()
        # self.series.setName(name)
        for i in range(1, self.model.rowCount()):
            x = float(self.model.index(i, 0).data())
            y = float(self.model.index(i, c_index).data())
            # print(i, x, y)
            self.series.append(x, y)
            if x > 0 and y > 0:
                self.series.append(x, y)

        self.chart.addSeries(self.series)
        self.update_axes()
