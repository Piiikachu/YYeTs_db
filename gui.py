from season import SeasonWindow
from PySide6.QtWidgets import QAbstractItemView, QApplication, QLineEdit, QMainWindow, QTableView, QDialog, QToolBar
from PySide6.QtGui import QAction
from PySide6.QtCore import QAbstractTableModel, QModelIndex, Qt

import sys

import core


class MovieModel(QAbstractTableModel):
    def __init__(self):
        super().__init__()
        self.header = ['序号', '中文名', '英文名', '别名', '类型', '地区']
        self.movies = []

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
            return self.movies[index.row()][index.column()]

    def update(self, movies: list):
        self.movies = movies
        self.layoutChanged.emit()

    def getMovie(self, index: QModelIndex):
        return self.movies[index.row()]


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setWindowTitle("YYeTs.db In PyQT6")
        self.setMinimumSize(800, 600)

        # todo: set icon
        # self.setWindowIcon(QIcon('icon/g2.png'))

        # file_menu = self.menuBar().addMenu("&File")

        # help_menu = self.menuBar().addMenu("&About")

        self.model = MovieModel()
        self.table = QTableView()
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.doubleClicked.connect(self.querySeason)
        self.table.setModel(self.model)
        self.setCentralWidget(self.table)

        searchBar = QToolBar()
        self.searchEdit = QLineEdit()
        self.searchEdit.setPlaceholderText('请输入影片名称')
        searchBtn = QAction('search', self)

        searchBar.addWidget(self.searchEdit)
        searchBtn.triggered.connect(self.search)
        searchBar.addAction(searchBtn)

        self.addToolBar(searchBar)

        self.loadDataBase()

    def search(self):
        movies = self.core.queryMovie(self.searchEdit.text())
        self.model.update(movies)

    def querySeason(self, index: QModelIndex):
        movie = self.model.getMovie(index)
        SeasonWindow(self, movie).show()

    def loadDataBase(self):
        self.core = core.AppCore()
        try:
            self.core.connect()
        except core.SqlError:
            SettingDialog(self).show()


class SettingDialog(QDialog):
    def __init__(self, parent: MainWindow) -> None:
        super(SettingDialog, self).__init__(parent)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setOrganizationName("ShitHappens")
    app.setOrganizationDomain("ShitHappens.ltd")
    app.setApplicationName("YYeTs.db")
    mainwindow = MainWindow()
    mainwindow.searchEdit.setText('west')
    mainwindow.show()
    sys.exit(app.exec_())
