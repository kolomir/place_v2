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
        self.licz_wsparcie()


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
                            d.Nr_akt 
                            ,case 
                                when p.Kod is null then 0
                                else p.Kod
                            end as Kod
                            ,d.Nazwisko_i_imie 
                            ,d.dzial 
                            ,d.Direct_ 
                            ,d.Indirect_ 
                            ,ROUND(COALESCE(SUM(lz.reported), 0), 2) AS 'raportowany'
                            ,ROUND(COALESCE(SUM(lz.planned), 0), 2) AS 'planowany'
                            ,ROUND(SUM(lz.planned) / SUM(lz.reported), 2) AS 'wydajnosci'
                            ,ROUND(d.Direct_ * COALESCE(SUM(lz.planned) / NULLIF(SUM(lz.reported), 0), 0), 2) AS 'produktywnosc'
                            ,case
                                when np.nr_akt > 5999 then np.razem 
                                else 
                                    case 
                                        when (np.krew + np.rodz + np.rehab + np.nn + np.usp) = 0 then np.krew + np.rodz + np.rehab + np.nn + np.usp + np.inne_nieobecn + np.urlop_wychow + np.opieka_zus + np.urlop_macierz + np.zwol_lek + np.urlop_okolicznosc + np.`Urlop_opieka_(art_188kp)` + np.urlop_szkoleniowy + np.urlop_bezplatny + np.urlop_wypocz 
                                        else np.krew + np.rodz + np.rehab + np.nn + np.usp + np.urlop_wychow + np.opieka_zus + np.urlop_macierz + np.zwol_lek + np.urlop_okolicznosc + np.`Urlop_opieka_(art_188kp)` + np.urlop_szkoleniowy + np.urlop_bezplatny + np.urlop_wypocz
                                    end
                            end as nieobecnosci
                            ,case 
                                when bp.bledy is null then 0
                                else bp.bledy
                            end as bledow
                        from 
                            direct d
                                join logowanie_zlecen lz on d.Nr_akt = lz.nr_akt 
                                left join nieobecnosci_prod np on np.nr_akt  = d.Nr_akt 
                                left join bledy_prod bp on bp.nr_akt = d.Nr_akt 
		                        left join pracownicy p on p.Nr_akt = d.Nr_akt 
                        where 
                            d.dzial not in ('2030', '1-210', '4001', '4002', '4003', '4004', '4005', '4006', '4007', '4008', '4009', '4010', '401', '2-305')
                            and d.miesiac = '%s'
                            and lz.miesiac = '%s'
	                        and p.miesiac = '%s'
                        group by 
                            d.Nr_akt 
                            ,d.Nazwisko_i_imie 
                            ,d.dzial 
                            ,d.Direct_work 
                            ,d.Direct_ 
                            ,d.Indirect_work
                            ,d.Indirect_ 
                        ''' % (miesiac,miesiac,miesiac)
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
            wynik = 0
            if dane[4] > prog:
                if dane[9] > results_progi[0][6]:
                    wynik = results_progi[0][7]
                elif dane[9] > results_progi[0][4]:
                    wynik = results_progi[0][5]
                elif dane[9] > results_progi[0][2]:
                    wynik = results_progi[0][3]

                wsp = 0
                wynik_n = wynik
                if dane[10] > int(float(prog50)):
                    wsp = 2
                    wynik_n = 0.0
                if dane[10] <= int(float(prog50)) and dane[10] > (int(float(prog100)) - int(float(prog75))):
                    wsp = 1
                    wynik_n = wynik / 2

                wynik_b = wynik_n
                if dane[11] == 1:
                    wynik_b = (wynik_n / 4) * 3
                if dane[11] == 2:
                    wynik_b = wynik_n / 2
                if dane[11] == 3:
                    wynik_b = wynik_n / 4
                if dane[11] > 3:
                    wynik_b = 0.0

            else:
                wynik = wynik_n = wynik_b = 0.00

                wsp = 0
                wynik_n = wynik
                if dane[10] > int(float(prog50)):
                    wsp = 2
                if dane[10] <= int(float(prog50)) and dane[10] > (int(float(prog100)) - int(float(prog75))):
                    wsp = 1


            #print([dane[0], dane[1], dane[2], dane[3], dane[4], dane[5], dane[6], dane[7], dane[8], dane[9], wynik, dane[10], wsp, wynik_n, dane[11], wynik_b])
            lista.append([dane[0], dane[1], dane[2], dane[3], dane[4], dane[5], dane[6], dane[7], dane[8], dane[9], wynik, dane[10], wsp, wynik_n, dane[11], wynik_b])

        suma_kwot = sum(round(float(wiersz[15]), 2) for wiersz in lista)
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

    def naglowki_tabeli_pracownicy(self):
        self.ui.tab_dane_pracownicy.setColumnCount(17)  # Zmień na liczbę kolumn w twojej tabeli
        self.ui.tab_dane_pracownicy.setRowCount(0)  # Ustawienie liczby wierszy na 0
        self.ui.tab_dane_pracownicy.setHorizontalHeaderLabels([
            'Nr akt',
            'Kod',
            'Nazwisko i imię',
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

# = WSPARCIE ========================================================================================================================================================

    def licz_wsparcie(self):
        miesiac = dodatki.data_miesiac_dzis()
        select_data = '''
                        select 
                            l.nazwa 
                            ,( select sum(d.Direct_work) from direct d where d.miesiac = '{0}' and d.dzial = l.nazwa ) as direct
                            ,( select sum(d.Indirect_work) from direct d where d.miesiac = '{0}' and d.dzial = l.nazwa ) as indirect
                            ,ROUND(((( select sum(d.Direct_work) from direct d where d.miesiac = '{0}' and d.dzial = l.nazwa )/(( select sum(d.Direct_work) from direct d where d.miesiac = '{0}' and d.dzial = l.nazwa ) + ( select sum(d.Indirect_work) from direct d where d.miesiac = '{0}' and d.dzial = l.nazwa )))*100),2) as 'Direct %'
                            ,ROUND(((( select sum(d.Indirect_work) from direct d where d.miesiac = '{0}' and d.dzial = l.nazwa )/(( select sum(d.Direct_work) from direct d where d.miesiac = '{0}' and d.dzial = l.nazwa ) + ( select sum(d.Indirect_work) from direct d where d.miesiac = '{0}' and d.dzial = l.nazwa )))*100),2) as 'Indirect %'
                            ,rt.Pl_total_time 
                            ,rt.Rep_total_time 
                            ,ROUND(((rt.Pl_total_time/rt.Rep_total_time)*100),2) as 'Wydajnosc'
                            ,ROUND(((( select sum(d.Direct_work) from direct d where d.miesiac = '{0}' and d.dzial = l.nazwa )/(( select sum(d.Direct_work) from direct d where d.miesiac = '{0}' and d.dzial = l.nazwa ) + ( select sum(d.Indirect_work) from direct d where d.miesiac = '{0}' and d.dzial = l.nazwa )))*((rt.Pl_total_time/rt.Rep_total_time))*100),2) as 'Produktywnosc'
                            ,i.nr_akt
                        from 
                            wsparcie_produkcji wp 
                                left join instruktor i on i.id = wp.id_pracownik 
                                left join linie l on l.id = wp.id_linia 
                                    left join raportowanie_total rt on rt.Work_center = l.nazwa
                        where 
                            wp.aktywny = 1
                            and i.aktywny = 1
                            and l.aktywne  = 1
                            and rt.miesiac = '{0}'
                        '''.format(miesiac)
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
        for dane in results:
            #print([dane[0], dane[1], dane[2], dane[3], dane[4], dane[5], dane[6], dane[7], dane[8]])
            lista.append([dane[0], dane[1], dane[2], dane[3], dane[4], dane[5], dane[6], dane[7], dane[8]])

        lista2 = []
        for dane in results:
            # print([dane[0], dane[1], dane[2], dane[3], dane[4], dane[5], dane[6], dane[7], dane[8]])
            lista2.append([dane[9], dane[1], dane[2], dane[5], dane[6]])

        suma_direct = {}
        suma_indirect = {}
        suma_planowany = {}
        suma_raportowany = {}

        # Iterujemy po liście
        for wiersz in lista2:
            klucz = wiersz[0]  # Wartość z pierwszej kolumny
            wartosc = wiersz[1]  # Wartość z trzeciej kolumny

            if klucz in suma_direct:
                suma_direct[klucz] += wartosc
            else:
                suma_direct[klucz] = wartosc
        for wiersz in lista2:
            klucz = wiersz[0]  # Wartość z pierwszej kolumny
            wartosc = wiersz[2]  # Wartość z trzeciej kolumny

            if klucz in suma_indirect:
                suma_indirect[klucz] += wartosc
            else:
                suma_indirect[klucz] = wartosc
        for wiersz in lista2:
            klucz = wiersz[0]  # Wartość z pierwszej kolumny
            wartosc = wiersz[3]  # Wartość z trzeciej kolumny

            if klucz in suma_planowany:
                suma_planowany[klucz] += wartosc
            else:
                suma_planowany[klucz] = wartosc
        for wiersz in lista2:
            klucz = wiersz[0]  # Wartość z pierwszej kolumny
            wartosc = wiersz[4]  # Wartość z trzeciej kolumny

            if klucz in suma_raportowany:
                suma_raportowany[klucz] += wartosc
            else:
                suma_raportowany[klucz] = wartosc



        select_data_pracownik = '''
                                select 
                                    i.nr_akt 
                                    ,p.Kod 
                                    ,CONCAT(i.nazwisko,' ',i.imie) as 'Nazwisko i imie' 
                                from 
                                    instruktor i 
                                        left join pracownicy p on p.Nr_akt = i.nr_akt 
                                where 
                                    i.id_ranga = 4
                                    and p.miesiac = '{0}'
                                group by 
                                    i.nr_akt 
                                    ,p.Kod 
                                '''.format(miesiac)
        connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
        results_pracownik = db.read_query(connection, select_data_pracownik)
        connection.close()

        lista_pracownik = []
        for dane in results_pracownik:
            direct = round(suma_direct[dane[0]]/(suma_direct[dane[0]]+suma_indirect[dane[0]]),2)
            indirect = round(suma_indirect[dane[0]]/(suma_direct[dane[0]]+suma_indirect[dane[0]]),2)
            wydajnosc = round((suma_planowany[dane[0]]/suma_raportowany[dane[0]])*100,2)
            produktywnosc = round((direct*(suma_planowany[dane[0]]/suma_raportowany[dane[0]]))*100,2)
            print([dane[0], dane[1], dane[2],direct, indirect, wydajnosc, produktywnosc])
            lista_pracownik.append([dane[0], dane[1], dane[2], wydajnosc, produktywnosc])


        #suma_kwot = sum(round(float(wiersz[15]), 2) for wiersz in lista)
        #self.ui.lab_sumaPracownicy.setText(str(suma_kwot))

        if not results:
            self.clear_table_wsparcie()
            self.naglowki_tabeli_wsparcie()
        else:
            self.naglowki_tabeli_wsparcie()
            self.pokaz_dane_wsparcie(lista)

    def pokaz_dane_wsparcie(self, rows):
        # Column count
        if int(len(rows[0])) > 0:
            self.ui.tab_wyliczenia_pomoc.setColumnCount(int(len(rows[0])))

        # Row count
        self.ui.tab_wyliczenia_pomoc.setRowCount(int(len(rows)))

        wiersz = 0
        for wynik in rows:
            self.ui.tab_wyliczenia_pomoc.setItem(wiersz, 0, QTableWidgetItem(str(wynik[0])))
            self.ui.tab_wyliczenia_pomoc.setItem(wiersz, 1, QTableWidgetItem(str(wynik[1])))
            self.ui.tab_wyliczenia_pomoc.setItem(wiersz, 2, QTableWidgetItem(str(wynik[2])))
            self.ui.tab_wyliczenia_pomoc.setItem(wiersz, 3, QTableWidgetItem(str(wynik[3])))
            self.ui.tab_wyliczenia_pomoc.setItem(wiersz, 4, QTableWidgetItem(str(wynik[4])))
            self.ui.tab_wyliczenia_pomoc.setItem(wiersz, 5, QTableWidgetItem(str(wynik[5])))
            self.ui.tab_wyliczenia_pomoc.setItem(wiersz, 6, QTableWidgetItem(str(wynik[6])))
            self.ui.tab_wyliczenia_pomoc.setItem(wiersz, 7, QTableWidgetItem(str(wynik[7])))
            self.ui.tab_wyliczenia_pomoc.setItem(wiersz, 8, QTableWidgetItem(str(wynik[8])))
            wiersz += 1

        self.ui.tab_wyliczenia_pomoc.horizontalHeader().setStretchLastSection(True)
        self.ui.tab_wyliczenia_pomoc.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.ui.tab_wyliczenia_pomoc.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.ui.tab_wyliczenia_pomoc.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.ui.tab_wyliczenia_pomoc.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.ui.tab_wyliczenia_pomoc.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)
        self.ui.tab_wyliczenia_pomoc.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeToContents)
        self.ui.tab_wyliczenia_pomoc.horizontalHeader().setSectionResizeMode(6, QHeaderView.ResizeToContents)
        self.ui.tab_wyliczenia_pomoc.horizontalHeader().setSectionResizeMode(7, QHeaderView.ResizeToContents)
        self.ui.tab_wyliczenia_pomoc.horizontalHeader().setSectionResizeMode(8, QHeaderView.ResizeToContents)

    def naglowki_tabeli_wsparcie(self):
        self.ui.tab_wyliczenia_pomoc.setColumnCount(9)  # Zmień na liczbę kolumn w twojej tabeli
        self.ui.tab_wyliczenia_pomoc.setRowCount(0)  # Ustawienie liczby wierszy na 0
        self.ui.tab_wyliczenia_pomoc.setHorizontalHeaderLabels([
            'Linia',
            'Direct',
            'Indirect',
            'Direct %',
            'Indirect %',
            'Planowany',
            'Raportowany',
            'Wydajność',
            'Produktywność'
        ])

    def clear_table_wsparcie(self):
        # Wyczyść zawartość tabeli
        self.ui.tab_wyliczenia_pomoc.clearContents()
        self.ui.tab_wyliczenia_pomoc.setRowCount(0)

# = LIDERZY =========================================================================================================================================================

# = INSTRUKTOR ======================================================================================================================================================

