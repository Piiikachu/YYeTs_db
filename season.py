from PySide6.QtWidgets import QMainWindow, QTableView
from PySide6.QtCore import QAbstractTableModel, QModelIndex, Qt


class SeasonModel(QAbstractTableModel):
    def __init__(self, seasons: list) -> None:
        super().__init__()
        self.header = ['序号', '季名', '集数', '格式']
        self.seasons = seasons

    def rowCount(self, parent: QModelIndex) -> int:
        return len(self.seasons)

    def columnCount(self, parent: QModelIndex) -> int:
        return len(self.header)

    def headerData(self, section: int, orientation: Qt.Orientation, role: int):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self.header[section]

    def data(self, index: QModelIndex, role: int):
        if index.isValid() and role == Qt.DisplayRole:
            if index.column() == 0:
                return index.row()+1
            return self.seasons[index.row()][index.column()+2]

    def update(self, seasons: list):
        self.seasons = seasons
        self.layoutChanged.emit()

    def getSeason(self, index: QModelIndex):
        return self.seasons[index.row()]


class SeasonWindow(QMainWindow):
    def __init__(self, parent, movie: tuple) -> None:
        super(SeasonWindow, self).__init__(parent)
        self.setWindowTitle(movie[1])
        self.resize(600,600)
        seasons = parent.core.querySeason(movie[0])
        print(seasons)

        self.model = SeasonModel(seasons)
        table = QTableView()
        table.setModel(self.model)
        self.setCentralWidget(table)
