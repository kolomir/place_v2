from PyQt5.QtWidgets import QWidget, QMessageBox, QFileDialog, QTableWidgetItem,QHeaderView
import configparser
import openpyxl
#import sys
import os
from datetime import date, datetime

from _wyliczeniaForm_mag_ui import Ui_Form
import db, dodatki


class MainWindow_wyliczeniaForm_mag(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.ui.btn_przelicz.clicked.connect(self.przeliczenie)

    def przeliczenie(self):
        self.licz_nieobecnosci()
        self.miesiac_info_nieobecnosci()
        self.licz_przyjecia()
        self.licz_transport_cz()
        self.licz_wysylka()
        self.licz_transport_bs()
        self.licz_wydania()

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

# = WYDANIA ==============================================================================================================================================================

    def licz_wydania(self):
        miesiac = dodatki.data_miesiac_dzis()
        select_data_direct = '''
                                    select 
                                        ROUND(COALESCE(SUM(case 
                                                                when (select ki.czas from korekta_indirect ki where ki.miesiac = '{0}' and ki.nr_akt = d.Nr_akt) is null then d.Direct_work
                                                                else d.Direct_work + (select ki.czas from korekta_indirect ki where ki.miesiac = '{0}' and ki.nr_akt = d.Nr_akt)
                                                            end), 0), 2) AS 'Direct_work'
                                        ,ROUND(COALESCE(SUM(case 
                                                                when (select ki.czas from korekta_indirect ki where ki.miesiac = '{0}' and ki.nr_akt = d.Nr_akt) is null then d.Indirect_work
                                                                else d.Indirect_work - (select ki.czas from korekta_indirect ki where ki.miesiac = '{0}' and ki.nr_akt = d.Nr_akt)
                                                            end), 0), 2) AS 'Indirect_work'
                                        ,pm.zmiana 
                                    from 
                                        direct d 
                                        left join pracownicy_mag pm on pm.nr_akt = d.Nr_akt 
                                    where 
                                        d.miesiac = '{0}'
                                        and d.dzial = '101'
                                    group by 
                                        pm.zmiana
                                '''.format(miesiac)
        connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
        results_direct = db.read_query(connection, select_data_direct)
        connection.close()

        select_data_wydajnosc = '''
                                            select 
                                                ROUND(COALESCE(SUM(lz.reported), 0), 2) AS 'reported'
                                                ,ROUND(COALESCE(SUM(lz.planned), 0), 2) AS 'planned'
                                                ,ROUND((SUM(lz.planned) / SUM(lz.reported) * 100), 2) AS 'wydajnosci'
                                                ,lz.zmiana_lit 
                                            from 
                                                logowanie_zlecen lz 
                                            where 
                                                lz.miesiac = '{0}'
                                                and lz.grupa = '101'
                                            group by
                                                lz.zmiana_lit 
                                        '''.format(miesiac)
        connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
        results_wydajnosc = db.read_query(connection, select_data_wydajnosc)
        connection.close()

        ile_zmian = len(results_direct)
        print('ile_zmian:',ile_zmian)

        lista = []
        if ile_zmian == 1:
            for row in results_direct:
                reported = planned = wydaj = produkt = 0.0
                if row[2] == 'A':
                    zmiana = row[2]
                    dir = round(row[0], 2)
                    indir = round(row[1], 2)
                    direct = round((row[0]/(row[0]+row[1]))*100, 2)
                    indirect = round((row[1]/(row[0]+row[1]))*100, 2)
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
                    direct = round((row[0]/(row[0]+row[1]))*100, 2)
                    indirect = round((row[1]/(row[0]+row[1]))*100, 2)
                    for row2 in results_wydajnosc:
                        if row2[3] == 'A':
                            reported = round(row2[0], 2)
                            planned = round(row2[1], 2)
                            wydajnosci = round(row2[2], 2)
                        if row2[3] == 'C':
                            reported = round(reported + (row2[0]/2), 2)
                            planned = round(planned + (row2[1]/2), 2)
                            wydajnosci = round(wydajnosci + (row2[2]/2), 2)
                        if row2[3] == 'inna':
                            reported = round(reported + (row2[0]/2), 2)
                            planned = round(planned + (row2[1]/2), 2)
                            wydajnosci = round(wydajnosci + (row2[2]/2), 2)
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
                            reported = reported + round((row2[0]/2), 2)
                            planned = planned + round((row2[1]/2), 2)
                        if row2[3] == 'inna':
                            reported = reported + round((row2[0]/2), 2)
                            planned = planned + round((row2[1]/2), 2)

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
                    direct = round((row[0]/(row[0]+row[1]))*100, 2)
                    indirect = round((row[1]/(row[0]+row[1]))*100, 2)
                    for row2 in results_wydajnosc:
                        if row2[3] == 'A':
                            reported = round(row2[0], 2)
                            planned = round(row2[1], 2)
                            wydajnosci = round(row2[2], 2)
                        if row2[3] == 'inna':
                            reported = round(reported + (row2[0]/3), 2)
                            planned = round(planned + (row2[1]/3), 2)
                            wydajnosci = round(wydajnosci + (row2[2]/3), 2)
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
                            reported = round(reported + (row2[0]/3), 2)
                            planned = round(planned + (row2[1]/3), 2)

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
                            reported = round(reported + (row2[0]/3), 2)
                            planned = round(planned + (row2[1]/3), 2)

                    wydaj = round((planned / reported) * 100, 2)
                    produkt = round(direct * (planned / reported), 2)

                lista.append([zmiana, dir, indir, direct, indirect, reported, planned, wydaj, produkt])

        prog100 = self.ui.lab_pracujacychNieobecnosci.text()
        prog75 = self.ui.lab_pracujacych075Nieobecnosci.text()
        prog50 = self.ui.lab_pracujacych050Nieobecnosci.text()

        select_data_pracownik = '''
                                        select 
                                            pm.nr_akt 
                                            ,p.Kod 
                                            ,CONCAT(pm.nazwisko,' ',pm.imie) as 'Nazwisko i imie' 
                                            ,case 
                                                when np.nr_akt > 6000 then np.razem 
                                                else case 
                                                        when (np.krew + np.rodz + np.rehab + np.nn + np.usp) = 0 then np.krew + np.rodz + np.rehab + np.nn + np.usp + np.inne_nieobecn + np.urlop_wychow + np.opieka_zus + np.urlop_macierz + np.zwol_lek + np.urlop_okolicznosc + np.`Urlop_opieka_(art_188kp)` + np.urlop_szkoleniowy + np.urlop_bezplatny + np.urlop_wypocz 
                                                        else np.krew + np.rodz + np.rehab + np.nn + np.usp + np.urlop_wychow + np.opieka_zus + np.urlop_macierz + np.zwol_lek + np.urlop_okolicznosc + np.`Urlop_opieka_(art_188kp)` + np.urlop_szkoleniowy + np.urlop_bezplatny + np.urlop_wypocz
                                                    end 
                                            end as nieobecnosci
                                            ,bm.bledy_zew 
                                            ,bm.bledy_wew 
                                            ,pm.zmiana 
                                        from 
                                            pracownicy_mag pm 
                                                left join pracownicy p on p.Nr_akt = pm.nr_akt and p.miesiac = '{0}'
                                                left join nieobecnosci_prod np on np.nr_akt = pm.Nr_akt and np.miesiac = '{0}'
                                                left join bledy_mag bm on bm.nr_akt = pm.nr_akt and bm.miesiac = '{0}'
                                        where 
                                            pm.id_grupa = 1
                                            and pm.aktywny = 1
                                        '''.format(miesiac)
        connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
        results_pracownik = db.read_query(connection, select_data_pracownik)
        connection.close()

        select_data_bledy = "select * from bledy_mag bm where bm.miesiac = '{0}'".format(miesiac)
        connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
        results_bledy = db.read_query(connection, select_data_bledy)
        connection.close()

        select_iw = ''' 
                select 
                    d.Nr_akt 
                    ,ROUND(case 
                        when (select ki.czas from korekta_indirect ki where ki.miesiac = '{0}' and ki.nr_akt = d.Nr_akt) is null then d.Direct_work
                        else d.Direct_work + (select ki.czas from korekta_indirect ki where ki.miesiac = '{0}' and ki.nr_akt = d.Nr_akt)
                    end, 2) AS 'DW'
                    ,ROUND(case 
                        when (select ki.czas from korekta_indirect ki where ki.miesiac = '{0}' and ki.nr_akt = d.Nr_akt) is null then d.Indirect_work
                        else d.Indirect_work - (select ki.czas from korekta_indirect ki where ki.miesiac = '{0}' and ki.nr_akt = d.Nr_akt)
                    end, 2) as 'IW'
                    ,ROUND(case 
                        when (select ki.czas from korekta_indirect ki where ki.miesiac = '{0}' and ki.nr_akt = d.Nr_akt) is null then d.Indirect_work
                        else d.Indirect_work - (select ki.czas from korekta_indirect ki where ki.miesiac = '{0}' and ki.nr_akt = d.Nr_akt)
                    end / (case 
                        when (select ki.czas from korekta_indirect ki where ki.miesiac = '{0}' and ki.nr_akt = d.Nr_akt) is null then d.Indirect_work
                        else d.Indirect_work - (select ki.czas from korekta_indirect ki where ki.miesiac = '{0}' and ki.nr_akt = d.Nr_akt)
                    end + case 
                        when (select ki.czas from korekta_indirect ki where ki.miesiac = '{0}' and ki.nr_akt = d.Nr_akt) is null then d.Direct_work
                        else d.Direct_work + (select ki.czas from korekta_indirect ki where ki.miesiac = '{0}' and ki.nr_akt = d.Nr_akt)
                    end), 2) as 'IW2'
                from
                    direct d 
                where 
                    d.miesiac = '{0}' and d.dzial = '101'
         '''.format(miesiac)
        connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
        results_iw = db.read_query(connection, select_iw)
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


        lista_pracownik = []

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

            #print(dane[0], dane[1], dane[2], blad_zew, blad_wew, '---', prod_zmian, suma, '---', wsp, wynik_n)
            lista_pracownik.append([dane[0], dane[1], dane[2], blad_zew, blad_wew, prod_zmian, suma, wsp, wynik_n])


        suma_kwot = sum(round(float(wiersz[8]), 2) for wiersz in lista_pracownik)
        self.ui.lab_sumaWydania.setText(str(suma_kwot))
        self.ui.lab_sumaWydania2.setText(str(suma_kwot))

        if not results_direct:
            self.clear_table_wydania()
            self.naglowki_tabeli_wydania()
            self.clear_table_dane_wydania()
            self.naglowki_tabeli_dane_wydania()
        else:
            self.naglowki_tabeli_wydania()
            self.pokaz_dane_wydania(lista)
            self.naglowki_tabeli_dane_wydania()
            self.pokaz_dane_dane_wydania(lista_pracownik)

    def pokaz_dane_wydania(self, rows):
        # Column count
        if int(len(rows[0])) > 0:
            self.ui.tab_wyliczenia_wydania.setColumnCount(int(len(rows[0])))

        # Row count
        self.ui.tab_wyliczenia_wydania.setRowCount(int(len(rows)))

        wiersz = 0
        for wynik in rows:
            self.ui.tab_wyliczenia_wydania.setItem(wiersz, 0, QTableWidgetItem(str(wynik[0])))
            self.ui.tab_wyliczenia_wydania.setItem(wiersz, 1, QTableWidgetItem(str(wynik[1])))
            self.ui.tab_wyliczenia_wydania.setItem(wiersz, 2, QTableWidgetItem(str(wynik[2])))
            self.ui.tab_wyliczenia_wydania.setItem(wiersz, 3, QTableWidgetItem(str(wynik[3])))
            self.ui.tab_wyliczenia_wydania.setItem(wiersz, 4, QTableWidgetItem(str(wynik[4])))
            self.ui.tab_wyliczenia_wydania.setItem(wiersz, 5, QTableWidgetItem(str(wynik[5])))
            self.ui.tab_wyliczenia_wydania.setItem(wiersz, 6, QTableWidgetItem(str(wynik[6])))
            self.ui.tab_wyliczenia_wydania.setItem(wiersz, 7, QTableWidgetItem(str(wynik[7])))
            self.ui.tab_wyliczenia_wydania.setItem(wiersz, 8, QTableWidgetItem(str(wynik[8])))
            wiersz += 1

        self.ui.tab_wyliczenia_wydania.horizontalHeader().setStretchLastSection(True)
        self.ui.tab_wyliczenia_wydania.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.ui.tab_wyliczenia_wydania.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.ui.tab_wyliczenia_wydania.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.ui.tab_wyliczenia_wydania.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.ui.tab_wyliczenia_wydania.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)
        self.ui.tab_wyliczenia_wydania.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeToContents)
        self.ui.tab_wyliczenia_wydania.horizontalHeader().setSectionResizeMode(6, QHeaderView.ResizeToContents)
        self.ui.tab_wyliczenia_wydania.horizontalHeader().setSectionResizeMode(7, QHeaderView.ResizeToContents)
        self.ui.tab_wyliczenia_wydania.horizontalHeader().setSectionResizeMode(8, QHeaderView.ResizeToContents)

    def naglowki_tabeli_wydania(self):
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

    def clear_table_wydania(self):
        # Wyczyść zawartość tabeli
        self.ui.tab_wyliczenia_wydania.clearContents()
        self.ui.tab_wyliczenia_wydania.setRowCount(0)

    def pokaz_dane_dane_wydania(self, rows):
        # Column count
        if int(len(rows[0])) > 0:
            self.ui.tab_dane_wydania.setColumnCount(int(len(rows[0])))

        # Row count
        self.ui.tab_dane_wydania.setRowCount(int(len(rows)))

        wiersz = 0
        for wynik in rows:
            self.ui.tab_dane_wydania.setItem(wiersz, 0, QTableWidgetItem(str(wynik[0])))
            self.ui.tab_dane_wydania.setItem(wiersz, 1, QTableWidgetItem(str(wynik[1])))
            self.ui.tab_dane_wydania.setItem(wiersz, 2, QTableWidgetItem(str(wynik[2])))
            self.ui.tab_dane_wydania.setItem(wiersz, 3, QTableWidgetItem(str(wynik[3])))
            self.ui.tab_dane_wydania.setItem(wiersz, 4, QTableWidgetItem(str(wynik[4])))
            self.ui.tab_dane_wydania.setItem(wiersz, 5, QTableWidgetItem(str(wynik[5])))
            self.ui.tab_dane_wydania.setItem(wiersz, 6, QTableWidgetItem(str(wynik[6])))
            self.ui.tab_dane_wydania.setItem(wiersz, 7, QTableWidgetItem(str(wynik[7])))
            self.ui.tab_dane_wydania.setItem(wiersz, 8, QTableWidgetItem(str(wynik[8])))
            wiersz += 1

        self.ui.tab_dane_wydania.horizontalHeader().setStretchLastSection(True)
        self.ui.tab_dane_wydania.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.ui.tab_dane_wydania.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.ui.tab_dane_wydania.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.ui.tab_dane_wydania.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.ui.tab_dane_wydania.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)
        self.ui.tab_dane_wydania.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeToContents)
        self.ui.tab_dane_wydania.horizontalHeader().setSectionResizeMode(6, QHeaderView.ResizeToContents)
        self.ui.tab_dane_wydania.horizontalHeader().setSectionResizeMode(7, QHeaderView.ResizeToContents)
        self.ui.tab_dane_wydania.horizontalHeader().setSectionResizeMode(8, QHeaderView.ResizeToContents)

    def naglowki_tabeli_dane_wydania(self):
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

    def clear_table_dane_wydania(self):
        # Wyczyść zawartość tabeli
        self.ui.tab_dane_wydania.clearContents()
        self.ui.tab_dane_wydania.setRowCount(0)


# = PRZYJĘCIA ============================================================================================================================================================

    def licz_przyjecia(self):
        miesiac = dodatki.data_miesiac_dzis()
        select_data = '''
                            select 
                                pm.nr_akt 
                                ,CONCAT(pm.nazwisko,' ',pm.imie) as 'Nazwisko i imie' 
                                ,gm.nazwa 
                                ,case 
                                    when np.nr_akt is null then 0
                                    else case 
                                            when (np.krew + np.rodz + np.rehab + np.nn + np.usp) = 0 then np.krew + np.rodz + np.rehab + np.nn + np.usp + np.inne_nieobecn + np.urlop_wychow + np.opieka_zus + np.urlop_macierz + np.zwol_lek + np.urlop_okolicznosc + np.`Urlop_opieka_(art_188kp)` + np.urlop_szkoleniowy + np.urlop_bezplatny + np.urlop_wypocz 
                                            else np.krew + np.rodz + np.rehab + np.nn + np.usp + np.urlop_wychow + np.opieka_zus + np.urlop_macierz + np.zwol_lek + np.urlop_okolicznosc + np.`Urlop_opieka_(art_188kp)` + np.urlop_szkoleniowy + np.urlop_bezplatny + np.urlop_wypocz
                                        end
                                end as nieobecnosci
                                ,p.Kod 
                            from 
                                pracownicy_mag pm 
                                    left join grupy_mag gm on gm.id = pm.id_grupa 
                                    left join nieobecnosci_prod np on np.nr_akt = pm.Nr_akt 
		                            left join pracownicy p on p.Nr_akt = pm.nr_akt 
                            where 
                            gm.id = 2
                            and pm.aktywny = 1
                            and np.miesiac = '{0}'
                            and p.miesiac = '{0}'
                        '''.format(miesiac)
        connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
        results = db.read_query(connection, select_data)
        connection.close()

        select_kpi = ''' select * from kpi_mag km where km.miesiac = '{0}' '''.format(miesiac)
        connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
        results_kpi = db.read_query(connection, select_kpi)
        connection.close()

        select_bledy = ''' select * from bledy_mag bm where bm.miesiac = '{0}' '''.format(miesiac)
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

        lista_pracownik = []
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
            lista_pracownik.append([dane[0],dane[4],dane[1],dane[2],prem_dp,prem_blad,suma_prem,wsp,wynik_n])

            suma_kwot = sum(round(float(wiersz[8]), 2) for wiersz in lista_pracownik)
            self.ui.lab_sumaPrzyjecia.setText(str(suma_kwot))
            self.ui.lab_sumaPrzyjecia2.setText(str(suma_kwot))

            if not results:
                self.clear_table_przyjecia()
                self.naglowki_tabeli_przyjecia()
            else:
                self.naglowki_tabeli_przyjecia()
                self.pokaz_dane_przyjecia(lista_pracownik)

    def pokaz_dane_przyjecia(self, rows):
        # Column count
        if int(len(rows[0])) > 0:
            self.ui.tab_dane_przyjecia.setColumnCount(int(len(rows[0])))

        # Row count
        self.ui.tab_dane_przyjecia.setRowCount(int(len(rows)))

        wiersz = 0
        for wynik in rows:
            self.ui.tab_dane_przyjecia.setItem(wiersz, 0, QTableWidgetItem(str(wynik[0])))
            self.ui.tab_dane_przyjecia.setItem(wiersz, 1, QTableWidgetItem(str(wynik[1])))
            self.ui.tab_dane_przyjecia.setItem(wiersz, 2, QTableWidgetItem(str(wynik[2])))
            self.ui.tab_dane_przyjecia.setItem(wiersz, 3, QTableWidgetItem(str(wynik[3])))
            self.ui.tab_dane_przyjecia.setItem(wiersz, 4, QTableWidgetItem(str(wynik[4])))
            self.ui.tab_dane_przyjecia.setItem(wiersz, 5, QTableWidgetItem(str(wynik[5])))
            self.ui.tab_dane_przyjecia.setItem(wiersz, 6, QTableWidgetItem(str(wynik[6])))
            self.ui.tab_dane_przyjecia.setItem(wiersz, 7, QTableWidgetItem(str(wynik[7])))
            self.ui.tab_dane_przyjecia.setItem(wiersz, 8, QTableWidgetItem(str(wynik[8])))
            wiersz += 1

        self.ui.tab_dane_przyjecia.horizontalHeader().setStretchLastSection(True)
        self.ui.tab_dane_przyjecia.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.ui.tab_dane_przyjecia.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.ui.tab_dane_przyjecia.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.ui.tab_dane_przyjecia.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.ui.tab_dane_przyjecia.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)
        self.ui.tab_dane_przyjecia.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeToContents)
        self.ui.tab_dane_przyjecia.horizontalHeader().setSectionResizeMode(6, QHeaderView.ResizeToContents)
        self.ui.tab_dane_przyjecia.horizontalHeader().setSectionResizeMode(7, QHeaderView.ResizeToContents)
        self.ui.tab_dane_przyjecia.horizontalHeader().setSectionResizeMode(8, QHeaderView.ResizeToContents)

    def naglowki_tabeli_przyjecia(self):
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

    def clear_table_przyjecia(self):
        # Wyczyść zawartość tabeli
        self.ui.tab_dane_przyjecia.clearContents()
        self.ui.tab_dane_przyjecia.setRowCount(0)


# = TRANSPORT BS =========================================================================================================================================================

    def licz_transport_bs(self):
        miesiac = dodatki.data_miesiac_dzis()
        select_data = '''
                            select 
                                pm.nr_akt 
                                ,CONCAT(pm.nazwisko,' ',pm.imie) as 'Nazwisko i imie' 
                                ,gm.nazwa 
                                ,case 
                                    when np.nr_akt is null then 0
                                    else case 
                                            when (np.krew + np.rodz + np.rehab + np.nn + np.usp) = 0 then np.krew + np.rodz + np.rehab + np.nn + np.usp + np.inne_nieobecn + np.urlop_wychow + np.opieka_zus + np.urlop_macierz + np.zwol_lek + np.urlop_okolicznosc + np.`Urlop_opieka_(art_188kp)` + np.urlop_szkoleniowy + np.urlop_bezplatny + np.urlop_wypocz 
                                            else np.krew + np.rodz + np.rehab + np.nn + np.usp + np.urlop_wychow + np.opieka_zus + np.urlop_macierz + np.zwol_lek + np.urlop_okolicznosc + np.`Urlop_opieka_(art_188kp)` + np.urlop_szkoleniowy + np.urlop_bezplatny + np.urlop_wypocz
                                        end
                                end as nieobecnosci
                                ,p.Kod 
                            from 
                                pracownicy_mag pm 
                                    left join grupy_mag gm on gm.id = pm.id_grupa 
                                    left join nieobecnosci_prod np on np.nr_akt = pm.Nr_akt 
		                            left join pracownicy p on p.Nr_akt = pm.nr_akt and p.miesiac = '{0}'
                            where 
                            gm.id = 3
                            and pm.aktywny = 1
                            and np.miesiac = '{0}'
                        '''.format(miesiac)
        connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
        results = db.read_query(connection, select_data)
        connection.close()

        select_kpi = ''' select * from kpi_mag km where km.miesiac = '{0}' '''.format(miesiac)
        connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
        results_kpi = db.read_query(connection, select_kpi)
        connection.close()

        select_bledy = ''' select * from bledy_mag bm where bm.miesiac = '{0}' '''.format(miesiac)
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

        lista_pracownik = []
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
            lista_pracownik.append([dane[0],dane[4],dane[1],dane[2],prem_dp,prem_blad,prem_zgodnosc,suma_prem,wsp,wynik_n])

            suma_kwot = sum(round(float(wiersz[9]), 2) for wiersz in lista_pracownik)
            self.ui.lab_sumaTransport_BS.setText(str(suma_kwot))
            self.ui.lab_sumaTransport_BS2.setText(str(suma_kwot))

            if not results:
                self.clear_table_transport_bs()
                self.naglowki_tabeli_transport_bs()
            else:
                self.naglowki_tabeli_transport_bs()
                self.pokaz_dane_transport_bs(lista_pracownik)

    def pokaz_dane_transport_bs(self, rows):
        # Column count
        if int(len(rows[0])) > 0:
            self.ui.tab_dane_transport_bs.setColumnCount(int(len(rows[0])))

        # Row count
        self.ui.tab_dane_transport_bs.setRowCount(int(len(rows)))

        wiersz = 0
        for wynik in rows:
            self.ui.tab_dane_transport_bs.setItem(wiersz, 0, QTableWidgetItem(str(wynik[0])))
            self.ui.tab_dane_transport_bs.setItem(wiersz, 1, QTableWidgetItem(str(wynik[1])))
            self.ui.tab_dane_transport_bs.setItem(wiersz, 2, QTableWidgetItem(str(wynik[2])))
            self.ui.tab_dane_transport_bs.setItem(wiersz, 3, QTableWidgetItem(str(wynik[3])))
            self.ui.tab_dane_transport_bs.setItem(wiersz, 4, QTableWidgetItem(str(wynik[4])))
            self.ui.tab_dane_transport_bs.setItem(wiersz, 5, QTableWidgetItem(str(wynik[5])))
            self.ui.tab_dane_transport_bs.setItem(wiersz, 6, QTableWidgetItem(str(wynik[6])))
            self.ui.tab_dane_transport_bs.setItem(wiersz, 7, QTableWidgetItem(str(wynik[7])))
            self.ui.tab_dane_transport_bs.setItem(wiersz, 8, QTableWidgetItem(str(wynik[8])))
            self.ui.tab_dane_transport_bs.setItem(wiersz, 9, QTableWidgetItem(str(wynik[9])))
            wiersz += 1

        self.ui.tab_dane_transport_bs.horizontalHeader().setStretchLastSection(True)
        self.ui.tab_dane_transport_bs.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.ui.tab_dane_transport_bs.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.ui.tab_dane_transport_bs.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.ui.tab_dane_transport_bs.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.ui.tab_dane_transport_bs.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)
        self.ui.tab_dane_transport_bs.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeToContents)
        self.ui.tab_dane_transport_bs.horizontalHeader().setSectionResizeMode(6, QHeaderView.ResizeToContents)
        self.ui.tab_dane_transport_bs.horizontalHeader().setSectionResizeMode(7, QHeaderView.ResizeToContents)
        self.ui.tab_dane_transport_bs.horizontalHeader().setSectionResizeMode(8, QHeaderView.ResizeToContents)
        self.ui.tab_dane_transport_bs.horizontalHeader().setSectionResizeMode(9, QHeaderView.ResizeToContents)

    def naglowki_tabeli_transport_bs(self):
        self.ui.tab_dane_transport_bs.setColumnCount(9)  # Zmień na liczbę kolumn w twojej tabeli
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

    def clear_table_transport_bs(self):
        # Wyczyść zawartość tabeli
        self.ui.tab_dane_transport_bs.clearContents()
        self.ui.tab_dane_transport_bs.setRowCount(0)

# = TRANSPORT CZ =========================================================================================================================================================

    def licz_transport_cz(self):
        miesiac = dodatki.data_miesiac_dzis()
        select_data = '''
                            select 
                                pm.nr_akt 
                                ,CONCAT(pm.nazwisko,' ',pm.imie) as 'Nazwisko i imie' 
                                ,gm.nazwa 
                                ,case 
                                    when np.nr_akt is null then 0
                                    else case 
                                            when (np.krew + np.rodz + np.rehab + np.nn + np.usp) = 0 then np.krew + np.rodz + np.rehab + np.nn + np.usp + np.inne_nieobecn + np.urlop_wychow + np.opieka_zus + np.urlop_macierz + np.zwol_lek + np.urlop_okolicznosc + np.`Urlop_opieka_(art_188kp)` + np.urlop_szkoleniowy + np.urlop_bezplatny + np.urlop_wypocz 
                                            else np.krew + np.rodz + np.rehab + np.nn + np.usp + np.urlop_wychow + np.opieka_zus + np.urlop_macierz + np.zwol_lek + np.urlop_okolicznosc + np.`Urlop_opieka_(art_188kp)` + np.urlop_szkoleniowy + np.urlop_bezplatny + np.urlop_wypocz
                                        end
                                end as nieobecnosci
                                ,p.Kod 
                            from 
                                pracownicy_mag pm 
                                    left join grupy_mag gm on gm.id = pm.id_grupa 
                                    left join nieobecnosci_prod np on np.nr_akt = pm.Nr_akt 
		                            left join pracownicy p on p.Nr_akt = pm.nr_akt 
                            where 
                            gm.id = 4
                            and pm.aktywny = 1
                            and np.miesiac = '{0}'
                            and p.miesiac = '{0}'
                        '''.format(miesiac)
        connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
        results = db.read_query(connection, select_data)
        connection.close()

        select_kpi = ''' select * from kpi_mag km where km.miesiac = '{0}' '''.format(miesiac)
        connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
        results_kpi = db.read_query(connection, select_kpi)
        connection.close()

        select_bledy = ''' select * from bledy_mag bm where bm.miesiac = '{0}' '''.format(miesiac)
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

        lista_pracownik = []
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
            lista_pracownik.append([dane[0],dane[4],dane[1],dane[2],prem_dp,prem_zgodnosc,prem_zapasy,prem_raportowanie,suma_prem,wsp,wynik_n])

            suma_kwot = sum(round(float(wiersz[10]), 2) for wiersz in lista_pracownik)
            self.ui.lab_sumaTransport_Cz.setText(str(suma_kwot))
            self.ui.lab_sumaTransport_Cz2.setText(str(suma_kwot))

            if not results:
                self.clear_table_transport_cz()
                self.naglowki_tabeli_transport_cz()
            else:
                self.naglowki_tabeli_transport_cz()
                self.pokaz_dane_transport_cz(lista_pracownik)

    def pokaz_dane_transport_cz(self, rows):
        # Column count
        if int(len(rows[0])) > 0:
            self.ui.tab_dane_transport_Cz.setColumnCount(int(len(rows[0])))

        # Row count
        self.ui.tab_dane_transport_Cz.setRowCount(int(len(rows)))

        wiersz = 0
        for wynik in rows:
            self.ui.tab_dane_transport_Cz.setItem(wiersz, 0, QTableWidgetItem(str(wynik[0])))
            self.ui.tab_dane_transport_Cz.setItem(wiersz, 1, QTableWidgetItem(str(wynik[1])))
            self.ui.tab_dane_transport_Cz.setItem(wiersz, 2, QTableWidgetItem(str(wynik[2])))
            self.ui.tab_dane_transport_Cz.setItem(wiersz, 3, QTableWidgetItem(str(wynik[3])))
            self.ui.tab_dane_transport_Cz.setItem(wiersz, 4, QTableWidgetItem(str(wynik[4])))
            self.ui.tab_dane_transport_Cz.setItem(wiersz, 5, QTableWidgetItem(str(wynik[5])))
            self.ui.tab_dane_transport_Cz.setItem(wiersz, 6, QTableWidgetItem(str(wynik[6])))
            self.ui.tab_dane_transport_Cz.setItem(wiersz, 7, QTableWidgetItem(str(wynik[7])))
            self.ui.tab_dane_transport_Cz.setItem(wiersz, 8, QTableWidgetItem(str(wynik[8])))
            self.ui.tab_dane_transport_Cz.setItem(wiersz, 9, QTableWidgetItem(str(wynik[9])))
            self.ui.tab_dane_transport_Cz.setItem(wiersz, 10, QTableWidgetItem(str(wynik[10])))
            wiersz += 1

        self.ui.tab_dane_transport_Cz.horizontalHeader().setStretchLastSection(True)
        self.ui.tab_dane_transport_Cz.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.ui.tab_dane_transport_Cz.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.ui.tab_dane_transport_Cz.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.ui.tab_dane_transport_Cz.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.ui.tab_dane_transport_Cz.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)
        self.ui.tab_dane_transport_Cz.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeToContents)
        self.ui.tab_dane_transport_Cz.horizontalHeader().setSectionResizeMode(6, QHeaderView.ResizeToContents)
        self.ui.tab_dane_transport_Cz.horizontalHeader().setSectionResizeMode(7, QHeaderView.ResizeToContents)
        self.ui.tab_dane_transport_Cz.horizontalHeader().setSectionResizeMode(8, QHeaderView.ResizeToContents)
        self.ui.tab_dane_transport_Cz.horizontalHeader().setSectionResizeMode(9, QHeaderView.ResizeToContents)
        self.ui.tab_dane_transport_Cz.horizontalHeader().setSectionResizeMode(10, QHeaderView.ResizeToContents)

    def naglowki_tabeli_transport_cz(self):
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

    def clear_table_transport_cz(self):
        # Wyczyść zawartość tabeli
        self.ui.tab_dane_transport_Cz.clearContents()
        self.ui.tab_dane_transport_Cz.setRowCount(0)

# = WYSYŁKA ==============================================================================================================================================================

    def licz_wysylka(self):
        miesiac = dodatki.data_miesiac_dzis()
        select_data = '''
                            select 
                                pm.nr_akt 
                                ,CONCAT(pm.nazwisko,' ',pm.imie) as 'Nazwisko i imie' 
                                ,gm.nazwa 
                                ,case 
                                    when np.nr_akt is null then 0
                                    else case 
                                            when (np.krew + np.rodz + np.rehab + np.nn + np.usp) = 0 then np.krew + np.rodz + np.rehab + np.nn + np.usp + np.inne_nieobecn + np.urlop_wychow + np.opieka_zus + np.urlop_macierz + np.zwol_lek + np.urlop_okolicznosc + np.`Urlop_opieka_(art_188kp)` + np.urlop_szkoleniowy + np.urlop_bezplatny + np.urlop_wypocz 
                                            else np.krew + np.rodz + np.rehab + np.nn + np.usp + np.urlop_wychow + np.opieka_zus + np.urlop_macierz + np.zwol_lek + np.urlop_okolicznosc + np.`Urlop_opieka_(art_188kp)` + np.urlop_szkoleniowy + np.urlop_bezplatny + np.urlop_wypocz
                                        end
                                end as nieobecnosci
                                ,p.Kod 
                            from 
                                pracownicy_mag pm 
                                    left join grupy_mag gm on gm.id = pm.id_grupa 
                                    left join nieobecnosci_prod np on np.nr_akt = pm.Nr_akt 
		                            left join pracownicy p on p.Nr_akt = pm.nr_akt 
                            where 
                            gm.id = 4
                            and pm.aktywny = 1
                            and np.miesiac = '{0}'
                            and p.miesiac = '{0}'
                        '''.format(miesiac)
        connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
        results = db.read_query(connection, select_data)
        connection.close()

        select_kpi = ''' select * from kpi_mag km where km.miesiac = '{0}' '''.format(miesiac)
        connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
        results_kpi = db.read_query(connection, select_kpi)
        connection.close()

        select_bledy = ''' select * from bledy_mag bm where bm.miesiac = '{0}' '''.format(miesiac)
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

        lista_pracownik = []
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
            lista_pracownik.append([dane[0],dane[4],dane[1],dane[2],prem_delivery,prem_blad,suma_prem,wsp,wynik_n])

            suma_kwot = sum(round(float(wiersz[8]), 2) for wiersz in lista_pracownik)
            self.ui.lab_sumaWysylka.setText(str(suma_kwot))
            self.ui.lab_sumaWysylka2.setText(str(suma_kwot))

            if not results:
                self.clear_table_wysylka()
                self.naglowki_tabeli_wysylka()
            else:
                self.naglowki_tabeli_wysylka()
                self.pokaz_dane_wysylka(lista_pracownik)

    def pokaz_dane_wysylka(self, rows):
        # Column count
        if int(len(rows[0])) > 0:
            self.ui.tab_dane_wysylka.setColumnCount(int(len(rows[0])))

        # Row count
        self.ui.tab_dane_wysylka.setRowCount(int(len(rows)))

        wiersz = 0
        for wynik in rows:
            self.ui.tab_dane_wysylka.setItem(wiersz, 0, QTableWidgetItem(str(wynik[0])))
            self.ui.tab_dane_wysylka.setItem(wiersz, 1, QTableWidgetItem(str(wynik[1])))
            self.ui.tab_dane_wysylka.setItem(wiersz, 2, QTableWidgetItem(str(wynik[2])))
            self.ui.tab_dane_wysylka.setItem(wiersz, 3, QTableWidgetItem(str(wynik[3])))
            self.ui.tab_dane_wysylka.setItem(wiersz, 4, QTableWidgetItem(str(wynik[4])))
            self.ui.tab_dane_wysylka.setItem(wiersz, 5, QTableWidgetItem(str(wynik[5])))
            self.ui.tab_dane_wysylka.setItem(wiersz, 6, QTableWidgetItem(str(wynik[6])))
            self.ui.tab_dane_wysylka.setItem(wiersz, 7, QTableWidgetItem(str(wynik[7])))
            self.ui.tab_dane_wysylka.setItem(wiersz, 8, QTableWidgetItem(str(wynik[8])))
            wiersz += 1

        self.ui.tab_dane_wysylka.horizontalHeader().setStretchLastSection(True)
        self.ui.tab_dane_wysylka.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.ui.tab_dane_wysylka.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.ui.tab_dane_wysylka.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.ui.tab_dane_wysylka.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.ui.tab_dane_wysylka.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)
        self.ui.tab_dane_wysylka.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeToContents)
        self.ui.tab_dane_wysylka.horizontalHeader().setSectionResizeMode(6, QHeaderView.ResizeToContents)
        self.ui.tab_dane_wysylka.horizontalHeader().setSectionResizeMode(7, QHeaderView.ResizeToContents)
        self.ui.tab_dane_wysylka.horizontalHeader().setSectionResizeMode(8, QHeaderView.ResizeToContents)

    def naglowki_tabeli_wysylka(self):
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

    def clear_table_wysylka(self):
        # Wyczyść zawartość tabeli
        self.ui.tab_dane_wysylka.clearContents()
        self.ui.tab_dane_wysylka.setRowCount(0)