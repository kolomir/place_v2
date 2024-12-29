from PyQt5.QtWidgets import QWidget, QTableWidgetItem,QHeaderView,QApplication
from PyQt5.QtCore import pyqtSlot, Qt

from _wytyczne_mag_ui import Ui_Form
import db

from wytyczne_magDodaj import MainWindow_wytyczne_magDodaj
from linieFormEdytuj import MainWindow_linieEdytuj

class MainWindow_wytyczne_mag(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.load_data_from_database()
        self.ui.btn_zapisz.clicked.connect(self.otworz_okno_wytyczne_magDodaj)

        QApplication.instance().focusChanged.connect(self.load_data_from_database)

    def load_data_from_database(self):
        """Funkcja do załadowania danych z bazy do QTableWidget."""
        try:
            select_data = "select wm.id, gm.nazwa, wm.kwota , wm.nazwa1, wm.target1, wm.jednostka1, wm.nazwa2, wm.target2, wm.jednostka2, wm.data_edycji from wytyczne_mag wm left join grupy_mag gm on gm.id = wm.id_grupa where wm.aktywny = 1;"
            connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
            results = db.read_query(connection, select_data)

            self.ui.tab_dane.setColumnCount(9)  # Zmień na liczbę kolumn w twojej tabeli
            self.ui.tab_dane.setRowCount(0)  # Ustawienie liczby wierszy na 0
            self.ui.tab_dane.setHorizontalHeaderLabels([
                'Grupa',
                'Kwota',
                'Nazwa KPI',
                'Target',
                'Jednostka',
                'Nazwa KPI dodatkowego',
                'Target',
                'Jednostka',
                'Data dodania'
            ])

            # Ustawianie liczby wierszy na podstawie danych z bazy
            self.ui.tab_dane.setRowCount(len(results))


            # Wypełnianie tabeli danymi
            for row_idx, row_data in enumerate(results):
                # Przechowujemy id każdego wiersza
                for col_idx, value in enumerate(row_data[1:]):  # Pomijamy id
                    item = QTableWidgetItem(str(value))
                    self.ui.tab_dane.setItem(row_idx, col_idx, item)

            # Przechowywanie id wierszy
            self.row_ids = [row_data[0] for row_data in results]
            #print(row_data[0] for row_data in results)

        except db.Error as e:
            print(f"Błąd przy pobieraniu danych z bazy danych: {e}")

    def otworz_okno_wytyczne_magDodaj(self):
        self.okno_wytyczne_magDodaj = MainWindow_wytyczne_magDodaj()
        self.okno_wytyczne_magDodaj.show()