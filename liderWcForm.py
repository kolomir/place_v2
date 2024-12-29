from PyQt5.QtWidgets import QWidget, QTableWidgetItem,QHeaderView,QApplication,QMessageBox
from PyQt5.QtCore import pyqtSlot, Qt

from _liderWcForm_ui import Ui_Form
import db, dodatki

from liderWcFormDodaj import MainWindow_liderWcDodaj
from liderWcFormEdytuj import MainWindow_liderWcEdytuj

class MainWindow_liderWc(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.load_data_from_database()
        self.ui.btn_zapisz.clicked.connect(self.otworz_okno_liderWcFormDodaj)
        self.ui.tab_dane.doubleClicked.connect(self.otworz_okno_liderWcFormEdytuj)
        QApplication.instance().focusChanged.connect(self.load_data_from_database)

    def load_data_from_database(self):
        """Funkcja do załadowania danych z bazy do QTableWidget."""
        try:
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
            # select_data = "select * from kpi_mag"
            connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
            results = db.read_query(connection, select_data)

            self.ui.tab_dane.setColumnCount(8)  # Zmień na liczbę kolumn w twojej tabeli
            self.ui.tab_dane.setRowCount(0)  # Ustawienie liczby wierszy na 0
            self.ui.tab_dane.setHorizontalHeaderLabels([
                'Nazwisko i imię',
                'Nr akt',
                'Ranga',
                'Lokalizacja',
                'Grupa robocza',
                'Aktywny',
                'Data dodania',
                'Data edycji'
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
            print(row_data[0] for row_data in results)

        except db.Error as e:
            print(f"Błąd przy pobieraniu danych z bazy danych: {e}")

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