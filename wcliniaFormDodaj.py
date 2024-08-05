from PyQt5.QtWidgets import QWidget, QMessageBox

from _wcliniaFormDodaj_ui import Ui_Form
import db

class MainWindow_wcliniaDodaj(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.ui.btn_zapisz.clicked.connect(self.zapisz)
        self.combo_linia()
        self.combo_wc()

    def sprawdz_pole(self):
        combo_linia_id = self.ui.combo_linia.currentData()
        combo_grupa_id = self.ui.combo_grupa.currentData()

        if combo_linia_id == 0:
            QMessageBox.critical(self, 'Error', 'Wybierz linię')
            self.ui.combo_linia.setFocus()
            return False
        if combo_grupa_id == 0:
            QMessageBox.critical(self, 'Error', 'Wybierz grupę roboczą')
            self.ui.combo_grupa.setFocus()
            return False
        return True

    def combo_linia(self):
        select_data_linie = "SELECT * FROM linie WHERE aktywne = 1 and uzyta = 0;"
        connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
        results = db.read_query(connection, select_data_linie)

        id = 0
        value = '-----'
        self.ui.combo_linia.addItem(value, id)

        for wynik in results:
            id = wynik[0]
            value = wynik[1]
            self.ui.combo_linia.addItem(value, id)

    def combo_wc(self):
        select_data_linie = "SELECT * FROM gniazda_robocze WHERE aktywna = 1;"
        connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
        results = db.read_query(connection, select_data_linie)

        id = 0
        value = '-----'
        self.ui.combo_grupa.addItem(value, id)

        for wynik in results:
            id = wynik[0]
            value = wynik[1]
            self.ui.combo_grupa.addItem(value, id)

    def zapisz(self):
        if not self.sprawdz_pole():
            return

        combo_linia_text = self.ui.combo_linia.currentText()
        combo_linia_id = self.ui.combo_linia.currentData()
        combo_wc_text = self.ui.combo_grupa.currentText()
        combo_wc_id = self.ui.combo_grupa.currentData()
        if self.ui.check_aktywny.isChecked():
            aktywny = 1
        else:
            aktywny = 0
        print('aktywny:', aktywny)
        insert_data1 = "INSERT INTO gniazdo_linia VALUES (NULL, '%s', '%s', '%s');" % (combo_wc_id, combo_linia_id, str(aktywny))
        insert_data2 = "UPDATE linie SET uzyta = 1 WHERE linie.id = %s;" % (combo_linia_id)
        print(insert_data1)
        print(insert_data2)
        connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
        db.execute_query(connection, insert_data1)
        db.execute_query(connection, insert_data2)
        connection.close()
        self.close()