from PyQt5.QtWidgets import QWidget, QMessageBox, QFileDialog, QTableWidgetItem,QHeaderView
import configparser
import openpyxl
#import sys
import os
from datetime import date, datetime

from _wyliczeniaForm_ui import Ui_Form
import db, dodatki


class MainWindow_wyliczeniaForm(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.ui.btn_przelicz.clicked.connect(self.przeliczenie)

    def przeliczenie(self):
        self.licz_nieobecnosci()
        self.miesiac_info_nieobecnosci()
        self.licz_pracownicy()


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

#---------------------------------------------------------------
#- belka podsumowująca w zakładce nieobecności -----------------
#- przedstawia progi nieobecności w danym miesiącu -------------
#---------------------------------------------------------------
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
        self.ui.lab_pracujacychNieobecnosci.setText(str(dni_robocze))
        self.ui.lab_pracujacych075Nieobecnosci.setText(str(round(dni_robocze_075,2)))
        self.ui.lab_pracujacych050Nieobecnosci.setText(str(round(dni_robocze_050,2)))

# = NIEOBECNOŚCI =========================================================================================================================================================

    def licz_nieobecnosci(self):
        miesiac = dodatki.data_miesiac_dzis()
        select_data = "SELECT * FROM `nieobecnosci_prod` WHERE miesiac = '%s';" % (miesiac)
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

        if not results:
            self.clear_table_nieobecnosci()
            self.naglowki_tabeli_nieobecnosci()
        else:
            self.naglowki_tabeli_nieobecnosci()
            self.pokaz_dane_nieobecnosci(lista)
        connection.close()

    def pokaz_dane_nieobecnosci(self, rows):
        # Column count
        if int(len(rows[0])) > 0:
            self.ui.tab_dane_nieobecnosci.setColumnCount(int(len(rows[0])))

        # Row count
        self.ui.tab_dane_nieobecnosci.setRowCount(int(len(rows)))

        wiersz = 0
        for wynik in rows:
            self.ui.tab_dane_nieobecnosci.setItem(wiersz, 0, QTableWidgetItem(str(wynik[0])))
            self.ui.tab_dane_nieobecnosci.setItem(wiersz, 1, QTableWidgetItem(str(wynik[1])))
            self.ui.tab_dane_nieobecnosci.setItem(wiersz, 2, QTableWidgetItem(str(wynik[2])))
            self.ui.tab_dane_nieobecnosci.setItem(wiersz, 3, QTableWidgetItem(str(wynik[3])))
            self.ui.tab_dane_nieobecnosci.setItem(wiersz, 4, QTableWidgetItem(str(wynik[4])))
            self.ui.tab_dane_nieobecnosci.setItem(wiersz, 5, QTableWidgetItem(str(wynik[5])))
            wiersz += 1

        self.ui.tab_dane_nieobecnosci.horizontalHeader().setStretchLastSection(True)
        self.ui.tab_dane_nieobecnosci.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.ui.tab_dane_nieobecnosci.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.ui.tab_dane_nieobecnosci.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.ui.tab_dane_nieobecnosci.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.ui.tab_dane_nieobecnosci.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)
        self.ui.tab_dane_nieobecnosci.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeToContents)

    def naglowki_tabeli_nieobecnosci(self):
        self.ui.tab_dane_nieobecnosci.setColumnCount(6)  # Zmień na liczbę kolumn w twojej tabeli
        self.ui.tab_dane_nieobecnosci.setRowCount(0)  # Ustawienie liczby wierszy na 0
        self.ui.tab_dane_nieobecnosci.setHorizontalHeaderLabels([
            'ID',
            'Nazwisko i imię',
            'Nr akt',
            'Stanowisko',
            'Razem',
            'Próg'
        ])

    def clear_table_nieobecnosci(self):
        # Wyczyść zawartość tabeli
        self.ui.tab_dane_nieobecnosci.clearContents()
        self.ui.tab_dane_nieobecnosci.setRowCount(0)

# = PRODUKTYWNOŚĆ =========================================================================================================================================================

    def licz_pracownicy(self):
        miesiac = dodatki.data_miesiac_dzis()
        select_data = '''select 
                            p.Nr_akt 
                            ,p.Kod 
                            ,p.Nazwisko 
                            ,p.Imie
                            ,d.dzial 
                            ,d.Direct_work 
                            ,d.Direct_ 
                            ,d.Indirect_work 
                            ,d.Indirect_
                            ,ROUND(COALESCE(SUM(lz.reported), 0), 2) AS 'raportowany'
                            ,ROUND(COALESCE(SUM(lz.planned), 0), 2) AS 'planowany'
                            ,ROUND(COALESCE(lz.planned / NULLIF(lz.reported, 0), 0), 2) AS 'wydajnosci'
                            ,ROUND(d.Direct_ * COALESCE(lz.planned / NULLIF(lz.reported, 0), 0), 2) AS 'produktywnosc'
                            ,np.urlop_wypocz 
                            ,np.urlop_bezplatny
                            ,np.urlop_szkoleniowy 
                            ,np.`Urlop_opieka_(art_188kp)` 
                            ,np.urlop_okolicznosc 
                            ,np.zwol_lek 
                            ,np.urlop_macierz 
                            ,np.opieka_zus 
                            ,np.urlop_wychow 
                            ,np.inne_nieobecn 
                            ,np.usp 
                            ,np.nn 
                            ,np.rehab 
                            ,np.rodz 
                            ,np.krew 
                            ,np.razem 
                            ,case 
                                when bp.bledy is null then 0
                                else bp.bledy
                            end as bledy2
                        from 
        	                pracownicy p 
        	                    left join direct d on d.Nr_akt = p.Nr_akt 
        		                left join logowanie_zlecen lz on lz.nr_akt = p.Nr_akt 
                                left join nieobecnosci_prod np on np.nr_akt  = p.Nr_akt 
                                left join bledy_prod bp on bp.nr_akt = p.Nr_akt 
        	            where
        	                d.dzial not in ('2030', '1-210', '4001', '4002', '4003', '4004', '4005', '4006', '4007', '4008', '4009', '4010', '401', '2-305')
        	                and p.miesiac = '%s'
        	            group by p.Nr_akt 
                            ,p.Kod 
                            ,p.Nazwisko 
                            ,p.Imie
                            ,d.dzial 
                            ,d.Direct_work 
                            ,d.Direct_ 
                            ,d.Indirect_work 
                            ,d.Indirect_
                        ''' % (miesiac)
        connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
        results = db.read_query(connection, select_data)
        connection.close()

        select_data_progi = "select * from progi_prod pp where pp.id_ranga = 3 and pp.aktywny = 1"
        connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
        results_progi = db.read_query(connection, select_data_progi)
        connection.close()

        prog100 = self.ui.lab_pracujacychNieobecnosci.text()
        prog75 = self.ui.lab_pracujacych075Nieobecnosci.text()
        prog50 = self.ui.lab_pracujacych050Nieobecnosci.text()

        lista = []
        prog = 96.00
        for dane in results:
            if dane[6] > prog:
                if dane[12] > results_progi[0][6]:
                    wynik = results_progi[0][7]
                elif dane[12] > results_progi[0][4]:
                    wynik = results_progi[0][5]
                elif dane[12] > results_progi[0][2]:
                    wynik = results_progi[0][3]

                wsp = 0
                wynik_n = wynik
                suma_warunek = dane[23] + dane[24] + dane[25] + dane[26] + dane[27]
                if suma_warunek == 0:
                    suma = int(float(dane[13])) + int(float(dane[14])) + int(float(dane[15])) + int(
                        float(dane[16])) + int(
                        float(dane[17])) + int(float(dane[18])) + int(float(dane[19])) + int(
                        float(dane[20])) + int(
                        float(dane[21])) + int(float(dane[22])) + int(float(dane[23])) + int(
                        float(dane[24])) + int(
                        float(dane[25])) + int(float(dane[26])) + int(float(dane[27]))
                else:
                    suma = int(float(dane[13])) + int(float(dane[14])) + int(float(dane[15])) + int(
                        float(dane[16])) + int(
                        float(dane[17])) + int(float(dane[18])) + int(float(dane[19])) + int(
                        float(dane[20])) + int(
                        float(dane[21])) + int(float(dane[23])) + int(float(dane[24])) + int(
                        float(dane[25])) + int(
                        float(dane[26])) + int(float(dane[27]))

                if suma > int(float(prog50)):
                    wsp = 2
                    wynik_n = 0.0
                if suma <= int(float(prog50)) and suma > (int(float(prog100)) - int(float(prog75))):
                    wsp = 1
                    wynik_n = wynik / 2

                wynik_b = wynik_n
                if dane[28] == 1:
                    wynik_b = (wynik_n / 4) * 3
                if dane[28] == 2:
                    wynik_b = wynik_n / 2
                if dane[28] == 3:
                    wynik_b = wynik_n / 4
                if dane[28] > 3:
                    wynik_b = 0.0

            else:
                wynik = wynik_n = wynik_b = 0.00

                wsp = 0
                suma_warunek = dane[23] + dane[24] + dane[25] + dane[26] + dane[27]
                if suma_warunek == 0:
                    suma = int(float(dane[13])) + int(float(dane[14])) + int(float(dane[15])) + int(
                        float(dane[16])) + int(
                        float(dane[17])) + int(float(dane[18])) + int(float(dane[19])) + int(
                        float(dane[20])) + int(
                        float(dane[21])) + int(float(dane[22])) + int(float(dane[23])) + int(
                        float(dane[24])) + int(
                        float(dane[25])) + int(float(dane[26])) + int(float(dane[27]))
                else:
                    suma = int(float(dane[13])) + int(float(dane[14])) + int(float(dane[15])) + int(
                        float(dane[16])) + int(
                        float(dane[17])) + int(float(dane[18])) + int(float(dane[19])) + int(
                        float(dane[20])) + int(
                        float(dane[21])) + int(float(dane[23])) + int(float(dane[24])) + int(
                        float(dane[25])) + int(
                        float(dane[26])) + int(float(dane[27]))

                if suma > int(float(prog50)):
                    wsp = 2
                if suma <= int(float(prog50)) and suma > (int(float(prog100)) - int(float(prog75))):
                    wsp = 1
            #print([dane[0], dane[1], dane[2], dane[3], dane[4], dane[6], dane[8], dane[9], dane[10], dane[11], dane[12], wynik, suma, wsp, wynik_n, dane[28], wynik_b])
            lista.append([dane[0], dane[1], dane[2], dane[3], dane[4], dane[6], dane[8], dane[9], dane[10], dane[11], dane[12], wynik, suma, wsp, wynik_n, dane[28], wynik_b])

        suma_kwot = sum(round(float(wiersz[16]), 2) for wiersz in lista)
        self.ui.lab_sumaPracownicy.setText(str(suma_kwot))

        if not results:
            self.clear_table_pracownicy()
            self.naglowki_tabeli_pracownicy()
        else:
            self.naglowki_tabeli_pracownicy()
            self.pokaz_dane_pracownicy(lista)

    def pokaz_dane_pracownicy(self, rows):
        # Column count
        if int(len(rows[0])) > 0:
            self.ui.tab_dane_pracownicy.setColumnCount(int(len(rows[0])))

        # Row count
        self.ui.tab_dane_pracownicy.setRowCount(int(len(rows)))

        wiersz = 0
        for wynik in rows:
            self.ui.tab_dane_pracownicy.setItem(wiersz, 0, QTableWidgetItem(str(wynik[0])))
            self.ui.tab_dane_pracownicy.setItem(wiersz, 1, QTableWidgetItem(str(wynik[1])))
            self.ui.tab_dane_pracownicy.setItem(wiersz, 2, QTableWidgetItem(str(wynik[2])))
            self.ui.tab_dane_pracownicy.setItem(wiersz, 3, QTableWidgetItem(str(wynik[3])))
            self.ui.tab_dane_pracownicy.setItem(wiersz, 4, QTableWidgetItem(str(wynik[4])))
            self.ui.tab_dane_pracownicy.setItem(wiersz, 5, QTableWidgetItem(str(wynik[5])))
            self.ui.tab_dane_pracownicy.setItem(wiersz, 6, QTableWidgetItem(str(wynik[6])))
            self.ui.tab_dane_pracownicy.setItem(wiersz, 7, QTableWidgetItem(str(wynik[7])))
            self.ui.tab_dane_pracownicy.setItem(wiersz, 8, QTableWidgetItem(str(wynik[8])))
            self.ui.tab_dane_pracownicy.setItem(wiersz, 9, QTableWidgetItem(str(wynik[9])))
            self.ui.tab_dane_pracownicy.setItem(wiersz, 10, QTableWidgetItem(str(wynik[10])))
            self.ui.tab_dane_pracownicy.setItem(wiersz, 11, QTableWidgetItem(str(wynik[11])))
            self.ui.tab_dane_pracownicy.setItem(wiersz, 12, QTableWidgetItem(str(wynik[12])))
            self.ui.tab_dane_pracownicy.setItem(wiersz, 13, QTableWidgetItem(str(wynik[13])))
            self.ui.tab_dane_pracownicy.setItem(wiersz, 14, QTableWidgetItem(str(wynik[14])))
            self.ui.tab_dane_pracownicy.setItem(wiersz, 15, QTableWidgetItem(str(wynik[15])))
            self.ui.tab_dane_pracownicy.setItem(wiersz, 16, QTableWidgetItem(str(wynik[16])))
            wiersz += 1

        self.ui.tab_dane_pracownicy.horizontalHeader().setStretchLastSection(True)
        self.ui.tab_dane_pracownicy.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.ui.tab_dane_pracownicy.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.ui.tab_dane_pracownicy.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.ui.tab_dane_pracownicy.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.ui.tab_dane_pracownicy.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)
        self.ui.tab_dane_pracownicy.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeToContents)
        self.ui.tab_dane_pracownicy.horizontalHeader().setSectionResizeMode(6, QHeaderView.ResizeToContents)
        self.ui.tab_dane_pracownicy.horizontalHeader().setSectionResizeMode(7, QHeaderView.ResizeToContents)
        self.ui.tab_dane_pracownicy.horizontalHeader().setSectionResizeMode(8, QHeaderView.ResizeToContents)
        self.ui.tab_dane_pracownicy.horizontalHeader().setSectionResizeMode(9, QHeaderView.ResizeToContents)
        self.ui.tab_dane_pracownicy.horizontalHeader().setSectionResizeMode(10, QHeaderView.ResizeToContents)
        self.ui.tab_dane_pracownicy.horizontalHeader().setSectionResizeMode(11, QHeaderView.ResizeToContents)
        self.ui.tab_dane_pracownicy.horizontalHeader().setSectionResizeMode(12, QHeaderView.ResizeToContents)
        self.ui.tab_dane_pracownicy.horizontalHeader().setSectionResizeMode(13, QHeaderView.ResizeToContents)
        self.ui.tab_dane_pracownicy.horizontalHeader().setSectionResizeMode(14, QHeaderView.ResizeToContents)
        self.ui.tab_dane_pracownicy.horizontalHeader().setSectionResizeMode(15, QHeaderView.ResizeToContents)
        self.ui.tab_dane_pracownicy.horizontalHeader().setSectionResizeMode(16, QHeaderView.ResizeToContents)

    def naglowki_tabeli_pracownicy(self):
        self.ui.tab_dane_pracownicy.setColumnCount(17)  # Zmień na liczbę kolumn w twojej tabeli
        self.ui.tab_dane_pracownicy.setRowCount(0)  # Ustawienie liczby wierszy na 0
        self.ui.tab_dane_pracownicy.setHorizontalHeaderLabels([
            'Nr akt',
            'Kod',
            'Nazwisko',
            'Imię',
            'Dział',
            'Direct %',
            'Indirect %',
            'Raportowany',
            'Planowany',
            'Wydajność',
            'Produktywność',
            'Kwota premia',
            'Suma nieobecności',
            'Współczynnik',
            'Kwota premia',
            'Błędy',
            'Premia łącznie'
        ])

    def clear_table_pracownicy(self):
        # Wyczyść zawartość tabeli
        self.ui.tab_dane_pracownicy.clearContents()
        self.ui.tab_dane_pracownicy.setRowCount(0)

# = LIDERZY =========================================================================================================================================================

