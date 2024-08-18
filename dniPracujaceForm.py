from PyQt5.QtWidgets import QWidget, QTableWidgetItem,QHeaderView,QApplication
from PyQt5.QtCore import pyqtSlot, Qt

import dodatki
from _dniPracujaceForm_ui import Ui_Form
import db
from datetime import date, datetime

from dniPracujaceFormDodaj import MainWindow_dniPracujaceFormDodaj

class MainWindow_dniPracujaceForm(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.ui.btn_zapisz.clicked.connect(self.otworz_okno_dniPracujaceFormDodaj)
        self.combo_rok()

        QApplication.instance().focusChanged.connect(self.wyszukaj_dane)
        self.wyszukaj_dane()

    def wyszukaj_dane(self):

        combo_rok_text = self.ui.comboRok.currentText()

        select_data = "select d.id, d.miesiac, d.godziny_pracy, d.dni_pracy, d.dni_wolne from dni_pracujace_w_roku d WHERE rok = %s;" % combo_rok_text
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
            miesiac = dodatki.nazwy_miesiecy[wynik[1]-1]
            self.ui.tab_dane.setItem(wiersz, 0, QTableWidgetItem(str(wynik[0])))
            self.ui.tab_dane.setItem(wiersz, 1, QTableWidgetItem(str(miesiac)))
            self.ui.tab_dane.setItem(wiersz, 2, QTableWidgetItem(str(wynik[2])))
            self.ui.tab_dane.setItem(wiersz, 3, QTableWidgetItem(str(wynik[3])))
            self.ui.tab_dane.setItem(wiersz, 4, QTableWidgetItem(str(wynik[4])))
            wiersz += 1

        self.ui.tab_dane.horizontalHeader().setStretchLastSection(True)
        self.ui.tab_dane.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.ui.tab_dane.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.ui.tab_dane.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.ui.tab_dane.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.ui.tab_dane.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)

    def naglowki_tabeli(self):
        self.ui.tab_dane.setColumnCount(5)  # Zmień na liczbę kolumn w twojej tabeli
        self.ui.tab_dane.setRowCount(0)  # Ustawienie liczby wierszy na 0
        self.ui.tab_dane.setHorizontalHeaderLabels([
            'ID',
            'Miesiac',
            'Godziny Pracy',
            'Dni Pracy',
            'Dni Wolne'
        ])

    def clear_table(self):
        # Wyczyść zawartość tabeli
        self.ui.tab_dane.clearContents()
        self.ui.tab_dane.setRowCount(0)

    def otworz_okno_dniPracujaceFormDodaj(self):
        self.okno_dniPracujaceFormDodaj = MainWindow_dniPracujaceFormDodaj()
        self.okno_dniPracujaceFormDodaj.show()

    def combo_rok(self):
        select_data_linie = "SELECT rok FROM dni_pracujace_w_roku GROUP BY rok;"
        connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
        results = db.read_query(connection, select_data_linie)

        ten_rok = datetime.today().year

        lata = []
        for wynik in results:
            lata.append(wynik[0])
            self.ui.comboRok.addItem(str(wynik[0]))

        if ten_rok in lata:
            self.ui.comboRok.setCurrentText(str(ten_rok))
        else:
            self.ui.comboRok.setCurrentIndex(0)  # domyślnie pierwszy element