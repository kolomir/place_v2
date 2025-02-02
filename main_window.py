from PyQt5.QtCore import QThread, pyqtSignal, QEvent
from PyQt5.QtWidgets import QMainWindow, qApp, QApplication
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QPixmap
import configparser
import sys
from datetime import date, datetime

from _main_ui import Ui_MainWindow
import db, dodatki

from bledy_prod import MainWindow_bledy
from nieobecnosci_prod import MainWindow_nieobecnosci
from ustawieniaMenu import MainWindow_ustawienia
from wyliczeniaForm import MainWindow_wyliczeniaForm
from pracownicy import MainWindow_pracownicy
from direct_prod import MainWindow_direct_prod
from raportowanie_prod import MainWindow_raportowanie_prod
from raportowanie_total_prod import MainWindow_raportowanie_total_prod
from jakosc_prod import MainWindow_jakosc
from korekta_indirect_prod import MainWindow_korekta_indirect_prod
from ustawieniaMenu_mag import MainWindow_ustawienia_mag
from bledy_mag import MainWindow_bledy_mag
from kpi_mag import MainWindow_kpi_mag
from wyliczeniaForm_mag import MainWindow_wyliczeniaForm_mag
from raporty import MainWindow_raporty

class QueryWorker(QThread):
    results_ready = pyqtSignal(dict)

    def __init__(self, miesiac_roboczy):
        super().__init__()
        self.miesiac_roboczy = miesiac_roboczy

    def run(self):
        query = f"""
        SELECT 'pracownicy' AS tabela, COUNT(*) > 0 AS status FROM pracownicy WHERE miesiac = '{self.miesiac_roboczy}'
        UNION ALL
        SELECT 'bledy_prod', COUNT(*) > 0 FROM bledy_prod WHERE miesiac = '{self.miesiac_roboczy}'
        UNION ALL
        SELECT 'nieobecnosci_prod', COUNT(*) > 0 FROM nieobecnosci_prod WHERE miesiac = '{self.miesiac_roboczy}'
        UNION ALL
        SELECT 'direct', COUNT(*) > 0 FROM direct WHERE miesiac = '{self.miesiac_roboczy}'
        UNION ALL
        SELECT 'logowanie_zlecen', COUNT(*) > 0 FROM logowanie_zlecen WHERE miesiac = '{self.miesiac_roboczy}'
        UNION ALL
        SELECT 'raportowanie_total', COUNT(*) > 0 FROM raportowanie_total WHERE miesiac = '{self.miesiac_roboczy}'
        UNION ALL
        SELECT 'jakosc_prod', COUNT(*) > 0 FROM jakosc_prod WHERE miesiac = '{self.miesiac_roboczy}'
        UNION ALL
        SELECT 'korekta_indirect', COUNT(*) > 0 FROM korekta_indirect WHERE miesiac = '{self.miesiac_roboczy}'
        UNION ALL
        SELECT 'bledy_mag', COUNT(*) > 0 FROM bledy_mag WHERE miesiac = '{self.miesiac_roboczy}'
        UNION ALL
        SELECT 'kpi_mag', COUNT(*) > 0 FROM kpi_mag WHERE miesiac = '{self.miesiac_roboczy}';
        """
        connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
        results = db.read_query(connection, query)
        connection.close()

        # Przekształcenie wyników w słownik
        status_map = {row[0]: bool(row[1]) for row in results}
        self.results_ready.emit(status_map)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        #- wczytanie pliku INI --------------------------------------------
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        #- załadowanie zmiennych z pliku INI ------------------------------
        #self.folder_bledy = self.config['sciezki']['folder_bledy']
        #self.plik_bledy = self.config['sciezki']['plik_bledy']
        #self.plik_nieobecnosci = self.config['sciezki']['plik_nieobecnosci']
        self.dostep = self.config['dostep']['poziom']
        #------------------------------------------------------------------

        if "--user" in sys.argv:
            user_index = sys.argv.index("--user") + 1
            if user_index < len(sys.argv):
                self.user = sys.argv[user_index]
                if self.user == 'admin':
                    self.dostep = '0'
                if self.user == 'hr':
                    self.dostep = '1'
                if self.user == 'jakosc':
                    self.dostep = '2'
                if self.user == 'produkcja':
                    self.dostep = '3'
                if self.user == 'magazyn':
                    self.dostep = '4'
                print(f"Uruchomiono aplikację dla użytkownika: {self.user}")
                print(f"dostęp_ustalony = {self.dostep}")
            else:
                print("Nie podano nazwy użytkownika!")
        else:
            print("Brak parametru --user!")

        # Inicjalizacja
        self.worker = None

        # Podłączenie zdarzenia aktywacji okna
        self.installEventFilter(self)

        #self.otwarty_miesiac()
        self.otwarty_miesiac_2()
        self.ui.btn_otworzMiesiac.clicked.connect(self.dodaj_miesiac)
        self.ui.btn_zaladuj_pracownicy.clicked.connect(self.otworz_okno_pracownicy)
        self.ui.btn_bledy.clicked.connect(self.otworz_okno_bledy)
        self.ui.btn_nieobecnosci.clicked.connect(self.otworz_okno_nieobecnosci)
        self.ui.btn_direct.clicked.connect(self.otworz_okno_direct_prod)
        self.ui.btn_zaladuj_raportowanie.clicked.connect(self.otworz_okno_raportowanie_prod)
        self.ui.btn_zaladuj_raportowanie_total.clicked.connect(self.otworz_okno_raportowanie_total_prod)
        self.ui.btn_zaladuj_jakosc.clicked.connect(self.otworz_okno_jakoscForm)
        self.ui.btn_zaladuj_korekta.clicked.connect(self.otworz_okno_korektaIW)
        self.ui.btn_ustawienia.clicked.connect(self.otworz_okno_ustawieniaMenu)
        self.ui.btn_oblicz.clicked.connect(self.otworz_okno_wyliczeniaForm)
        self.ui.btn_zamknij.clicked.connect(qApp.quit)
        self.ui.btn_ustawienia_mag.clicked.connect(self.otworz_okno_ustawieniaMenu_mag)
        self.ui.btn_bledy_magazyn.clicked.connect(self.otworz_okno_bledy_mag)
        self.ui.btn_kpi_magazyn.clicked.connect(self.otworz_okno_kpi_mag)
        self.ui.btn_oblicz_magazyn.clicked.connect(self.otworz_okno_wyliczeniaForm_mag)
        self.ui.btn_raporty.clicked.connect(self.otworz_okno_raporty)

    def data_miesiac_dzis(self):
        data_dzis = date.today()
        prev_miesiac = data_dzis.month - 1 if data_dzis.month > 1 else 12
        prev_rok = data_dzis.year if data_dzis.month > 1 else data_dzis.year - 1
        data_miesiac = "%s-%s-%s" % (prev_rok,prev_miesiac,"1")
        #print(data_miesiac)
        return data_miesiac

    #- TESTY --------------------------------------------------
    def otwarty_miesiac_2(self):
        miestac_roboczy = dodatki.data_miesiac_dzis()
        miestac_prev = dodatki.data_prev_miesiac()
        print(f"miestac_roboczy: {miestac_roboczy}")
        print(f"miestac_prev: {miestac_prev}")
        select_data = "SELECT * FROM aktywny_miesiac WHERE miesiac = '%s' and blokada = 0" % (str(miestac_roboczy))
        connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
        result = db.read_query(connection, select_data)
        #print('result1:', result)
        #print('result2:', result[0][1])
        #print(f"Wyniki zapytania: {result}")
        #print(f"miestac_roboczy: {miestac_roboczy}")
        if result:
            print('result2:', result[0][1])
        else:
            print('Brak wyników')
            try:
                #sql_query = f"UPDATE aktywny_miesiac SET blokada = 1 WHERE miesiac = {miestac_prev}"
                #date_str = str_to_date({miestac_prev},'%Y-%m-%d')
                sql_query = f"UPDATE aktywny_miesiac SET blokada = 1 WHERE miesiac = '{miestac_prev}'"
                connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
                db.execute_query(connection, sql_query)
                print('sql_query:', sql_query)

            except db.Error as e:
                print(f"Błąd zapisu do bazy danych: {e}")

        # Sprawdź, czy wynik jest pusty
        if result:
            print("Są nieaktywne rekordy")
            self.ui.lab_aktywnyMiesiac.setText('Bieżący miesiąc jest otwarty')
            self.ui.lab_aktywnyMiesiac.setStyleSheet("QLabel { background-color : green; }")
            self.ui.btn_otworzMiesiac.setEnabled(False)
            #if self.dostep == '0':
            print('Dostep 0:', self.dostep)
            self.ui.btn_zaladuj_pracownicy.setEnabled(True)
            self.ui.lab_pracownicy.setEnabled(True)
            self.ui.btn_nieobecnosci.setEnabled(True)
            self.ui.lab_nieobecnosci.setEnabled(True)
            self.ui.btn_bledy.setEnabled(True)
            self.ui.lab_bledy.setEnabled(True)
            self.ui.btn_direct.setEnabled(True)
            self.ui.lab_direct.setEnabled(True)
            self.ui.btn_zaladuj_raportowanie.setEnabled(True)
            self.ui.lab_raportowanie.setEnabled(True)
            self.ui.btn_zaladuj_raportowanie_total.setEnabled(True)
            self.ui.lab_raportowanie_total.setEnabled(True)
            self.ui.btn_zaladuj_jakosc.setEnabled(True)
            self.ui.lab_jakosc.setEnabled(True)
            self.ui.btn_zaladuj_korekta.setEnabled(True)
            self.ui.lab_korekta.setEnabled(True)
            self.ui.btn_oblicz.setEnabled(True)

            self.ui.btn_bledy_magazyn.setEnabled(True)
            self.ui.lab_bledy_magazyn.setEnabled(True)
            self.ui.btn_kpi_magazyn.setEnabled(True)
            self.ui.lab_kpi_magazyn.setEnabled(True)
            self.ui.btn_ustawienia.setEnabled(True)
            self.ui.btn_ustawienia_mag.setEnabled(True)
            self.ui.btn_oblicz_magazyn.setEnabled(True)


            if self.dostep == '1':
                print('Dostep 1:', self.dostep)
                self.ui.btn_bledy.setEnabled(False)
                self.ui.lab_bledy.setEnabled(False)
                self.ui.btn_direct.setEnabled(False)
                self.ui.lab_direct.setEnabled(False)
                self.ui.btn_zaladuj_raportowanie.setEnabled(False)
                self.ui.lab_raportowanie.setEnabled(False)
                self.ui.btn_zaladuj_raportowanie_total.setEnabled(False)
                self.ui.lab_raportowanie_total.setEnabled(False)
                self.ui.btn_zaladuj_jakosc.setEnabled(False)
                self.ui.lab_jakosc.setEnabled(False)
                self.ui.btn_zaladuj_korekta.setEnabled(False)
                self.ui.lab_korekta.setEnabled(False)
                self.ui.btn_bledy_magazyn.setEnabled(False)
                self.ui.lab_bledy_magazyn.setEnabled(False)
                self.ui.btn_kpi_magazyn.setEnabled(False)
                self.ui.lab_kpi_magazyn.setEnabled(False)

            if self.dostep == '2':
                print('Dostep 2:', self.dostep)
                self.ui.btn_zaladuj_pracownicy.setEnabled(False)
                self.ui.lab_pracownicy.setEnabled(False)
                self.ui.btn_nieobecnosci.setEnabled(False)
                self.ui.lab_nieobecnosci.setEnabled(False)
                self.ui.btn_direct.setEnabled(False)
                self.ui.lab_direct.setEnabled(False)
                self.ui.btn_zaladuj_raportowanie.setEnabled(False)
                self.ui.lab_raportowanie.setEnabled(False)
                self.ui.btn_zaladuj_raportowanie_total.setEnabled(False)
                self.ui.lab_raportowanie_total.setEnabled(False)
                self.ui.btn_zaladuj_korekta.setEnabled(False)
                self.ui.lab_korekta.setEnabled(False)
                self.ui.btn_oblicz.setEnabled(False)
                self.ui.btn_bledy_magazyn.setEnabled(False)
                self.ui.lab_bledy_magazyn.setEnabled(False)
                self.ui.btn_kpi_magazyn.setEnabled(False)
                self.ui.lab_kpi_magazyn.setEnabled(False)
                self.ui.btn_ustawienia.setEnabled(False)
                self.ui.btn_ustawienia_mag.setEnabled(False)
                self.ui.btn_ustawienia_mag.setEnabled(False)
                self.ui.btn_oblicz_magazyn.setEnabled(False)

            if self.dostep == '3':
                print('Dostep 3:', self.dostep)
                self.ui.btn_zaladuj_pracownicy.setEnabled(False)
                self.ui.lab_pracownicy.setEnabled(False)
                self.ui.btn_nieobecnosci.setEnabled(False)
                self.ui.lab_nieobecnosci.setEnabled(False)
                self.ui.btn_bledy.setEnabled(False)
                self.ui.lab_bledy.setEnabled(False)
                self.ui.btn_zaladuj_jakosc.setEnabled(False)
                self.ui.lab_jakosc.setEnabled(False)
                self.ui.btn_bledy_magazyn.setEnabled(False)
                self.ui.lab_bledy_magazyn.setEnabled(False)
                self.ui.btn_kpi_magazyn.setEnabled(False)
                self.ui.lab_kpi_magazyn.setEnabled(False)
                self.ui.btn_ustawienia_mag.setEnabled(False)
                self.ui.btn_ustawienia_mag.setEnabled(False)
                self.ui.btn_oblicz_magazyn.setEnabled(False)

            if self.dostep == '4':
                print('Dostep 4:', self.dostep)
                self.ui.btn_zaladuj_pracownicy.setEnabled(False)
                self.ui.lab_pracownicy.setEnabled(False)
                self.ui.btn_nieobecnosci.setEnabled(False)
                self.ui.lab_nieobecnosci.setEnabled(False)
                self.ui.btn_bledy.setEnabled(False)
                self.ui.lab_bledy.setEnabled(False)
                self.ui.btn_zaladuj_raportowanie_total.setEnabled(False)
                self.ui.lab_raportowanie_total.setEnabled(False)
                self.ui.btn_zaladuj_jakosc.setEnabled(False)
                self.ui.lab_jakosc.setEnabled(False)
                self.ui.btn_oblicz.setEnabled(False)
                self.ui.btn_ustawienia.setEnabled(False)

        else:
            print("Brak nieaktywnych rekordów")
            data_miesiac = date.today()
            data_miesiac_string = "%s %s" % (dodatki.nazwy_miesiecy[(data_miesiac.month - 1) - 1], data_miesiac.year)
            self.ui.lab_aktywnyMiesiac.setText('Bieżący miesiąc nie został otwarty')
            self.ui.lab_aktywnyMiesiac.setStyleSheet("QLabel { background-color : red; }")
            self.ui.text_aktywny_miesiac.setText(data_miesiac_string)
            self.ui.btn_zaladuj_pracownicy.setEnabled(False)
            self.ui.lab_pracownicy.setEnabled(False)
            self.ui.btn_bledy.setEnabled(False)
            self.ui.lab_bledy.setEnabled(False)
            self.ui.btn_nieobecnosci.setEnabled(False)
            self.ui.lab_nieobecnosci.setEnabled(False)
            self.ui.btn_direct.setEnabled(False)
            self.ui.lab_direct.setEnabled(False)
            self.ui.btn_zaladuj_raportowanie.setEnabled(False)
            self.ui.lab_raportowanie.setEnabled(False)
            self.ui.btn_zaladuj_raportowanie_total.setEnabled(False)
            self.ui.lab_raportowanie_total.setEnabled(False)
            self.ui.btn_zaladuj_jakosc.setEnabled(False)
            self.ui.lab_jakosc.setEnabled(False)
            self.ui.btn_zaladuj_korekta.setEnabled(False)
            self.ui.lab_korekta.setEnabled(False)
            self.ui.btn_oblicz.setEnabled(False)

            self.ui.btn_bledy_magazyn.setEnabled(False)
            self.ui.lab_bledy_magazyn.setEnabled(False)
            self.ui.btn_kpi_magazyn.setEnabled(False)
            self.ui.lab_kpi_magazyn.setEnabled(False)
            self.ui.btn_ustawienia.setEnabled(False)
            self.ui.btn_ustawienia_mag.setEnabled(False)
            self.ui.btn_oblicz_magazyn.setEnabled(False)


    def otwarty_miesiac(self):
        miestac_roboczy = self.data_miesiac_dzis()
        #print('miestac_roboczy:', miestac_roboczy)
        select_data = "SELECT * FROM aktywny_miesiac WHERE miesiac = '%s' and blokada = 0" % (str(miestac_roboczy))
        #select_data = "SELECT * FROM aktywny_miesiac WHERE blokada = 0"
        connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
        result = db.read_query(connection, select_data)
        #print('result1:', result)
        #print('result2:', result[0][1])
        data_obj = datetime.strptime(str(result[0][1]), '%Y-%m-%d')
        data_baza = "%s-%s-%s" % (data_obj.year, data_obj.month, "1")
        zamkniete_baza = result[0][2]
        #print('miesiac:', data_baza)
        #print('zamkniete_baza:', zamkniete_baza)

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
            self.ui.btn_zaladuj_raportowanie_total.setEnabled(False)
            self.ui.lab_raportowanie_total.setEnabled(False)
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
            self.ui.btn_zaladuj_raportowanie_total.setEnabled(True)
            self.ui.lab_raportowanie_total.setEnabled(True)

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

    def otworz_okno_pracownicy(self):
        self.okno_pracownicy = MainWindow_pracownicy()
        self.okno_pracownicy.show()

    def otworz_okno_bledy(self):
        self.okno_bledy = MainWindow_bledy()
        self.okno_bledy.show()

    def otworz_okno_nieobecnosci(self):
        self.okno_nieobecnosci = MainWindow_nieobecnosci()
        self.okno_nieobecnosci.show()

    def otworz_okno_direct_prod(self):
        self.okno_direct_prod = MainWindow_direct_prod()
        self.okno_direct_prod.show()

    def otworz_okno_raportowanie_prod(self):
        self.okno_raportowanie_prod = MainWindow_raportowanie_prod()
        self.okno_raportowanie_prod.show()

    def otworz_okno_raportowanie_total_prod(self):
        self.okno_raportowanie_total_prod = MainWindow_raportowanie_total_prod()
        self.okno_raportowanie_total_prod.show()

    def otworz_okno_ustawieniaMenu(self):
        self.okno_ustawieniaMenu = MainWindow_ustawienia()
        self.okno_ustawieniaMenu.show()

    def otworz_okno_wyliczeniaForm(self):
        self.okno_wyliczeniaForm = MainWindow_wyliczeniaForm()
        self.okno_wyliczeniaForm.show()

    def otworz_okno_jakoscForm(self):
        self.okno_jakoscForm = MainWindow_jakosc()
        self.okno_jakoscForm.show()

    def otworz_okno_korektaIW(self):
        self.okno_korekta_indirect_prod = MainWindow_korekta_indirect_prod()
        self.okno_korekta_indirect_prod.show()

    def otworz_okno_ustawieniaMenu_mag(self):
        self.otworz_ustawieniaMenu_mag = MainWindow_ustawienia_mag()
        self.otworz_ustawieniaMenu_mag.show()

    def otworz_okno_bledy_mag(self):
        self.okno_bledy_mag = MainWindow_bledy_mag()
        self.okno_bledy_mag.show()

    def otworz_okno_kpi_mag(self):
        self.okno_kpi_mag = MainWindow_kpi_mag()
        self.okno_kpi_mag.show()

    def otworz_okno_wyliczeniaForm_mag(self):
        self.okno_wyliczeniaForm_mag = MainWindow_wyliczeniaForm_mag()
        self.okno_wyliczeniaForm_mag.show()

    def otworz_okno_raporty(self):
        self.okno_raporty = MainWindow_raporty()
        self.okno_raporty.show()

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.WindowActivate:
            self.odswiez_statusy()
        return super(MainWindow, self).eventFilter(obj, event)

    def odswiez_statusy(self):
        miesiac_roboczy = self.data_miesiac_dzis()

        # Tworzenie wątku i podłączanie wyników
        self.worker = QueryWorker(miesiac_roboczy)
        self.worker.results_ready.connect(self.aktualizuj_statusy)
        self.worker.start()

    def aktualizuj_statusy(self, status_map):
        # Mapowanie statusów na kontrolki
        self.ui.lab_dot_pracownicy.setPixmap(QPixmap(
            ":/icon/img/svg_icons/dot_green.svg" if status_map.get("pracownicy") else ":/icon/img/svg_icons/dot_red.svg"
        ))
        self.ui.lab_dot_bledy.setPixmap(QPixmap(
            ":/icon/img/svg_icons/dot_green.svg" if status_map.get("bledy_prod") else ":/icon/img/svg_icons/dot_red.svg"
        ))
        self.ui.lab_dot_nieobecnosci.setPixmap(QPixmap(
            ":/icon/img/svg_icons/dot_green.svg" if status_map.get("nieobecnosci_prod") else ":/icon/img/svg_icons/dot_red.svg"
        ))
        self.ui.lab_dot_direct.setPixmap(QPixmap(
            ":/icon/img/svg_icons/dot_green.svg" if status_map.get("direct") else ":/icon/img/svg_icons/dot_red.svg"
        ))
        self.ui.lab_dot_raportowanie.setPixmap(QPixmap(
            ":/icon/img/svg_icons/dot_green.svg" if status_map.get("logowanie_zlecen") else ":/icon/img/svg_icons/dot_red.svg"
        ))
        self.ui.lab_dot_raportowanie_total.setPixmap(QPixmap(
            ":/icon/img/svg_icons/dot_green.svg" if status_map.get("raportowanie_total") else ":/icon/img/svg_icons/dot_red.svg"
        ))
        self.ui.lab_dot_jakosc.setPixmap(QPixmap(
            ":/icon/img/svg_icons/dot_green.svg" if status_map.get("jakosc_prod") else ":/icon/img/svg_icons/dot_red.svg"
        ))
        self.ui.lab_dot_korekta.setPixmap(QPixmap(
            ":/icon/img/svg_icons/dot_green.svg" if status_map.get("korekta_indirect") else ":/icon/img/svg_icons/dot_red.svg"
        ))
        self.ui.lab_dot_bledy_magazyn.setPixmap(QPixmap(
            ":/icon/img/svg_icons/dot_green.svg" if status_map.get("bledy_mag") else ":/icon/img/svg_icons/dot_red.svg"
        ))
        self.ui.lab_dot_kpi_magazyn.setPixmap(QPixmap(
            ":/icon/img/svg_icons/dot_green.svg" if status_map.get("kpi_mag") else ":/icon/img/svg_icons/dot_red.svg"
        ))