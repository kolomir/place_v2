from PyQt5.QtWidgets import QWidget, QMessageBox

from _wcliniaFormEdytuj_ui import Ui_Form
import db

class MainWindow_wcliniaEdytuj(QWidget):
    def __init__(self, data):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.ui.btn_zapisz.clicked.connect(self.zapisz)
        self.edytuj(data)
        self.id_rekord = data[0]
        self.aktywny = data[3]

    def edytuj(self,data):
        id_data = data[0]
        id_grupa_data = data[1]
        id_linia_data = data[2]
        aktywny_data = int(data[3])

        print('id_data:',id_data,'; id_grupa_data:',id_grupa_data,'; id_linia_data:',id_linia_data,'; aktywny_data:',aktywny_data )
        print('------------------------------')
        self.ui.lab_gniazdo.setText(id_grupa_data)
        self.ui.lab_linia.setText(id_linia_data)
        self.ui.check_aktywny.setChecked(bool(aktywny_data))
        if aktywny_data == 0:
            self.ui.btn_zapisz.setText("Aktywuj")
        else:
            self.ui.btn_zapisz.setText("Dezaktywuj")

    def zapisz(self):
        linie_id_data = "select * from gniazdo_linia where gniazdo_linia.id = %s;" % self.id_rekord
        connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
        result_linia = db.read_query(connection, linie_id_data)
        connection.close()
        id_linia = result_linia[0][2]
        linie_data = "select * from linie where linie.id = %s;" % id_linia
        connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
        result_linie_data = db.read_query(connection, linie_data)
        connection.close()
        sprawdz_linia = result_linie_data[0][3]
        print('sprawdz_linia:',sprawdz_linia)

        if self.aktywny == '0':
            if sprawdz_linia == 1:
                QMessageBox.critical(self, 'Error', 'Nie można aktywować tego połączenia. Linia jest już przypisana do innej Grupy Roboczej!!!')
                return
            else:
                aktywuj = 1
                uzyty = 1
        else:
            aktywuj = 0
            uzyty = 0

        print('aktywny:',self.aktywny, '; aktywuj: ',aktywuj, '; uzyty: ',uzyty)

        insert_data = "UPDATE gniazdo_linia SET aktywny = %s WHERE gniazdo_linia.id = %s" % (aktywuj,self.id_rekord)
        insert_data2 = "UPDATE linie SET uzyta = %s WHERE linie.id = '%s'" % (uzyty,id_linia)
        connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
        db.execute_query(connection, insert_data)
        db.execute_query(connection, insert_data2)
        connection.close()
        self.close()