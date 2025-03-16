from PyQt5.QtWidgets import QWidget, QMessageBox

from _korekta_indirect_prod_dodaj_ui import Ui_Form
import db, dodatki
from datetime import datetime

class MainWindow_korekta_indirect_prod_dodaj(QWidget):
    def __init__(self, dzial):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.combo_pracownik()
        self.ui.combo_nr_akt.currentIndexChanged.connect(self.on_combobox_changed)

        self.ui.btn_zapisz.clicked.connect(self.zapisz)
        print('dzial 3',dzial)
        self.dzial_nazwa = dzial

    def combo_pracownik(self):
        miestac_roboczy = dodatki.data_miesiac_dzis()
        query = '''
                select 
                    d.id
                    ,d.Nr_akt 
                    ,d.Nazwisko_i_imie 
                    ,d.Direct_work 
                    ,d.Indirect_work 
                    ,d.Diff 
                from 
                    direct d 
                where 
                    miesiac = '{0}'
                '''.format(miestac_roboczy)
        connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
        results = db.read_query(connection, query)
        connection.close()

        posortowana_lista = sorted(results, key=lambda x: x[1])
        #print(posortowana_lista)

        id = 0
        value = '-----'
        self.ui.combo_nr_akt.addItem(value, id)

        for item in posortowana_lista:
            #print('item',item)
            #print('item',item[0])
            id = item[0]
            value = '%s %s' % (item[1], item[2])
            #print('wynik:', id, value)
            self.ui.combo_nr_akt.addItem(value, item)

    def on_combobox_changed(self):
        index = self.ui.combo_nr_akt.currentData()
        #print(index)
        self.ui.lab_direct.setText(str(index[3]))
        self.ui.lab_indirect.setText(str(index[4]))
        self.ui.lab_difference.setText(str(index[5]))
        self.ui.text_nazwisko_i_imie.setText(index[2])

    def sprawdz_pole(self):
        pole_ranga = self.ui.combo_nr_akt.currentData()
        pole_czas = self.ui.text_czas.text().strip()

        if not pole_ranga:
            QMessageBox.critical(self, 'Error', 'Nie wybrano pracownika')
            self.ui.pole_nr_akt.setFocus()
            return False
        if not pole_czas:
            QMessageBox.critical(self, 'Error', 'Nie podano czasu do korekty')
            self.ui.pole_czas.setFocus()
            return False
        return True

    def sprawdz_czy_istnieje(self,dane):
        miestac = dodatki.data_miesiac_dzis()
        select_data = '''
                        select 
                            ki.id
                            ,ki.nr_akt 
                            ,ki.`nazwisko_i_imie` 
                            ,ki.czas 
                            ,ki.opis 
                            ,ki.data_dodania
                            ,ki.dzial
                        from 
                            korekta_indirect ki 
                        where 
                            miesiac = '{0}'
                            and ki.nr_akt = '{1}'
                            and ki.dzial = '{2}'
                        '''.format(miestac,dane,self.dzial_nazwa)
        connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
        results = db.read_query(connection, select_data)
        connection.close()
        return len(results) # Zwraca True, jeśli istnieje

    def zapisz(self):
        if not self.sprawdz_pole():
            return

        pole_nr_akt = self.ui.combo_nr_akt.currentData()
        pole_czas = self.ui.text_czas.text().strip()
        pole_nazwisko_i_imie = self.ui.text_nazwisko_i_imie.text()
        pole_powod = self.ui.text_powod.text()

        nr_akt = pole_nr_akt[1]
        pole_czas = pole_czas.replace(",",".")

        teraz = datetime.today()
        miestac = dodatki.data_miesiac_dzis()

        if self.sprawdz_czy_istnieje(nr_akt) > 0:
            QMessageBox.warning(self, "Błąd", "Osoba ma już zmieniony czas IW!")
        else:

            insert_data = "INSERT INTO korekta_indirect VALUES (NULL, '%s', '%s', '%s', '%s', '%s', '%s', '%s');" % (nr_akt, pole_nazwisko_i_imie, pole_czas, pole_powod, miestac, teraz, self.dzial_nazwa)
            connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
            db.execute_query(connection, insert_data)
            connection.close()
            self.close()

        #print('insert_data:',insert_data)
        #print('pole_nr_akt:',pole_nr_akt)
        #print('pole_czas:',pole_czas)
        #print('pole_nazwisko_i_imie:',pole_nazwisko_i_imie)
        #print('pole_powod:',pole_powod)
