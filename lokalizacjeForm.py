from PyQt5.QtWidgets import QWidget, QTableWidgetItem,QHeaderView,QApplication
from PyQt5.QtCore import pyqtSlot, Qt

from _lokalizacjeForm_ui import Ui_Form
import db

from lokalizacjeFormDodaj import MainWindow_lokalizacjeDodaj
from lokalizacjeFormEdytuj import MainWindow_lokalizacjeEdytuj

class MainWindow_lokalizacje(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.load_data_from_database()
        self.ui.btn_zapisz.clicked.connect(self.otworz_okno_lokalizacjeFormDodaj)
        self.ui.tab_dane.doubleClicked.connect(self.otworz_okno_lokalizacjeFormEdytuj)
        QApplication.instance().focusChanged.connect(self.load_data_from_database)

    def load_data_from_database(self):
        """Funkcja do załadowania danych z bazy do QTableWidget."""
        try:
            select_data = "SELECT * FROM lokalizacja where aktywny = 1;"
            #select_data = "select * from kpi_mag"
            connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
            results = db.read_query(connection, select_data)

            self.ui.tab_dane.setColumnCount(2)  # Zmień na liczbę kolumn w twojej tabeli
            self.ui.tab_dane.setRowCount(0)  # Ustawienie liczby wierszy na 0
            self.ui.tab_dane.setHorizontalHeaderLabels([
                'Lokalizacja',
                'Aktywny'
            ])

            # Ustawianie liczby wierszy na podstawie danych z bazy
            self.ui.tab_dane.setRowCount(len(results))


            # Wypełnianie tabeli danymi
            for row_idx, row_data in enumerate(results):
                # Przechowujemy id każdego wiersza
                for col_idx, value in enumerate(row_data[1:]):  # Pomijamy id
                    item = QTableWidgetItem(str(value))
                    if col_idx == 6 or col_idx == 7:  # Zablokowanie edycji dla kolumny "nazwa"
                        item.setFlags(item.flags() & ~Qt.ItemIsEditable)  # Usuwamy flagę edytowalności
                    else:
                        item.setFlags(item.flags() | Qt.ItemIsEditable)  # Ustawienie komórek jako edytowalne
                    print(row_idx, col_idx, item.text())
                    self.ui.tab_dane.setItem(row_idx, col_idx, item)

            # Przechowywanie id wierszy
            self.row_ids = [row_data[0] for row_data in results]
            print(row_data[0] for row_data in results)

        except db.Error as e:
            print(f"Błąd przy pobieraniu danych z bazy danych: {e}")

    def otworz_okno_lokalizacjeFormDodaj(self):
        self.okno_lokalizacjeFormDodaj = MainWindow_lokalizacjeDodaj()
        self.okno_lokalizacjeFormDodaj.show()

    @pyqtSlot()
    def otworz_okno_lokalizacjeFormEdytuj(self):
        row = self.ui.tab_dane.currentRow()
        data = [self.ui.tab_dane.item(row, col).text() for col in range(self.ui.tab_dane.columnCount())]
        self.okno_lokalizacjeFormEdytuj = MainWindow_lokalizacjeEdytuj(data)
        self.okno_lokalizacjeFormEdytuj.setAttribute(Qt.WA_DeleteOnClose)  # Ensure the window is deleted when closed
        self.okno_lokalizacjeFormEdytuj.show()