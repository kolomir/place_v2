from PyQt5.QtWidgets import QWidget, QMessageBox, QFileDialog, QTableWidgetItem, QHeaderView
import configparser
import openpyxl
#import sys
import os
from datetime import date, datetime

from _bledy_mag_ui import Ui_Form
import db, dodatki


class MainWindow_bledy_mag(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        #- wczytanie pliku INI --------------------------------------------
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        #- załadowanie zmiennych z pliku INI ------------------------------
        self.folder_bledy = self.config['sciezki']['folder_bledy']
        self.plik = self.config['sciezki']['plik_bledy_mag']
        #------------------------------------------------------------------
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
        data_miesiac = "%s-%s-%s" % (prev_rok,prev_miesiac,"1")
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
        #print(folder)
        self.ui.ed_sciezka_dane.setText(folder)

    def czytaj_dane(self):
        if not self.folder_istnieje():
            return
        folder = self.ui.ed_sciezka_dane.text().strip()
        print(folder)
        wb = openpyxl.load_workbook(os.path.join(f'{folder}\\{self.plik}'))
        sheet = wb['Arkusz1']
        teraz = datetime.today()
        data_miesiac = str(dodatki.data_miesiac_dzis())
        print(data_miesiac)

        lista_wpisow = []

        #czytamy wszystkie kolumny i wiersze ze wskazanego pliku
        for row in sheet.iter_rows(min_row=2, min_col=1, max_col=5, values_only=True):
            #sprawdzamy czy wiersz nie jest pusty (zakładając że pusty wiersz ma wszystkie kolumny o wartosci None i kończy zestawienie)
            if any(cell is not None for cell in row):
                lista_wpisow.append([row[1],row[3],row[4],data_miesiac,teraz])
            else:
                break

        connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)

        for row in lista_wpisow:
            insert_data = "INSERT INTO bledy_mag VALUES (NULL,'%s','%s','%s','%s','%s');" % (row[0],row[1],row[2],row[3],row[4])
            db.execute_query(connection, insert_data)

        self.wyszukaj_dane()

    def wyszukaj_dane(self):
        miestac_roboczy = dodatki.data_miesiac_dzis()
        print('miesiac',miestac_roboczy)
        select_data = "SELECT * FROM `bledy_mag` WHERE miesiac = '%s';" % (miestac_roboczy) #(miestac_roboczy)
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
        self.ui.tab_dane.setColumnCount(5)  # Zmień na liczbę kolumn w twojej tabeli
        self.ui.tab_dane.setRowCount(0)  # Ustawienie liczby wierszy na 0
        self.ui.tab_dane.setHorizontalHeaderLabels(['Nr akt', 'Bledy zewnętrzne', 'Bledy wewnętrzne', 'Miesiac', 'Data dodania'])

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
            wiersz += 1

        self.ui.tab_dane.horizontalHeader().setStretchLastSection(True)
        self.ui.tab_dane.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.ui.tab_dane.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.ui.tab_dane.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.ui.tab_dane.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.ui.tab_dane.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)