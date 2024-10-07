from PyQt5.QtWidgets import QWidget, QMessageBox

from _pomocFormDodaj_ui import Ui_Form
import db, re
from datetime import datetime

class MainWindow_pomocFormDodaj(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.combo_pomoc()
        self.combo_linie()
        self.ui.btn_zapisz.clicked.connect(self.zapisz)

    def combo_pomoc(self):
        query = "SELECT * FROM instruktor WHERE aktywny = 1 and id_ranga = 4;"
        connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
        results = db.read_query(connection, query)
        print('results', results)
        filtered_data = [(i, item) for i, item in enumerate(results)]
        print('filtered_data',filtered_data)

        id = 0
        value = '-----'
        self.ui.combo_wsparcie.addItem(value, id)

        for _,item in filtered_data:
            print('item',item)
            print('item',item[0])
            id = item[0]
            value = '%s %s (%s)' % (item[3], item[2], item[1])
            print('wynik:', id, value)
            self.ui.combo_wsparcie.addItem(value, item)

    def combo_linie(self):
        query = "SELECT * FROM linie WHERE aktywne = 1;"
        connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
        results = db.read_query(connection, query)

        id = 0
        value = '-----'
        self.ui.combo_linia.addItem(value, id)

        for wynik in results:
            id = wynik[0]
            value = wynik[1]
            self.ui.combo_linia.addItem(value, id)

    def zapisz(self):
        pole_wsparcie = self.ui.combo_wsparcie.currentData()
        pole_wsparcie_id = pole_wsparcie[0]
        pole_linie = self.ui.combo_linia.currentData()
        if self.ui.check_aktywny.isChecked():
            aktywny = 1
        else:
            aktywny = 0
        teraz = datetime.today()
        print('pole_wsparcie_id:',pole_wsparcie_id)
        print('pole_linie:',pole_linie)
        insert_data1 = "INSERT INTO wsparcie_produkcji VALUES (NULL, '%s', '%s', '%s', '%s', '%s');" % (pole_wsparcie_id,pole_linie,str(aktywny), teraz, None)
        print('insert_data1',insert_data1)
        connection1 = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
        db.execute_query(connection1, insert_data1)
        connection1.close()
        self.close()