from PyQt5.QtWidgets import QWidget, QFileDialog, QTableWidgetItem
from PyQt5.QtCore import Qt
import configparser
import openpyxl
from datetime import date, datetime
import os

from plik_pomoc_direct import MainWindow_pomoc_direct
from _direct_prod_ui import Ui_Form
import db, dodatki

from plik_pomoc_direct import MainWindow_pomoc_direct

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

class MainWindow_direct_prod(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.load_data_from_database()
        self.ui.btn_przegladaj.clicked.connect(self.open_file_dialog)
        self.ui.btn_importuj.clicked.connect(self.czytaj_dane)
        self.ui.btn_foto.clicked.connect(self.otworz_okno_plik_pomoc_direct)

    def load_data_from_database(self):
        """Funkcja do załadowania danych z bazy do QTableWidget."""
        try:
            miestac_roboczy = dodatki.data_miesiac_dzis()
            select_data = "SELECT * FROM `direct` WHERE miesiac = '%s';" % (miestac_roboczy)
            #select_data = "select * from kpi_mag"
            connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
            results = db.read_query(connection, select_data)

            self.ui.tab_dane.setSortingEnabled(True)

            self.ui.tab_dane.setColumnCount(13)  # Zmień na liczbę kolumn w twojej tabeli
            self.ui.tab_dane.setRowCount(0)  # Ustawienie liczby wierszy na 0
            self.ui.tab_dane.setHorizontalHeaderLabels([
                'Nr akt.',
                'Imię i Nazwisko',
                'Dział',
                'Worked',
                'Direct Work',
                'Direct %',
                'Indirect Work',
                'Indirect %',
                'Pause',
                'Diff',
                'Diff %',
                'Miesiąc',
                'Data dodania'
            ])

            # Ustawianie liczby wierszy na podstawie danych z bazy
            self.ui.tab_dane.setRowCount(len(results))


            # Wypełnianie tabeli danymi
            for row_idx, row_data in enumerate(results):
                # Przechowujemy id każdego wiersza
                for col_idx, value in enumerate(row_data[1:]):  # Pomijamy id
                    item = NumericTableWidgetItem(str(value))              # Użycie klasy soryującej dane numeryczne
                    self.ui.tab_dane.setItem(row_idx, col_idx, item)

                    # Ustawianie wyrównania
                    #if col_idx == 0 or col_idx == 1 or col_idx == 2 or col_idx == 3 or col_idx == 4:
                    item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    # Kolumna 1: do lewej               (Qt.AlignLeft | Qt.AlignVCenter)
                    # Kolumna 2: wyśrodkowane           (Qt.AlignHCenter | Qt.AlignVCenter)
                    # Kolumna 3: do prawej              (Qt.AlignRight | Qt.AlignVCenter)

                    self.ui.tab_dane.setColumnWidth(0, 75)  # Stała szerokość: 150 pikseli
                    self.ui.tab_dane.setColumnWidth(1, 200)  # Stała szerokość: 150 pikseli
                    self.ui.tab_dane.setColumnWidth(2, 75)  # Stała szerokość: 150 pikseli
                    self.ui.tab_dane.setColumnWidth(3, 75)  # Stała szerokość: 150 pikseli
                    self.ui.tab_dane.setColumnWidth(4, 75)  # Stała szerokość: 150 pikseli
                    self.ui.tab_dane.setColumnWidth(5, 75)  # Stała szerokość: 150 pikseli
                    self.ui.tab_dane.setColumnWidth(6, 75)  # Stała szerokość: 150 pikseli
                    self.ui.tab_dane.setColumnWidth(7, 75)  # Stała szerokość: 150 pikseli
                    self.ui.tab_dane.setColumnWidth(8, 75)  # Stała szerokość: 150 pikseli
                    self.ui.tab_dane.setColumnWidth(9, 75)  # Stała szerokość: 150 pikseli
                    self.ui.tab_dane.setColumnWidth(10, 75)  # Stała szerokość: 150 pikseli
                    self.ui.tab_dane.setColumnWidth(11, 75)  # Stała szerokość: 150 pikseli
                    self.ui.tab_dane.setColumnWidth(12, 150)  # Stała szerokość: 150 pikseli

            # Przechowywanie id wierszy
            self.row_ids = [row_data[0] for row_data in results]
            #print(row_data[0] for row_data in results)

        except db.Error as e:
            print(f"Błąd przy pobieraniu danych z bazy danych: {e}")

    def open_file_dialog(self):
        # Otwieranie dialogu wyboru pliku
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Wybierz plik Excel", "", "Pliki tekstowe (*.xlsx);;Wszystkie pliki (*)", options=options)
        if file_path:
            self.ui.ed_sciezka_dane.setText(file_path)  # Ustawienie ścieżki w polu tekstowym

    def load_from_path(self):
        # Wczytanie pliku z ręcznie wpisanej ścieżki
        file_path = self.ui.ed_sciezka_dane.text()
        if file_path:
            self.load_file(file_path)

    def sprawdz_wpisy(self):
        try:
            miestac_roboczy = dodatki.data_miesiac_dzis()
            select_data = "SELECT * FROM `direct` WHERE miesiac = '%s';" % (miestac_roboczy)  # (miestac_roboczy)
            connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
            results = db.read_query(connection, select_data)
            connection.close()

            connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
            if results:
                for x in results:
                    delete_data = "delete from direct where id = '%s' and miesiac = '%s';" % (x[0],miestac_roboczy)
                    print('Do skasowania:',delete_data)
                    db.execute_query(connection, delete_data)
            else:
                print('--Brak wpisów jeszcze--')
            connection.close()

        except db.Error as e:
            print(f"Błąd przy pobieraniu danych z bazy danych: {e}")

    def czytaj_dane(self):
        try:
            if not self.folder_istnieje():
                return
            self.sprawdz_wpisy()
            file_path = self.ui.ed_sciezka_dane.text()
            wb = openpyxl.load_workbook(os.path.join(file_path))
            sheet = wb.active
            teraz = datetime.today()
            data_miesiac = str(dodatki.data_miesiac_dzis())
            print(data_miesiac)

            lista_wpisow = []

            #czytamy wszystkie kolumny i wiersze ze wskazanego pliku
            for row in sheet.iter_rows(min_row=2, min_col=1, max_col=25, values_only=True):
                #sprawdzamy czy wiersz nie jest pusty (zakładając że pusty wiersz ma wszystkie kolumny o wartosci None i kończy zestawienie)
                if any(cell is not None for cell in row):
                    nr_akt = int(row[0])
                    dep = int(row[2])
                    worked = round(row[7], 2)
                    direct_work = round(row[8], 2)
                    direct = round(row[9], 2)
                    indirect_work = round(row[10], 2)
                    indirect = round(row[11], 2)
                    pause = round(row[12], 2)
                    diff_hr = round(row[13], 2)
                    diff = round(row[14], 2)
                    lista_wpisow.append([nr_akt,row[1],dep,worked,direct_work,direct,indirect_work,indirect,pause,diff_hr,diff,data_miesiac,teraz])
                else:
                    break

            connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)

            for row in lista_wpisow:
                insert_data = "INSERT INTO direct VALUES (NULL,'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s');" % (row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12])
                db.execute_query(connection, insert_data)

            self.load_data_from_database()

        except db.Error as e:
            print(f"Błąd przy pobieraniu danych z bazy danych: {e}")

    def otworz_okno_plik_pomoc_direct(self):
        self.okno_plik_pomoc_direct = MainWindow_pomoc_direct()
        self.okno_plik_pomoc_direct.show()