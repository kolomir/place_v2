from PyQt5.QtWidgets import QWidget, QMessageBox, QFileDialog, QTableWidgetItem, QHeaderView
import configparser
import openpyxl
from datetime import date, datetime
import os

from _raportowanie_total_prod_ui import Ui_Form
import db, dodatki

class MainWindow_raportowanie_total_prod(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        # - wczytanie pliku INI --------------------------------------------
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        # - załadowanie zmiennych z pliku INI ------------------------------
        self.folder_bledy = self.config['sciezki']['folder_bledy']
        self.plik = self.config['sciezki']['plik_raportowanie_tot']
        # ------------------------------------------------------------------
        # - domyślna ścieżka dla pliku -----------------
        domyslny = f"{self.folder_bledy}"
        self.ui.ed_sciezka_dane.setText(domyslny)
        # -----------------------------------------------

        self.ui.btn_przegladaj.clicked.connect(self.przycisk_sciezka)
        self.ui.btn_importuj.clicked.connect(self.czytaj_dane)
        self.wyszukaj_dane()

    def data_miesiac_dzis(self):
        data_dzis = date.today()
        prev_miesiac = data_dzis.month - 1 if data_dzis.month > 1 else 12
        prev_rok = data_dzis.year if data_dzis.month > 1 else data_dzis.year - 1
        data_miesiac = "%s-%s-%s" % (prev_rok, prev_miesiac, "1")
        print(data_miesiac)
        return data_miesiac

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

    def przycisk_sciezka(self):
        options = QFileDialog.Options()
        default_directory = self.folder_bledy
        folder = QFileDialog.getExistingDirectory(self, 'Wybierz folder...', default_directory, options=options)
        folder = folder.replace("/", "\\")
        print(folder)
        self.ui.ed_sciezka_dane.setText(folder)

    def czytaj_dane(self):
        if not self.folder_istnieje():
            return
        folder = self.ui.ed_sciezka_dane.text().strip()
        # print(folder)
        wb = openpyxl.load_workbook(os.path.join(f'{folder}\\{self.plik}'))
        sheet = wb['Sheet']
        teraz = datetime.today()
        data_miesiac = str(dodatki.data_miesiac_dzis())
        # print(data_miesiac)

        lista_wpisow = []
        # czytamy wszystkie kolumny i wiersze ze wskazanego pliku
        for row in sheet.iter_rows(min_row=2, min_col=1, max_col=8, values_only=True):
            # sprawdzamy czy wiersz nie jest pusty (zakładając że pusty wiersz ma wszystkie kolumny o wartosci None i kończy zestawienie)
            if any(cell is not None for cell in row):

                #print([row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], data_miesiac, teraz])
                lista_wpisow.append( [row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], data_miesiac, teraz])
            else:
                break

        connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)

        for row in lista_wpisow:
            insert_data = "INSERT INTO raportowanie_total VALUES (NULL,'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s');" % ( row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9])
            db.execute_query(connection, insert_data)

        self.wyszukaj_dane()

    def czysc_string_int(self, tekst):
        wynik = int(tekst.replace(' ', ''))
        return wynik

    def czysc_string_dec(self, tekst):
        wynik = tekst.replace(' ', '')
        wynik = wynik.replace(',', '.')
        return wynik

    def wyszukaj_dane(self):
        miestac_roboczy = dodatki.data_miesiac_dzis()
        print('miesiac', miestac_roboczy)
        select_data = "SELECT * FROM `raportowanie_total` WHERE miesiac = '%s';" % (
            miestac_roboczy)  # (miestac_roboczy)
        connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
        results = db.read_query(connection, select_data)

        if not results:
            print('wynik ZLE')
            self.clear_table()
            self.naglowki_tabeli()
        else:
            print('wynik OK')
            self.naglowki_tabeli()
            self.pokaz_dane(results)
        connection.close()

    def clear_table(self):
        # Wyczyść zawartość tabeli
        self.ui.tab_dane.clearContents()
        self.ui.tab_dane.setRowCount(0)

    def naglowki_tabeli(self):
        self.ui.tab_dane.setColumnCount(16)  # Zmień na liczbę kolumn w twojej tabeli
        self.ui.tab_dane.setRowCount(0)  # Ustawienie liczby wierszy na 0
        self.ui.tab_dane.setHorizontalHeaderLabels(
            ['Work center', 'WC name', 'Planned qty', 'Rep. qty', 'Pl. time. for rep.', 'Pl. total time', 'Rep. total time',
             'E-factor', 'Miesiąc', 'Data dodania'])

    def pokaz_dane(self, rows):
        # Column count
        if int(len(rows[0])) > 0:
            self.ui.tab_dane.setColumnCount(int(len(rows[0])) - 1)

        # Row count
        self.ui.tab_dane.setRowCount(int(len(rows)))

        wiersz = 0
        for wynik in rows:
            self.ui.tab_dane.setItem(wiersz, 0, QTableWidgetItem(str(wynik[1])))
            self.ui.tab_dane.setItem(wiersz, 1, QTableWidgetItem(str(wynik[2])))
            self.ui.tab_dane.setItem(wiersz, 2, QTableWidgetItem(str(wynik[3])))
            self.ui.tab_dane.setItem(wiersz, 3, QTableWidgetItem(str(wynik[4])))
            self.ui.tab_dane.setItem(wiersz, 4, QTableWidgetItem(str(wynik[5])))
            self.ui.tab_dane.setItem(wiersz, 5, QTableWidgetItem(str(wynik[6])))
            self.ui.tab_dane.setItem(wiersz, 6, QTableWidgetItem(str(wynik[7])))
            self.ui.tab_dane.setItem(wiersz, 7, QTableWidgetItem(str(wynik[8])))
            self.ui.tab_dane.setItem(wiersz, 8, QTableWidgetItem(str(wynik[9])))
            self.ui.tab_dane.setItem(wiersz, 9, QTableWidgetItem(str(wynik[10])))
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