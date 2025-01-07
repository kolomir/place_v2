from PyQt5.QtWidgets import QWidget, QTableWidgetItem,QHeaderView,QApplication
from PyQt5.QtCore import pyqtSlot, Qt

from _lokalizacjeForm_ui import Ui_Form
import db

from lokalizacjeFormDodaj import MainWindow_lokalizacjeDodaj
from lokalizacjeFormEdytuj import MainWindow_lokalizacjeEdytuj
# TODO: dostosować formularz - wymagany jest szerszy tak by nie przewijać
class MainWindow_lokalizacje(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.ui.btn_zapisz.clicked.connect(self.otworz_okno_lokalizacjeFormDodaj)
        self.ui.tab_dane.doubleClicked.connect(self.otworz_okno_lokalizacjeFormEdytuj)
        self.ui.tab_dane_nieaktywne.doubleClicked.connect(self.otworz_okno_lokalizacjeFormEdytuj_nieaktywne)

        QApplication.instance().focusChanged.connect(self.wyszukaj_dane_nieaktywne)
        QApplication.instance().focusChanged.connect(self.wyszukaj_dane)
        self.wyszukaj_dane()
        self.wyszukaj_dane_nieaktywne()

    def wyszukaj_dane(self):
        select_data = "SELECT * FROM lokalizacja where aktywny = 1;"
        connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
        results = db.read_query(connection, select_data)

        if not results:
            self.clear_table()
            self.naglowki_tabeli()
        else:
            self.naglowki_tabeli()
            self.pokaz_dane(results)
        connection.close()

    def pokaz_dane(self, rows):
        # Column count
        if int(len(rows[0])) > 0:
            self.ui.tab_dane.setColumnCount(int(len(rows[0])))

        # Row count
        self.ui.tab_dane.setRowCount(int(len(rows)))

        wiersz = 0
        for wynik in rows:
            print(wynik[0])
            self.ui.tab_dane.setItem(wiersz, 0, QTableWidgetItem(str(wynik[0])))
            self.ui.tab_dane.setItem(wiersz, 1, QTableWidgetItem(str(wynik[1])))
            self.ui.tab_dane.setItem(wiersz, 2, QTableWidgetItem(str(wynik[2])))
            wiersz += 1

        self.ui.tab_dane.horizontalHeader().setStretchLastSection(True)
        self.ui.tab_dane.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.ui.tab_dane.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.ui.tab_dane.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)

    def naglowki_tabeli(self):
        self.ui.tab_dane.setColumnCount(3)  # Zmień na liczbę kolumn w twojej tabeli
        self.ui.tab_dane.setRowCount(0)  # Ustawienie liczby wierszy na 0
        self.ui.tab_dane.setHorizontalHeaderLabels([
            'ID',
            'Lokalizacja',
            'Aktywny'
        ])

    def wyszukaj_dane_nieaktywne(self):
        select_data = "SELECT * FROM lokalizacja where aktywny = 0;"
        connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
        results = db.read_query(connection, select_data)

        if not results:
            self.clear_table()
            self.naglowki_tabeli_nieaktywne()
        else:
            self.naglowki_tabeli_nieaktywne()
            self.pokaz_dane_nieaktywne(results)
        connection.close()

    def pokaz_dane_nieaktywne(self, rows):
        # Column count
        if int(len(rows[0])) > 0:
            self.ui.tab_dane_nieaktywne.setColumnCount(int(len(rows[0])))

        # Row count
        self.ui.tab_dane_nieaktywne.setRowCount(int(len(rows)))

        wiersz = 0
        for wynik in rows:
            self.ui.tab_dane_nieaktywne.setItem(wiersz, 0, QTableWidgetItem(str(wynik[0])))
            self.ui.tab_dane_nieaktywne.setItem(wiersz, 1, QTableWidgetItem(str(wynik[1])))
            self.ui.tab_dane_nieaktywne.setItem(wiersz, 2, QTableWidgetItem(str(wynik[2])))
            wiersz += 1

        self.ui.tab_dane_nieaktywne.horizontalHeader().setStretchLastSection(True)
        self.ui.tab_dane_nieaktywne.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.ui.tab_dane_nieaktywne.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.ui.tab_dane_nieaktywne.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)

    def naglowki_tabeli_nieaktywne(self):
        self.ui.tab_dane.setColumnCount(3)  # Zmień na liczbę kolumn w twojej tabeli
        self.ui.tab_dane.setRowCount(0)  # Ustawienie liczby wierszy na 0
        self.ui.tab_dane.setHorizontalHeaderLabels([
            'ID',
            'Lokalizacja',
            'Aktywny'
        ])

    def clear_table(self):
        # Wyczyść zawartość tabeli
        self.ui.tab_dane.clearContents()
        self.ui.tab_dane.setRowCount(0)

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

    @pyqtSlot()
    def otworz_okno_lokalizacjeFormEdytuj_nieaktywne(self):
        row = self.ui.tab_dane_nieaktywne.currentRow()
        data = [self.ui.tab_dane_nieaktywne.item(row, col).text() for col in range(self.ui.tab_dane_nieaktywne.columnCount())]
        self.okno_lokalizacjeFormEdytuj = MainWindow_lokalizacjeEdytuj(data)
        self.okno_lokalizacjeFormEdytuj.setAttribute(Qt.WA_DeleteOnClose)  # Ensure the window is deleted when closed
        self.okno_lokalizacjeFormEdytuj.show()