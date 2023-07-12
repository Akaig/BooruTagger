from PyQt5 import QtWidgets

class TableWidgetCompleter(QtWidgets.QTableWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setEditTriggers(QtWidgets.QAbstractItemView.DoubleClicked | QtWidgets.QAbstractItemView.EditKeyPressed | QtWidgets.QAbstractItemView.AnyKeyPressed)
        self.delegate = LineEditDelegate()
        self.setItemDelegateForColumn(0, self.delegate)
        self.completer = None

    def set_completer(self, completer):
        self.completer = completer
        self.delegate.set_completer(completer)

class LineEditDelegate(QtWidgets.QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.completer = None

    def set_completer(self, completer):
        self.completer = completer

    def createEditor(self, parent, option, index):
        editor = QtWidgets.QLineEdit(parent)
        editor.setCompleter(self.completer)
        return editor