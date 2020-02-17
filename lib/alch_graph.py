# from PySide2.QtWidgets import *
#from PySide2.QtCore import Qt
from PySide2.QtGui import QPainter, QBrush
#from PySide2.QtCharts import QtCharts
from PySide2.QtPrintSupport import QPrinter
from PySide2 import QtWidgets, QtCore, QtGui, QtCharts, QtPrintSupport, QtSvg

from lib import alch_pandas_model, alch_theme
# TODO: SVG saving: https://stackoverflow.com/questions/38800759/rendering-qchart-without-qgraphicsview


class Graph(QtWidgets.QWidget):
    def __init__(self):
        """
        Container widget for all elements of a waveform graph plot
        """
        QtWidgets.QWidget.__init__(self)
        self.series = None
        self.model = None

        # Create chart
        # self.chart = QtCharts.QChart()
        self.chart = alch_theme.DarkChart()
        self.chart_view = QtCharts.QtCharts.QChartView(self.chart)
        self.chart_view.setRenderHint(QPainter.Antialiasing)

        # Placeholder axes
        self.axis_x = alch_theme.DarkAxis()
        self.axis_y = alch_theme.DarkAxis()

        # Left layout
        self.main_layout = QtWidgets.QHBoxLayout()
        size = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
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
        self.axis_x = alch_theme.DarkAxis()
        self.axis_x.setTickCount(6)
        self.axis_x.setLabelFormat("%.0f")
        # self.axis_x.setTitleText("Wavelength")
        self.chart.addAxis(self.axis_x, QtCore.Qt.AlignBottom)

        # Setting Y-axis
        self.axis_y = alch_theme.DarkAxis()
        # self.axis_y.setTickCount(10)
        self.axis_y.setLabelFormat("%.2f")
        # self.axis_y.setTitleText("Absorbance")
        self.chart.addAxis(self.axis_y, QtCore.Qt.AlignLeft)

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
        self.series = QtCharts.QtCharts.QLineSeries()
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

    def save_image(self):
        """
        Record the current chart contents to a vectorized image file
        :return:
        """

        # printer = QPrinter(QPrinter.HighResolution)
        # printer.setOutputFormat(QPrinter.PdfFormat)
        # printer.setOutputFileName('test_chart.pdf')
        # painter = QPainter(printer)

        output_size = QtCore.QSize(800, 600)
        output_rect = QtCore.QRectF(QtCore.QPointF(0, 0), QtCore.QSizeF(output_size))
        svg = QtSvg.QSvgGenerator()
        svg.setFileName('test_chart.svg')
        svg.setTitle('some title')
        svg.setSize(output_size)
        svg.setViewBox(output_rect)

        canvas = svg
        # uncomment to hide background
        # chart.setBackgroundBrush(brush = QtGui.QBrush(QtCore.Qt.NoBrush))
        # resize the chart, as otherwise the size/scaling of the axes etc.
        # will be dependent on the size of the chart in the GUI
        # this way, a consistent output size is enforced
        original_size = self.chart.size()
        self.chart.resize(output_rect.size())
        painter = QtGui.QPainter()
        painter.begin(canvas)
        self.chart.scene().render(painter, source=output_rect, target=output_rect, mode=QtCore.Qt.IgnoreAspectRatio)
        painter.end()

        self.chart.resize(original_size)

        # Save the QChartView object to an image file

        """
        printer = QPrinter(QPrinter.HighResolution)
        printer.setOutputFormat(QPrinter.PdfFormat)
        printer.setOutputFileName('test_chart.pdf')
        painter = QPainter(printer)
        painter.setViewport(self.chart_view.rect())
        painter.setWindow(self.chart_view.rect())
        self.chart_view.render(painter)
        painter.end()
        """

