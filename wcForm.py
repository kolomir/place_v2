from PyQt5.QtWidgets import QWidget, QTableWidgetItem,QHeaderView,QApplication
from PyQt5.QtCore import pyqtSlot, Qt

from _wcForm_ui import Ui_Form
import db

from wcFormDodaj import MainWindow_wcDodaj
from wcFormEdytuj import MainWindow_wcEdytuj

# klasa która pozwala na poprawne sortowanie danych w kolumnach numerycznych.
# Normalnie dane układają się w sposób 1,10,11,2,23,245
# Po zastosowaniu klasy dane posortują się w sposób 1,2,10,11,23,245
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

class MainWindow_wc(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.load_data_from_database()
        self.ui.btn_zapisz.clicked.connect(self.otworz_okno_wcFormDodaj)
        self.ui.tab_dane.doubleClicked.connect(self.otworz_okno_linieFormEdytuj)
        QApplication.instance().focusChanged.connect(self.load_data_from_database)

    def load_data_from_database(self):
        """Funkcja do załadowania danych z bazy do QTableWidget."""
        try:
            select_data = "SELECT * FROM gniazda_robocze;"
            connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
            results = db.read_query(connection, select_data)

            self.ui.tab_dane.setSortingEnabled(True)

            self.ui.tab_dane.setColumnCount(2)  # Zmień na liczbę kolumn w twojej tabeli
            self.ui.tab_dane.setRowCount(0)  # Ustawienie liczby wierszy na 0
            self.ui.tab_dane.setHorizontalHeaderLabels([
                'Gniazdo',
                'Aktywny'
            ])

            # Ustawianie liczby wierszy na podstawie danych z bazy
            self.ui.tab_dane.setRowCount(len(results))

            # Wypełnianie tabeli danymi
            for row_idx, row_data in enumerate(results):
                # Przechowujemy id każdego wiersza
                for col_idx, value in enumerate(row_data[1:]):  # Pomijamy id
                    item = NumericTableWidgetItem(str(value))              # Użycie klasy soryującej dane numeryczne

                    item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

                    self.ui.tab_dane.setColumnWidth(0, 75)  # Stała szerokość: 150 pikseli
                    self.ui.tab_dane.setColumnWidth(1, 75)  # Stała szerokość: 150 pikseli

                    self.ui.tab_dane.setItem(row_idx, col_idx, item)

            # Przechowywanie id wierszy
            self.row_ids = [row_data[0] for row_data in results]
            #print(row_data[0] for row_data in results)

        except db.Error as e:
            print(f"Błąd przy pobieraniu danych z bazy danych: {e}")

    def otworz_okno_wcFormDodaj(self):
        self.okno_wcFormDodaj = MainWindow_wcDodaj()
        self.okno_wcFormDodaj.show()

    @pyqtSlot()
    def otworz_okno_linieFormEdytuj(self):
        row = self.ui.tab_dane.currentRow()
        data = [self.ui.tab_dane.item(row, col).text() for col in range(self.ui.tab_dane.columnCount())]
        self.okno_wcFormEdytuj = MainWindow_wcEdytuj(data)
        self.okno_wcFormEdytuj.setAttribute(Qt.WA_DeleteOnClose)  # Ensure the window is deleted when closed
        self.okno_wcFormEdytuj.show()