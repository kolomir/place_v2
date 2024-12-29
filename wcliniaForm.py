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

        self.load_data_from_database()
        self.ui.btn_zapisz.clicked.connect(self.otworz_okno_wcFormDodaj)
        self.ui.tab_dane.doubleClicked.connect(self.otworz_okno_wcFormEdytuj)
        QApplication.instance().focusChanged.connect(self.load_data_from_database)

    def load_data_from_database(self):
        """Funkcja do załadowania danych z bazy do QTableWidget."""
        try:
            select_data = "select gl.id, gr.nazwa, l.nazwa, gl.aktywny from gniazdo_linia gl left join linie l on l.id = gl.id_linia left join gniazda_robocze gr on gr.id = gl.id_gniazdo Order by gr.nazwa, l.nazwa;"
            connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
            results = db.read_query(connection, select_data)

            self.ui.tab_dane.setColumnCount(3)  # Zmień na liczbę kolumn w twojej tabeli
            self.ui.tab_dane.setRowCount(0)  # Ustawienie liczby wierszy na 0
            self.ui.tab_dane.setHorizontalHeaderLabels([
                'Gniazdo',
                'Linia',
                'Aktywny'
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