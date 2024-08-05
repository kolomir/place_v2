from PyQt5.QtWidgets import QMainWindow, qApp
from PyQt5 import QtGui
import configparser
#import sys
from datetime import date, datetime

from _main_ui import Ui_MainWindow
import db, dodatki

from bledy_prod import MainWindow_bledy
from nieobecnosci_prod import MainWindow_nieobecnosci
from ustawieniaMenu import MainWindow_ustawienia

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        #- wczytanie pliku INI --------------------------------------------
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        #- załadowanie zmiennych z pliku INI ------------------------------
        self.folder_bledy = self.config['sciezki']['folder_bledy']
        self.plik_bledy = self.config['sciezki']['plik_bledy']
        self.plik_nieobecnosci = self.config['sciezki']['plik_nieobecnosci']
        #------------------------------------------------------------------

        #self.otwarty_miesiac()
        self.otwarty_miesiac_2()
        self.ui.btn_otworzMiesiac.clicked.connect(self.dodaj_miesiac)
        self.ui.btn_bledy.clicked.connect(self.otworz_okno_bledy)
        self.ui.btn_nieobecnosci.clicked.connect(self.otworz_okno_nieobecnosci)
        self.ui.btn_ustawienia.clicked.connect(self.otworz_okno_ustawieniaMenu)
        self.ui.btn_zamknij.clicked.connect(qApp.quit)

        self.sprawdz_zaladowanie_bledy()
        self.sprawdz_zaladowanie_nieobecnosci()

    def data_miesiac_dzis(self):
        data_dzis = date.today()
        prev_miesiac = data_dzis.month - 1 if data_dzis.month > 1 else 12
        prev_rok = data_dzis.year if data_dzis.month > 1 else data_dzis.year - 1
        data_miesiac = "%s-%s-%s" % (prev_rok,prev_miesiac,"1")
        print(data_miesiac)
        return data_miesiac

    #- TESTY --------------------------------------------------
    def otwarty_miesiac_2(self):
        miestac_roboczy = self.data_miesiac_dzis()
        select_data = "SELECT * FROM aktywny_miesiac WHERE blokada = 0"
        connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
        result = db.read_query(connection, select_data)
        #print('result1:', result)
        #print('result2:', result[0][1])
        print(f"Wyniki zapytania: {result}")
        print(f"miestac_roboczy: {miestac_roboczy}")

        # Sprawdź, czy wynik jest pusty
        if result:
            print("Są nieaktywne rekordy")
            self.ui.lab_aktywnyMiesiac.setText('Bieżący miesiąc jest otwarty')
            self.ui.lab_aktywnyMiesiac.setStyleSheet("QLabel { background-color : green; }")
            self.ui.btn_otworzMiesiac.setEnabled(False)
            self.ui.btn_bledy.setEnabled(True)
            self.ui.lab_bledy.setEnabled(True)
            self.ui.btn_nieobecnosci.setEnabled(True)
            self.ui.lab_nieobecnosci.setEnabled(True)
            self.ui.btn_direct.setEnabled(True)
            self.ui.lab_direct.setEnabled(True)
            self.ui.btn_zaladuj_raportowanie.setEnabled(True)
            self.ui.lab_raportowanie.setEnabled(True)
        else:
            print("Brak nieaktywnych rekordów")
            data_miesiac = date.today()
            data_miesiac_string = "%s %s" % (dodatki.nazwy_miesiecy[(data_miesiac.month - 1) - 1], data_miesiac.year)
            self.ui.lab_aktywnyMiesiac.setText('Bieżący miesiąc nie został otwarty')
            self.ui.lab_aktywnyMiesiac.setStyleSheet("QLabel { background-color : red; }")
            self.ui.text_aktywny_miesiac.setText(data_miesiac_string)
            self.ui.btn_bledy.setEnabled(False)
            self.ui.lab_bledy.setEnabled(False)
            self.ui.btn_nieobecnosci.setEnabled(False)
            self.ui.lab_nieobecnosci.setEnabled(False)
            self.ui.btn_direct.setEnabled(False)
            self.ui.lab_direct.setEnabled(False)
            self.ui.btn_zaladuj_raportowanie.setEnabled(False)
            self.ui.lab_raportowanie.setEnabled(False)


    def otwarty_miesiac(self):
        miestac_roboczy = self.data_miesiac_dzis()
        print('miestac_roboczy:', miestac_roboczy)
        select_data = "SELECT * FROM aktywny_miesiac WHERE miesiac = '%s'" % (str(miestac_roboczy))
        select_data = "SELECT * FROM aktywny_miesiac WHERE blokada = 0"
        connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
        result = db.read_query(connection, select_data)
        print('result1:', result)
        print('result2:', result[0][1])
        data_obj = datetime.strptime(str(result[0][1]), '%Y-%m-%d')
        data_baza = "%s-%s-%s" % (data_obj.year, data_obj.month, "1")
        zamkniete_baza = result[0][2]
        print('miesiac:', data_baza)
        print('zamkniete_baza:', zamkniete_baza)

        if not result:
            print("Brak danych")
            data_miesiac = date.today()
            data_miesiac_string = "%s %s" % (dodatki.nazwy_miesiecy[(data_miesiac.month - 1)-1],data_miesiac.year)
            self.ui.lab_aktywnyMiesiac.setText('Bieżący miesiąc nie został otwarty')
            self.ui.lab_aktywnyMiesiac.setStyleSheet("QLabel { background-color : red; }")
            self.ui.text_aktywny_miesiac.setText(data_miesiac_string)
            self.ui.btn_bledy.setEnabled(False)
            self.ui.lab_bledy.setEnabled(False)
            self.ui.btn_nieobecnosci.setEnabled(False)
            self.ui.lab_nieobecnosci.setEnabled(False)
            self.ui.btn_direct.setEnabled(False)
            self.ui.lab_direct.setEnabled(False)
            self.ui.btn_zaladuj_raportowanie.setEnabled(False)
            self.ui.lab_raportowanie.setEnabled(False)
        else:
            self.ui.lab_aktywnyMiesiac.setText('Bieżący miesiąc jest otwarty')
            self.ui.lab_aktywnyMiesiac.setStyleSheet("QLabel { background-color : green; }")
            self.ui.btn_otworzMiesiac.setEnabled(False)
            self.ui.btn_bledy.setEnabled(True)
            self.ui.lab_bledy.setEnabled(True)
            self.ui.btn_nieobecnosci.setEnabled(True)
            self.ui.lab_nieobecnosci.setEnabled(True)
            self.ui.btn_direct.setEnabled(True)
            self.ui.lab_direct.setEnabled(True)
            self.ui.btn_zaladuj_raportowanie.setEnabled(True)
            self.ui.lab_raportowanie.setEnabled(True)

    def dodaj_miesiac(self):
        connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
        teraz = datetime.today()
        pytanie1 = "INSERT INTO aktywny_miesiac VALUES (NULL, '%s', 0, '%s', NULL)" % (str(self.data_miesiac_dzis()), teraz)
        print(pytanie1)
        db.execute_query(connection, pytanie1)
        pytanie2 = "INSERT INTO importowane_tabele VALUES (NULL, '%s', 0, NULL, 0, NULL, 0, NULL, 0, NULL)" % (str(self.data_miesiac_dzis()))
        print(pytanie2)
        db.execute_query(connection, pytanie2)

        self.otwarty_miesiac_2()

    def otworz_okno_bledy(self):
        self.okno_bledy = MainWindow_bledy()
        self.okno_bledy.show()

    def otworz_okno_nieobecnosci(self):
        self.okno_nieobecnosci = MainWindow_nieobecnosci()
        self.okno_nieobecnosci.show()

    def otworz_okno_ustawieniaMenu(self):
        self.okno_ustawieniaMenu = MainWindow_ustawienia()
        self.okno_ustawieniaMenu.show()

    def sprawdz_zaladowanie_bledy(self):
        miestac_roboczy = self.data_miesiac_dzis()
        print('miesiac', miestac_roboczy)
        select_data = "SELECT * FROM `bledy_prod` WHERE miesiac = '%s';" % ('2024-06-01')  # (miestac_roboczy)
        connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
        results = db.read_query(connection, select_data)

        if not results:
            self.ui.lab_dot_bledy.setPixmap(QtGui.QPixmap(":/icon/img/svg_icons/dot_red.svg"))
        else:
            self.ui.lab_dot_bledy.setPixmap(QtGui.QPixmap(":/icon/img/svg_icons/dot_green.svg"))
        connection.close()

    def sprawdz_zaladowanie_nieobecnosci(self):
        miestac_roboczy = self.data_miesiac_dzis()
        print('miesiac', miestac_roboczy)
        select_data = "SELECT * FROM `nieobecnosci_prod` WHERE miesiac = '%s';" % ('2024-06-01')  # (miestac_roboczy)
        connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
        results = db.read_query(connection, select_data)

        if not results:
            self.ui.lab_dot_nieobecnosci.setPixmap(QtGui.QPixmap(":/icon/img/svg_icons/dot_red.svg"))
        else:
            self.ui.lab_dot_nieobecnosci.setPixmap(QtGui.QPixmap(":/icon/img/svg_icons/dot_green.svg"))
        connection.close()