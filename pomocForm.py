from PyQt5.QtWidgets import QWidget, QTableWidgetItem,QHeaderView,QApplication
from PyQt5.QtCore import pyqtSlot, Qt

from _pomocForm_ui import Ui_Form
import db

from pomocFormDodaj import MainWindow_pomocFormDodaj

class MainWindow_pomocForm(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.load_data_from_database()
        self.ui.btn_zapisz.clicked.connect(self.otworz_okno_pomocFormDodaj)
        #self.ui.tab_dane.doubleClicked.connect(self.otworz_okno_linieFormEdytuj)

        QApplication.instance().focusChanged.connect(self.load_data_from_database)

    def load_data_from_database(self):
        """Funkcja do załadowania danych z bazy do QTableWidget."""
        try:
            select_data = '''select 
                                        i.nazwisko 
                                        ,i.imie 
                                        ,i.nr_akt 
                                        ,l.nazwa 
                                        ,wp.aktywny 
                                        ,wp.data_dodania 
                                        ,wp.data_edycji 
                                    from 
                                        wsparcie_produkcji wp 
                                            left join instruktor i on i.id = wp.id_pracownik 
                                            left join linie l on l.id = wp.id_linia;'''
            connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
            results = db.read_query(connection, select_data)

            self.ui.tab_dane.setColumnCount(5)  # Zmień na liczbę kolumn w twojej tabeli
            self.ui.tab_dane.setRowCount(0)  # Ustawienie liczby wierszy na 0
            self.ui.tab_dane.setHorizontalHeaderLabels([
                'Nazwisko',
                'Imie',
                'Nr akt',
                'Linia',
                'aktywny'
            ])

            # Ustawianie liczby wierszy na podstawie danych z bazy
            self.ui.tab_dane.setRowCount(len(results))


            # Wypełnianie tabeli danymi
            for row_idx, row_data in enumerate(results):
                # Przechowujemy id każdego wiersza
                for col_idx, value in enumerate(row_data[0:]):  # Pomijamy id
                    item = QTableWidgetItem(str(value))
                    self.ui.tab_dane.setItem(row_idx, col_idx, item)

            # Przechowywanie id wierszy
            self.row_ids = [row_data[0] for row_data in results]
            print(row_data[0] for row_data in results)

        except db.Error as e:
            print(f"Błąd przy pobieraniu danych z bazy danych: {e}")

    def otworz_okno_pomocFormDodaj(self):
        self.okno_pomocFormDodaj = MainWindow_pomocFormDodaj()
        self.okno_pomocFormDodaj.show()