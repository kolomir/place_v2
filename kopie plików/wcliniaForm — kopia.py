from PyQt5.QtWidgets import QWidget, QTableWidgetItem,QHeaderView,QApplication,QMessageBox
from PyQt5.QtCore import pyqtSlot, Qt

from _wcliniaForm_ui import Ui_Form
import db

from wcliniaFormDodaj import MainWindow_wcliniaDodaj
from wcliniaFormEdytuj import MainWindow_wcliniaEdytuj

class MainWindow_wclinia(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.ui.btn_zapisz.clicked.connect(self.otworz_okno_wcFormDodaj)
        #self.ui.btn_kasuj.clicked.connect(self.kasuj_wiersz)
        self.ui.tab_dane.doubleClicked.connect(self.otworz_okno_wcFormEdytuj)
        QApplication.instance().focusChanged.connect(self.wyszukaj_dane)
        self.wyszukaj_dane()

    def wyszukaj_dane(self):
        select_data = "select gl.id, gr.nazwa, l.nazwa, gl.aktywny from gniazdo_linia gl left join linie l on l.id = gl.id_linia left join gniazda_robocze gr on gr.id = gl.id_gniazdo Order by gr.nazwa, l.nazwa;"
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
            wiersz += 1

        self.ui.tab_dane.horizontalHeader().setStretchLastSection(True)
        self.ui.tab_dane.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.ui.tab_dane.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.ui.tab_dane.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.ui.tab_dane.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)

    def naglowki_tabeli(self):
        self.ui.tab_dane.setColumnCount(4)  # Zmień na liczbę kolumn w twojej tabeli
        self.ui.tab_dane.setRowCount(0)  # Ustawienie liczby wierszy na 0
        self.ui.tab_dane.setHorizontalHeaderLabels([
            'ID',
            'Gniazdo',
            'Linia',
            'Aktywny'
        ])

    def clear_table(self):
        # Wyczyść zawartość tabeli
        self.ui.tab_dane.clearContents()
        self.ui.tab_dane.setRowCount(0)

    def otworz_okno_wcFormDodaj(self):
        self.okno_wcliniaFormDodaj = MainWindow_wcliniaDodaj()
        self.okno_wcliniaFormDodaj.show()

    @pyqtSlot()
    def otworz_okno_wcFormEdytuj(self):
        row = self.ui.tab_dane.currentRow()
        data = [self.ui.tab_dane.item(row, col).text() for col in range(self.ui.tab_dane.columnCount())]
        self.okno_wcliniaFormEdytuj = MainWindow_wcliniaEdytuj(data)
        self.okno_wcliniaFormEdytuj.setAttribute(Qt.WA_DeleteOnClose)  # Ensure the window is deleted when closed
        self.okno_wcliniaFormEdytuj.show()