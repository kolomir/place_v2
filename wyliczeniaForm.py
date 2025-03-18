from PyQt5.QtWidgets import QWidget, QMessageBox, QFileDialog, QTableWidgetItem,QHeaderView, QMenu, QCheckBox, QWidgetAction, QScrollArea, QPushButton, QFrame, QVBoxLayout
from PyQt5.QtCore import Qt, QPoint
from PyQt5 import QtGui
import configparser
import openpyxl
#import sys
import os
from datetime import date, datetime

from _wyliczeniaForm_ui import Ui_Form
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

class MainWindow_wyliczeniaForm(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.ui.btn_przelicz.clicked.connect(self.przeliczenie)
        self.ui.btn_zapisz.clicked.connect(self.zapis_dane_pracownicy)

        self.lista = []
        self.lista_pracownik_wsparcia = []
        self.lista_pracownik_lider = []
        self.lista_instruktor_prem = []

        self.miesiac_roboczy = dodatki.data_miesiac_dzis()

        self.sprzwdzenie_raportow()
        self.sprawdzenie_zapisu_prod()
        self.ui.check_blokada.setChecked(False)
        self.ui.btn_zapisz.setEnabled(False)

        self.ui.tab_dane_nieobecnosci.horizontalHeader().setSectionsClickable(True)
        self.ui.tab_dane_nieobecnosci.horizontalHeader().sectionClicked.connect(self.show_filter_menu_nieobecnosci)
        self.active_filters_nieobecnosci = {}  # Przechowywanie aktywnych filtrów dla każdej kolumny

        self.ui.tab_dane_pracownicy.horizontalHeader().setSectionsClickable(True)
        self.ui.tab_dane_pracownicy.horizontalHeader().sectionClicked.connect(self.show_filter_menu_pracownicy)
        self.active_filters_pracownicy = {}  # Przechowywanie aktywnych filtrów dla każdej kolumny



    def przeliczenie(self):
        self.czysc_tabele()
        self.sprawdzenie_zapisu_prod()
        self.miesiac_info_nieobecnosci()
        self.licz_nieobecnosci()
        self.licz_pracownicy()
        self.licz_wsparcie()
        self.licz_liderzy()
        self.licz_instruktorzy()
        self.ui.btn_zapisz.setEnabled(True)

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

    def sprzwdzenie_raportow(self):
        data_miesiac = str(dodatki.data_miesiac_dzis())
        select_data_eksport = "SELECT * FROM eksport_danych ed WHERE ed.miesiac = '{0}'".format(data_miesiac)
        connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
        result_eksport = db.read_query(connection, select_data_eksport)
        connection.close()

        licz_cz = 0
        for dane in result_eksport:
            if dane[6] == 'prod':
                licz_cz += 1

        if licz_cz == 0:
            self.ui.lab_dot_eksport_enova_prod.setPixmap(QtGui.QPixmap(":/icon/img/svg_icons/dot_red.svg"))
        else:
            self.ui.lab_dot_eksport_enova_prod.setPixmap(QtGui.QPixmap(":/icon/img/svg_icons/dot_green.svg"))

    def sprawdzenie_zapisu_prod(self):
        query = "SELECT COUNT(*) > 0 AS status FROM eksport_danych WHERE miesiac = '{0}' and dzial = 'prod'".format(self.miesiac_roboczy)
                #"SELECT * FROM eksport_danych ed WHERE ed.miesiac = '{0}' and ed.dzial = 'prod'".format(data_miesiac)
        connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
        results = db.read_query(connection, query)
        connection.close()
        if results[0][0] == 1:
            print("Zapisane wyliczenia produkcji")
            self.ui.check_blokada.setChecked(True)
        else:
            print("Jeszcze nie zapisane wyliczenia produkcji")
            self.ui.check_blokada.setChecked(False)

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
        self.ui.lab_miesiacNieobecnosci2.setText('%s-%s' % (miesiac_s,rok))
        self.ui.lab_pracujacychNieobecnosci.setText(str(dni_robocze))
        self.ui.lab_pracujacychNieobecnosci2.setText(str(dni_robocze))
        self.ui.lab_pracujacych075Nieobecnosci.setText(str(round(dni_robocze_075,2)))
        self.ui.lab_pracujacych075Nieobecnosci2.setText(str(round(dni_robocze_075,2)))
        self.ui.lab_pracujacych050Nieobecnosci.setText(str(round(dni_robocze_050,2)))
        self.ui.lab_pracujacych050Nieobecnosci2.setText(str(round(dni_robocze_050,2)))

# =========================================================================================================================================================================
# = NIEOBECNOŚCI ==========================================================================================================================================================

    def licz_nieobecnosci(self):
        """Funkcja do załadowania danych z bazy do QTableWidget."""
        try:
            self.ui.tab_dane_nieobecnosci.setSortingEnabled(False)

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

            self.ui.tab_dane_nieobecnosci.setSortingEnabled(True)

            # Przechowywanie id wierszy
            self.row_ids = [row_data[0] for row_data in lista]
            #print(row_data[0] for row_data in results)

        except db.Error as e:
            print(f"Błąd przy pobieraniu danych z bazy danych: {e}")

    def show_filter_menu_nieobecnosci(self, col):
        values = set(
            self.ui.tab_dane_nieobecnosci.item(row, col).text()
            for row in range(self.ui.tab_dane_nieobecnosci.rowCount())
            if self.ui.tab_dane_nieobecnosci.item(row, col)
        )

        menu = QMenu(self)

        # Tworzenie obszaru przewijania
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_content = QFrame()
        layout = QVBoxLayout(scroll_content)

        checkboxes = {}
        max_width = 200  # Minimalna szerokość
        for value in sorted(values):
            checkbox = QCheckBox(value)
            checkbox.setChecked(
                col not in self.active_filters_nieobecnosci or value in self.active_filters_nieobecnosci[col]
            )
            layout.addWidget(checkbox)
            checkboxes[checkbox] = value

            # Dostosowanie szerokości na podstawie tekstu
            width = checkbox.fontMetrics().boundingRect(value).width() + 30
            max_width = min(max(max_width, width), 800)  # Maksymalna szerokość 800

        # Dodanie przycisków "Zaznacz wszystko" i "Wyczyść wszystko"
        button_select_all = QPushButton("Zaznacz wszystko")
        button_clear_all = QPushButton("Wyczyść wszystko")
        layout.addWidget(button_select_all)
        layout.addWidget(button_clear_all)

        button_select_all.clicked.connect(lambda: self.set_all_checkboxes_nieobecnosci(checkboxes, True))
        button_clear_all.clicked.connect(lambda: self.set_all_checkboxes_nieobecnosci(checkboxes, False))

        scroll_area.setWidget(scroll_content)
        scroll_area.setFixedHeight(200)  # Ograniczenie widocznych elementów do około 10 pozycji
        scroll_area.setMinimumWidth(max_width)
        scroll_area.setMaximumWidth(800)

        # Dodanie przewijanego obszaru do menu
        scroll_action = QWidgetAction(self)
        scroll_action.setDefaultWidget(scroll_area)
        menu.addAction(scroll_action)

        apply_action = menu.addAction("Zastosuj filtr")
        menu.addSeparator()
        clear_action = menu.addAction("Wyczyść filtr")

        header_pos = self.ui.tab_dane_nieobecnosci.mapToGlobal(self.ui.tab_dane_nieobecnosci.horizontalHeader().pos())
        section_pos = self.ui.tab_dane_nieobecnosci.horizontalHeader().sectionPosition(col)
        menu_pos = header_pos + QPoint(section_pos, self.ui.tab_dane_nieobecnosci.horizontalHeader().height())
        selected_action = menu.exec(menu_pos)

        if selected_action == apply_action:
            selected_values = [value for checkbox, value in checkboxes.items() if checkbox.isChecked()]
            self.active_filters_nieobecnosci[col] = selected_values
            self.apply_filters_nieobecnosci()
        elif selected_action == clear_action:
            if col in self.active_filters_nieobecnosci:
                del self.active_filters_nieobecnosci[col]
            self.apply_filters_nieobecnosci()

    def set_all_checkboxes_nieobecnosci(self, checkboxes, state):
        for checkbox in checkboxes.keys():
            checkbox.setChecked(state)

    def apply_filters_nieobecnosci(self):
        for row in range(self.ui.tab_dane_nieobecnosci.rowCount()):
            show_row = True
            for col, filter_values in self.active_filters_nieobecnosci.items():
                item = self.ui.tab_dane_nieobecnosci.item(row, col)
                if item and item.text() not in filter_values:
                    show_row = False
                    break
            self.ui.tab_dane_nieobecnosci.setRowHidden(row, not show_row)

# =========================================================================================================================================================================
# = PRACOWNICY PRODUKCJI =========================================================================================================================================================

    def licz_pracownicy(self):
        """Funkcja do załadowania danych z bazy do QTableWidget."""
        try:
            self.ui.tab_dane_pracownicy.setSortingEnabled(False)

            connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
            results = db.wywolaj_procedure_zmienna(connection, 'wyliczenia_prod_pracownicy_produktywnosc', self.miesiac_roboczy)
            connection.close()

            select_data_progi = "select * from progi_prod pp where pp.id_ranga = 3 and pp.aktywny = 1"
            connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
            results_progi = db.read_query(connection, select_data_progi)
            connection.close()

            prog100 = self.ui.lab_pracujacychNieobecnosci.text()
            prog75 = self.ui.lab_pracujacych075Nieobecnosci.text()
            prog50 = self.ui.lab_pracujacych050Nieobecnosci.text()

            prog = 96.00
            print('testy:',str((int(float(prog100)) - int(float(prog75)))))
            for dane in results:
                wynik = 0
                dir_wartosc = indir_wartosc = wyd_wartosc = prod_wartosc = 0.00
                if dane[6] is not None:
                    dir_wartosc = dane[6]
                if dane[7] is not None:
                    indir_wartosc = dane[7]
                if dane[10] is not None:
                    wyd_wartosc = dane[10]
                if dane[11] is not None:
                    prod_wartosc = dane[11]

                if dir_wartosc > prog:
                    if prod_wartosc > results_progi[0][6]:
                        wynik = results_progi[0][7]
                    elif prod_wartosc > results_progi[0][4]:
                        wynik = results_progi[0][5]
                    elif prod_wartosc > results_progi[0][2]:
                        wynik = results_progi[0][3]

                    wsp = 0
                    wynik_n = wynik
                    #if dane[10] > int(float(prog50)):
                    if dane[12] > int(float(prog50)):
                        wsp = 2
                        wynik_n = 0.0
                    #if dane[10] <= int(float(prog50)) and dane[10] > (int(float(prog100)) - int(float(prog75))):
                    if dane[12] <= int(float(prog50)) and dane[12] > (int(float(prog100)) - int(float(prog75))):
                        wsp = 1
                        wynik_n = wynik / 2

                    wynik_b = wynik_n
                    if dane[13] == 2:
                        wynik_b = (wynik_n / 4) * 3
                    if dane[13] == 3:
                        wynik_b = wynik_n / 2
                    if dane[13] == 4:
                        wynik_b = wynik_n / 4
                    if dane[13] > 4:
                        wynik_b = 0.0

                else:
                    wynik = wynik_n = wynik_b = 0.00

                    wsp = 0
                    wynik_n = wynik
                    if int(dane[12]) > int(float(prog50)):
                        wsp = 2
                    if int(dane[12]) <= int(float(prog50)) and dane[12] > (int(float(prog100)) - int(float(prog75))):
                        wsp = 1


                #print([dane[0], dane[1], dane[2], dane[3], dane[4], dane[5], dane[6], dane[7], dane[8], dane[9], wynik, dane[10], wsp, wynik_n, dane[11], wynik_b])
                self.lista.append([dane[0], dane[1], dane[2], dane[3], dane[4], dane[5], dir_wartosc, indir_wartosc, dane[8], dane[9], wyd_wartosc, prod_wartosc, wynik, dane[12], wsp, wynik_n, dane[13], wynik_b])


            suma_kwot = sum(round(float(wiersz[17]), 2) for wiersz in self.lista)
            self.ui.lab_sumaPracownicy.setText(str(suma_kwot))
            self.ui.lab_sumaPracownicy2.setText(str(suma_kwot))

            self.ui.tab_dane_pracownicy.setColumnCount(18)  # Zmień na liczbę kolumn w twojej tabeli
            self.ui.tab_dane_pracownicy.setRowCount(0)  # Ustawienie liczby wierszy na 0
            self.ui.tab_dane_pracownicy.setHorizontalHeaderLabels([
                'Nr akt',
                'Kod',
                'Nazwisko i imię',
                'Dział',
                'Direct [t]',
                'Indirect [t]',
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

            # Ustawianie liczby wierszy na podstawie danych z bazy
            self.ui.tab_dane_pracownicy.setRowCount(len(self.lista))

            # Wypełnianie tabeli danymi
            for row_idx, row_data in enumerate(self.lista):
                # Przechowujemy id każdego wiersza
                for col_idx, value in enumerate(row_data[0:]):  # Pomijamy id
                    item = NumericTableWidgetItem(str(value))              # Użycie klasy soryującej dane numeryczne

                    item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

                    self.ui.tab_dane_pracownicy.setColumnWidth(0, 75)  # Stała szerokość: 150 pikseli
                    self.ui.tab_dane_pracownicy.setColumnWidth(1, 75)  # Stała szerokość: 150 pikseli
                    self.ui.tab_dane_pracownicy.setColumnWidth(2, 200)  # Stała szerokość: 150 pikseli
                    self.ui.tab_dane_pracownicy.setColumnWidth(3, 75)  # Stała szerokość: 150 pikseli
                    self.ui.tab_dane_pracownicy.setColumnWidth(4, 75)  # Stała szerokość: 150 pikseli
                    self.ui.tab_dane_pracownicy.setColumnWidth(5, 75)  # Stała szerokość: 150 pikseli
                    self.ui.tab_dane_pracownicy.setColumnWidth(6, 75)  # Stała szerokość: 150 pikseli
                    self.ui.tab_dane_pracownicy.setColumnWidth(7, 75)  # Stała szerokość: 150 pikseli
                    self.ui.tab_dane_pracownicy.setColumnWidth(8, 75)  # Stała szerokość: 150 pikseli
                    self.ui.tab_dane_pracownicy.setColumnWidth(9, 75)  # Stała szerokość: 150 pikseli
                    self.ui.tab_dane_pracownicy.setColumnWidth(10, 75)  # Stała szerokość: 150 pikseli
                    self.ui.tab_dane_pracownicy.setColumnWidth(11, 75)  # Stała szerokość: 150 pikseli
                    self.ui.tab_dane_pracownicy.setColumnWidth(12, 75)  # Stała szerokość: 150 pikseli
                    self.ui.tab_dane_pracownicy.setColumnWidth(13, 75)  # Stała szerokość: 150 pikseli
                    self.ui.tab_dane_pracownicy.setColumnWidth(14, 75)  # Stała szerokość: 150 pikseli
                    self.ui.tab_dane_pracownicy.setColumnWidth(15, 75)  # Stała szerokość: 150 pikseli
                    self.ui.tab_dane_pracownicy.setColumnWidth(16, 75)  # Stała szerokość: 150 pikseli
                    self.ui.tab_dane_pracownicy.setColumnWidth(17, 75)  # Stała szerokość: 150 pikseli

                    self.ui.tab_dane_pracownicy.setItem(row_idx, col_idx, item)

            self.ui.tab_dane_pracownicy.setSortingEnabled(True)

            # Przechowywanie id wierszy
            self.row_ids = [row_data[0] for row_data in self.lista]
            #print(row_data[0] for row_data in self.lista)

        except db.Error as e:
            print(f"Błąd przy pobieraniu danych z bazy danych: {e}")

    def show_filter_menu_pracownicy(self, col):
        values = set(
            self.ui.tab_dane_pracownicy.item(row, col).text()
            for row in range(self.ui.tab_dane_pracownicy.rowCount())
            if self.ui.tab_dane_pracownicy.item(row, col)
        )

        menu = QMenu(self)

        # Tworzenie obszaru przewijania
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_content = QFrame()
        layout = QVBoxLayout(scroll_content)

        checkboxes = {}
        max_width = 200  # Minimalna szerokość
        for value in sorted(values):
            checkbox = QCheckBox(value)
            checkbox.setChecked(
                col not in self.active_filters_pracownicy or value in self.active_filters_pracownicy[col]
            )
            layout.addWidget(checkbox)
            checkboxes[checkbox] = value

            # Dostosowanie szerokości na podstawie tekstu
            width = checkbox.fontMetrics().boundingRect(value).width() + 30
            max_width = min(max(max_width, width), 800)  # Maksymalna szerokość 800

        # Dodanie przycisków "Zaznacz wszystko" i "Wyczyść wszystko"
        button_select_all = QPushButton("Zaznacz wszystko")
        button_clear_all = QPushButton("Wyczyść wszystko")
        layout.addWidget(button_select_all)
        layout.addWidget(button_clear_all)

        button_select_all.clicked.connect(lambda: self.set_all_checkboxes_pracownicy(checkboxes, True))
        button_clear_all.clicked.connect(lambda: self.set_all_checkboxes_pracownicy(checkboxes, False))

        scroll_area.setWidget(scroll_content)
        scroll_area.setFixedHeight(200)  # Ograniczenie widocznych elementów do około 10 pozycji
        scroll_area.setMinimumWidth(max_width)
        scroll_area.setMaximumWidth(800)

        # Dodanie przewijanego obszaru do menu
        scroll_action = QWidgetAction(self)
        scroll_action.setDefaultWidget(scroll_area)
        menu.addAction(scroll_action)

        apply_action = menu.addAction("Zastosuj filtr")
        menu.addSeparator()
        clear_action = menu.addAction("Wyczyść filtr")

        header_pos = self.ui.tab_dane_pracownicy.mapToGlobal(self.ui.tab_dane_pracownicy.horizontalHeader().pos())
        section_pos = self.ui.tab_dane_pracownicy.horizontalHeader().sectionPosition(col)
        menu_pos = header_pos + QPoint(section_pos, self.ui.tab_dane_pracownicy.horizontalHeader().height())
        selected_action = menu.exec(menu_pos)

        if selected_action == apply_action:
            selected_values = [value for checkbox, value in checkboxes.items() if checkbox.isChecked()]
            self.active_filters_pracownicy[col] = selected_values
            self.apply_filters_pracownicy()
        elif selected_action == clear_action:
            if col in self.active_filters_pracownicy:
                del self.active_filters_pracownicy[col]
            self.apply_filters_pracownicy()

    def set_all_checkboxes_pracownicy(self, checkboxes, state):
        for checkbox in checkboxes.keys():
            checkbox.setChecked(state)

    def apply_filters_pracownicy(self):
        for row in range(self.ui.tab_dane_pracownicy.rowCount()):
            show_row = True
            for col, filter_values in self.active_filters_pracownicy.items():
                item = self.ui.tab_dane_pracownicy.item(row, col)
                if item and item.text() not in filter_values:
                    show_row = False
                    break
            self.ui.tab_dane_pracownicy.setRowHidden(row, not show_row)

# =========================================================================================================================================================================
# = WSPARCIE ==============================================================================================================================================================

    def licz_wsparcie(self):
        """Funkcja do załadowania danych z bazy do QTableWidget."""
        try:
            self.ui.tab_dane_pomoc.setSortingEnabled(False)
            self.ui.tab_wyliczenia_pomoc.setSortingEnabled(False)

            connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
            results = db.wywolaj_procedure_zmienna(connection, 'wyliczenia_prod_wsparcie_produktywnosc', self.miesiac_roboczy)
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
                # print([dane[0], dane[1], dane[2], dane[3], dane[4], dane[5], dane[6], dane[7], dane[8]])
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


            connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
            results_pracownik = db.wywolaj_procedure_zmienna(connection, 'wyliczenia_prod_wsparcie_pracownik', self.miesiac_roboczy)
            connection.close()

            # self.lista_pracownik_wsparcia = []
            for dane in results_pracownik:

                direct = round(suma_direct[dane[0]] / (suma_direct[dane[0]] + suma_indirect[dane[0]]), 2)
                indirect = round(suma_indirect[dane[0]] / (suma_direct[dane[0]] + suma_indirect[dane[0]]), 2)
                wydajnosc = round((suma_planowany[dane[0]] / suma_raportowany[dane[0]]) * 100, 2)
                produktywnosc = round((direct * (suma_planowany[dane[0]] / suma_raportowany[dane[0]])) * 100, 2)

                wynik = 0
                if produktywnosc > results_progi[0][6]:
                    wynik = results_progi[0][7]
                elif produktywnosc > results_progi[0][4]:
                    wynik = results_progi[0][5]
                elif produktywnosc > results_progi[0][2]:
                    wynik = results_progi[0][3]

                wsp = 0
                wynik_n = wynik
                if dane[3] > int(float(prog50)):
                    wsp = 2
                    wynik_n = 0.0
                if dane[3] <= int(float(prog50)) and dane[3] > (int(float(prog100)) - int(float(prog75))):
                    wsp = 1
                    wynik_n = wynik / 2
                # print('dane[3]:', dane[3], 'wsp:', wsp, 'wynik:', wynik, 'wynik_n:', wynik_n)

                # print([dane[0], dane[1], dane[2],direct, indirect, wydajnosc, produktywnosc,wynik, wsp, wynik_n])
                self.lista_pracownik_wsparcia.append([dane[0], dane[1], dane[2], wydajnosc, produktywnosc, wynik, wsp, wynik_n])

            # print(lista_pracownik_wsparcia)
            suma_kwot = sum(round(float(wiersz[7]), 2) for wiersz in self.lista_pracownik_wsparcia)
            self.ui.lab_sumaPomoc.setText(str(suma_kwot))
            self.ui.lab_sumaPomoc2.setText(str(suma_kwot))

            self.ui.tab_dane_pomoc.setColumnCount(8)  # Zmień na liczbę kolumn w twojej tabeli
            self.ui.tab_dane_pomoc.setRowCount(0)  # Ustawienie liczby wierszy na 0
            self.ui.tab_dane_pomoc.setHorizontalHeaderLabels([
                'Nr akt',
                'Kod',
                'Imię i nazwisko',
                'Wydajność',
                'Produktywność',
                'Premia_prod',
                'Chorował',
                'Premia'
            ])

            # Ustawianie liczby wierszy na podstawie danych z bazy
            self.ui.tab_dane_pomoc.setRowCount(len(self.lista_pracownik_wsparcia))

            # Wypełnianie tabeli danymi
            for row_idx, row_data in enumerate(self.lista_pracownik_wsparcia):
                # Przechowujemy id każdego wiersza
                for col_idx, value in enumerate(row_data[0:]):  # Pomijamy id
                    item = NumericTableWidgetItem(str(value))              # Użycie klasy soryującej dane numeryczne

                    item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

                    self.ui.tab_dane_pomoc.setColumnWidth(0, 75)  # Stała szerokość: 150 pikseli
                    self.ui.tab_dane_pomoc.setColumnWidth(1, 75)  # Stała szerokość: 150 pikseli
                    self.ui.tab_dane_pomoc.setColumnWidth(2, 150)  # Stała szerokość: 150 pikseli
                    self.ui.tab_dane_pomoc.setColumnWidth(3, 75)  # Stała szerokość: 150 pikseli
                    self.ui.tab_dane_pomoc.setColumnWidth(4, 75)  # Stała szerokość: 150 pikseli
                    self.ui.tab_dane_pomoc.setColumnWidth(5, 75)  # Stała szerokość: 150 pikseli
                    self.ui.tab_dane_pomoc.setColumnWidth(6, 75)  # Stała szerokość: 150 pikseli
                    self.ui.tab_dane_pomoc.setColumnWidth(7, 75)  # Stała szerokość: 150 pikseli

                    self.ui.tab_dane_pomoc.setItem(row_idx, col_idx, item)

            self.ui.tab_dane_pomoc.setSortingEnabled(True)

            # Przechowywanie id wierszy
            #self.row_ids = [row_data[0] for row_data in self.lista_pracownik_wsparcia]
            #print(row_data[0] for row_data in results)

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

            # Ustawianie liczby wierszy na podstawie danych z bazy
            self.ui.tab_wyliczenia_pomoc.setRowCount(len(lista))

            # Wypełnianie tabeli danymi
            for row_idx, row_data in enumerate(lista):
                # Przechowujemy id każdego wiersza
                for col_idx, value in enumerate(row_data[0:]):  # Pomijamy id
                    item = NumericTableWidgetItem(str(value))              # Użycie klasy soryującej dane numeryczne

                    item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

                    self.ui.tab_wyliczenia_pomoc.setColumnWidth(0, 75)  # Stała szerokość: 150 pikseli
                    self.ui.tab_wyliczenia_pomoc.setColumnWidth(1, 75)  # Stała szerokość: 150 pikseli
                    self.ui.tab_wyliczenia_pomoc.setColumnWidth(2, 75)  # Stała szerokość: 150 pikseli
                    self.ui.tab_wyliczenia_pomoc.setColumnWidth(3, 75)  # Stała szerokość: 150 pikseli
                    self.ui.tab_wyliczenia_pomoc.setColumnWidth(4, 75)  # Stała szerokość: 150 pikseli
                    self.ui.tab_wyliczenia_pomoc.setColumnWidth(5, 75)  # Stała szerokość: 150 pikseli
                    self.ui.tab_wyliczenia_pomoc.setColumnWidth(6, 75)  # Stała szerokość: 150 pikseli
                    self.ui.tab_wyliczenia_pomoc.setColumnWidth(7, 75)  # Stała szerokość: 150 pikseli
                    self.ui.tab_wyliczenia_pomoc.setColumnWidth(8, 75)  # Stała szerokość: 150 pikseli

                    self.ui.tab_wyliczenia_pomoc.setItem(row_idx, col_idx, item)

            self.ui.tab_wyliczenia_pomoc.setSortingEnabled(True)

            # Przechowywanie id wierszy
            #self.row_ids = [row_data[0] for row_data in self.lista_pracownik_wsparcia]
            # print(row_data[0] for row_data in results)

        except db.Error as e:
            print(f"Błąd przy pobieraniu danych z bazy danych: {e}")

# =========================================================================================================================================================================
# = LIDERZY ===============================================================================================================================================================

    def licz_liderzy(self):
        """Funkcja do załadowania danych z bazy do QTableWidget."""
        try:
            self.ui.tab_dane_liderzy.setSortingEnabled(False)
            self.ui.tab_wyliczenia_liderzy.setSortingEnabled(False)

            connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
            results = db.wywolaj_procedure_zmienna(connection, 'wyliczenia_prod_liderzy_produktywnosc', self.miesiac_roboczy)
            connection.close()


            select_data_progi = "select * from progi_prod pp where pp.id_ranga = 2 and pp.aktywny = 1"
            connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
            results_progi = db.read_query(connection, select_data_progi)
            connection.close()

            select_data_q_kwoty = "select kj.kwota from kwoty_jakosc kj where kj.aktywny = 1 and kj.id_ranga = 2"
            connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
            results_q_kwoty = db.read_query(connection, select_data_q_kwoty)
            connection.close()

            kwota_jakosc = results_q_kwoty[0][0]

            prog100 = self.ui.lab_pracujacychNieobecnosci.text()
            prog75 = self.ui.lab_pracujacych075Nieobecnosci.text()
            prog50 = self.ui.lab_pracujacych050Nieobecnosci.text()

            lista = []
            for dane in results:
                #print([dane[0], dane[1], dane[2], dane[3], dane[4], dane[5], dane[6], dane[7], dane[8]])
                lista.append([dane[1], dane[2], dane[3], dane[4], dane[5], dane[6], dane[7], dane[8], dane[9]])

            lista2 = []
            for dane in results:
                # print([dane[0], dane[1], dane[2], dane[3], dane[4], dane[5], dane[6], dane[7], dane[8]])
                lista2.append([dane[0], dane[2], dane[3], dane[6], dane[7]])

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
            #print(suma_indirect)


            connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
            results_pracownik = db.wywolaj_procedure_zmienna(connection, 'wyliczenia_prod_liderzy_pracownik', self.miesiac_roboczy)
            connection.close()


            for dane in results_pracownik:

                direct = round(suma_direct[dane[5]] / (suma_direct[dane[5]] + suma_indirect[dane[5]]), 2)
                indirect = round(suma_indirect[dane[5]] / (suma_direct[dane[5]] + suma_indirect[dane[5]]), 2)
                wydajnosc = round((suma_planowany[dane[5]] / suma_raportowany[dane[5]]) * 100, 2)
                produktywnosc = round((direct * (suma_planowany[dane[5]] / suma_raportowany[dane[5]])) * 100, 2)

                wynik = 0
                if produktywnosc > results_progi[0][6]:
                    wynik = results_progi[0][7]
                elif produktywnosc > results_progi[0][4]:
                    wynik = results_progi[0][5]
                elif produktywnosc > results_progi[0][2]:
                    wynik = results_progi[0][3]

                wsp = 0
                wynik_n = wynik
                if dane[3] > int(float(prog50)):
                    wsp = 2
                    wynik_n = 0.0
                if dane[3] <= int(float(prog50)) and dane[3] > (int(float(prog100)) - int(float(prog75))):
                    wsp = 1
                    wynik_n = wynik / 2

                wynik_j = 0
                kwota_j = 0
                progi_jakosc = self.progi(dane[4])
                if dane[6] == 0:
                    if dane[7] == 0:
                        wynik_j = float(wynik_n) + float(kwota_jakosc)
                        kwota_j = float(kwota_jakosc)
                    elif dane[7] == 1:
                        wynik_j = float(wynik_n) + (float(kwota_jakosc) * 0.75)
                        kwota_j = float(kwota_jakosc) * 0.75
                    elif dane[7] == 2:
                        wynik_j = float(wynik_n) + (float(kwota_jakosc) * 0.5)
                        kwota_j = float(kwota_jakosc) * 0.5
                    else:
                        wynik_j = float(wynik_n)
                else:
                    if dane[7] == 0:
                        if dane[6] > progi_jakosc[2]:
                            wynik_j = float(wynik_n)
                        if dane[6] > progi_jakosc[1] and dane[6] <= progi_jakosc[2]:
                            wynik_j = float(wynik_n) + (float(kwota_jakosc) * 0.5)
                            kwota_j = float(kwota_jakosc) * 0.5
                        if dane[6] > progi_jakosc[0] and dane[6] <= progi_jakosc[1]:
                            wynik_j = float(wynik_n) + (float(kwota_jakosc) * 0.75)
                            kwota_j = float(kwota_jakosc) * 0.75
                        if dane[6] <= progi_jakosc[0]:
                            wynik_j = float(wynik_n) + float(kwota_jakosc)
                            kwota_j = float(kwota_jakosc)
                    else:
                        wynik_j = float(wynik_n)

                print('dane[3]:', dane[3], 'wsp:', wsp, 'wynik:', wynik, 'wynik_n:', wynik_n)

                print([dane[0], dane[1], dane[2], direct, indirect, wydajnosc, produktywnosc, wynik, wsp, wynik_n, kwota_j, wynik_j])
                self.lista_pracownik_lider.append([dane[0], dane[1], dane[2], dane[8], wydajnosc, produktywnosc, wynik, wsp, wynik_n, kwota_j, wynik_j])

            #print(self.lista_pracownik_lider)
            suma_kwot = sum(round(float(wiersz[10]), 2) for wiersz in self.lista_pracownik_lider)
            self.ui.lab_sumaLiderzy.setText(str(suma_kwot))
            self.ui.lab_sumaLiderzy2.setText(str(suma_kwot))

            self.ui.tab_dane_liderzy.setColumnCount(11)  # Zmień na liczbę kolumn w twojej tabeli
            self.ui.tab_dane_liderzy.setRowCount(0)  # Ustawienie liczby wierszy na 0
            self.ui.tab_dane_liderzy.setHorizontalHeaderLabels([
                'Nr akt',
                'Kod',
                'Imię i nazwisko',
                'WC',
                'Wydajność',
                'Produktywność',
                'Premia_prod',
                'Chorował',
                'Premia',
                'Dodatek jakość',
                'Premia Suma'
            ])

            # Ustawianie liczby wierszy na podstawie danych z bazy
            self.ui.tab_dane_liderzy.setRowCount(len(self.lista_pracownik_lider))

            # Wypełnianie tabeli danymi
            for row_idx, row_data in enumerate(self.lista_pracownik_lider):
                # Przechowujemy id każdego wiersza
                for col_idx, value in enumerate(row_data[0:]):  # Pomijamy id
                    item = NumericTableWidgetItem(str(value))              # Użycie klasy soryującej dane numeryczne

                    item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

                    self.ui.tab_dane_liderzy.setColumnWidth(0, 75)  # Stała szerokość: 150 pikseli
                    self.ui.tab_dane_liderzy.setColumnWidth(1, 75)  # Stała szerokość: 150 pikseli
                    self.ui.tab_dane_liderzy.setColumnWidth(2, 150)  # Stała szerokość: 150 pikseli
                    self.ui.tab_dane_liderzy.setColumnWidth(3, 75)  # Stała szerokość: 150 pikseli
                    self.ui.tab_dane_liderzy.setColumnWidth(4, 75)  # Stała szerokość: 150 pikseli
                    self.ui.tab_dane_liderzy.setColumnWidth(5, 75)  # Stała szerokość: 150 pikseli
                    self.ui.tab_dane_liderzy.setColumnWidth(6, 75)  # Stała szerokość: 150 pikseli
                    self.ui.tab_dane_liderzy.setColumnWidth(7, 75)  # Stała szerokość: 150 pikseli
                    self.ui.tab_dane_liderzy.setColumnWidth(8, 75)  # Stała szerokość: 150 pikseli
                    self.ui.tab_dane_liderzy.setColumnWidth(9, 75)  # Stała szerokość: 150 pikseli
                    self.ui.tab_dane_liderzy.setColumnWidth(10, 75)  # Stała szerokość: 150 pikseli

                    self.ui.tab_dane_liderzy.setItem(row_idx, col_idx, item)

            self.ui.tab_dane_liderzy.setSortingEnabled(True)

            # Przechowywanie id wierszy
            #self.row_ids = [row_data[0] for row_data in results]
            #print(row_data[0] for row_data in results)

            self.ui.tab_wyliczenia_liderzy.setColumnCount(9)  # Zmień na liczbę kolumn w twojej tabeli
            self.ui.tab_wyliczenia_liderzy.setRowCount(0)  # Ustawienie liczby wierszy na 0
            self.ui.tab_wyliczenia_liderzy.setHorizontalHeaderLabels([
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

            # Ustawianie liczby wierszy na podstawie danych z bazy
            self.ui.tab_wyliczenia_liderzy.setRowCount(len(lista))

            # Wypełnianie tabeli danymi
            for row_idx, row_data in enumerate(lista):
                # Przechowujemy id każdego wiersza
                for col_idx, value in enumerate(row_data[0:]):  # Pomijamy id
                    item = NumericTableWidgetItem(str(value))              # Użycie klasy soryującej dane numeryczne

                    item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

                    self.ui.tab_wyliczenia_liderzy.setColumnWidth(0, 75)  # Stała szerokość: 150 pikseli
                    self.ui.tab_wyliczenia_liderzy.setColumnWidth(1, 75)  # Stała szerokość: 150 pikseli
                    self.ui.tab_wyliczenia_liderzy.setColumnWidth(2, 75)  # Stała szerokość: 150 pikseli
                    self.ui.tab_wyliczenia_liderzy.setColumnWidth(3, 75)  # Stała szerokość: 150 pikseli
                    self.ui.tab_wyliczenia_liderzy.setColumnWidth(4, 75)  # Stała szerokość: 150 pikseli
                    self.ui.tab_wyliczenia_liderzy.setColumnWidth(5, 75)  # Stała szerokość: 150 pikseli
                    self.ui.tab_wyliczenia_liderzy.setColumnWidth(6, 75)  # Stała szerokość: 150 pikseli
                    self.ui.tab_wyliczenia_liderzy.setColumnWidth(7, 75)  # Stała szerokość: 150 pikseli

                    self.ui.tab_wyliczenia_liderzy.setItem(row_idx, col_idx, item)

            self.ui.tab_wyliczenia_liderzy.setSortingEnabled(True)

        except db.Error as e:
            print(f"Błąd przy pobieraniu danych z bazy danych: {e}")

    def progi(self, wc_id):
        select_data_q_progi = "select * from progi_jakosc pj where pj.aktywny = 1 and id_ranga = 2"
        connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
        results_q_progi = db.read_query(connection, select_data_q_progi)
        connection.close()

        for dane in results_q_progi:
            if dane[2] == wc_id:
                dol = dane[4]
                srodek = dane[5]
                gora = dane[6]
        return dol, srodek, gora

    def progi_inst(self, local):
        select_data_q_progi = '''
                                select 
                                pj.id
                                ,l.lokalizacja 
                                ,pj.id_ranga 
                                ,pj.pulap1 
                                ,pj.pulap2
                                ,pj.pulap3 
                                from 
                                progi_jakosc pj 
                                left join lokalizacja l on l.id = pj.id_lokalizacja 
                                where 
                                l.aktywny = 1 and pj.aktywny = 1 and id_ranga = 1
                                '''
        connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
        results_q_progi = db.read_query(connection, select_data_q_progi)
        connection.close()

        for dane in results_q_progi:
            if dane[1] == local:
                dol = dane[3]
                srodek = dane[4]
                gora = dane[5]
        return dol, srodek, gora

# =========================================================================================================================================================================
# = INSTRUKTOR ============================================================================================================================================================

    def licz_instruktorzy(self):
        """Funkcja do załadowania danych z bazy do QTableWidget."""
        try:
            self.ui.tab_dane_instruktorzy.setSortingEnabled(False)
            self.ui.tab_wyliczenia_zmiany_instruktorzy.setSortingEnabled(False)
            self.ui.tab_wyliczenia_all_instruktorzy.setSortingEnabled(False)

            connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
            results = db.wywolaj_procedure_zmienna(connection, 'wyliczenia_prod_instruktorzy_produktywnosc', self.miesiac_roboczy)
            connection.close()

            select_data_ilosc = '''
                                    select 
                                        l.lokalizacja , count(l.lokalizacja) 
                                    from 
                                        instruktor i 
                                            left join linia_gniazdo lg on lg.id_lider = i.id 
                                                left join lokalizacja l on l.id = lg.id_lokalizacja 
                                    where 
                                        i.aktywny = 1
                                        and i.id_ranga = 1
                                    GROUP by 
                                        l.lokalizacja 
                                    '''
            connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
            results_ilosc = db.read_query(connection, select_data_ilosc)
            connection.close()

            connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
            results_instruktor = db.wywolaj_procedure_zmienna(connection, 'wyliczenia_prod_instruktorzy_pracownik', self.miesiac_roboczy)
            connection.close()

            select_data_progi = "select * from progi_prod pp where pp.id_ranga = 1 and pp.aktywny = 1"
            connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
            results_progi = db.read_query(connection, select_data_progi)
            connection.close()

            select_data_q_kwoty = "select kj.kwota from kwoty_jakosc kj where kj.aktywny = 1 and kj.id_ranga = 1"
            connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
            results_q_kwoty = db.read_query(connection, select_data_q_kwoty)
            connection.close()

            kwota_jakosc = results_q_kwoty[0][0]

            prog100 = self.ui.lab_pracujacychNieobecnosci.text()
            prog75 = self.ui.lab_pracujacych075Nieobecnosci.text()
            prog50 = self.ui.lab_pracujacych050Nieobecnosci.text()

            ile_czaplinek = results_ilosc[1][1]
            ile_borne = results_ilosc[0][1]

            lista_wpisow_notNone = [tuple(0 if x is None else x for x in wiersz) for wiersz in results]

            data_lista = []
            for row in lista_wpisow_notNone:
                data_lista.append({
                    'NrAkt': row[0],
                    'dział': row[1],
                    'Direct': float(row[2]),
                    'Indirect': float(row[3]),
                    'raportowany': float(row[4]),
                    'planowany': float(row[5]),
                    'wydajnosc': float(row[6]),
                    'produktywnosc': float(row[7]),
                    'zmiana': row[8],
                    'zmianaLit': row[9],
                    'lokalizacja': row[10]
                })

            grouped_data = {}

            for row in data_lista:
                key = (row['lokalizacja'], row['zmianaLit'])  # Klucz to kombinacja lokalizacji i zmiany
                if key not in grouped_data:
                    grouped_data[key] = {
                        'Direct': 0,
                        'Indirect': 0,
                        'raportowany': 0,
                        'planowany': 0,
                        'wydajnosc': 0,
                        'produktywnosc': 0
                    }
                    grouped_data[key]['Direct'] += row['Direct']
                    grouped_data[key]['Indirect'] += row['Indirect']
                    grouped_data[key]['raportowany'] += row['raportowany']
                    grouped_data[key]['planowany'] += row['planowany']
                    grouped_data[key]['wydajnosc'] += row['wydajnosc']
                    grouped_data[key]['produktywnosc'] += row['produktywnosc']
            lista = []
            for key, values in grouped_data.items():
                lokalizacja, zmianaLit = key

                #wyd = 0 if values['raportowany'] == 0 else wyd = round((values['planowany']/values['raportowany'])*100,2)
                if values['raportowany'] == 0:
                    wyd = 0.0
                    prod = 0.0
                else:
                    wyd = round((values['planowany']/values['raportowany'])*100,2)
                    prod = round((values['Direct']/(values['Direct']+values['Indirect']))*wyd,2)
                lista.append([lokalizacja,zmianaLit,values['Direct'],values['Indirect'],values['raportowany'],values['planowany'],wyd,prod])
                #lista.append([lokalizacja,zmianaLit,values['Direct'],values['Indirect'],values['raportowany'],values['planowany'],values['wydajnosc'],values['produktywnosc']])

            #print('===========================================')
            #for test in lista:
            #    print(test)
            #print('===========================================')

            # Inicjalizacja sum dla grup
            sum_grupy_czaplinek = {'A': [0] * 6, 'B': [0] * 6, 'C': [0] * 6}
            sum_inna_czaplinek = [0] * 6
            sum_grupy_borne_sulinowo = {'A': [0] * 6, 'B': [0] * 6, 'C': [0] * 6}
            sum_inna_borne_sulinowo = [0] * 6

            lista_zminy = []
            lista_instruktor = []

            # Sumowanie z podziałem na lokalizacje i grupy
            for row in lista:
                if row[0] == 'Czaplinek':
                    if row[1] in sum_grupy_czaplinek:
                        self.dodaj_do_sumy(sum_grupy_czaplinek[row[1]], row)
                    elif row[1] == 'inna':
                        self.dodaj_do_sumy(sum_inna_czaplinek, row)
                elif row[0] == 'Borne Sulinowo':
                    if row[1] in sum_grupy_borne_sulinowo:
                        self.dodaj_do_sumy(sum_grupy_borne_sulinowo[row[1]], row)
                    elif row[1] == 'inna':
                        self.dodaj_do_sumy(sum_inna_borne_sulinowo, row)

            # Przypisywanie wartości z grupy 'inna' do głównych grup w Czaplinku
            if ile_czaplinek == 1:
                # Suma dla wszystkich grup w Czaplinku (A + B + C + inna -> A)
                for i in range(6):
                    sum_grupy_czaplinek['A'][i] += sum_grupy_czaplinek['B'][i] + sum_grupy_czaplinek['C'][i] + sum_inna_czaplinek[i]
                sum_grupy_czaplinek['A'].insert(0,'Czaplinek')
                sum_grupy_czaplinek['A'].insert(1,'A')
                lista_zminy.append(sum_grupy_czaplinek['A'])
                dane_direct = round(sum_grupy_czaplinek['A'][2], 2)
                dane_indirect = round(sum_grupy_czaplinek['A'][3],2)
                dane_raportowany = round(sum_grupy_czaplinek['A'][4],2)
                dane_planowany = round(sum_grupy_czaplinek['A'][5],2)
                for dane_czaplinek in results_instruktor:
                    if dane_czaplinek[2] == 'Czaplinek' and dane_czaplinek[3] == 'A':
                        lokalizacje = dane_czaplinek[2]
                        nrAkt = dane_czaplinek[0]
                        kod = dane_czaplinek[4]
                        instruktor = dane_czaplinek[1]
                        chorowal = dane_czaplinek[5]
                        ppm = dane_czaplinek[6]
                        reklamacje = dane_czaplinek[7]
                        dane_wydajnosc = round((dane_planowany / dane_raportowany) * 100, 2)
                        dane_produktywnosc = round(((dane_direct / (dane_direct + dane_indirect)) * dane_wydajnosc), 2)
                        lista_instruktor.append(
                            [nrAkt, kod, instruktor, dane_wydajnosc, dane_produktywnosc, chorowal, lokalizacje, ppm,
                             reklamacje])
                # Zerujemy inne grupy, bo wszystko zostało przypisane do A
                sum_grupy_czaplinek['B'] = [0] * 6
                sum_grupy_czaplinek['C'] = [0] * 6
            elif ile_czaplinek == 2:
                # Podział sum z grupy 'C' i 'inna' na grupy A i B
                for i in range(len(sum_inna_czaplinek)):
                    suma_dzielona = sum_grupy_czaplinek['C'][i] + sum_inna_czaplinek[i]
                    sum_grupy_czaplinek['A'][i] += suma_dzielona / 2
                    sum_grupy_czaplinek['B'][i] += suma_dzielona / 2
                sum_grupy_czaplinek['A'].insert(0,'Czaplinek')
                sum_grupy_czaplinek['A'].insert(1,'A')
                sum_grupy_czaplinek['B'].insert(0,'Czaplinek')
                sum_grupy_czaplinek['B'].insert(1,'B')
                lista_zminy.append(sum_grupy_czaplinek['A'])
                lista_zminy.append(sum_grupy_czaplinek['B'])
                dane_direct = round(sum_grupy_czaplinek['A'][2], 2)
                dane_indirect = round(sum_grupy_czaplinek['A'][3],2)
                dane_raportowany = round(sum_grupy_czaplinek['A'][4],2)
                dane_planowany = round(sum_grupy_czaplinek['A'][5],2)
                for dane_czaplinek in results_instruktor:
                    if dane_czaplinek[2] == 'Czaplinek' and dane_czaplinek[3] == 'A':
                        lokalizacje = dane_czaplinek[2]
                        nrAkt = dane_czaplinek[0]
                        kod = dane_czaplinek[4]
                        instruktor = dane_czaplinek[1]
                        chorowal = dane_czaplinek[5]
                        ppm = dane_czaplinek[6]
                        reklamacje = dane_czaplinek[7]
                        dane_wydajnosc = round((dane_planowany / dane_raportowany) * 100, 2)
                        dane_produktywnosc = round(((dane_direct / (dane_direct + dane_indirect)) * dane_wydajnosc), 2)
                        lista_instruktor.append(
                            [nrAkt, kod, instruktor, dane_wydajnosc, dane_produktywnosc, chorowal, lokalizacje, ppm,
                             reklamacje])
                dane_direct = round(sum_grupy_czaplinek['B'][2], 2)
                dane_indirect = round(sum_grupy_czaplinek['B'][3],2)
                dane_raportowany = round(sum_grupy_czaplinek['B'][4],2)
                dane_planowany = round(sum_grupy_czaplinek['B'][5],2)
                for dane_czaplinek in results_instruktor:
                    if dane_czaplinek[2] == 'Czaplinek' and dane_czaplinek[3] == 'B':
                        lokalizacje = dane_czaplinek[2]
                        nrAkt = dane_czaplinek[0]
                        kod = dane_czaplinek[4]
                        instruktor = dane_czaplinek[1]
                        chorowal = dane_czaplinek[5]
                        ppm = dane_czaplinek[6]
                        reklamacje = dane_czaplinek[7]
                        dane_wydajnosc = round((dane_planowany / dane_raportowany) * 100, 2)
                        dane_produktywnosc = round(((dane_direct / (dane_direct + dane_indirect)) * dane_wydajnosc), 2)
                        lista_instruktor.append(
                            [nrAkt, kod, instruktor, dane_wydajnosc, dane_produktywnosc, chorowal, lokalizacje, ppm,
                             reklamacje])
            elif ile_czaplinek == 3:
                # Podział grupy 'inna' na grupy A, B i C
                for i in range(len(sum_inna_czaplinek)):
                    sum_grupy_czaplinek['A'][i] += sum_inna_czaplinek[i] / 3
                    sum_grupy_czaplinek['B'][i] += sum_inna_czaplinek[i] / 3
                    sum_grupy_czaplinek['C'][i] += sum_inna_czaplinek[i] / 3
                sum_grupy_czaplinek['A'].insert(0,'Czaplinek')
                sum_grupy_czaplinek['A'].insert(1,'A')
                sum_grupy_czaplinek['B'].insert(0,'Czaplinek')
                sum_grupy_czaplinek['B'].insert(1,'B')
                sum_grupy_czaplinek['C'].insert(0,'Czaplinek')
                sum_grupy_czaplinek['C'].insert(1,'C')
                lista_zminy.append(sum_grupy_czaplinek['A'])
                lista_zminy.append(sum_grupy_czaplinek['B'])
                lista_zminy.append(sum_grupy_czaplinek['C'])
                dane_direct = round(sum_grupy_czaplinek['A'][2], 2)
                dane_indirect = round(sum_grupy_czaplinek['A'][3],2)
                dane_raportowany = round(sum_grupy_czaplinek['A'][4],2)
                dane_planowany = round(sum_grupy_czaplinek['A'][5],2)
                for dane_czaplinek in results_instruktor:
                    if dane_czaplinek[2] == 'Czaplinek' and dane_czaplinek[3] == 'A':
                        lokalizacje = dane_czaplinek[2]
                        nrAkt = dane_czaplinek[0]
                        kod = dane_czaplinek[4]
                        instruktor = dane_czaplinek[1]
                        chorowal = dane_czaplinek[5]
                        ppm = dane_czaplinek[6]
                        reklamacje = dane_czaplinek[7]
                        dane_wydajnosc = round((dane_planowany / dane_raportowany) * 100, 2)
                        dane_produktywnosc = round(((dane_direct / (dane_direct + dane_indirect)) * dane_wydajnosc), 2)
                        lista_instruktor.append(
                            [nrAkt, kod, instruktor, dane_wydajnosc, dane_produktywnosc, chorowal, lokalizacje, ppm,
                             reklamacje])
                dane_direct = round(sum_grupy_czaplinek['B'][2], 2)
                dane_indirect = round(sum_grupy_czaplinek['B'][3],2)
                dane_raportowany = round(sum_grupy_czaplinek['B'][4],2)
                dane_planowany = round(sum_grupy_czaplinek['B'][5],2)
                for dane_czaplinek in results_instruktor:
                    if dane_czaplinek[2] == 'Czaplinek' and dane_czaplinek[3] == 'B':
                        lokalizacje = dane_czaplinek[2]
                        nrAkt = dane_czaplinek[0]
                        kod = dane_czaplinek[4]
                        instruktor = dane_czaplinek[1]
                        chorowal = dane_czaplinek[5]
                        ppm = dane_czaplinek[6]
                        reklamacje = dane_czaplinek[7]
                        dane_wydajnosc = round((dane_planowany / dane_raportowany) * 100, 2)
                        dane_produktywnosc = round(((dane_direct / (dane_direct + dane_indirect)) * dane_wydajnosc), 2)
                        lista_instruktor.append(
                            [nrAkt, kod, instruktor, dane_wydajnosc, dane_produktywnosc, chorowal, lokalizacje, ppm,
                             reklamacje])
                dane_direct = round(sum_grupy_czaplinek['C'][2], 2)
                dane_indirect = round(sum_grupy_czaplinek['C'][3],2)
                dane_raportowany = round(sum_grupy_czaplinek['C'][4],2)
                dane_planowany = round(sum_grupy_czaplinek['C'][5],2)
                for dane_czaplinek in results_instruktor:
                    if dane_czaplinek[2] == 'Czaplinek' and dane_czaplinek[3] == 'C':
                        lokalizacje = dane_czaplinek[2]
                        nrAkt = dane_czaplinek[0]
                        kod = dane_czaplinek[4]
                        instruktor = dane_czaplinek[1]
                        chorowal = dane_czaplinek[5]
                        ppm = dane_czaplinek[6]
                        reklamacje = dane_czaplinek[7]
                        dane_wydajnosc = round((dane_planowany / dane_raportowany) * 100, 2)
                        dane_produktywnosc = round(((dane_direct / (dane_direct + dane_indirect)) * dane_wydajnosc), 2)
                        lista_instruktor.append(
                            [nrAkt, kod, instruktor, dane_wydajnosc, dane_produktywnosc, chorowal, lokalizacje, ppm,
                             reklamacje])

            # Przypisywanie wartości z grupy 'inna' do głównych grup w Borne Sulinowo
            if ile_borne == 1:
                # Suma dla wszystkich grup w Borne Sulinowo (A + B + C + inna -> A)
                for i in range(6):
                    sum_grupy_borne_sulinowo['A'][i] += sum_grupy_borne_sulinowo['B'][i] + sum_grupy_borne_sulinowo['C'][i] + sum_inna_borne_sulinowo[i]
                sum_grupy_borne_sulinowo['A'].insert(0,'Borne Sulinowo')
                sum_grupy_borne_sulinowo['A'].insert(1,'A')
                lista_zminy.append(sum_grupy_borne_sulinowo['A'])
                dane_direct = round(sum_grupy_borne_sulinowo['A'][2], 2)
                dane_indirect = round(sum_grupy_borne_sulinowo['A'][3],2)
                dane_raportowany = round(sum_grupy_borne_sulinowo['A'][4],2)
                dane_planowany = round(sum_grupy_borne_sulinowo['A'][5],2)
                for dane_czaplinek in results_instruktor:
                    if dane_czaplinek[2] == 'Borne Sulinowo' and dane_czaplinek[3] == 'A':
                        lokalizacje = dane_czaplinek[2]
                        nrAkt = dane_czaplinek[0]
                        kod = dane_czaplinek[4]
                        instruktor = dane_czaplinek[1]
                        chorowal = dane_czaplinek[5]
                        ppm = dane_czaplinek[6]
                        reklamacje = dane_czaplinek[7]
                        dane_wydajnosc = round((dane_planowany / dane_raportowany) * 100, 2)
                        dane_produktywnosc = round(((dane_direct / (dane_direct + dane_indirect)) * dane_wydajnosc), 2)
                        lista_instruktor.append(
                            [nrAkt, kod, instruktor, dane_wydajnosc, dane_produktywnosc, chorowal, lokalizacje, ppm,
                             reklamacje])
                # Zerujemy inne grupy, bo wszystko zostało przypisane do A
                sum_grupy_borne_sulinowo['B'] = [0] * 6
                sum_grupy_borne_sulinowo['C'] = [0] * 6
            elif ile_borne == 2:
                # Podział sum z grupy 'C' i 'inna' na grupy A i B
                for i in range(len(sum_inna_borne_sulinowo)):
                    suma_dzielona = sum_grupy_borne_sulinowo['C'][i] + sum_inna_borne_sulinowo[i]
                    sum_grupy_borne_sulinowo['A'][i] += suma_dzielona / 2
                    sum_grupy_borne_sulinowo['B'][i] += suma_dzielona / 2
                sum_grupy_borne_sulinowo['A'].insert(0,'Borne Sulinowo')
                sum_grupy_borne_sulinowo['A'].insert(1,'A')
                sum_grupy_borne_sulinowo['B'].insert(0,'Borne Sulinowo')
                sum_grupy_borne_sulinowo['B'].insert(1,'B')
                lista_zminy.append(sum_grupy_borne_sulinowo['A'])
                lista_zminy.append(sum_grupy_borne_sulinowo['B'])
                dane_direct = round(sum_grupy_borne_sulinowo['A'][2], 2)
                dane_indirect = round(sum_grupy_borne_sulinowo['A'][3],2)
                dane_raportowany = round(sum_grupy_borne_sulinowo['A'][4],2)
                dane_planowany = round(sum_grupy_borne_sulinowo['A'][5],2)
                for dane_czaplinek in results_instruktor:
                    if dane_czaplinek[2] == 'Borne Sulinowo' and dane_czaplinek[3] == 'A':
                        lokalizacje = dane_czaplinek[2]
                        nrAkt = dane_czaplinek[0]
                        kod = dane_czaplinek[4]
                        instruktor = dane_czaplinek[1]
                        chorowal = dane_czaplinek[5]
                        ppm = dane_czaplinek[6]
                        reklamacje = dane_czaplinek[7]
                        dane_wydajnosc = round((dane_planowany / dane_raportowany) * 100, 2)
                        dane_produktywnosc = round(((dane_direct / (dane_direct + dane_indirect)) * dane_wydajnosc), 2)
                        lista_instruktor.append(
                            [nrAkt, kod, instruktor, dane_wydajnosc, dane_produktywnosc, chorowal, lokalizacje, ppm,
                             reklamacje])
                dane_direct = round(sum_grupy_borne_sulinowo['B'][2], 2)
                dane_indirect = round(sum_grupy_borne_sulinowo['B'][3],2)
                dane_raportowany = round(sum_grupy_borne_sulinowo['B'][4],2)
                dane_planowany = round(sum_grupy_borne_sulinowo['B'][5],2)
                for dane_czaplinek in results_instruktor:
                    if dane_czaplinek[2] == 'Borne Sulinowo' and dane_czaplinek[3] == 'B':
                        lokalizacje = dane_czaplinek[2]
                        nrAkt = dane_czaplinek[0]
                        kod = dane_czaplinek[4]
                        instruktor = dane_czaplinek[1]
                        chorowal = dane_czaplinek[5]
                        ppm = dane_czaplinek[6]
                        reklamacje = dane_czaplinek[7]
                        dane_wydajnosc = round((dane_planowany / dane_raportowany) * 100, 2)
                        dane_produktywnosc = round(((dane_direct / (dane_direct + dane_indirect)) * dane_wydajnosc), 2)
                        lista_instruktor.append(
                            [nrAkt, kod, instruktor, dane_wydajnosc, dane_produktywnosc, chorowal, lokalizacje, ppm,
                             reklamacje])
            elif ile_borne == 3:
                # Podział grupy 'inna' na grupy A, B i C
                for i in range(len(sum_inna_borne_sulinowo)):
                    sum_grupy_borne_sulinowo['A'][i] += sum_inna_borne_sulinowo[i] / 3
                    sum_grupy_borne_sulinowo['B'][i] += sum_inna_borne_sulinowo[i] / 3
                    sum_grupy_borne_sulinowo['C'][i] += sum_inna_borne_sulinowo[i] / 3
                sum_grupy_borne_sulinowo['A'].insert(0,'Borne Sulinowo')
                sum_grupy_borne_sulinowo['A'].insert(1,'A')
                sum_grupy_borne_sulinowo['B'].insert(0,'Borne Sulinowo')
                sum_grupy_borne_sulinowo['B'].insert(1,'B')
                sum_grupy_borne_sulinowo['C'].insert(0,'Borne Sulinowo')
                sum_grupy_borne_sulinowo['C'].insert(1,'C')
                lista_zminy.append(sum_grupy_borne_sulinowo['A'])
                lista_zminy.append(sum_grupy_borne_sulinowo['B'])
                lista_zminy.append(sum_grupy_borne_sulinowo['C'])
                dane_direct = round(sum_grupy_borne_sulinowo['A'][2], 2)
                dane_indirect = round(sum_grupy_borne_sulinowo['A'][3],2)
                dane_raportowany = round(sum_grupy_borne_sulinowo['A'][4],2)
                dane_planowany = round(sum_grupy_borne_sulinowo['A'][5],2)
                for dane_czaplinek in results_instruktor:
                    if dane_czaplinek[2] == 'Borne Sulinowo' and dane_czaplinek[3] == 'A':
                        lokalizacje = dane_czaplinek[2]
                        nrAkt = dane_czaplinek[0]
                        kod = dane_czaplinek[4]
                        instruktor = dane_czaplinek[1]
                        chorowal = dane_czaplinek[5]
                        ppm = dane_czaplinek[6]
                        reklamacje = dane_czaplinek[7]
                        dane_wydajnosc = round((dane_planowany / dane_raportowany) * 100, 2)
                        dane_produktywnosc = round(((dane_direct / (dane_direct + dane_indirect)) * dane_wydajnosc), 2)
                        lista_instruktor.append(
                            [nrAkt, kod, instruktor, dane_wydajnosc, dane_produktywnosc, chorowal, lokalizacje, ppm,
                             reklamacje])
                dane_direct = round(sum_grupy_borne_sulinowo['B'][2], 2)
                dane_indirect = round(sum_grupy_borne_sulinowo['B'][3],2)
                dane_raportowany = round(sum_grupy_borne_sulinowo['B'][4],2)
                dane_planowany = round(sum_grupy_borne_sulinowo['B'][5],2)
                for dane_czaplinek in results_instruktor:
                    if dane_czaplinek[2] == 'Borne Sulinowo' and dane_czaplinek[3] == 'B':
                        lokalizacje = dane_czaplinek[2]
                        nrAkt = dane_czaplinek[0]
                        kod = dane_czaplinek[4]
                        instruktor = dane_czaplinek[1]
                        chorowal = dane_czaplinek[5]
                        ppm = dane_czaplinek[6]
                        reklamacje = dane_czaplinek[7]
                        dane_wydajnosc = round((dane_planowany / dane_raportowany) * 100, 2)
                        dane_produktywnosc = round(((dane_direct / (dane_direct + dane_indirect)) * dane_wydajnosc), 2)
                        lista_instruktor.append(
                            [nrAkt, kod, instruktor, dane_wydajnosc, dane_produktywnosc, chorowal, lokalizacje, ppm,
                             reklamacje])
                dane_direct = round(sum_grupy_borne_sulinowo['C'][2], 2)
                dane_indirect = round(sum_grupy_borne_sulinowo['C'][3],2)
                dane_raportowany = round(sum_grupy_borne_sulinowo['C'][4],2)
                dane_planowany = round(sum_grupy_borne_sulinowo['C'][5],2)
                for dane_czaplinek in results_instruktor:
                    if dane_czaplinek[2] == 'Borne Sulinowo' and dane_czaplinek[3] == 'C':
                        lokalizacje = dane_czaplinek[2]
                        nrAkt = dane_czaplinek[0]
                        kod = dane_czaplinek[4]
                        instruktor = dane_czaplinek[1]
                        chorowal = dane_czaplinek[5]
                        ppm = dane_czaplinek[6]
                        reklamacje = dane_czaplinek[7]
                        dane_wydajnosc = round((dane_planowany/dane_raportowany)*100,2)
                        dane_produktywnosc = round(((dane_direct/(dane_direct+dane_indirect))*dane_wydajnosc),2)
                        lista_instruktor.append([nrAkt, kod, instruktor, dane_wydajnosc, dane_produktywnosc, chorowal, lokalizacje, ppm, reklamacje])


            for dane in lista_instruktor:
                wynik = 0
                if dane[4] > results_progi[0][6]:
                    wynik = results_progi[0][7]
                elif dane[4] > results_progi[0][4]:
                    wynik = results_progi[0][5]
                elif dane[4] > results_progi[0][2]:
                    wynik = results_progi[0][3]

                wsp = 0
                wynik_n = wynik
                if dane[5] > int(float(prog50)):
                    wsp = 2
                    wynik_n = 0.0
                if dane[5] <= int(float(prog50)) and dane[5] > (int(float(prog100)) - int(float(prog75))):
                    wsp = 1
                    wynik_n = wynik / 2

                wynik_j = 0
                kwota_j = 0
                progi_jakosc = self.progi_inst(dane[6])
                if dane[8] == 0:
                    if dane[7] > progi_jakosc[2]:
                        wynik_j = float(wynik_n)
                    if dane[7] > progi_jakosc[1] and dane[7] <= progi_jakosc[2]:
                        wynik_j = float(wynik_n) + (float(kwota_jakosc) * 0.5)
                        kwota_j = float(kwota_jakosc) * 0.5
                    if dane[7] > progi_jakosc[0] and dane[7] <= progi_jakosc[1]:
                        wynik_j = float(wynik_n) + (float(kwota_jakosc) * 0.75)
                        kwota_j = float(kwota_jakosc) * 0.75
                    if dane[7] <= progi_jakosc[0]:
                        wynik_j = float(wynik_n) + float(kwota_jakosc)
                        kwota_j = float(kwota_jakosc)
                else:
                    wynik_j = float(wynik_n)

                self.lista_instruktor_prem.append([dane[0],dane[1],dane[2],dane[3],dane[4],wynik,wsp,wynik_n,kwota_j,wynik_j])
            print(self.lista_instruktor_prem)


            print('---------------------------------------')
            print('lista_zmian')
            for test in lista_zminy:
                print(test)
            print('---------------------------------------')

            # Wyświetlanie wyników
            print("Suma dla Czaplinka (A):", sum_grupy_czaplinek['A'])
            print("Suma dla Czaplinka (B):", sum_grupy_czaplinek['B'])
            if ile_czaplinek == 3:
                print("Suma dla Czaplinka (C):", sum_grupy_czaplinek['C'])

            print("Suma dla Borne Sulinowo (A):", sum_grupy_borne_sulinowo['A'])
            print("Suma dla Borne Sulinowo (B):", sum_grupy_borne_sulinowo['B'])
            if ile_borne == 3:
                print("Suma dla Borne Sulinowo (C):", sum_grupy_borne_sulinowo['C'])

            #lista_instruktor = []
            print('=Czaplinek=============================================================')
            dane_direct = round(sum_grupy_czaplinek['A'][2],2)
            dane_indirect = round(sum_grupy_czaplinek['A'][3],2)
            dane_raportowany = round(sum_grupy_czaplinek['A'][4],2)
            dane_planowany = round(sum_grupy_czaplinek['A'][5],2)
            print('dane_direct:',dane_direct)
            print('dane_indirect:',dane_indirect)
            print('dane_raportowany:',dane_raportowany)
            print('dane_planowany:',dane_planowany)
            dane_wydajnosc = round((dane_planowany/dane_raportowany)*100,2)
            print('dane_wydajnosc:',dane_wydajnosc)
            dane_produktywnosc = round(((dane_direct/(dane_direct+dane_indirect))*dane_wydajnosc),2)
            print('dane_produktywnosc:',dane_produktywnosc)

            for dane_czaplinek in results_instruktor:
                if dane_czaplinek[2] == 'Czaplinek' and dane_czaplinek[3] == 'A':
                    nrAkt = dane_czaplinek[0]
                    kod = dane_czaplinek[4]
                    instruktor = dane_czaplinek[1]
                    chorowal = dane_czaplinek[5]
                    #lista_instruktor.append([nrAkt,kod,instruktor,dane_wydajnosc,dane_produktywnosc,0,chorowal,0,0,0])
                    print('JEST w Czaplinek1')
                if dane_czaplinek[2] == 'Czaplinek' and dane_czaplinek[3] == 'B':
                    nrAkt = dane_czaplinek[0]
                    kod = dane_czaplinek[4]
                    instruktor = dane_czaplinek[1]
                    chorowal = dane_czaplinek[5]
                    #lista_instruktor.append([nrAkt,kod,instruktor,dane_wydajnosc,dane_produktywnosc,0,chorowal,0,0,0])
                    print('JEST w Czaplinek2')
                if dane_czaplinek[2] == 'Czaplinek' and dane_czaplinek[3] == 'C':
                    nrAkt = dane_czaplinek[0]
                    kod = dane_czaplinek[4]
                    instruktor = dane_czaplinek[1]
                    chorowal = dane_czaplinek[5]
                    #lista_instruktor.append([nrAkt,kod,instruktor,dane_wydajnosc,dane_produktywnosc,0,chorowal,0,0,0])
                    print('JEST w Czaplinek3')


            print('=======================================================================')
            print('=Borne Sulinowo========================================================')
            dane_direct = round(sum_grupy_borne_sulinowo['A'][2], 2)
            dane_indirect = round(sum_grupy_borne_sulinowo['A'][3], 2)
            dane_raportowany = round(sum_grupy_borne_sulinowo['A'][4], 2)
            dane_planowany = round(sum_grupy_borne_sulinowo['A'][5], 2)
            print('dane_direct:', dane_direct)
            print('dane_indirect:', dane_indirect)
            print('dane_raportowany:', dane_raportowany)
            print('dane_planowany:', dane_planowany)
            dane_wydajnosc = round((dane_planowany / dane_raportowany) * 100, 2)
            print('dane_wydajnosc:', dane_wydajnosc)
            dane_produktywnosc = round(((dane_direct / (dane_direct + dane_indirect)) * dane_wydajnosc), 2)
            print('dane_produktywnosc:', dane_produktywnosc)

            for dane_borne in results_instruktor:
                if dane_borne[2] == 'Borne Sulinowo' and dane_czaplinek[3] == 'A':
                    nrAkt = dane_czaplinek[0]
                    kod = dane_czaplinek[4]
                    instruktor = dane_czaplinek[1]
                    chorowal = dane_czaplinek[5]
                    #lista_instruktor.append([nrAkt,kod,instruktor,dane_wydajnosc,dane_produktywnosc,0,chorowal,0,0,0])
                    print('JEST w Borne Sulinowo1')
                if dane_borne[2] == 'Borne Sulinowo' and dane_czaplinek[3] == 'B':
                    nrAkt = dane_czaplinek[0]
                    kod = dane_czaplinek[4]
                    instruktor = dane_czaplinek[1]
                    chorowal = dane_czaplinek[5]
                    #lista_instruktor.append([nrAkt,kod,instruktor,dane_wydajnosc,dane_produktywnosc,0,chorowal,0,0,0])
                    print('JEST w Borne Sulinowo2')
                if dane_borne[2] == 'Borne Sulinowo' and dane_czaplinek[3] == 'C':
                    nrAkt = dane_czaplinek[0]
                    kod = dane_czaplinek[4]
                    instruktor = dane_czaplinek[1]
                    chorowal = dane_czaplinek[5]
                    #lista_instruktor.append([nrAkt,kod,instruktor,dane_wydajnosc,dane_produktywnosc,0,chorowal,0,0,0])
                    print('JEST w Borne Sulinowo3')
            print('=======================================================================')

            suma_kwot = sum(round(float(wiersz[9]), 2) for wiersz in self.lista_instruktor_prem)
            print('suma_kwot:',suma_kwot)
            self.ui.lab_sumaInstruktorzy.setText(str(suma_kwot))
            self.ui.lab_sumaInstruktorzy2.setText(str(suma_kwot))

            self.ui.tab_dane_instruktorzy.setColumnCount(10)  # Zmień na liczbę kolumn w twojej tabeli
            self.ui.tab_dane_instruktorzy.setRowCount(0)  # Ustawienie liczby wierszy na 0
            self.ui.tab_dane_instruktorzy.setHorizontalHeaderLabels([
                'Nr akt',
                'Kod',
                'Imię i nazwisko',
                'Wydajność',
                'Produktywność',
                'Premia_prod',
                'Chorował',
                'Premia',
                'Dodatek jakość',
                'Premia Suma'
            ])

            # Ustawianie liczby wierszy na podstawie danych z bazy
            self.ui.tab_dane_instruktorzy.setRowCount(len(self.lista_instruktor_prem))

            # Wypełnianie tabeli danymi
            for row_idx, row_data in enumerate(self.lista_instruktor_prem):
                # Przechowujemy id każdego wiersza
                for col_idx, value in enumerate(row_data[0:]):  # Pomijamy id
                    item = NumericTableWidgetItem(str(value))              # Użycie klasy soryującej dane numeryczne

                    item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

                    self.ui.tab_dane_instruktorzy.setColumnWidth(0, 75)  # Stała szerokość: 150 pikseli
                    self.ui.tab_dane_instruktorzy.setColumnWidth(1, 75)  # Stała szerokość: 150 pikseli
                    self.ui.tab_dane_instruktorzy.setColumnWidth(2, 150)  # Stała szerokość: 150 pikseli
                    self.ui.tab_dane_instruktorzy.setColumnWidth(3, 75)  # Stała szerokość: 150 pikseli
                    self.ui.tab_dane_instruktorzy.setColumnWidth(4, 75)  # Stała szerokość: 150 pikseli
                    self.ui.tab_dane_instruktorzy.setColumnWidth(5, 75)  # Stała szerokość: 150 pikseli
                    self.ui.tab_dane_instruktorzy.setColumnWidth(6, 75)  # Stała szerokość: 150 pikseli
                    self.ui.tab_dane_instruktorzy.setColumnWidth(7, 75)  # Stała szerokość: 150 pikseli
                    self.ui.tab_dane_instruktorzy.setColumnWidth(8, 75)  # Stała szerokość: 150 pikseli
                    self.ui.tab_dane_instruktorzy.setColumnWidth(9, 75)  # Stała szerokość: 150 pikseli

                    self.ui.tab_dane_instruktorzy.setItem(row_idx, col_idx, item)

            self.ui.tab_dane_instruktorzy.setSortingEnabled(True)

            # Przechowywanie id wierszy
            #self.row_ids = [row_data[0] for row_data in results]
            #print(row_data[0] for row_data in results)

            self.ui.tab_wyliczenia_zmiany_instruktorzy.setColumnCount(8)  # Zmień na liczbę kolumn w twojej tabeli
            self.ui.tab_wyliczenia_zmiany_instruktorzy.setRowCount(0)  # Ustawienie liczby wierszy na 0
            self.ui.tab_wyliczenia_zmiany_instruktorzy.setHorizontalHeaderLabels([
                'Lokalizacja',
                'Zmiana',
                'Direct',
                'Indirect',
                'raportowany',
                'planowany',
                'wydajnosc',
                'produktywnosc'
            ])

            # Ustawianie liczby wierszy na podstawie danych z bazy
            self.ui.tab_wyliczenia_zmiany_instruktorzy.setRowCount(len(lista_zminy))

            # Wypełnianie tabeli danymi
            for row_idx, row_data in enumerate(lista_zminy):
                # Przechowujemy id każdego wiersza
                for col_idx, value in enumerate(row_data[0:]):  # Pomijamy id
                    item = NumericTableWidgetItem(str(value))              # Użycie klasy soryującej dane numeryczne

                    item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

                    self.ui.tab_wyliczenia_zmiany_instruktorzy.setColumnWidth(0, 150)  # Stała szerokość: 150 pikseli
                    self.ui.tab_wyliczenia_zmiany_instruktorzy.setColumnWidth(1, 75)  # Stała szerokość: 150 pikseli
                    self.ui.tab_wyliczenia_zmiany_instruktorzy.setColumnWidth(2, 75)  # Stała szerokość: 150 pikseli
                    self.ui.tab_wyliczenia_zmiany_instruktorzy.setColumnWidth(3, 75)  # Stała szerokość: 150 pikseli
                    self.ui.tab_wyliczenia_zmiany_instruktorzy.setColumnWidth(4, 75)  # Stała szerokość: 150 pikseli
                    self.ui.tab_wyliczenia_zmiany_instruktorzy.setColumnWidth(5, 75)  # Stała szerokość: 150 pikseli
                    self.ui.tab_wyliczenia_zmiany_instruktorzy.setColumnWidth(6, 75)  # Stała szerokość: 150 pikseli
                    self.ui.tab_wyliczenia_zmiany_instruktorzy.setColumnWidth(7, 75)  # Stała szerokość: 150 pikseli

                    self.ui.tab_wyliczenia_zmiany_instruktorzy.setItem(row_idx, col_idx, item)

            self.ui.tab_wyliczenia_zmiany_instruktorzy.setSortingEnabled(True)

            self.ui.tab_wyliczenia_all_instruktorzy.setColumnCount(8)  # Zmień na liczbę kolumn w twojej tabeli
            self.ui.tab_wyliczenia_all_instruktorzy.setRowCount(0)  # Ustawienie liczby wierszy na 0
            self.ui.tab_wyliczenia_all_instruktorzy.setHorizontalHeaderLabels([
                'Lokalizacja',
                'Zmiana',
                'Direct',
                'Indirect',
                'raportowany',
                'planowany',
                'wydajnosc',
                'produktywnosc'
            ])

            # Ustawianie liczby wierszy na podstawie danych z bazy
            self.ui.tab_wyliczenia_all_instruktorzy.setRowCount(len(lista))

            # Wypełnianie tabeli danymi
            for row_idx, row_data in enumerate(lista):
                # Przechowujemy id każdego wiersza
                for col_idx, value in enumerate(row_data[0:]):  # Pomijamy id
                    item = NumericTableWidgetItem(str(value))              # Użycie klasy soryującej dane numeryczne

                    item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

                    self.ui.tab_wyliczenia_all_instruktorzy.setColumnWidth(0, 150)  # Stała szerokość: 150 pikseli
                    self.ui.tab_wyliczenia_all_instruktorzy.setColumnWidth(1, 75)  # Stała szerokość: 150 pikseli
                    self.ui.tab_wyliczenia_all_instruktorzy.setColumnWidth(2, 75)  # Stała szerokość: 150 pikseli
                    self.ui.tab_wyliczenia_all_instruktorzy.setColumnWidth(3, 75)  # Stała szerokość: 150 pikseli
                    self.ui.tab_wyliczenia_all_instruktorzy.setColumnWidth(4, 75)  # Stała szerokość: 150 pikseli
                    self.ui.tab_wyliczenia_all_instruktorzy.setColumnWidth(5, 75)  # Stała szerokość: 150 pikseli
                    self.ui.tab_wyliczenia_all_instruktorzy.setColumnWidth(6, 75)  # Stała szerokość: 150 pikseli
                    self.ui.tab_wyliczenia_all_instruktorzy.setColumnWidth(7, 75)  # Stała szerokość: 150 pikseli

                    self.ui.tab_wyliczenia_all_instruktorzy.setItem(row_idx, col_idx, item)

            self.ui.tab_wyliczenia_all_instruktorzy.setSortingEnabled(True)

        except db.Error as e:
            print(f"Błąd przy pobieraniu danych z bazy danych: {e}")

    def dodaj_do_sumy(self, suma, row):
        for i in range(2, len(row)):
            suma[i - 2] += row[i]

# =========================================================================================================================================================================
# = INNE ==================================================================================================================================================================

    def sprawdz_wpisy(self):
        miestac_roboczy = dodatki.data_miesiac_dzis()
        select_data = "SELECT * FROM zestawienia_prod zp WHERE zp.miesiac = '{0}'".format(
            miestac_roboczy)  # (miestac_roboczy)
        connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
        results = db.read_query(connection, select_data)
        connection.close()
        select_data_eksport = "SELECT * FROM eksport_danych ed WHERE ed.miesiac = '{0}' and ed.dzial = 'prod'".format(
            miestac_roboczy)
        connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
        result_eksport = db.read_query(connection, select_data_eksport)
        connection.close()

        if results:
            connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
            for x in results:
                delete_data = "delete from zestawienia_prod where id = '%s' and miesiac = '%s';" % (
                x[0], miestac_roboczy)
                print('Do skasowania z zestawienia:', delete_data)
                db.execute_query(connection, delete_data)
            connection.close()
        else:
            print('--Brak wpisów jeszcze--')

        if result_eksport:
            connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
            for x in result_eksport:
                delete_data = "delete from eksport_danych where id = '%s' and miesiac = '%s' and dzial = 'prod';" % (
                x[0], miestac_roboczy)
                print('Do skasowania z eksportu:', delete_data)
                db.execute_query(connection, delete_data)
            connection.close()
        else:
            print('--Brak wpisów jeszcze--')

    def zapis_dane_pracownicy(self):
        blokada = self.ui.check_blokada.isChecked()
        if blokada:
            QMessageBox.critical(self, 'Error', 'Dane są już zapisane. Zdejmij blokadę i zapisz raz jeszcze.!')
            return
        data_miesiac = str(dodatki.data_miesiac_dzis())
        teraz = datetime.today()
        self.sprawdz_wpisy()
        select_data = "SELECT * FROM zestawienia_prod zp WHERE zp.miesiac = '{0}'".format(data_miesiac)
        connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
        result = db.read_query(connection, select_data)
        select_data_eksport = "SELECT * FROM eksport_danych ed WHERE ed.miesiac = '{0}' and ed.dzial = 'prod'".format(
            data_miesiac)
        connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
        result_eksport = db.read_query(connection, select_data_eksport)

        lista_place = []

        if result:
            QMessageBox.critical(self, 'Error', 'Zestawienie dla pracowników zostało już dodane!')
        else:
            connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)

            for dane in self.lista:
                # if dane[6] == 0 and dane[7] == 0:
                #    direct = 0
                #    indirect = 0
                # else:
                #    direct = round(dane[4]/(dane[4]+dane[5]), 2)
                #    indirect = round(dane[5]/(dane[4]+dane[5]), 2)
                print(dane[0], dane[2], dane[3], dane[6], dane[7], dane[8], dane[9], dane[11], dane[14], data_miesiac,
                      teraz)
                insert_data = "INSERT INTO zestawienia_prod VALUES (NULL,'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s');" % (
                dane[0], dane[2], dane[3], dane[6], dane[7], dane[10], dane[11], dane[13], dane[16], data_miesiac,
                teraz)
                db.execute_query(connection, insert_data)
            connection.close()

        if result_eksport:
            QMessageBox.critical(self, 'Error', 'Zestawienie do eksportu dla pracowników produkcji jest już dodane.!')
        else:
            connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)

            for dane_place in self.lista:
                nr_akt = dane_place[0]  # nr akt
                kod = dane_place[1]  # kod
                imie_i_nazwisko = dane_place[2]  # Imie i nazwisko
                kwota = dane_place[17]  # kwota
                opis = 'produkcja'
                dzial = 'prod'

                if kwota > 0:
                    lista_place.append([nr_akt, kod, imie_i_nazwisko, kwota, opis, dzial, data_miesiac, teraz])

            for dane_wsparcie in self.lista_pracownik_wsparcia:
                nr_akt = dane_wsparcie[0]  # nr akt
                kod = dane_wsparcie[1]  # kod
                imie_i_nazwisko = dane_wsparcie[2]  # Imie i nazwisko
                kwota = dane_wsparcie[7]  # kwota
                opis = 'wsparcie'
                dzial = 'prod'

                if dane_wsparcie[7] > 0:
                    lista_place.append([nr_akt, kod, imie_i_nazwisko, kwota, opis, dzial, data_miesiac, teraz])

            for dane_lider in self.lista_pracownik_lider:
                nr_akt = dane_lider[0]  # nr akt
                kod = dane_lider[1]  # kod
                imie_i_nazwisko = dane_lider[2]  # Imie i nazwisko
                kwota = dane_lider[10]  # kwota
                opis = 'lider'
                dzial = 'prod'

                if kwota > 0:
                    lista_place.append([nr_akt, kod, imie_i_nazwisko, kwota, opis, dzial, data_miesiac, teraz])

            for dane_instruktor in self.lista_instruktor_prem:
                nr_akt = dane_instruktor[0]  # nr akt
                kod = dane_instruktor[1]  # kod
                imie_i_nazwisko = dane_instruktor[2]  # Imie i nazwisko
                kwota = dane_instruktor[9]  # kwota
                opis = 'instruktor'
                dzial = 'prod'

                if kwota > 0:
                    lista_place.append([nr_akt, kod, imie_i_nazwisko, kwota, opis, dzial, data_miesiac, teraz])

            for test in lista_place:
                # print(test[0],test[1],test[2],test[3],test[4],test[5],test[6],test[7])
                insert_data = "INSERT INTO eksport_danych VALUES (NULL,'%s','%s','%s','%s','%s','%s','%s','%s');" % (test[0], test[1], test[2], test[3], test[4], test[5], test[6], test[7])
                db.execute_query(connection, insert_data)

            self.ui.check_blokada.setChecked(True)

            connection.close()
            self.ui.lab_dot_eksport_enova_prod.setPixmap(QtGui.QPixmap(":/icon/img/svg_icons/dot_green.svg"))

    def czysc_tabele(self):
        self.ui.tab_dane_nieobecnosci.clearContents()
        self.ui.tab_dane_nieobecnosci.setRowCount(0)

        self.ui.tab_dane_pracownicy.clearContents()
        self.ui.tab_dane_pracownicy.setRowCount(0)

        self.ui.tab_dane_pomoc.clearContents()
        self.ui.tab_dane_pomoc.setRowCount(0)
        self.ui.tab_wyliczenia_pomoc.clearContents()
        self.ui.tab_wyliczenia_pomoc.setRowCount(0)

        self.ui.tab_dane_liderzy.clearContents()
        self.ui.tab_dane_liderzy.setRowCount(0)
        self.ui.tab_wyliczenia_liderzy.clearContents()
        self.ui.tab_wyliczenia_liderzy.setRowCount(0)

        self.ui.tab_dane_instruktorzy.clearContents()
        self.ui.tab_dane_instruktorzy.setRowCount(0)
        self.ui.tab_wyliczenia_zmiany_instruktorzy.clearContents()
        self.ui.tab_wyliczenia_zmiany_instruktorzy.setRowCount(0)
        self.ui.tab_wyliczenia_all_instruktorzy.clearContents()
        self.ui.tab_wyliczenia_all_instruktorzy.setRowCount(0)

        self.lista.clear()
        self.lista_pracownik_wsparcia.clear()
        self.lista_pracownik_lider.clear()
        self.lista_instruktor_prem.clear()