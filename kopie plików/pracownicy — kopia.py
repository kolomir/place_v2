from PyQt5.QtWidgets import QWidget, QMessageBox, QFileDialog, QTableWidgetItem, QHeaderView
import configparser
import openpyxl
from datetime import date, datetime
import os

from plik_pomoc_pracownicy import MainWindow_pomoc_pracownicy
from _pracownicy_ui import Ui_Form
import db, dodatki

class MainWindow_pracownicy(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        #- wczytanie pliku INI --------------------------------------------
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        #- załadowanie zmiennych z pliku INI ------------------------------
        self.folder_bledy = self.config['sciezki']['folder_bledy']
        self.plik = self.config['sciezki']['plik_pracownicy']
        #------------------------------------------------------------------
        # - domyślna ścieżka dla pliku -----------------
        #domyslny = f"{self.folder_bledy}"
        #self.ui.ed_sciezka_dane.setText(self.load_from_path)
        # -----------------------------------------------

        self.ui.btn_przegladaj.clicked.connect(self.open_file_dialog)
        self.ui.btn_importuj.clicked.connect(self.czytaj_dane)
        self.ui.btn_pomoc.clicked.connect(self.otworz_okno_plik_pomoc_pracownicy)
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
        select_data = "SELECT * FROM `pracownicy` WHERE miesiac = '%s';" % (miestac_roboczy)  # (miestac_roboczy)
        connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
        results = db.read_query(connection, select_data)
        connection.close()

        connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
        if results:
            for x in results:
                delete_data = "delete from pracownicy where id = '%s' and miesiac = '%s';" % (x[0],miestac_roboczy)
                print('Do skasowania:',delete_data)
                db.execute_query(connection, delete_data)
        else:
            print('--Brak wpisów jeszcze--')
        connection.close()

    def czytaj_dane(self):
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
        for row in sheet.iter_rows(min_row=2, min_col=1, max_col=4, values_only=True):
            #sprawdzamy czy wiersz nie jest pusty (zakładając że pusty wiersz ma wszystkie kolumny o wartosci None i kończy zestawienie)
            if any(cell is not None for cell in row):
                lista_wpisow.append([row[0],row[1],row[2],row[3],data_miesiac,teraz])
            else:
                break

        connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)

        for row in lista_wpisow:
            insert_data = "INSERT INTO pracownicy VALUES (NULL,'%s','%s','%s','%s','%s','%s');" % (row[0],row[1],row[2],row[3],row[4],row[5])
            db.execute_query(connection, insert_data)

        self.wyszukaj_dane()

    def wyszukaj_dane(self):
        miestac_roboczy = dodatki.data_miesiac_dzis()
        print('miesiac',miestac_roboczy)
        select_data = "SELECT * FROM `pracownicy` WHERE miesiac = '%s';" % (miestac_roboczy) #(miestac_roboczy)
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
        self.ui.tab_dane.setColumnCount(6)  # Zmień na liczbę kolumn w twojej tabeli
        self.ui.tab_dane.setRowCount(0)  # Ustawienie liczby wierszy na 0
        self.ui.tab_dane.setHorizontalHeaderLabels(['Nr akt', 'Kod', 'Nazwisko', 'Imie', 'Miesiąc', 'Data dodania'])

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
            wiersz += 1

        self.ui.tab_dane.horizontalHeader().setStretchLastSection(True)
        self.ui.tab_dane.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.ui.tab_dane.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.ui.tab_dane.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.ui.tab_dane.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.ui.tab_dane.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)
        self.ui.tab_dane.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeToContents)

    def otworz_okno_plik_pomoc_pracownicy(self):
        self.okno_plik_pomoc_pracownicy = MainWindow_pomoc_pracownicy()
        self.okno_plik_pomoc_pracownicy.show()
