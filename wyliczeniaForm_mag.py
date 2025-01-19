from PyQt5.QtWidgets import QWidget, QMessageBox, QFileDialog, QTableWidgetItem,QHeaderView
from PyQt5.QtCore import Qt
import configparser
import openpyxl
#import sys
import os
from datetime import date, datetime

from _wyliczeniaForm_mag_ui import Ui_Form
import db, dodatki

# klasa która pozwala na poprawne sortowanie danych w kolumnach numerycznych.
# Normalnie dane układają się w sposób 1,10,11,2,23,245
# Po zastosowaniu klasy dane posortują się w sposób 1,2,10,11,23,245
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

class MainWindow_wyliczeniaForm_mag(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.ui.btn_przelicz.clicked.connect(self.przeliczenie)
        self.ui.btn_zapisz.clicked.connect(self.zapis_dane_pracownicy)

        self.lista_pracownik_wydania = []
        self.lista_pracownik_przyjecia = []
        self.lista_pracownik_transport_bs = []
        self.lista_pracownik_transport_cz = []
        self.lista_pracownik_wysylka = []

        self.miesiac_roboczy = dodatki.data_miesiac_dzis()

    def przeliczenie(self):
        self.miesiac_info_nieobecnosci()
        self.licz_nieobecnosci()
        self.licz_wydania()
        self.licz_przyjecia()
        self.licz_transport_bs()
        self.licz_transport_cz()
        self.licz_wysylka()

    def miesiac_robocze(self):
        data_str = dodatki.data_miesiac_dzis()
        data = datetime.strptime(data_str, "%Y-%m-%d")
        miesiac = data.month
        rok = data.year
        select_data = "SELECT * FROM `dni_pracujace_w_roku` WHERE rok = '%s' and miesiac = '%s';" % (rok,miesiac)
        connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
        results = db.read_query(connection, select_data)
        robocze = results[0][4]
        connection.close()
        return robocze

    def miesiac_info_nieobecnosci(self):
        dni_robocze = self.miesiac_robocze()
        data_str = dodatki.data_miesiac_dzis()
        data = datetime.strptime(data_str, "%Y-%m-%d")
        miesiac = data.month
        if miesiac < 10:
            miesiac_s = '0%s' % miesiac
        else:
            miesiac_s = '%s' % miesiac
        rok = data.year
        print('dni_robocze:',dni_robocze)
        dni_robocze_075 = dni_robocze * 0.75
        dni_robocze_050 = dni_robocze * 0.50
        print('dni_robocze 075:',round(dni_robocze_075,2),' dni_robocze 050:',round(dni_robocze_050,2))
        self.ui.lab_miesiacNieobecnosci.setText('%s-%s' % (miesiac_s,rok))
        self.ui.lab_miesiacNieobecnosci2.setText('%s-%s' % (miesiac_s,rok))
        self.ui.lab_pracujacychNieobecnosci.setText(str(dni_robocze))
        self.ui.lab_pracujacychNieobecnosci2.setText(str(dni_robocze))
        self.ui.lab_pracujacych075Nieobecnosci.setText(str(round(dni_robocze_075,2)))
        self.ui.lab_pracujacych075Nieobecnosci2.setText(str(round(dni_robocze_075,2)))
        self.ui.lab_pracujacych050Nieobecnosci.setText(str(round(dni_robocze_050,2)))
        self.ui.lab_pracujacych050Nieobecnosci2.setText(str(round(dni_robocze_050,2)))


# ========================================================================================================================================================================
# = NIEOBECNOŚCI =========================================================================================================================================================

    def licz_nieobecnosci(self):
        """Funkcja do załadowania danych z bazy do QTableWidget."""
        try:
            miestac_roboczy = dodatki.data_miesiac_dzis()
            select_data = "SELECT * FROM `nieobecnosci_prod` WHERE miesiac = '%s';" % (miestac_roboczy)
            # select_data = "select * from kpi_mag"
            connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
            results = db.read_query(connection, select_data)

            prog100 = self.ui.lab_pracujacychNieobecnosci.text()
            prog75 = self.ui.lab_pracujacych075Nieobecnosci.text()
            prog50 = self.ui.lab_pracujacych050Nieobecnosci.text()

            lista = []
            for dane in results:
                wsp = 0
                suma_warunek = dane[14]+dane[15]+dane[16]+dane[17]+dane[18]
                if suma_warunek == 0:
                    suma = int(float(dane[4])) + int(float(dane[5])) + int(float(dane[6])) + int(float(dane[7])) + int(float(dane[8])) + int(float(dane[9])) + int(float(dane[10])) + int(float(dane[11])) + int(float(dane[12])) + int(float(dane[13])) + int(float(dane[14])) + int(float(dane[15])) + int(float(dane[16])) + int(float(dane[17])) + int(float(dane[18]))
                else:
                    suma = int(float(dane[4])) + int(float(dane[5])) + int(float(dane[6])) + int(float(dane[7])) + int(float(dane[8])) + int(float(dane[9])) + int(float(dane[10])) + int(float(dane[11])) + int(float(dane[12])) + int(float(dane[14])) + int(float(dane[15])) + int(float(dane[16])) + int(float(dane[17])) + int(float(dane[18]))

                if suma > int(float(prog50)):
                    wsp = 2
                if suma <= int(float(prog50)) and suma > (int(float(prog100)) - int(float(prog75))):
                    wsp = 1
                lista.append([dane[0], dane[1], dane[2], dane[3], suma, wsp])

            self.ui.tab_dane_nieobecnosci.setSortingEnabled(True)

            self.ui.tab_dane_nieobecnosci.setColumnCount(5)  # Zmień na liczbę kolumn w twojej tabeli
            self.ui.tab_dane_nieobecnosci.setRowCount(0)  # Ustawienie liczby wierszy na 0
            self.ui.tab_dane_nieobecnosci.setHorizontalHeaderLabels([
                'Nazwisko i imię',
                'Nr akt',
                'Stanowisko',
                'Razem',
                'Próg'
            ])

            # Ustawianie liczby wierszy na podstawie danych z bazy
            self.ui.tab_dane_nieobecnosci.setRowCount(len(lista))

            # Wypełnianie tabeli danymi
            for row_idx, row_data in enumerate(lista):
                # Przechowujemy id każdego wiersza
                for col_idx, value in enumerate(row_data[1:]):  # Pomijamy id
                    item = NumericTableWidgetItem(str(value))              # Użycie klasy soryującej dane numeryczne

                    item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

                    self.ui.tab_dane_nieobecnosci.setColumnWidth(0, 200)  # Stała szerokość: 150 pikseli
                    self.ui.tab_dane_nieobecnosci.setColumnWidth(1, 75)  # Stała szerokość: 150 pikseli
                    self.ui.tab_dane_nieobecnosci.setColumnWidth(2, 200)  # Stała szerokość: 150 pikseli
                    self.ui.tab_dane_nieobecnosci.setColumnWidth(3, 75)  # Stała szerokość: 150 pikseli
                    self.ui.tab_dane_nieobecnosci.setColumnWidth(4, 75)  # Stała szerokość: 150 pikseli

                    self.ui.tab_dane_nieobecnosci.setItem(row_idx, col_idx, item)

        except db.Error as e:
            print(f"Błąd przy pobieraniu danych z bazy danych: {e}")

# ========================================================================================================================================================================
# = WYDANIA ==============================================================================================================================================================

    def licz_wydania(self):
        """Funkcja do załadowania danych z bazy do QTableWidget."""
        try:
            connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
            results_direct = db.wywolaj_procedure_zmienna(connection, 'wyliczenia_mag_wydania_direct', self.miesiac_roboczy)
            connection.close()

            connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
            results_wydajnosc = db.wywolaj_procedure_zmienna(connection, 'wyliczenia_mag_wydania_wydajnosc', self.miesiac_roboczy)
            connection.close()

            ile_zmian = len(results_direct)

            lista = []
            if ile_zmian == 1:
                for row in results_direct:
                    reported = planned = wydaj = produkt = 0.0
                    if row[2] == 'A':
                        zmiana = row[2]
                        dir = round(row[0], 2)
                        indir = round(row[1], 2)
                        direct = round((row[0] / (row[0] + row[1])) * 100, 2)
                        indirect = round((row[1] / (row[0] + row[1])) * 100, 2)
                        for row2 in results_wydajnosc:
                            if row2[3] == 'A':
                                reported = round(row2[0], 2)
                                planned = round(row2[1], 2)
                                wydajnosci = row2[2]
                            if row2[3] == 'B' or row2[3] == 'C' or row2[3] == 'inna':
                                reported = round(reported + row2[0], 2)
                                planned = round(planned + row2[1], 2)
                        wydaj = round((planned / reported) * 100, 2)
                        produkt = round(direct * (planned / reported), 2)
                    lista.append([zmiana, dir, indir, direct, indirect, reported, planned, wydaj, produkt])

            if ile_zmian == 2:
                for row in results_direct:
                    reported = planned = wydaj = produkt = 0.0
                    if row[2] == 'A':
                        zmiana = row[2]
                        dir = round(row[0], 2)
                        indir = round(row[1], 2)
                        direct = round((row[0] / (row[0] + row[1])) * 100, 2)
                        indirect = round((row[1] / (row[0] + row[1])) * 100, 2)
                        for row2 in results_wydajnosc:
                            if row2[3] == 'A':
                                reported = round(row2[0], 2)
                                planned = round(row2[1], 2)
                                wydajnosci = round(row2[2], 2)
                            if row2[3] == 'C':
                                reported = round(reported + (row2[0] / 2), 2)
                                planned = round(planned + (row2[1] / 2), 2)
                                wydajnosci = round(wydajnosci + (row2[2] / 2), 2)
                            if row2[3] == 'inna':
                                reported = round(reported + (row2[0] / 2), 2)
                                planned = round(planned + (row2[1] / 2), 2)
                                wydajnosci = round(wydajnosci + (row2[2] / 2), 2)
                        wydaj = round((planned / reported) * 100, 2)
                        produkt = round(direct * (planned / reported), 2)
                    if row[2] == 'B':
                        zmiana = row[2]
                        dir = round(row[0], 2)
                        indir = round(row[1], 2)
                        direct = round((row[0] / (row[0] + row[1])) * 100, 2)
                        indirect = round((row[1] / (row[0] + row[1])) * 100, 2)
                        for row2 in results_wydajnosc:
                            if row2[3] == 'B':
                                reported = round(row2[0], 2)
                                planned = round(row2[1], 2)
                                wydajnosci = round(row2[2], 2)
                            if row2[3] == 'C':
                                reported = reported + round((row2[0] / 2), 2)
                                planned = planned + round((row2[1] / 2), 2)
                            if row2[3] == 'inna':
                                reported = reported + round((row2[0] / 2), 2)
                                planned = planned + round((row2[1] / 2), 2)

                        wydaj = round((planned / reported) * 100, 2)
                        produkt = round(direct * (planned / reported), 2)
                    lista.append([zmiana, dir, indir, direct, indirect, reported, planned, wydaj, produkt])

            if ile_zmian == 3:
                for row in results_direct:
                    reported = planned = wydaj = produkt = 0.0
                    if row[2] == 'A':
                        zmiana = row[2]
                        dir = round(row[0], 2)
                        indir = round(row[1], 2)
                        direct = round((row[0] / (row[0] + row[1])) * 100, 2)
                        indirect = round((row[1] / (row[0] + row[1])) * 100, 2)
                        for row2 in results_wydajnosc:
                            if row2[3] == 'A':
                                reported = round(row2[0], 2)
                                planned = round(row2[1], 2)
                                wydajnosci = round(row2[2], 2)
                            if row2[3] == 'inna':
                                reported = round(reported + (row2[0] / 3), 2)
                                planned = round(planned + (row2[1] / 3), 2)
                                wydajnosci = round(wydajnosci + (row2[2] / 3), 2)
                        wydaj = round((planned / reported) * 100, 2)
                        produkt = round(direct * (planned / reported), 2)
                    if row[2] == 'B':
                        zmiana = row[2]
                        dir = round(row[0], 2)
                        indir = round(row[1], 2)
                        direct = round((row[0] / (row[0] + row[1])) * 100, 2)
                        indirect = round((row[1] / (row[0] + row[1])) * 100, 2)
                        for row2 in results_wydajnosc:
                            if row2[3] == 'B':
                                reported = round(row2[0], 2)
                                planned = round(row2[1], 2)
                                wydajnosci = round(row2[2], 2)
                            if row2[3] == 'inna':
                                reported = round(reported + (row2[0] / 3), 2)
                                planned = round(planned + (row2[1] / 3), 2)

                        wydaj = round((planned / reported) * 100, 2)
                        produkt = round(direct * (planned / reported), 2)
                    if row[2] == 'C':
                        zmiana = row[2]
                        dir = round(row[0], 2)
                        indir = round(row[1], 2)
                        direct = round((row[0] / (row[0] + row[1])) * 100, 2)
                        indirect = round((row[1] / (row[0] + row[1])) * 100, 2)
                        for row2 in results_wydajnosc:
                            if row2[3] == 'C':
                                reported = round(row2[0], 2)
                                planned = round(row2[1], 2)
                                wydajnosci = round(row2[2], 2)
                            if row2[3] == 'inna':
                                reported = round(reported + (row2[0] / 3), 2)
                                planned = round(planned + (row2[1] / 3), 2)

                        wydaj = round((planned / reported) * 100, 2)
                        produkt = round(direct * (planned / reported), 2)

                    lista.append([zmiana, dir, indir, direct, indirect, reported, planned, wydaj, produkt])

            prog100 = self.ui.lab_pracujacychNieobecnosci.text()
            prog75 = self.ui.lab_pracujacych075Nieobecnosci.text()
            prog50 = self.ui.lab_pracujacych050Nieobecnosci.text()


            connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
            results_pracownik = db.wywolaj_procedure_zmienna(connection, 'wyliczenia_mag_wydania_pracownik', self.miesiac_roboczy)
            connection.close()

            select_data_bledy = "select * from bledy_mag bm where bm.miesiac = '{0}'".format(self.miesiac_roboczy)
            connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
            results_bledy = db.read_query(connection, select_data_bledy)
            connection.close()

            connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
            results_iw = db.wywolaj_procedure_zmienna(connection, 'wyliczenia_mag_wydania_iw', self.miesiac_roboczy)
            connection.close()

            select_wytyczne = ''' select * from wytyczne_mag wm where wm.aktywny = 1 and wm.id_grupa = 1 '''
            connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
            results_wytyczne = db.read_query(connection, select_wytyczne)
            connection.close()

            kwota_bledy_zew = results_wytyczne[0][8]
            kwota_bledy_wew = results_wytyczne[1][8]
            target_ind_IW = results_wytyczne[2][3]
            target_produkt = results_wytyczne[2][6]
            kwota_produkt = results_wytyczne[2][8]

            for dane in results_pracownik:
                blad_zew = blad_wew = prod_zmian = suma = 0.0
                prod_prem = iw_prem = 0
                for blad in results_bledy:
                    if dane[0] == blad[1]:
                        if blad[2] == 0:
                            blad_zew = float(kwota_bledy_zew)
                        if blad[3] == 0:
                            blad_wew = float(kwota_bledy_wew)
                        if blad[3] == 1:
                            blad_wew = float(kwota_bledy_wew) * 0.75
                        if blad[3] == 2:
                            blad_wew = float(kwota_bledy_wew) * 0.50
                        if blad[3] > 2:
                            blad_wew = float(kwota_bledy_wew) * 0.0
                    suma = float(blad_zew) + float(blad_wew)
                for wyd in lista:
                    if dane[6] == wyd[0]:
                        if float(wyd[8]) >= float(target_produkt):
                            prod_prem = 1
                for iw_lim in results_iw:
                    if dane[0] == iw_lim[0]:
                        if float(iw_lim[3]) <= float(target_ind_IW):
                            iw_prem = 1
                if prod_prem == 1 and iw_prem == 1:
                    prod_zmian = float(kwota_produkt)

                suma = float(suma) + float(prod_zmian)

                wsp = 0
                wynik_n = suma
                if dane[3] > int(float(prog50)):
                    wsp = 2
                    wynik_n = 0.0
                if dane[3] <= int(float(prog50)) and dane[3] > (int(float(prog100)) - int(float(prog75))):
                    wsp = 1
                    wynik_n = suma / 2

                # print(dane[0], dane[1], dane[2], blad_zew, blad_wew, '---', prod_zmian, suma, '---', wsp, wynik_n)
                self.lista_pracownik_wydania.append(
                    [dane[0], dane[1], dane[2], blad_zew, blad_wew, prod_zmian, suma, wsp, wynik_n])

            suma_kwot = sum(round(float(wiersz[8]), 2) for wiersz in self.lista_pracownik_wydania)
            self.ui.lab_sumaWydania.setText(str(suma_kwot))
            self.ui.lab_sumaWydania2.setText(str(suma_kwot))

            self.ui.tab_wyliczenia_wydania.setSortingEnabled(True)

            self.ui.tab_wyliczenia_wydania.setColumnCount(9)  # Zmień na liczbę kolumn w twojej tabeli
            self.ui.tab_wyliczenia_wydania.setRowCount(0)  # Ustawienie liczby wierszy na 0
            self.ui.tab_wyliczenia_wydania.setHorizontalHeaderLabels([
                'Zmiana',
                'Direct',
                'Indirect',
                'Direct %',
                'Indirect %',
                'Planowany',
                'Raportowany',
                'Wydajność',
                'Produktywność'
            ])

            # Ustawianie liczby wierszy na podstawie danych z bazy
            self.ui.tab_wyliczenia_wydania.setRowCount(len(lista))

            # Wypełnianie tabeli danymi
            for row_idx, row_data in enumerate(lista):
                # Przechowujemy id każdego wiersza
                for col_idx, value in enumerate(row_data[0:]):  # Pomijamy id
                    item = NumericTableWidgetItem(str(value))              # Użycie klasy soryującej dane numeryczne

                    item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

                    self.ui.tab_wyliczenia_wydania.setColumnWidth(0, 75)  # Stała szerokość: 150 pikseli
                    self.ui.tab_wyliczenia_wydania.setColumnWidth(1, 75)  # Stała szerokość: 150 pikseli
                    self.ui.tab_wyliczenia_wydania.setColumnWidth(2, 75)  # Stała szerokość: 150 pikseli
                    self.ui.tab_wyliczenia_wydania.setColumnWidth(3, 75)  # Stała szerokość: 150 pikseli
                    self.ui.tab_wyliczenia_wydania.setColumnWidth(4, 75)  # Stała szerokość: 150 pikseli
                    self.ui.tab_wyliczenia_wydania.setColumnWidth(5, 75)  # Stała szerokość: 150 pikseli
                    self.ui.tab_wyliczenia_wydania.setColumnWidth(6, 75)  # Stała szerokość: 150 pikseli
                    self.ui.tab_wyliczenia_wydania.setColumnWidth(7, 75)  # Stała szerokość: 150 pikseli

                    self.ui.tab_wyliczenia_wydania.setItem(row_idx, col_idx, item)

            self.ui.tab_dane_wydania.setSortingEnabled(True)

            self.ui.tab_dane_wydania.setColumnCount(9)  # Zmień na liczbę kolumn w twojej tabeli
            self.ui.tab_dane_wydania.setRowCount(0)  # Ustawienie liczby wierszy na 0
            self.ui.tab_dane_wydania.setHorizontalHeaderLabels([
                'Nr akt',
                'Kod',
                'Imię i nazwisko',
                'Błędy zew.',
                'Błędy wew.',
                'Produktywnosc',
                'Suma',
                'Nieobecnosc',
                'Premia'
            ])

            # Ustawianie liczby wierszy na podstawie danych z bazy
            self.ui.tab_dane_wydania.setRowCount(len(self.lista_pracownik_wydania))

            # Wypełnianie tabeli danymi
            for row_idx, row_data in enumerate(self.lista_pracownik_wydania):
                # Przechowujemy id każdego wiersza
                for col_idx, value in enumerate(row_data[0:]):  # Pomijamy id
                    item = NumericTableWidgetItem(str(value))              # Użycie klasy soryującej dane numeryczne

                    item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

                    self.ui.tab_dane_wydania.setColumnWidth(0, 75)  # Stała szerokość: 150 pikseli
                    self.ui.tab_dane_wydania.setColumnWidth(1, 75)  # Stała szerokość: 150 pikseli
                    self.ui.tab_dane_wydania.setColumnWidth(2, 200)  # Stała szerokość: 150 pikseli
                    self.ui.tab_dane_wydania.setColumnWidth(3, 75)  # Stała szerokość: 150 pikseli
                    self.ui.tab_dane_wydania.setColumnWidth(4, 75)  # Stała szerokość: 150 pikseli
                    self.ui.tab_dane_wydania.setColumnWidth(5, 75)  # Stała szerokość: 150 pikseli
                    self.ui.tab_dane_wydania.setColumnWidth(6, 75)  # Stała szerokość: 150 pikseli
                    self.ui.tab_dane_wydania.setColumnWidth(7, 75)  # Stała szerokość: 150 pikseli
                    self.ui.tab_dane_wydania.setColumnWidth(8, 75)  # Stała szerokość: 150 pikseli

                    self.ui.tab_dane_wydania.setItem(row_idx, col_idx, item)

        except db.Error as e:
            print(f"Błąd przy pobieraniu danych z bazy danych: {e}")

# ========================================================================================================================================================================
# = PRZYJĘCIA ============================================================================================================================================================

    def licz_przyjecia(self):
        """Funkcja do załadowania danych z bazy do QTableWidget."""
        try:
            connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
            grupa_mag = 2                               # jest to ID grypy pracowników magazynu zgodnie z tabelą grupy_mag
            results = db.wywolaj_procedure_zmienna2(connection, 'wyliczenia_mag_pracownik', self.miesiac_roboczy, grupa_mag)
            connection.close()

            select_kpi = ''' select * from kpi_mag km where km.miesiac = '{0}' '''.format(self.miesiac_roboczy)
            connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
            results_kpi = db.read_query(connection, select_kpi)
            connection.close()

            select_bledy = ''' select * from bledy_mag bm where bm.miesiac = '{0}' '''.format(self.miesiac_roboczy)
            connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
            results_bledy = db.read_query(connection, select_bledy)
            connection.close()

            select_wytyczne = ''' select * from wytyczne_mag wm where wm.aktywny = 1 and wm.id_grupa = 2 '''
            connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
            results_wytyczne = db.read_query(connection, select_wytyczne)
            connection.close()

            prog100 = self.ui.lab_pracujacychNieobecnosci.text()
            prog75 = self.ui.lab_pracujacych075Nieobecnosci.text()
            prog50 = self.ui.lab_pracujacych050Nieobecnosci.text()

            dp_dane = int(results_kpi[0][3])
            target_dp_init = int(results_wytyczne[0][3])
            kwota_dp_init = results_wytyczne[0][8]
            target_reklamacje = results_wytyczne[1][3]
            kwota_reklamacje = results_wytyczne[1][8]
            if dp_dane >= target_dp_init:
                prem_dp = int(kwota_dp_init)

            for dane in results:
                for blad in results_bledy:
                    if dane[0] == blad[1]:
                        blad = blad[3]
                        print('blad:',blad)
                        if int(blad) == 0:
                            prem_blad = float(kwota_reklamacje)
                        elif int(blad) == 1:
                            prem_blad = float(kwota_reklamacje) * 0.75
                        elif int(blad) == 2:
                            prem_blad = float(kwota_reklamacje) * 0.50
                        else:
                            prem_blad = 0.0
                        break
                suma_prem = prem_dp +prem_blad

                wsp = 0
                wynik_n = suma_prem
                if dane[3] > int(float(prog50)):
                    wsp = 2
                    wynik_n = 0.0
                if dane[3] <= int(float(prog50)) and dane[3] > (int(float(prog100)) - int(float(prog75))):
                    wsp = 1
                    wynik_n = suma_prem / 2

                #print(dane[0],dane[1],dane[2],prem_dp,prem_blad,suma_prem,wsp,wynik_n)
                self.lista_pracownik_przyjecia.append([dane[0],dane[4],dane[1],dane[2],prem_dp,prem_blad,suma_prem,wsp,wynik_n])

                suma_kwot = sum(round(float(wiersz[8]), 2) for wiersz in self.lista_pracownik_przyjecia)
                self.ui.lab_sumaPrzyjecia.setText(str(suma_kwot))
                self.ui.lab_sumaPrzyjecia2.setText(str(suma_kwot))

            self.ui.tab_dane_przyjecia.setSortingEnabled(True)

            self.ui.tab_dane_przyjecia.setColumnCount(9)  # Zmień na liczbę kolumn w twojej tabeli
            self.ui.tab_dane_przyjecia.setRowCount(0)  # Ustawienie liczby wierszy na 0
            self.ui.tab_dane_przyjecia.setHorizontalHeaderLabels([
                'Nr akt',
                'Kod',
                'Imię i nazwisko',
                'Dział',
                'DP',
                'Reklamacje',
                'Suma Prem',
                'Chorował',
                'PREMIA'
            ])

            # Ustawianie liczby wierszy na podstawie danych z bazy
            self.ui.tab_dane_przyjecia.setRowCount(len(self.lista_pracownik_przyjecia))

            # Wypełnianie tabeli danymi
            for row_idx, row_data in enumerate(self.lista_pracownik_przyjecia):
                # Przechowujemy id każdego wiersza
                for col_idx, value in enumerate(row_data[0:]):  # Pomijamy id
                    item = NumericTableWidgetItem(str(value))              # Użycie klasy soryującej dane numeryczne

                    item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

                    self.ui.tab_dane_przyjecia.setColumnWidth(0, 75)  # Stała szerokość: 150 pikseli
                    self.ui.tab_dane_przyjecia.setColumnWidth(1, 75)  # Stała szerokość: 150 pikseli
                    self.ui.tab_dane_przyjecia.setColumnWidth(2, 200)  # Stała szerokość: 150 pikseli
                    self.ui.tab_dane_przyjecia.setColumnWidth(3, 75)  # Stała szerokość: 150 pikseli
                    self.ui.tab_dane_przyjecia.setColumnWidth(4, 75)  # Stała szerokość: 150 pikseli
                    self.ui.tab_dane_przyjecia.setColumnWidth(5, 75)  # Stała szerokość: 150 pikseli
                    self.ui.tab_dane_przyjecia.setColumnWidth(6, 75)  # Stała szerokość: 150 pikseli
                    self.ui.tab_dane_przyjecia.setColumnWidth(7, 75)  # Stała szerokość: 150 pikseli
                    self.ui.tab_dane_przyjecia.setColumnWidth(8, 75)  # Stała szerokość: 150 pikseli

                    self.ui.tab_dane_przyjecia.setItem(row_idx, col_idx, item)

        except db.Error as e:
            print(f"Błąd przy pobieraniu danych z bazy danych: {e}")

# ========================================================================================================================================================================
# = TRANSPORT BS =========================================================================================================================================================

    def licz_transport_bs(self):
        """Funkcja do załadowania danych z bazy do QTableWidget."""
        try:
            connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
            grupa_mag = 3  # jest to ID grypy pracowników magazynu zgodnie z tabelą grupy_mag
            results = db.wywolaj_procedure_zmienna2(connection, 'wyliczenia_mag_pracownik', self.miesiac_roboczy, grupa_mag)
            connection.close()

            select_kpi = ''' select * from kpi_mag km where km.miesiac = '{0}' '''.format(self.miesiac_roboczy)
            connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
            results_kpi = db.read_query(connection, select_kpi)
            connection.close()

            select_bledy = ''' select * from bledy_mag bm where bm.miesiac = '{0}' '''.format(self.miesiac_roboczy)
            connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
            results_bledy = db.read_query(connection, select_bledy)
            connection.close()

            select_wytyczne = ''' select * from wytyczne_mag wm where wm.aktywny = 1 and wm.id_grupa = 3 '''
            connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
            results_wytyczne = db.read_query(connection, select_wytyczne)
            connection.close()

            prog100 = self.ui.lab_pracujacychNieobecnosci.text()
            prog75 = self.ui.lab_pracujacych075Nieobecnosci.text()
            prog50 = self.ui.lab_pracujacych050Nieobecnosci.text()

            prem_dp = prem_zgodnosc = prem_blad = 0
            dp_dane = int(results_kpi[0][3])
            zgodnosc_dane = int(results_kpi[0][4])
            target_dp_init = int(results_wytyczne[0][3])
            kwota_dp_init = results_wytyczne[0][8]
            target_zgodnosc = int(results_wytyczne[1][3])
            kwota_zgodnosc = results_wytyczne[1][8]
            target_reklamacje = int(results_wytyczne[2][3])
            kwota_reklamacje = results_wytyczne[2][8]
            if dp_dane >= target_dp_init:
                prem_dp = int(kwota_dp_init)
            if zgodnosc_dane >= target_zgodnosc:
                prem_zgodnosc = int(kwota_zgodnosc)

            for dane in results:
                for blad in results_bledy:
                    if dane[0] == blad[1]:
                        blad = blad[3]
                        print('blad:', blad)
                        if int(blad) == 0:
                            prem_blad = float(kwota_reklamacje)
                        elif int(blad) == 1:
                            prem_blad = float(kwota_reklamacje) * 0.75
                        elif int(blad) == 2:
                            prem_blad = float(kwota_reklamacje) * 0.50
                        else:
                            prem_blad = 0.0
                        break
                suma_prem = prem_dp + prem_blad + prem_zgodnosc

                wsp = 0
                wynik_n = suma_prem
                if dane[3] > int(float(prog50)):
                    wsp = 2
                    wynik_n = 0.0
                if dane[3] <= int(float(prog50)) and dane[3] > (int(float(prog100)) - int(float(prog75))):
                    wsp = 1
                    wynik_n = suma_prem / 2

                #print(dane[0],dane[1],dane[2],prem_dp,prem_blad,suma_prem,wsp,wynik_n)
                self.lista_pracownik_transport_bs.append([dane[0],dane[4],dane[1],dane[2],prem_dp,prem_blad,prem_zgodnosc,suma_prem,wsp,wynik_n])

                suma_kwot = sum(round(float(wiersz[9]), 2) for wiersz in self.lista_pracownik_transport_bs)
                self.ui.lab_sumaTransport_BS.setText(str(suma_kwot))
                self.ui.lab_sumaTransport_BS2.setText(str(suma_kwot))

            self.ui.tab_dane_transport_bs.setSortingEnabled(True)

            self.ui.tab_dane_transport_bs.setColumnCount(10)  # Zmień na liczbę kolumn w twojej tabeli
            self.ui.tab_dane_transport_bs.setRowCount(0)  # Ustawienie liczby wierszy na 0
            self.ui.tab_dane_transport_bs.setHorizontalHeaderLabels([
                'Nr akt',
                'Kod',
                'Imię i nazwisko',
                'Dział',
                'DP',
                'Reklamacje',
                'stany mat.',
                'Suma Prem',
                'Chorował',
                'PREMIA'
            ])

            # Ustawianie liczby wierszy na podstawie danych z bazy
            self.ui.tab_dane_transport_bs.setRowCount(len(self.lista_pracownik_transport_bs))

            # Wypełnianie tabeli danymi
            for row_idx, row_data in enumerate(self.lista_pracownik_transport_bs):
                # Przechowujemy id każdego wiersza
                for col_idx, value in enumerate(row_data[0:]):  # Pomijamy id
                    item = NumericTableWidgetItem(str(value))              # Użycie klasy soryującej dane numeryczne

                    item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

                    self.ui.tab_dane_transport_bs.setColumnWidth(0, 75)  # Stała szerokość: 150 pikseli
                    self.ui.tab_dane_transport_bs.setColumnWidth(1, 75)  # Stała szerokość: 150 pikseli
                    self.ui.tab_dane_transport_bs.setColumnWidth(2, 200)  # Stała szerokość: 150 pikseli
                    self.ui.tab_dane_transport_bs.setColumnWidth(3, 75)  # Stała szerokość: 150 pikseli
                    self.ui.tab_dane_transport_bs.setColumnWidth(4, 75)  # Stała szerokość: 150 pikseli
                    self.ui.tab_dane_transport_bs.setColumnWidth(5, 75)  # Stała szerokość: 150 pikseli
                    self.ui.tab_dane_transport_bs.setColumnWidth(6, 75)  # Stała szerokość: 150 pikseli
                    self.ui.tab_dane_transport_bs.setColumnWidth(7, 75)  # Stała szerokość: 150 pikseli
                    self.ui.tab_dane_transport_bs.setColumnWidth(8, 75)  # Stała szerokość: 150 pikseli
                    self.ui.tab_dane_transport_bs.setColumnWidth(9, 75)  # Stała szerokość: 150 pikseli

                    self.ui.tab_dane_transport_bs.setItem(row_idx, col_idx, item)

        except db.Error as e:
            print(f"Błąd przy pobieraniu danych z bazy danych: {e}")

# ========================================================================================================================================================================
# = TRANSPORT CZ =========================================================================================================================================================

    def licz_transport_cz(self):
        """Funkcja do załadowania danych z bazy do QTableWidget."""
        try:
            connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
            grupa_mag = 4  # jest to ID grypy pracowników magazynu zgodnie z tabelą grupy_mag
            results = db.wywolaj_procedure_zmienna2(connection, 'wyliczenia_mag_pracownik', self.miesiac_roboczy, grupa_mag)
            connection.close()

            select_kpi = ''' select * from kpi_mag km where km.miesiac = '{0}' '''.format(self.miesiac_roboczy)
            connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
            results_kpi = db.read_query(connection, select_kpi)
            connection.close()

            select_bledy = ''' select * from bledy_mag bm where bm.miesiac = '{0}' '''.format(self.miesiac_roboczy)
            connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
            results_bledy = db.read_query(connection, select_bledy)
            connection.close()

            select_wytyczne = ''' select * from wytyczne_mag wm where wm.aktywny = 1 and wm.id_grupa = 4 '''
            connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
            results_wytyczne = db.read_query(connection, select_wytyczne)
            connection.close()

            prog100 = self.ui.lab_pracujacychNieobecnosci.text()
            prog75 = self.ui.lab_pracujacych075Nieobecnosci.text()
            prog50 = self.ui.lab_pracujacych050Nieobecnosci.text()

            prem_dp = prem_zgodnosc = prem_zapasy = prem_raportowanie = 0
            dp_dane = int(results_kpi[0][3])
            zgodnosc_dane = int(results_kpi[0][4])
            zapasy_dane = int(results_kpi[0][5])
            raportowanie_dane = int(results_kpi[0][6])
            target_dp_init = int(results_wytyczne[0][3])
            kwota_dp_init = results_wytyczne[0][8]
            target_zgodnosc = int(results_wytyczne[1][3])
            kwota_zgodnosc = results_wytyczne[1][8]
            target_zapasy = int(results_wytyczne[2][3])
            kwota_zapasy = results_wytyczne[2][8]
            target_raportowanie = int(results_wytyczne[3][3])
            kwota_raportowanie = results_wytyczne[3][8]
            if dp_dane >= target_dp_init:
                prem_dp = int(kwota_dp_init)
            if zgodnosc_dane >= target_zgodnosc:
                prem_zgodnosc = int(kwota_zgodnosc)
            if zapasy_dane <= target_zapasy:
                prem_zapasy = int(kwota_zapasy)
            if raportowanie_dane <= target_raportowanie:
                prem_raportowanie = int(kwota_raportowanie)

            for dane in results:
                suma_prem = prem_dp + prem_zgodnosc + prem_zapasy + prem_raportowanie

                wsp = 0
                wynik_n = suma_prem
                if dane[3] > int(float(prog50)):
                    wsp = 2
                    wynik_n = 0.0
                if dane[3] <= int(float(prog50)) and dane[3] > (int(float(prog100)) - int(float(prog75))):
                    wsp = 1
                    wynik_n = suma_prem / 2

                #print(dane[0],dane[1],dane[2],prem_dp,prem_blad,suma_prem,wsp,wynik_n)
                self.lista_pracownik_transport_cz.append([dane[0],dane[4],dane[1],dane[2],prem_dp,prem_zgodnosc,prem_zapasy,prem_raportowanie,suma_prem,wsp,wynik_n])

                suma_kwot = sum(round(float(wiersz[10]), 2) for wiersz in self.lista_pracownik_transport_cz)
                self.ui.lab_sumaTransport_Cz.setText(str(suma_kwot))
                self.ui.lab_sumaTransport_Cz2.setText(str(suma_kwot))

            self.ui.tab_dane_transport_Cz.setSortingEnabled(True)

            self.ui.tab_dane_transport_Cz.setColumnCount(11)  # Zmień na liczbę kolumn w twojej tabeli
            self.ui.tab_dane_transport_Cz.setRowCount(0)  # Ustawienie liczby wierszy na 0
            self.ui.tab_dane_transport_Cz.setHorizontalHeaderLabels([
                'Nr akt',
                'Kod',
                'Imię i nazwisko',
                'Dział',
                'DP',
                'stany mat.',
                'lokal. ****',
                'oper. Przych. ',
                'Suma Prem',
                'Chorował',
                'PREMIA'
            ])

            # Ustawianie liczby wierszy na podstawie danych z bazy
            self.ui.tab_dane_transport_Cz.setRowCount(len(self.lista_pracownik_transport_cz))

            # Wypełnianie tabeli danymi
            for row_idx, row_data in enumerate(self.lista_pracownik_transport_cz):
                # Przechowujemy id każdego wiersza
                for col_idx, value in enumerate(row_data[0:]):  # Pomijamy id
                    item = NumericTableWidgetItem(str(value))              # Użycie klasy soryującej dane numeryczne

                    item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

                    self.ui.tab_dane_transport_Cz.setColumnWidth(0, 75)  # Stała szerokość: 150 pikseli
                    self.ui.tab_dane_transport_Cz.setColumnWidth(1, 75)  # Stała szerokość: 150 pikseli
                    self.ui.tab_dane_transport_Cz.setColumnWidth(2, 200)  # Stała szerokość: 150 pikseli
                    self.ui.tab_dane_transport_Cz.setColumnWidth(3, 75)  # Stała szerokość: 150 pikseli
                    self.ui.tab_dane_transport_Cz.setColumnWidth(4, 75)  # Stała szerokość: 150 pikseli
                    self.ui.tab_dane_transport_Cz.setColumnWidth(5, 75)  # Stała szerokość: 150 pikseli
                    self.ui.tab_dane_transport_Cz.setColumnWidth(6, 75)  # Stała szerokość: 150 pikseli
                    self.ui.tab_dane_transport_Cz.setColumnWidth(7, 75)  # Stała szerokość: 150 pikseli
                    self.ui.tab_dane_transport_Cz.setColumnWidth(8, 75)  # Stała szerokość: 150 pikseli
                    self.ui.tab_dane_transport_Cz.setColumnWidth(9, 75)  # Stała szerokość: 150 pikseli
                    self.ui.tab_dane_transport_Cz.setColumnWidth(10, 75)  # Stała szerokość: 150 pikseli

                    self.ui.tab_dane_transport_Cz.setItem(row_idx, col_idx, item)

        except db.Error as e:
            print(f"Błąd przy pobieraniu danych z bazy danych: {e}")

# ========================================================================================================================================================================
# = WYSYŁKA ==============================================================================================================================================================

    def licz_wysylka(self):
        """Funkcja do załadowania danych z bazy do QTableWidget."""
        try:
            connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
            grupa_mag = 5  # jest to ID grypy pracowników magazynu zgodnie z tabelą grupy_mag
            results = db.wywolaj_procedure_zmienna2(connection, 'wyliczenia_mag_pracownik', self.miesiac_roboczy, grupa_mag)
            connection.close()

            select_kpi = ''' select * from kpi_mag km where km.miesiac = '{0}' '''.format(self.miesiac_roboczy)
            connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
            results_kpi = db.read_query(connection, select_kpi)
            connection.close()

            select_bledy = ''' select * from bledy_mag bm where bm.miesiac = '{0}' '''.format(self.miesiac_roboczy)
            connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
            results_bledy = db.read_query(connection, select_bledy)
            connection.close()

            select_wytyczne = ''' select * from wytyczne_mag wm where wm.aktywny = 1 and wm.id_grupa = 5 '''
            connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
            results_wytyczne = db.read_query(connection, select_wytyczne)
            connection.close()

            prog100 = self.ui.lab_pracujacychNieobecnosci.text()
            prog75 = self.ui.lab_pracujacych075Nieobecnosci.text()
            prog50 = self.ui.lab_pracujacych050Nieobecnosci.text()

            prem_delivery = bledy_zew = 0
            delivery = int(results_kpi[0][1])
            target_bledy = int(results_wytyczne[0][3])
            kwota_bledy = results_wytyczne[0][8]
            target_delivery = int(results_wytyczne[1][3])
            kwota_delivery = results_wytyczne[1][8]

            if delivery >= target_delivery:
                prem_delivery = int(kwota_delivery)

            for dane in results:
                for blad in results_bledy:
                    if dane[0] == blad[1]:
                        blad = blad[2]
                        if int(blad) == target_bledy:
                            prem_blad = int(kwota_bledy)
                        else:
                            prem_blad = 0
                        break

                suma_prem = prem_delivery + prem_blad

                wsp = 0
                wynik_n = suma_prem
                if dane[3] > int(float(prog50)):
                    wsp = 2
                    wynik_n = 0.0
                if dane[3] <= int(float(prog50)) and dane[3] > (int(float(prog100)) - int(float(prog75))):
                    wsp = 1
                    wynik_n = suma_prem / 2

                #print(dane[0],dane[1],dane[2],prem_dp,prem_blad,suma_prem,wsp,wynik_n)
                self.lista_pracownik_wysylka.append([dane[0],dane[4],dane[1],dane[2],prem_delivery,prem_blad,suma_prem,wsp,wynik_n])

                suma_kwot = sum(round(float(wiersz[8]), 2) for wiersz in self.lista_pracownik_wysylka)
                self.ui.lab_sumaWysylka.setText(str(suma_kwot))
                self.ui.lab_sumaWysylka2.setText(str(suma_kwot))

            self.ui.tab_dane_wysylka.setSortingEnabled(True)

            self.ui.tab_dane_wysylka.setColumnCount(9)  # Zmień na liczbę kolumn w twojej tabeli
            self.ui.tab_dane_wysylka.setRowCount(0)  # Ustawienie liczby wierszy na 0
            self.ui.tab_dane_wysylka.setHorizontalHeaderLabels([
                'Nr akt',
                'Kod',
                'Imię i nazwisko',
                'Dział',
                'Delivery',
                'Reklamacje zew',
                'Suma Prem',
                'Chorował',
                'PREMIA'
            ])

            # Ustawianie liczby wierszy na podstawie danych z bazy
            self.ui.tab_dane_wysylka.setRowCount(len(self.lista_pracownik_wysylka))

            # Wypełnianie tabeli danymi
            for row_idx, row_data in enumerate(self.lista_pracownik_wysylka):
                # Przechowujemy id każdego wiersza
                for col_idx, value in enumerate(row_data[0:]):  # Pomijamy id
                    item = NumericTableWidgetItem(str(value))              # Użycie klasy soryującej dane numeryczne

                    item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

                    self.ui.tab_dane_wysylka.setColumnWidth(0, 75)  # Stała szerokość: 150 pikseli
                    self.ui.tab_dane_wysylka.setColumnWidth(1, 75)  # Stała szerokość: 150 pikseli
                    self.ui.tab_dane_wysylka.setColumnWidth(2, 200)  # Stała szerokość: 150 pikseli
                    self.ui.tab_dane_wysylka.setColumnWidth(3, 75)  # Stała szerokość: 150 pikseli
                    self.ui.tab_dane_wysylka.setColumnWidth(4, 75)  # Stała szerokość: 150 pikseli
                    self.ui.tab_dane_wysylka.setColumnWidth(5, 75)  # Stała szerokość: 150 pikseli
                    self.ui.tab_dane_wysylka.setColumnWidth(6, 75)  # Stała szerokość: 150 pikseli
                    self.ui.tab_dane_wysylka.setColumnWidth(7, 75)  # Stała szerokość: 150 pikseli
                    self.ui.tab_dane_wysylka.setColumnWidth(8, 75)  # Stała szerokość: 150 pikseli

                    self.ui.tab_dane_wysylka.setItem(row_idx, col_idx, item)

        except db.Error as e:
            print(f"Błąd przy pobieraniu danych z bazy danych: {e}")

# ========================================================================================================================================================================
# = INNE =================================================================================================================================================================
    def sprawdz_wpisy(self):
        miestac_roboczy = dodatki.data_miesiac_dzis()
        select_data_eksport = "SELECT * FROM eksport_danych ed WHERE ed.miesiac = '{0}' and ed.dzial = 'mag'".format(
            miestac_roboczy)
        connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
        result_eksport = db.read_query(connection, select_data_eksport)
        connection.close()

        if result_eksport:
            connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
            for x in result_eksport:
                delete_data = "delete from eksport_danych where id = '%s' and miesiac = '%s' and dzial = 'mag';" % (
                x[0], miestac_roboczy)
                print('Do skasowania z eksportu:', delete_data)
                db.execute_query(connection, delete_data)
            connection.close()
        else:
            print('--Brak wpisów jeszcze--')

    def zapis_dane_pracownicy(self):
        data_miesiac = str(dodatki.data_miesiac_dzis())
        teraz = datetime.today()
        self.sprawdz_wpisy()

        select_data_eksport = "SELECT * FROM eksport_danych ed WHERE ed.miesiac = '{0}' and ed.dzial = 'mag'".format(
            data_miesiac)
        connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
        result_eksport = db.read_query(connection, select_data_eksport)

        lista_place = []

        if result_eksport:
            QMessageBox.critical(self, 'Error', 'Zestawienie do eksportu dla pracowników magazynu jest już dodane.!')
        else:
            connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)

            for dane_place in self.lista_pracownik_wydania:
                nr_akt = dane_place[0]  # nr akt
                kod = dane_place[1]  # kod
                imie_i_nazwisko = dane_place[2]  # Imie i nazwisko
                kwota = dane_place[8]  # kwota
                opis = 'wydania'
                dzial = 'mag'

                if kwota > 0:
                    lista_place.append([nr_akt, kod, imie_i_nazwisko, kwota, opis, dzial, data_miesiac, teraz])

            for dane_place in self.lista_pracownik_przyjecia:
                nr_akt = dane_place[0]  # nr akt
                kod = dane_place[1]  # kod
                imie_i_nazwisko = dane_place[2]  # Imie i nazwisko
                kwota = dane_place[8]  # kwota
                opis = 'przyjecia'
                dzial = 'mag'

                if kwota > 0:
                    lista_place.append([nr_akt, kod, imie_i_nazwisko, kwota, opis, dzial, data_miesiac, teraz])

            for dane_place in self.lista_pracownik_transport_bs:
                nr_akt = dane_place[0]  # nr akt
                if nr_akt > 5999:
                    kod = 0
                else:
                    kod = dane_place[1]  # kod
                imie_i_nazwisko = dane_place[2]  # Imie i nazwisko
                kwota = dane_place[9]  # kwota
                opis = 'transport_bs'
                dzial = 'mag'

                if kwota > 0:
                    lista_place.append([nr_akt, kod, imie_i_nazwisko, kwota, opis, dzial, data_miesiac, teraz])

            for dane_place in self.lista_pracownik_transport_cz:
                nr_akt = dane_place[0]  # nr akt
                kod = dane_place[1]  # kod
                imie_i_nazwisko = dane_place[2]  # Imie i nazwisko
                kwota = dane_place[10]  # kwota
                opis = 'transport_cz'
                dzial = 'mag'

                if kwota > 0:
                    lista_place.append([nr_akt, kod, imie_i_nazwisko, kwota, opis, dzial, data_miesiac, teraz])

            for dane_place in self.lista_pracownik_wysylka:
                nr_akt = dane_place[0]  # nr akt
                kod = dane_place[1]  # kod
                imie_i_nazwisko = dane_place[2]  # Imie i nazwisko
                kwota = dane_place[8]  # kwota
                opis = 'wysylka'
                dzial = 'mag'

                if kwota > 0:
                    lista_place.append([nr_akt, kod, imie_i_nazwisko, kwota, opis, dzial, data_miesiac, teraz])

            for test in lista_place:
                print(test[0],test[1],test[2],test[3],test[4],test[5],test[6],test[7])
                insert_data = "INSERT INTO eksport_danych VALUES (NULL,'%s','%s','%s','%s','%s','%s','%s','%s');" % (
                test[0], test[1], test[2], test[3], test[4], test[5], test[6], test[7])
                db.execute_query(connection, insert_data)

            connection.close()