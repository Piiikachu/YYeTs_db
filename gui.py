import sqlite3
from PySide6.QtWidgets import QApplication, QMainWindow, QTableView, QDialog
from PySide6.QtGui import QIcon
from PySide6.QtCore import QAbstractTableModel

import sys

import core


class MovieModel(QAbstractTableModel):
    def __init__(self):
        super().__init__()
        self.header = ['影片id', '中文名', '英文名', '别名', '类型', '地区']


class SearchDialog(QDialog):
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
        self.setCentralWidget(self.table)
        self.loadDataBase()

    def loadDataBase(self):
        dbPath = core.getDBPath()
        if dbPath == None:
            # todo: database path setting dialog
            print('path not found')
            pass
        self.connect = sqlite3.connect(dbPath)
        self.cursor = self.connect.cursor()
        query = "SELECT * FROM movie_info LIMIT 100"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        if len(result) == 0:
            print('movie not found')
        for m in result:
            print(m)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setOrganizationName("ShitHappens")
    app.setOrganizationDomain("ShitHappens.ltd")
    app.setApplicationName("YYeTs.db")
    mainwindow = MainWindow()
    mainwindow.show()
    sys.exit(app.exec_())
