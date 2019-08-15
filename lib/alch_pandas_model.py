"""
alch_pandas_model.py
Convert pandas dataframe to Qt model
from https://stackoverflow.com/questions/31475965/fastest-way-to-populate-qtableview-from-pandas-data-frame

"""
from PySide2.QtCore import QAbstractTableModel, Qt


class PandasModel(QAbstractTableModel):
    """
    Class to populate a table view with a pandas dataframe
    Usage:
    model = PandasModel(your_pandas_data_frame)
    your_tableview.setModel(model)
    """
    def __init__(self, data, parent=None):
        QAbstractTableModel.__init__(self, parent)
        self._data = data

    def rowCount(self, parent=None):
        return len(self._data.values)

    def columnCount(self, parent=None):
        return self._data.columns.size

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self._data.values[index.row()][index.column()])
        return None

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._data.columns[col]
        return None
