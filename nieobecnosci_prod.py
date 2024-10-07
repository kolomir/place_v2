from PyQt5.QtWidgets import QWidget, QMessageBox, QFileDialog, QTableWidgetItem,QHeaderView
import configparser
import openpyxl
#import sys
import os
from datetime import date, datetime
import calendar

from _nieobecnosci_prod_ui import Ui_Form
import db, dodatki


class MainWindow_nieobecnosci(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        #- wczytanie pliku INI --------------------------------------------
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        #- załadowanie zmiennych z pliku INI ------------------------------
        self.folder_bledy = self.config['sciezki']['folder_bledy']
        self.plik = self.config['sciezki']['plik_nieobecnosci']
        self.plik_obco = self.config['sciezki']['plik_obcokrajowcy']
        #------------------------------------------------------------------
        # - domyślna ścieżka dla pliku -----------------
        domyslny = f"{self.folder_bledy}"
        self.ui.ed_sciezka_dane.setText(domyslny)
        # -----------------------------------------------

        self.ui.btn_przegladaj.clicked.connect(self.przycisk_sciezka)
        self.ui.btn_importuj.clicked.connect(self.czytaj_dane)
        self.ui.btn_importuj_obco.clicked.connect(self.czytaj_dane_obco)
        self.wyszukaj_dane()


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

    def licz_dni_wolne(self,dane):
        miestac_roboczy = dodatki.data_miesiac_dzis()
        data = datetime.strptime(miestac_roboczy, "%Y-%m-%d")
        miesiac = data.month
        rok = data.year
        _, dni_miesiaca = calendar.monthrange(rok, miesiac)

        select_data = "SELECT * FROM `dni_pracujace_w_roku` WHERE rok = '%s' and miesiac = '%s';" % (rok,miesiac)  # (miestac_roboczy)
        connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
        results = db.read_query(connection, select_data)

        dni_z_bazy = results[0][4]

        dni_wolne = dni_z_bazy - int(dane)
        if dni_wolne < 0:
            dni_wolne = 0
        return dni_wolne

    def czytaj_dane_obco(self):
        if not self.folder_istnieje():
            return
        folder = self.ui.ed_sciezka_dane.text().strip()
        print(f'{folder}\\{self.plik_obco}')
        wb = openpyxl.load_workbook(os.path.join(f'{folder}\\{self.plik_obco}'))
        sheet = wb['Sheet']
        teraz = datetime.today()
        data_miesiac = str(dodatki.data_miesiac_dzis())
        print(data_miesiac)

        lista_wpisow = []

        #czytamy wszystkie kolumny i wiersze ze wskazanego pliku
        for row in sheet.iter_rows(min_row=2, min_col=0, max_col=3, values_only=True):
            #sprawdzamy czy wiersz nie jest pusty (zakładając że pusty wiersz ma wszystkie kolumny o wartosci None i kończy zestawienie)
            if any(cell is not None for cell in row):
                if row[1] == None:
                    break
                else:
                    dni_wolne = self.licz_dni_wolne(row[2])
                    lista_wpisow.append([row[0],row[1],row[2],dni_wolne,data_miesiac,teraz])
            else:
                break

        connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)

        for row in lista_wpisow:
            insert_data = "INSERT INTO nieobecnosci_prod VALUES (NULL,'%s','%s',NULL,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,'%s','%s','%s','%s');" % (row[1],row[0],row[2],row[3],row[4],row[5])
            db.execute_query(connection, insert_data)

        self.wyszukaj_dane()

    def czytaj_dane(self):
        if not self.folder_istnieje():
            return
        folder = self.ui.ed_sciezka_dane.text().strip()
        print(f'{folder}\\{self.plik}')
        wb = openpyxl.load_workbook(os.path.join(f'{folder}\\{self.plik}'))
        sheet = wb['Sheet']
        teraz = datetime.today()
        data_miesiac = str(dodatki.data_miesiac_dzis())
        print(data_miesiac)

        lista_wpisow = []

        #czytamy wszystkie kolumny i wiersze ze wskazanego pliku
        for row in sheet.iter_rows(min_row=13, min_col=0, max_col=30, values_only=True):
            #sprawdzamy czy wiersz nie jest pusty (zakładając że pusty wiersz ma wszystkie kolumny o wartosci None i kończy zestawienie)
            if any(cell is not None for cell in row):
                if row[4] == None:
                    break
                else:
                    tekst = row[4].split('|')
                    nazwisko = tekst[0].strip()
                    nr_akt = tekst[1].strip()
                    #
                    lista_wpisow.append([nazwisko,nr_akt,row[6],row[8],row[9],row[10],row[11],row[12],row[17],row[18],row[19],row[20],row[21],row[22],row[23],row[24],row[26],row[27],row[29],data_miesiac,teraz])
                    #print(nazwisko,nr_akt,row[6],row[8],row[9],row[10],row[11],row[12],row[17],row[18],row[19],row[20],row[21],row[22],row[23],row[24],row[26],row[27],row[29],data_miesiac,teraz)
            else:
                break

        connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)

        for row in lista_wpisow:
            insert_data = "INSERT INTO nieobecnosci_prod VALUES (NULL,'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s',0,'%s','%s','%s');" % (row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12],row[13],row[14],row[15],row[16],row[17],row[18],row[19],row[20])
            db.execute_query(connection, insert_data)

        self.wyszukaj_dane()

    def wyszukaj_dane(self):
        miestac_roboczy = dodatki.data_miesiac_dzis()
        print('miesiac',miestac_roboczy)
        select_data = "SELECT * FROM `nieobecnosci_prod` WHERE miesiac = '%s';" % (miestac_roboczy) #(miestac_roboczy)
        connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
        results = db.read_query(connection, select_data)

        if not results:
            print('wynik ZLE')
            self.clear_table()
            self.naglowki_tabeli()
        else:
            print('wynik OK')
            self.naglowki_tabeli()
            print(results)
            self.pokaz_dane(results)
        connection.close()

    def clear_table(self):
        # Wyczyść zawartość tabeli
        self.ui.tab_dane.clearContents()
        self.ui.tab_dane.setRowCount(0)

    def naglowki_tabeli(self):
        self.ui.tab_dane.setColumnCount(21)  # Zmień na liczbę kolumn w twojej tabeli
        self.ui.tab_dane.setRowCount(0)  # Ustawienie liczby wierszy na 0
        self.ui.tab_dane.setHorizontalHeaderLabels([
            'Nazwisko i imię',
            'Nr akt',
            'Stanowisko',
            'Urlop wypocz.',
            'Urlop bezpłatny',
            'Urlop szkoleniowy',
            'Urlop opieka (art. 188 kp) ',
            'Urlop okoliczność.',
            'Zwol. lek.',
            'Urlop macierz.',
            'Opieka ZUS',
            'Urlop wychow.',
            'Inne nieobecn.',
            'Usp.',
            'NN',
            'Rehab.',
            'Rodz.',
            'Krew',
            'Dni w pracy',
            'Razem',
            'Miesiac',
            'Data dodania'
        ])

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
            self.ui.tab_dane.setItem(wiersz, 10, QTableWidgetItem(str(wynik[11])))
            self.ui.tab_dane.setItem(wiersz, 11, QTableWidgetItem(str(wynik[12])))
            self.ui.tab_dane.setItem(wiersz, 12, QTableWidgetItem(str(wynik[13])))
            self.ui.tab_dane.setItem(wiersz, 13, QTableWidgetItem(str(wynik[14])))
            self.ui.tab_dane.setItem(wiersz, 14, QTableWidgetItem(str(wynik[15])))
            self.ui.tab_dane.setItem(wiersz, 15, QTableWidgetItem(str(wynik[16])))
            self.ui.tab_dane.setItem(wiersz, 16, QTableWidgetItem(str(wynik[17])))
            self.ui.tab_dane.setItem(wiersz, 17, QTableWidgetItem(str(wynik[18])))
            self.ui.tab_dane.setItem(wiersz, 18, QTableWidgetItem(str(wynik[19])))
            self.ui.tab_dane.setItem(wiersz, 19, QTableWidgetItem(str(wynik[20])))
            self.ui.tab_dane.setItem(wiersz, 20, QTableWidgetItem(str(wynik[21])))
            self.ui.tab_dane.setItem(wiersz, 21, QTableWidgetItem(str(wynik[22])))
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
        self.ui.tab_dane.horizontalHeader().setSectionResizeMode(10, QHeaderView.ResizeToContents)
        self.ui.tab_dane.horizontalHeader().setSectionResizeMode(11, QHeaderView.ResizeToContents)
        self.ui.tab_dane.horizontalHeader().setSectionResizeMode(12, QHeaderView.ResizeToContents)
        self.ui.tab_dane.horizontalHeader().setSectionResizeMode(13, QHeaderView.ResizeToContents)
        self.ui.tab_dane.horizontalHeader().setSectionResizeMode(14, QHeaderView.ResizeToContents)
        self.ui.tab_dane.horizontalHeader().setSectionResizeMode(15, QHeaderView.ResizeToContents)
        self.ui.tab_dane.horizontalHeader().setSectionResizeMode(16, QHeaderView.ResizeToContents)
        self.ui.tab_dane.horizontalHeader().setSectionResizeMode(17, QHeaderView.ResizeToContents)
        self.ui.tab_dane.horizontalHeader().setSectionResizeMode(18, QHeaderView.ResizeToContents)
        self.ui.tab_dane.horizontalHeader().setSectionResizeMode(19, QHeaderView.ResizeToContents)
        self.ui.tab_dane.horizontalHeader().setSectionResizeMode(20, QHeaderView.ResizeToContents)
        self.ui.tab_dane.horizontalHeader().setSectionResizeMode(21, QHeaderView.ResizeToContents)
