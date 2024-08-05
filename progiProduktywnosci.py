from PyQt5.QtWidgets import QWidget, QTableWidgetItem,QHeaderView,QApplication
from PyQt5.QtCore import pyqtSlot, Qt

from _progiProduktywnosci_ui import Ui_Form
import db

from progiProduktywnosciDodaj import MainWindow_progiProduktywnosciDodaj
from progiProduktywnosciEdytuj import MainWindow_progiProduktywnosciEdytuj

class MainWindow_progiProduktywnosci(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.ui.btn_zapisz.clicked.connect(self.otworz_okno_progiProduktywnosciDodaj)
        self.ui.tab_dane.doubleClicked.connect(self.otworz_okno_progiProduktywnosciEdytuj)

        QApplication.instance().focusChanged.connect(self.wyszukaj_dane)
        self.wyszukaj_dane()

    def wyszukaj_dane(self):
        select_data = "select p.id, r.ranga, p.pulap1, p.kwota1, p.pulap2, p.kwota2, p.pulap3, p.kwota3, p.aktywny, p.data_dodania from progi_prod p left join ranga r on r.id = p.id_ranga order by r.ranga ASC;"
        #select_data = "select * from progi_prod p;"
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
            self.ui.tab_dane.setItem(wiersz, 9, QTableWidgetItem(str(wynik[9])))
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
        self.ui.tab_dane.horizontalHeader().setSectionResizeMode(9, QHeaderView.ResizeToContents)

    def naglowki_tabeli(self):
        self.ui.tab_dane.setColumnCount(10)  # Zmień na liczbę kolumn w twojej tabeli
        self.ui.tab_dane.setRowCount(0)  # Ustawienie liczby wierszy na 0
        self.ui.tab_dane.setHorizontalHeaderLabels([
            'ID',
            'Ranga',
            'Pułap1',
            'Kwota1',
            'Pułap2',
            'Kwota2',
            'Pułap3',
            'Kwota3',
            'Aktywny',
            'Dodano'
        ])

    def clear_table(self):
        # Wyczyść zawartość tabeli
        self.ui.tab_dane.clearContents()
        self.ui.tab_dane.setRowCount(0)

    def otworz_okno_progiProduktywnosciDodaj(self):
        self.okno_progiProduktywnosciDodaj = MainWindow_progiProduktywnosciDodaj()
        self.okno_progiProduktywnosciDodaj.show()

    @pyqtSlot()
    def otworz_okno_progiProduktywnosciEdytuj(self):
        row = self.ui.tab_dane.currentRow()
        data = [self.ui.tab_dane.item(row, col).text() for col in range(self.ui.tab_dane.columnCount())]
        self.okno_progiProduktywnosciEdytuj = MainWindow_progiProduktywnosciEdytuj(data)
        self.okno_progiProduktywnosciEdytuj.setAttribute(Qt.WA_DeleteOnClose)  # Ensure the window is deleted when closed
        self.okno_progiProduktywnosciEdytuj.show()