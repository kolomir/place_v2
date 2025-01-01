from PyQt5.QtWidgets import (
    QApplication, QTableView, QVBoxLayout, QWidget, QLineEdit, QHBoxLayout, QHeaderView, QAbstractItemView
)
from PyQt5.QtCore import Qt, QSortFilterProxyModel, QAbstractTableModel
from PyQt5.QtGui import QStandardItemModel, QStandardItem


class FilterableTable(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Filtrowanie w nagłówkach")
        self.resize(800, 400)

        # Model danych
        self.model = QStandardItemModel(10, 3)  # 10 wierszy, 3 kolumny
        self.model.setHorizontalHeaderLabels(["Kolumna 1", "Kolumna 2", "Kolumna 3"])
        dane = [
            ["Jabłko", "123", "A"],
            ["Gruszka", "45", "B"],
            ["Banan", "789", "C"],
            ["Jabłko", "567", "A"],
            ["Gruszka", "234", "C"],
            ["Banan", "12", "B"],
            ["Ananas", "890", "C"],
            ["Winogrono", "678", "A"],
            ["Melon", "345", "B"],
            ["Pomarańcza", "456", "A"],
        ]
        for row, row_data in enumerate(dane):
            for col, value in enumerate(row_data):
                self.model.setItem(row, col, QStandardItem(value))

        # Proxy model do filtrowania danych
        self.proxy_model = QSortFilterProxyModel(self)
        self.proxy_model.setSourceModel(self.model)
        self.proxy_model.setFilterCaseSensitivity(Qt.CaseInsensitive)  # Ignorujemy wielkość liter

        # Tabela
        self.table = QTableView()
        self.table.setModel(self.proxy_model)
        self.table.setSortingEnabled(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)

        # Wiersz z filtrami
        self.add_filter_row()

        # Układ główny
        layout = QVBoxLayout()
        layout.addWidget(self.filter_row)
        layout.addWidget(self.table)
        self.setLayout(layout)

    def add_filter_row(self):
        # Tworzymy układ poziomy na filtry
        self.filter_row = QWidget()
        filter_layout = QHBoxLayout()
        filter_layout.setContentsMargins(0, 0, 0, 0)
        self.filter_inputs = []

        for col in range(self.model.columnCount()):
            filter_input = QLineEdit()
            filter_input.setPlaceholderText(f"Filtruj kolumnę {col + 1}")
            filter_input.textChanged.connect(lambda text, column=col: self.proxy_model.setFilterKeyColumn(column) or self.proxy_model.setFilterRegularExpression(text))
            filter_layout.addWidget(filter_input)
            self.filter_inputs.append(filter_input)

        self.filter_row.setLayout(filter_layout)


app = QApplication([])
window = FilterableTable()
window.show()
app.exec_()
