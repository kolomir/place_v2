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

        self.load_data_from_database()
        self.ui.btn_zapisz.clicked.connect(self.otworz_okno_progiProduktywnosciDodaj)
        self.ui.tab_dane.doubleClicked.connect(self.otworz_okno_progiProduktywnosciEdytuj)

        QApplication.instance().focusChanged.connect(self.load_data_from_database)

    def load_data_from_database(self):
        """Funkcja do załadowania danych z bazy do QTableWidget."""
        try:
            select_data = "select p.id, r.ranga, p.pulap1, p.kwota1, p.pulap2, p.kwota2, p.pulap3, p.kwota3, p.aktywny, p.data_dodania from progi_prod p left join ranga r on r.id = p.id_ranga order by r.ranga ASC;"
            connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
            results = db.read_query(connection, select_data)

            self.ui.tab_dane.setColumnCount(9)  # Zmień na liczbę kolumn w twojej tabeli
            self.ui.tab_dane.setRowCount(0)  # Ustawienie liczby wierszy na 0
            self.ui.tab_dane.setHorizontalHeaderLabels([
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