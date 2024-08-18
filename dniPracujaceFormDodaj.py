from PyQt5.QtWidgets import QWidget, QMessageBox, QFileDialog, QTableWidgetItem,QHeaderView,QApplication
from PyQt5.QtCore import pyqtSlot, Qt

from _dniPracujaceFormDodaj_ui import Ui_Form
import configparser
import db, dodatki
import os
import openpyxl
from datetime import date, datetime

class MainWindow_dniPracujaceFormDodaj(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        # - wczytanie pliku INI --------------------------------------------
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        # - załadowanie zmiennych z pliku INI ------------------------------
        self.folder_bledy = self.config['sciezki']['folder_bledy']
        self.plik = self.config['sciezki']['plik_dniPracujace']
        # ------------------------------------------------------------------
        # - domyślna ścieżka dla pliku -----------------
        domyslny = f"{self.folder_bledy}"
        self.ui.ed_sciezka_dane.setText(domyslny)
        # -----------------------------------------------
        self.ui.btn_przegladaj.clicked.connect(self.przycisk_sciezka)
        self.ui.btn_zapisz.clicked.connect(self.importuj)

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

    def importuj(self):
        if not self.folder_istnieje():
            return
        folder = self.ui.ed_sciezka_dane.text().strip()
        print(folder)
        wb = openpyxl.load_workbook(os.path.join(f'{folder}\\{self.plik}'))
        sheet = wb['Arkusz1']
        teraz = datetime.today()
        print('ROK: ',teraz.year)
        data_miesiac = str(dodatki.data_miesiac_dzis())
        print('Jakis tekst %s' % (data_miesiac))

        lista_wpisow = []
        # czytamy wszystkie kolumny i wiersze ze wskazanego pliku
        for row in sheet.iter_rows(min_row=2, min_col=1, max_col=4, values_only=True):
            # sprawdzamy czy wiersz nie jest pusty (zakładając że pusty wiersz ma wszystkie kolumny o wartosci None i kończy zestawienie)
            if any(cell is not None for cell in row):
                ktory_miesiac = 1
                for liczba in dodatki.nazwy_miesiecy:
                    if row[0].lower() == liczba.lower():
                        #print('wynik: %s || %s | %s' % (ktory_miesiac, liczba, row[0]))
                        miesiac_num = ktory_miesiac
                    ktory_miesiac += 1
                lista_wpisow.append([teraz.year, miesiac_num, row[1], row[2], row[3]])
                #print(teraz.year,' | ', miesiac_num,' | ',row[1],' | ',row[2],' | ',row[3])
                #print(row[0],' | ',row[1],' | ',row[2],' | ',row[3])
            else:
                break

        connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)

        for row in lista_wpisow:
            insert_data = "INSERT INTO dni_pracujace_w_roku VALUES (NULL,'%s','%s','%s','%s','%s');" % (row[0], row[1], row[2], row[3], row[4])
            db.execute_query(connection, insert_data)

        self.close()