from PyQt5.QtWidgets import QWidget, QTableWidgetItem,QHeaderView,QApplication
from PyQt5.QtCore import pyqtSlot, Qt

from _kpi_mag_ui import Ui_Form
import db, dodatki

from kpi_magDodaj import MainWindow_kpi_magDodaj

class MainWindow_kpi_mag(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.ui.btn_importuj.clicked.connect(self.otworz_okno_kpi_magDodaj)

        QApplication.instance().focusChanged.connect(self.wyszukaj_dane)
        self.wyszukaj_dane()

    def otworz_okno_kpi_magDodaj(self):
        self.okno_kpi_magDodaj = MainWindow_kpi_magDodaj()
        self.okno_kpi_magDodaj.show()

    def wyszukaj_dane(self):
        miestac_roboczy = dodatki.data_miesiac_dzis()
        select_data = "select * from kpi_mag where miesiac = '%s';" % (miestac_roboczy)
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
            self.ui.tab_dane.setItem(wiersz, 0, QTableWidgetItem(str(wynik[0])))
            self.ui.tab_dane.setItem(wiersz, 1, QTableWidgetItem(str(wynik[1])))
            self.ui.tab_dane.setItem(wiersz, 2, QTableWidgetItem(str(wynik[2])))
            self.ui.tab_dane.setItem(wiersz, 3, QTableWidgetItem(str(wynik[3])))
            self.ui.tab_dane.setItem(wiersz, 4, QTableWidgetItem(str(wynik[4])))
            self.ui.tab_dane.setItem(wiersz, 5, QTableWidgetItem(str(wynik[5])))
            self.ui.tab_dane.setItem(wiersz, 6, QTableWidgetItem(str(wynik[6])))
            self.ui.tab_dane.setItem(wiersz, 7, QTableWidgetItem(str(wynik[7])))
            self.ui.tab_dane.setItem(wiersz, 8, QTableWidgetItem(str(wynik[8])))
            wiersz += 1

        self.ui.tab_dane.horizontalHeader().setStretchLastSection(True)
        self.ui.tab_dane.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.ui.tab_dane.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.ui.tab_dane.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.ui.tab_dane.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.ui.tab_dane.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)
        self.ui.tab_dane.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeToContents)
        self.ui.tab_dane.horizontalHeader().setSectionResizeMode(7, QHeaderView.ResizeToContents)
        self.ui.tab_dane.horizontalHeader().setSectionResizeMode(8, QHeaderView.ResizeToContents)

    def naglowki_tabeli(self):
        self.ui.tab_dane.setColumnCount(9)  # Zmień na liczbę kolumn w twojej tabeli
        self.ui.tab_dane.setRowCount(0)  # Ustawienie liczby wierszy na 0
        self.ui.tab_dane.setHorizontalHeaderLabels([
            'ID',
            'Delivery',
            'Reklamacje',
            'DP po initial',
            'Zgodnosc',
            'Zapasy',
            'Raportowanie',
            'Miesiac',
            'Data dodania'
        ])

    def clear_table(self):
        # Wyczyść zawartość tabeli
        self.ui.tab_dane.clearContents()
        self.ui.tab_dane.setRowCount(0)