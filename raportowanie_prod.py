from PyQt5.QtWidgets import QWidget, QMessageBox, QFileDialog, QTableWidgetItem, QHeaderView
import configparser
import openpyxl
from datetime import date, datetime
import os

from plik_pomoc_raportowanie_prod import MainWindow_pomoc_raportowanie_prod
from _raportowanie_prod_ui import Ui_Form
import db, dodatki

class MainWindow_raportowanie_prod(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.load_data_from_database()

    def load_data_from_database(self):
        """Funkcja do załadowania danych z bazy do QTableWidget."""
        try:
            miestac_roboczy = dodatki.data_miesiac_dzis()
            select_data = "SELECT * FROM `logowanie_zlecen` WHERE miesiac = '%s';" % (miestac_roboczy)
            # select_data = "select * from kpi_mag"
            connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
            results = db.read_query(connection, select_data)

            self.ui.tab_dane.setColumnCount(18)  # Zmień na liczbę kolumn w twojej tabeli
            self.ui.tab_dane.setRowCount(0)  # Ustawienie liczby wierszy na 0
            self.ui.tab_dane.setHorizontalHeaderLabels([
                'Zlecenie',
                'Wiązka',
                'Operacja',
                'Miesiąc raportu',
                'Nr raportu',
                'Nr akt',
                'Raportowany',
                'Raporty All',
                'Planowany',
                'Planowany All',
                'Imie',
                'Nazwisko',
                'Grupa',
                'Zmiana',
                'Zmiana lit',
                'Wydajność',
                'Miesiąc',
                'Data dodania'
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

    def otworz_okno_plik_pomoc_raportowanie_prod(self):
        self.okno_plik_pomoc_raportowanie_prod = MainWindow_pomoc_raportowanie_prod()
        self.okno_plik_pomoc_raportowanie_prod.show()

    def czysc_string_int(self, tekst):
        wynik = int(tekst.replace(' ',''))
        return wynik

    def czysc_string_dec(self, tekst):
        wynik = tekst.replace(' ', '')
        wynik = wynik.replace(',', '.')
        return wynik

    def czytaj_dane(self):
        if not self.folder_istnieje():
            return
        self.sprawdz_wpisy()
        file_path = self.ui.ed_sciezka_dane.text()
        wb = openpyxl.load_workbook(os.path.join(file_path))
        sheet = wb.active
        teraz = datetime.today()
        data_miesiac = str(dodatki.data_miesiac_dzis())
        #print(data_miesiac)

        lista_wpisow = []

        i = 1
        #czytamy wszystkie kolumny i wiersze ze wskazanego pliku
        for row in sheet.iter_rows(min_row=2, min_col=1, max_col=14, values_only=True):
            #sprawdzamy czy wiersz nie jest pusty (zakładając że pusty wiersz ma wszystkie kolumny o wartosci None i kończy zestawienie)
            if any(cell is not None for cell in row):
                if len(row[13]) == 4:
                    zmiana_lit = row[13][3]
                else:
                    zmiana_lit = 'inna'
                wydajnosc = 0
                if row[6] == '' or row[6] < 0:
                    wydajnosc = 0
                elif row[6] > 0 and row[8] == 0:
                    wydajnosc = 0
                elif row[6] > 0 and row[8] == '':
                    wydajnosc = 0
                elif row[6] == 0:
                    wydajnosc = 0
                else:
                    wydajnosc = row[6] / row[8]
                #print(i,[row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12],wydajnosc,data_miesiac,teraz])
                lista_wpisow.append([row[0],row[1],row[2],data_miesiac,row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12],row[13],zmiana_lit,wydajnosc,data_miesiac,teraz])
                i=i+1
            else:
                break

        connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)

        for row in lista_wpisow:
            insert_data = "INSERT INTO logowanie_zlecen VALUES (NULL,'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s');" % (row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12],row[13],row[14],row[15],row[16],row[17])
            #print(insert_data)
            db.execute_query(connection, insert_data)

        self.load_data_from_database()

    def folder_istnieje(self):
        folder = self.ui.ed_sciezka_dane.text().strip()
        if not folder:
            QMessageBox.critical(self, 'Error', 'Nie wybrano lokalizacji pliku')
            self.ui.ed_sciezka_dane.setFocus()
            return False

        if not os.path.exists(folder):
            QMessageBox.critical(self, 'Error', 'Folder nie istnieje. Sprawdź lokalizację pliku')
            self.ui.ed_sciezka_dane.setFocus()
            return False
        return True

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
        miestac_roboczy = dodatki.data_miesiac_dzis()
        select_data = "SELECT * FROM `logowanie_zlecen` WHERE miesiac = '%s';" % (miestac_roboczy)  # (miestac_roboczy)
        connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
        results = db.read_query(connection, select_data)
        connection.close()

        connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
        if results:
            for x in results:
                delete_data = "delete from logowanie_zlecen where id = '%s' and miesiac = '%s';" % (x[0],miestac_roboczy)
                print('Do skasowania:',delete_data)
                db.execute_query(connection, delete_data)
        else:
            print('--Brak wpisów jeszcze--')
        connection.close()