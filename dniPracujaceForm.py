from PyQt5.QtWidgets import QWidget, QTableWidgetItem,QHeaderView,QApplication
from PyQt5.QtCore import pyqtSlot, Qt

import dodatki
from _dniPracujaceForm_ui import Ui_Form
import db
from datetime import date, datetime

from dniPracujaceFormDodaj import MainWindow_dniPracujaceFormDodaj

class NumericTableWidgetItem(QTableWidgetItem):
    def __lt__(self, other):
        # Sprawdzamy, czy drugi element też jest instancją QTableWidgetItem
        if isinstance(other, QTableWidgetItem):
            try:
                # Porównujemy jako liczby
                return float(self.text()) < float(other.text())
            except ValueError:
                # W przypadku błędu porównujemy jako tekst
                return self.text() < other.text()
        return super().__lt__(other)

class MainWindow_dniPracujaceForm(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.combo_rok()
        self.load_data_from_database()
        self.ui.btn_zapisz.clicked.connect(self.otworz_okno_dniPracujaceFormDodaj)

    def load_data_from_database(self):
        """Funkcja do załadowania danych z bazy do QTableWidget."""
        try:
            combo_rok_text = self.ui.comboRok.currentText()

            select_data = "select d.id, d.miesiac, d.godziny_pracy, d.dni_pracy, d.dni_wolne from dni_pracujace_w_roku d WHERE rok = %s;" % (combo_rok_text)
            connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
            results = db.read_query(connection, select_data)

            self.ui.tab_dane.setSortingEnabled(True)

            self.ui.tab_dane.setColumnCount(5)  # Zmień na liczbę kolumn w twojej tabeli
            self.ui.tab_dane.setRowCount(0)  # Ustawienie liczby wierszy na 0
            self.ui.tab_dane.setHorizontalHeaderLabels([
                'ID',
                'Miesiac',
                'Godziny Pracy',
                'Dni Pracy',
                'Dni Wolne'
            ])

            lista = []
            for dane in results:
                miesiac = dodatki.nazwy_miesiecy[dane[1] - 1]
                lista.append([dane[0], miesiac, dane[2], dane[3], dane[4]])

            # Ustawianie liczby wierszy na podstawie danych z bazy
            self.ui.tab_dane.setRowCount(len(lista))


            # Wypełnianie tabeli danymi
            for row_idx, row_data in enumerate(lista):
                # Przechowujemy id każdego wiersza
                for col_idx, value in enumerate(row_data):
                    item = NumericTableWidgetItem(str(value))              # Użycie klasy soryującej dane numeryczne

                    item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

                    self.ui.tab_dane.setColumnWidth(0, 75)  # Stała szerokość: 150 pikseli
                    self.ui.tab_dane.setColumnWidth(1, 75)  # Stała szerokość: 150 pikseli
                    self.ui.tab_dane.setColumnWidth(2, 75)  # Stała szerokość: 150 pikseli
                    self.ui.tab_dane.setColumnWidth(3, 75)  # Stała szerokość: 150 pikseli
                    self.ui.tab_dane.setColumnWidth(4, 75)  # Stała szerokość: 150 pikseli

                    self.ui.tab_dane.setItem(row_idx, col_idx, item)

            # Przechowywanie id wierszy
            self.row_ids = [row_data[0] for row_data in lista]
            #print(row_data[0] for row_data in lista)

        except db.Error as e:
            print(f"Błąd przy pobieraniu danych z bazy danych: {e}")

    def combo_rok(self):
        select_data_linie = "SELECT rok FROM dni_pracujace_w_roku GROUP BY rok;"
        connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
        results = db.read_query(connection, select_data_linie)

        # Aktualna data
        dzisiaj = datetime.now()

        # Obliczenie przesuniętego miesiąca i roku
        miesiac = dzisiaj.month - 1
        rok = dzisiaj.year
        dzien = 1

        # Obsługa zmiany roku, jeśli przesunięcie powoduje przejście do stycznia
        if miesiac < 1:
            miesiac = 12
            rok -= 1

        # Tworzenie nowej daty z przesuniętym miesiącem
        przesunieta_data = dzisiaj.replace(year=rok, month=miesiac, day=dzien)

        # Wyświetlenie roku z przesuniętej daty
        ten_rok = przesunieta_data.year

        lata = []
        for wynik in results:
            lata.append(wynik[0])
            self.ui.comboRok.addItem(str(wynik[0]))

        if ten_rok in lata:
            self.ui.comboRok.setCurrentText(str(ten_rok))
        else:
            self.ui.comboRok.setCurrentIndex(0)  # domyślnie pierwszy element

    def otworz_okno_dniPracujaceFormDodaj(self):
        self.okno_dniPracujaceFormDodaj = MainWindow_dniPracujaceFormDodaj()
        self.okno_dniPracujaceFormDodaj.show()