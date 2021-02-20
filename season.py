from PySide6.QtWidgets import QAbstractItemView, QComboBox, QDialog, QDialogButtonBox, QGridLayout, QItemDelegate, QMainWindow, QTableView, QStyleOptionViewItem, QVBoxLayout, QWidget
from PySide6.QtCore import QAbstractTableModel, QModelIndex, Qt
from PySide6.QtGui import QPainter


class SeasonModel(QAbstractTableModel):
    def __init__(self, seasons: list) -> None:
        super().__init__()
        self.header = ['序号', '季名', '集数']
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

    def getSeason(self, index: QModelIndex) -> tuple:
        return self.seasons[index.row()]


class SeasonWindow(QMainWindow):
    def __init__(self, parent, movie: tuple) -> None:
        super(SeasonWindow, self).__init__(parent)
        self.movie = movie
        self.setWindowTitle(movie[1])
        self.resize(600, 600)
        seasons = parent.core.querySeason(movie[0])
        # print(seasons)

        self.model = SeasonModel(seasons)

        self.table = QTableView(self)
        self.table.setModel(self.model)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.doubleClicked.connect(self.selectFormat)

        self.setCentralWidget(self.table)

    def selectFormat(self, index: QModelIndex):
        season = self.model.getSeason(index)
        FormatDialog(self, self.movie, season).show()


class FormatDialog(QDialog):
    def __init__(self, parent, movie, season) -> None:
        super(FormatDialog, self).__init__(parent)
        self.setWindowTitle(f'{movie[1]} {season[3]} 选择格式')
        self.season = season
        fmtList = season[5].split(',')

        self.vbox = QVBoxLayout()
        self.combo = QComboBox()
        self.combo.addItems(fmtList)
        self.btns = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.btns.button(QDialogButtonBox.Ok).setText('确定')
        self.btns.button(QDialogButtonBox.Cancel).setText('取消')
        self.btns.accepted.connect(self.accept)
        self.btns.rejected.connect(self.reject)

        self.vbox.addWidget(self.combo)
        self.vbox.addWidget(self.btns)

        self.setLayout(self.vbox)

    def accept(self) -> None:
        fmt = self.combo.currentText()
        movieId, seasonNum = self.season[1], self.season[2]
        episodes=self.parent().parent().core.queryEpisode(movieId, seasonNum, fmt)
        print(episodes)
        return super().accept()

    def reject(self) -> None:
        return super().reject()
