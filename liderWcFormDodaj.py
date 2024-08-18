from PyQt5.QtWidgets import QWidget, QMessageBox

from _liderWcFormDodaj_ui import Ui_Form
import db, re
from datetime import datetime

class MainWindow_liderWcDodaj(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        #self.data = self.get_data_from_db()

        #self.filtered_data = [(i, item) for i, item in enumerate(self.data) if item["aktywny"] == 1 and item["uzyte"] == 0]

        self.combo_lider()
        self.combo_wc()
        self.combo_lokalizacja()
        self.ui.combo_lokalizacja.setEnabled(False)
        self.ui.combo_wc.setEnabled(False)
        self.ui.combo_lider.currentTextChanged.connect(self.on_combobox_changed)
        self.ui.btn_zapisz.clicked.connect(self.zapisz)

    def combo_lider(self):
        query = "SELECT * FROM instruktor WHERE aktywny = 1 and uzyte = 0;"
        connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
        results = db.read_query(connection, query)
        print('results', results)
        #print('test1 ID:', results[0][0])
        #print('test2 Nazwisko i Imie:', results[0][3], results[0][2])
        filtered_data = [(i, item) for i, item in enumerate(results)]
        print('filtered_data',filtered_data)

        id = 0
        value = '-----'
        self.ui.combo_lider.addItem(value, id)

        for _,item in filtered_data:
            print('item',item)
            print('item',item[0])
            id = item[0]
            value = '%s %s (%s)' % (item[3], item[2], item[1])
            print('wynik:', id, value)
            self.ui.combo_lider.addItem(value, item)

    def combo_wc(self):
        query = "SELECT * FROM gniazda_robocze WHERE aktywna = 1;"
        connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
        results = db.read_query(connection, query)

        id = 0
        value = '-----'
        self.ui.combo_wc.addItem(value, id)

        for wynik in results:
            id = wynik[0]
            value = wynik[1]
            self.ui.combo_wc.addItem(value, id)

    def combo_lokalizacja(self):
        query = "SELECT * FROM lokalizacja WHERE aktywny = 1;"
        connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
        results = db.read_query(connection, query)

        id = 0
        value = '-----'
        self.ui.combo_lokalizacja.addItem(value, id)

        for wynik in results:
            id = wynik[0]
            value = wynik[1]
            self.ui.combo_lokalizacja.addItem(value, id)

    def get_data_from_db(self):
        # Przykładowe zapytanie SQL
        query = "SELECT * FROM instruktor WHERE aktywny = 1 and uzyte = 0"
        connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
        results = db.read_query(connection, query)
        print(results)
        return results

    def on_combobox_changed(self, index):
        number = re.search(r'\d+', index).group()
        query = "SELECT * FROM instruktor WHERE nr_akt = %s" % number
        connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
        results = db.read_query(connection, query)
        ranga_id = results[0][5]
        if ranga_id == 1:
            self.ui.combo_lokalizacja.setEnabled(True)
            self.ui.combo_wc.setEnabled(False)
        if ranga_id == 2:
            self.ui.combo_lokalizacja.setEnabled(False)
            self.ui.combo_wc.setEnabled(True)

    def zapisz(self):
        pole_lider = self.ui.combo_lider.currentData()
        pole_lider_id = pole_lider[0]
        pole_wc_id = self.ui.combo_wc.currentData()
        pole_lokalizacja_id = self.ui.combo_lokalizacja.currentData()
        if self.ui.check_aktywny.isChecked():
            aktywny = 1
        else:
            aktywny = 0
        teraz = datetime.today()
        print('pole_lider_id:',pole_lider_id)
        print('pole_wc_id:',pole_wc_id)
        print('pole_lokalizacja_id:',pole_lokalizacja_id)
        insert_data1 = "INSERT INTO linia_gniazdo VALUES (NULL, '%s', '%s', '%s', '%s', '%s', NULL);" % (pole_lider_id,pole_wc_id,pole_lokalizacja_id,str(aktywny),teraz)
        print('insert_data1',insert_data1)
        connection1 = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
        db.execute_query(connection1, insert_data1)
        connection1.close()
        insert_data2 = "UPDATE instruktor SET uzyte = 1 WHERE instruktor.id = '%s';" % (pole_lider_id)
        connection2 = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
        db.execute_query(connection2, insert_data2)
        connection2.close()
        self.close()


