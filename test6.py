from PyQt5.QtWidgets import (
    QApplication, QTableWidget, QTableWidgetItem, QHeaderView, QMenu, QVBoxLayout, QCheckBox, QWidgetAction, QMainWindow
)
from PyQt5.QtCore import Qt, QPoint


class FilterableTable(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Filtrowanie wielokrotne jak w Excelu")
        self.resize(600, 400)

        # Tworzenie tabeli
        self.table = QTableWidget(10, 3, self)
        self.table.setHorizontalHeaderLabels(["Kolumna 1", "Kolumna 2", "Kolumna 3"])
        self.table.horizontalHeader().setSectionsClickable(True)
        self.table.horizontalHeader().sectionClicked.connect(self.show_filter_menu)

        # Wypełnianie tabeli przykładowymi danymi
        data = [
            ["A", "X", "1"],
            ["B", "Y", "2"],
            ["C", "Z", "3"],
            ["A", "Y", "4"],
            ["B", "X", "5"],
            ["C", "Z", "6"],
        ]
        for row, rowData in enumerate(data):
            for col, value in enumerate(rowData):
                self.table.setItem(row, col, QTableWidgetItem(value))

        self.setCentralWidget(self.table)

    def show_filter_menu(self, col):
        # Pobierz wszystkie unikalne wartości z danej kolumny
        values = sorted(
            set(
                self.table.item(row, col).text()
                for row in range(self.table.rowCount())
                if self.table.item(row, col)
            )
        )

        # Tworzenie menu filtrowania
        menu = QMenu(self)
        checkboxes = {}
        for value in values:
            checkbox = QCheckBox(value)
            checkbox.setChecked(True)  # Domyślnie wszystkie wartości są zaznaczone
            action = QWidgetAction(self)
            action.setDefaultWidget(checkbox)
            menu.addAction(action)
            checkboxes[checkbox] = value

        # Dodanie przycisku zastosuj do menu
        apply_action = menu.addAction("Zastosuj filtr")
        menu.addSeparator()
        clear_action = menu.addAction("Wyczyść filtr")

        # Wyświetlanie menu przy nagłówku kolumny
        header_pos = self.table.mapToGlobal(self.table.horizontalHeader().pos())
        section_pos = self.table.horizontalHeader().sectionPosition(col)
        menu_pos = header_pos + QPoint(section_pos, self.table.horizontalHeader().height())
        selected_action = menu.exec(menu_pos)

        if selected_action == apply_action:
            # Zastosowanie filtra
            selected_values = [value for checkbox, value in checkboxes.items() if checkbox.isChecked()]
            self.apply_filter(col, selected_values)
        elif selected_action == clear_action:
            # Wyczyszczenie filtra
            self.apply_filter(col, None)

    def apply_filter(self, col, selected_values):
        for row in range(self.table.rowCount()):
            item = self.table.item(row, col)
            if selected_values is None or (item and item.text() in selected_values):
                self.table.setRowHidden(row, False)
            else:
                self.table.setRowHidden(row, True)


if __name__ == "__main__":
    app = QApplication([])
    window = FilterableTable()
    window.show()
    app.exec_()
