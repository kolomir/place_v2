from PyQt5.QtWidgets import QWidget, QTableWidgetItem,QHeaderView,QApplication,QMessageBox
from PyQt5.QtCore import pyqtSlot, Qt

from _liderWcForm_ui import Ui_Form
import db

from liderWcFormDodaj import MainWindow_liderWcDodaj
from liderWcFormEdytuj import MainWindow_liderWcEdytuj

class MainWindow_liderWc(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.ui.btn_zapisz.clicked.connect(self.otworz_okno_liderWcFormDodaj)
        self.ui.tab_dane.doubleClicked.connect(self.otworz_okno_liderWcFormEdytuj)
        QApplication.instance().focusChanged.connect(self.wyszukaj_dane)
        self.wyszukaj_dane()

    def wyszukaj_dane(self):
        select_data = """
                        select 
                            lg.id 
                            ,concat(i.nazwisko,' ',i.imie) as 'Nazwisko i imię'
                            ,i.nr_akt 
                            ,r.ranga 
                            ,l.lokalizacja 
                            ,gr.nazwa 
                            ,lg.aktywny 
                            ,lg.data_dodania 
                            ,lg.data_edycji 
                        from 
                            linia_gniazdo lg 
                                left join instruktor i on i.id = lg.id_lider
                                    left join ranga r on r.id = i.id_ranga 
                                left join lokalizacja l on l.id = lg.id_lokalizacja 
                                left join gniazda_robocze gr on gr.id = lg.id_grupa 
                        where 
                            l.aktywny = 1 or i.aktywny = 1 or gr.aktywna = 1
                """
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
        self.ui.tab_dane.horizontalHeader().setSectionResizeMode(6, QHeaderView.ResizeToContents)
        self.ui.tab_dane.horizontalHeader().setSectionResizeMode(7, QHeaderView.ResizeToContents)
        self.ui.tab_dane.horizontalHeader().setSectionResizeMode(8, QHeaderView.ResizeToContents)

    def naglowki_tabeli(self):
        self.ui.tab_dane.setColumnCount(9)  # Zmień na liczbę kolumn w twojej tabeli
        self.ui.tab_dane.setRowCount(0)  # Ustawienie liczby wierszy na 0
        self.ui.tab_dane.setHorizontalHeaderLabels([
            'ID',
            'Nazwisko i imię',
            'Nr akt',
            'Ranga',
            'Lokalizacja',
            'Grupa robocza',
            'Aktywny',
            'Data dodania',
            'Data edycji'
        ])

    def clear_table(self):
        # Wyczyść zawartość tabeli
        self.ui.tab_dane.clearContents()
        self.ui.tab_dane.setRowCount(0)

    def otworz_okno_liderWcFormDodaj(self):
        self.okno_liderWcFormDodaj = MainWindow_liderWcDodaj()
        self.okno_liderWcFormDodaj.show()

    @pyqtSlot()
    def otworz_okno_liderWcFormEdytuj(self):
        row = self.ui.tab_dane.currentRow()
        data = [self.ui.tab_dane.item(row, col).text() for col in range(self.ui.tab_dane.columnCount())]
        self.okno_liderWcFormEdytuj = MainWindow_liderWcEdytuj(data)
        self.okno_liderWcFormEdytuj.setAttribute(Qt.WA_DeleteOnClose)  # Ensure the window is deleted when closed
        self.okno_liderWcFormEdytuj.show()