import sqlite3
from PySide6.QtWidgets import QApplication, QMainWindow, QTableView, QDialog
from PySide6.QtGui import QIcon
from PySide6.QtCore import QAbstractTableModel, QModelIndex, Qt

import sys

import core


class MovieModel(QAbstractTableModel):
    def __init__(self):
        super().__init__()
        self.header = ['序号', '影片id', '中文名', '英文名', '别名', '类型', '地区']
        self.movies = [('a', 'b', 'c', 'd', 'e', 'f')]

    def rowCount(self, parent: QModelIndex) -> int:
        return len(self.movies)

    def columnCount(self, parent: QModelIndex) -> int:
        return len(self.header)

    def headerData(self, section: int, orientation: Qt.Orientation, role: int):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self.header[section]

    def data(self, index: QModelIndex, role: int):
        if index.isValid() and role == Qt.DisplayRole:
            if index.column() == 0:
                return index.row()+1
            return self.movies[index.row()][index.column()-1]

    def update(self, movies: list):
        self.movies = movies


class SearchDialog(QDialog):
    def __init__(self, parent: QMainWindow) -> None:
        super(SearchDialog, self).__init__(parent)


class SettingDialog(QDialog):
    def __init__(self, parent: QMainWindow) -> None:
        super(SearchDialog, self).__init__(parent)


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setWindowTitle("YYeTs.db In PyQT6")
        self.setMinimumSize(800, 600)

        # todo: set icon
        # self.setWindowIcon(QIcon('icon/g2.png'))

        file_menu = self.menuBar().addMenu("&File")

        help_menu = self.menuBar().addMenu("&About")

        self.table = QTableView()
        self.model = MovieModel()
        self.table.setModel(self.model)
        self.setCentralWidget(self.table)
        self.loadDataBase()

    def loadDataBase(self):
        self.core = core.AppCore()
        try:
            self.core.connect()
        except core.SqlError:
            SettingDialog().show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setOrganizationName("ShitHappens")
    app.setOrganizationDomain("ShitHappens.ltd")
    app.setApplicationName("YYeTs.db")
    mainwindow = MainWindow()
    mainwindow.show()
    sys.exit(app.exec_())
